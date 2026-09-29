# Implementation log

## RQ-00 / 2026-09-29 UTC — Scaffold and runtime preparation

Goal: establish the smallest real local demo. Read the handoff and inspected the empty repository. Preserved the handoff. Docker pipe access failed under sandbox; elevated execution confirmed a working Linux engine. Git commands need a per-command `-c safe.directory=D:/Projects/RunBookQA` override because repository ownership differs from the sandbox account. User explicitly authorized pushes.

Files: compose.yaml, backend/Dockerfile, backend/requirements.in, backend/migrations, scripts/bootstrap.ps1, scripts/demo.ps1, AGENTS.md. Runtime downloads started. Backend lock resolution uses Python 3.12.10 and uv 0.7.3 in Docker. Models use immutable Hugging Face revisions and Ollama digest verification; container digests will be recorded after pulling.

## RQ-01 / 2026-09-29 UTC — First vertical slice implementation

Files/functions: app/ingest.py (`read_source`, `chunk_source`, `ingest`, `corpus_version`); app/retrieval.py (`retrieve`, `reciprocal_rank_fusion`, `context_passages`); app/generation.py (`generate`, `model_metadata`); app/schemas.py (`GeneratedAnswer`, `validate_citations`); app/service.py (`ask`); frontend/src/main.tsx (`App`); corpus/*.md; evaluation/development-initial.json.

Flow: original Markdown -> tokenizer-aware heading chunks -> CPU embeddings prepared before transaction -> PostgreSQL documents/chunks -> keyword retrieval -> three passages -> Ollama schema-constrained JSON -> Pydantic and citation membership validation -> answer UI -> current source endpoint. Repeatable-read query transactions keep corpus metadata and chunks consistent during updates. Evidence is JSON-encoded as untrusted data. HTTP failures and timeouts become explicit 503 errors; malformed output permits one repair attempt.

Reasoning: retain fixed-stack storage from the first slice; use exact vector search for the small corpus; build replacement chunks before deleting old content; keep source text and document version inspectable. Keyword terms use OR after PostgreSQL stopword/stem normalization because AND across a full natural-language question suppresses useful matches. Semantic/hybrid code is present early but not claimed verified.

Observed commands: Docker version and Git remote checks succeeded with elevation; no remote refs existed. Corpus authoring created ten synthetic runbooks and twenty development-only labels before tuning. Pending: dependency locks, real model response, database migration, ingestion, browser verification, tests, commit hash and push.
