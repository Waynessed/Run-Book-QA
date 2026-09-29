from sqlalchemy import text, select
from .db import Chunk, Document
from .schemas import Passage
from .models import embedder, reranker

def reciprocal_rank_fusion(lists: list[list[tuple[str, float]]]) -> list[tuple[str, float]]:
    scores = {}
    for candidates in lists:
        for rank, (identity, _) in enumerate(candidates, 1):
            scores[identity] = scores.get(identity, 0) + 1 / (60 + rank)
    return sorted(scores.items(), key=lambda pair: (-pair[1], pair[0]))[:20]

def retrieve(session, question: str, mode: str, limit: int = 5) -> list[Passage]:
    keyword, semantic = [], []
    if mode in ("keyword", "hybrid"):
        keyword = list(session.execute(text("""
            SELECT id, ts_rank_cd(to_tsvector('english', text), replace(plainto_tsquery('english', :q)::text, ' & ', ' | ')::tsquery) AS score
            FROM chunks WHERE to_tsvector('english', text) @@ replace(plainto_tsquery('english', :q)::text, ' & ', ' | ')::tsquery
            ORDER BY score DESC, id LIMIT 20
        """), {"q": question}).all())
    if mode in ("semantic", "hybrid"):
        vector = embedder().encode(question, normalize_embeddings=True).tolist()
        semantic = list(session.execute(select(Chunk.id, (1 - Chunk.embedding.cosine_distance(vector)).label("score"))
                                       .order_by(Chunk.embedding.cosine_distance(vector), Chunk.id).limit(20)).all())
    candidates = reciprocal_rank_fusion([keyword, semantic]) if mode == "hybrid" else (keyword if mode == "keyword" else semantic)
    passages = []
    for identity, score in candidates:
        chunk = session.get(Chunk, identity)
        doc = session.get(Document, chunk.document_id)
        passages.append(Passage(id=identity, document_id=doc.id, title=doc.title, version=chunk.version,
                                heading=chunk.heading, section_id=chunk.section_id, text=chunk.text, score=float(score)))
    if mode == "hybrid" and passages:
        scores = reranker().predict([(question, p.text) for p in passages])
        for p, score in zip(passages, scores):
            p.score = float(score)
        passages.sort(key=lambda p: (-p.score, p.id))
    return passages[:limit]

def context_passages(passages: list[Passage]) -> list[Passage]:
    tokenizer = embedder().tokenizer
    output, count = [], 0
    for p in passages[:3]:
        size = len(tokenizer.encode(p.model_dump_json(), add_special_tokens=False))
        if count + size <= 1200:
            output.append(p)
            count += size
    return output
