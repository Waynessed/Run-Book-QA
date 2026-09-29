# Decisions

- Follow the handoff's Qwen 1.5B CPU model, MiniLM embeddings and cross-encoder. Small models make a CPU demo practical; accuracy must be measured.
- Tokenizer-aware 300-token heading chunks, 50-token overlap; prefix each chunk with title/heading. Source sections remain addressable even when split.
- Use PostgreSQL full-text OR term ranking for natural questions, exact pgvector cosine search, RRF k=60 then cross-encoder on twenty candidates for hybrid.
- A transaction atomically replaces one active document and its chunks; unchanged hashes skip embedding. Same-version content changes are rejected.
- Citation validation proves IDs exist in the supplied context. Factual support still needs human review.
- Reranker score is a ranking signal, never a probability. Threshold remains null until development-only calibration.
- Labels are authored before tuning; related questions remain in one split. Held-out execution requires an explicit CLI switch and a frozen manifest.

Primary references: [pgvector](https://github.com/pgvector/pgvector), [retrieve and rerank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html), [Qwen model](https://ollama.com/library/qwen2.5:1.5b), [Ollama generation API](https://docs.ollama.com/api/generate).
