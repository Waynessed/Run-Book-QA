import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from sqlalchemy import select, delete, text
from .db import Session, Document, Chunk
from .models import embedder

def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()

def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")

@dataclass
class Source:
    id: str
    version: str
    title: str
    markdown: str

def read_source(path: Path) -> Source:
    markdown = path.read_text(encoding="utf-8")
    metadata, body = markdown.split("---", 2)[1:]
    fields = dict(line.split(": ", 1) for line in metadata.strip().splitlines())
    return Source(fields["id"], fields["version"], fields["title"], body.strip())

def chunk_source(source: Source, tokenizer) -> list[dict]:
    chunks = []
    heading = source.title
    body = []
    sections = []
    for line in source.markdown.splitlines():
        if re.match(r"^#{1,6} ", line):
            if body:
                sections.append((heading, "\n".join(body)))
            heading, body = line.lstrip("# "), []
        else:
            body.append(line)
    sections.append((heading, "\n".join(body)))
    for heading, content in sections:
        content = content.strip()
        encoded = tokenizer(content, add_special_tokens=False, return_offsets_mapping=True)
        tokens = encoded["input_ids"]
        offsets = encoded["offset_mapping"]
        prefix = f"{source.title} / {heading}\n"
        budget = 300 - len(tokenizer.encode(prefix, add_special_tokens=False))
        if budget <= 50:
            raise ValueError("Heading exceeds chunk budget")
        for start in range(0, len(tokens), budget - 50):
            value = prefix + content[offsets[start][0]:offsets[min(start + budget, len(tokens)) - 1][1]]
            identity = f"{source.id}:{source.version}:{slug(heading)}:{start}"
            chunks.append(dict(id=identity, document_id=source.id, version=source.version,
                               heading=heading, section_id=slug(heading), text=value, content_hash=digest(value)))
            if start + budget >= len(tokens):
                break
    return chunks

def ingest(paths: list[Path], rebuild_index: bool = False) -> dict:
    changed, unchanged = 0, 0
    for path in paths:
        source = read_source(path)
        content_hash = digest(source.version + source.title + source.markdown)
        with Session() as session:
            previous = session.get(Document, source.id)
            if previous and previous.content_hash == content_hash and not rebuild_index:
                unchanged += 1
                continue
            if previous and previous.version == source.version and previous.content_hash != content_hash:
                raise ValueError(f"Bump version when editing {source.id}")
        # Expensive model work happens before the atomic replacement transaction.
        model = embedder()
        prepared = chunk_source(source, model.tokenizer)
        vectors = model.encode([c["text"] for c in prepared], normalize_embeddings=True).tolist()
        with Session.begin() as session:
            session.execute(text("SELECT pg_advisory_xact_lock(hashtext(:id))"), {"id": source.id})
            previous = session.get(Document, source.id)
            if previous and previous.content_hash == content_hash and not rebuild_index:
                unchanged += 1
                continue
            if previous:
                if previous.version == source.version and previous.content_hash != content_hash:
                    raise ValueError(f"Concurrent update requires a new version for {source.id}")
                session.execute(delete(Chunk).where(Chunk.document_id == source.id))
                previous.version, previous.title = source.version, source.title
                previous.markdown, previous.content_hash = source.markdown, content_hash
            else:
                session.add(Document(id=source.id, version=source.version, title=source.title,
                                     markdown=source.markdown, content_hash=content_hash))
                session.flush()
            session.add_all([Chunk(**c, embedding=v) for c, v in zip(prepared, vectors)])
        changed += 1
    return {"changed": changed, "unchanged": unchanged}

def corpus_version(session) -> str:
    rows = session.execute(select(Document.id, Document.content_hash).order_by(Document.id)).all()
    chunk_rows = session.execute(select(Chunk.id, Chunk.content_hash).order_by(Chunk.id)).all()
    return digest("\n".join(f"{a}:{b}" for a, b in rows + chunk_rows))
