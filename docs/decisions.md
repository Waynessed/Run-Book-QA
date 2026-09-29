# Decisions

- Follow the handoff's Qwen 1.5B CPU model, MiniLM embeddings and cross-encoder. Small models make a CPU demo practical; accuracy must be measured.
- Tokenizer-aware 300-token heading chunks, 50-token overlap; prefix each chunk with title/heading. Source sections remain addressable even when split.
- Use PostgreSQL full-text OR term ranking for natural questions, exact pgvector cosine search, RRF k=60 then cross-encoder on twenty candidates for hybrid.
- A transaction atomically replaces one active document and its chunks; unchanged hashes skip embedding. Same-version content changes are rejected.
- Citation validation proves IDs exist in the supplied context. Factual support still needs human review.
- Reranker score is a ranking signal, never a probability. Threshold remains null until development-only calibration.
- Labels are authored before tuning; related questions remain in one split. Held-out execution requires an explicit CLI switch and a frozen manifest.

Primary references: [pgvector](https://github.com/pgvector/pgvector), [retrieve and rerank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html), [Qwen model](https://ollama.com/library/qwen2.5:1.5b), [Ollama generation API](https://docs.ollama.com/api/generate).
## RQ-02 evaluation data provenance
All source text is original synthetic content. No production logs or credentials were used. Dataset authors necessarily saw labels while authoring them; the implementing assistant is not an independent blind human reviewer. Held-out labels have not been passed to calibration, model generation or prompt tuning. Normal CI checks a question-free manifest for counts and grouping, plus initial development ID stability. It does not ask held-out questions.
## Confidence comparison
Keyword and semantic ordering remain baseline order. For abstention, all modes use a cross-encoder relevance signal: best score among the baseline's first three candidate passages, or the best reranked hybrid passage. One development-calibrated hybrid threshold is applied to all modes; baseline gate coverage is therefore measured, not assumed equivalent. Reports must distinguish gate-only calibration from actual generated answer coverage.
