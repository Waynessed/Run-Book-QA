# Implementation walkthrough

## Ingestion
`backend/app/ingest.py:read_source` reads explicit document IDs and versions. `chunk_source` splits at headings and encodes with the embedding tokenizer. Each chunk carries stable section context and a content hash. `ingest` skips unchanged documents, embeds changed text outside the write transaction, then locks the document ID and replaces its active chunks atomically.

```python
prepared = chunk_source(source, model.tokenizer)
vectors = model.encode([c["text"] for c in prepared], normalize_embeddings=True).tolist()
```

## Retrieval
`backend/app/retrieval.py:retrieve` executes PostgreSQL full-text ranking or exact cosine distance. Hybrid merges twenty results from each using `reciprocal_rank_fusion`, then reranks twenty merged candidates. `context_passages` selects at most three passages within a 1,200-token serialized evidence budget. `service.ask` reads evidence and corpus hash from one repeatable-read snapshot.

## Generation and validation
`generation.generate` sends the question and JSON evidence to the pinned local model at temperature zero. It asks for `GeneratedAnswer.model_json_schema()`. Pydantic enforces status/claim consistency, three claims maximum and required citations. `schemas.validate_citations` rejects citation IDs absent from the supplied passages. One repair is allowed; HTTP errors and timeouts return visible errors. These checks establish structure, not whether a claim is factually entailed.

## User interface
`frontend/src/main.tsx:App` submits the selected mode, displays answers/abstentions/errors, and opens current documents through `/v1/documents/{id}`. The quoted retrieved section remains available if a source has since changed. Evaluation measurements appear only when a saved report exists.

## Scoring
Evaluation implementation and real measurements are pending. No accuracy claim has been made.
## Citation identity correction
The stored chunk ID remains stable in `Passage.chunk_id`. `context_passages` assigns short local IDs such as P1 for generation and UI citations. `generate` includes a response schema whose citation enum contains those exact local IDs. The source mapping remains explicit through document ID, section ID, version and chunk ID.
## Evaluation flow
`evaluation.load_cases` selects development by default. `validate_dataset` checks counts, unique IDs and grouped split isolation. `calibrate` sweeps development reranker scores, preferring a threshold meeting both gate targets; otherwise it chooses balanced accuracy. Corpus fingerprint checks reject a changed index during calibration.

`evaluate` retrieves five candidates for Recall@5, executes `service.ask` with the same mode and real generator, and records validated/raw outputs, traces, actual latency and errors. It writes pending progress atomically, then final JSON/Markdown and null-filled semantic annotation templates. `metric_rows` computes structural/retrieval/abstention/coverage metrics. Factual correctness and supporting-claim rates remain null until rubric-based review. `freeze` pins app files, dependency lock, configuration, corpus files and dataset hashes; held-out runs reject changes or a mismatched Git revision.
