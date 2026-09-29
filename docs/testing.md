# Test provenance

Engineering tests use a stub generator to verify schemas, citation membership, bounded repair, explicit failure handling and prompt data separation. They do not establish real-model answer quality or prompt-injection resistance. Database tests use PostgreSQL and a fixed synthetic embedder to verify replacement and full-text retrieval. Playwright fixtures verify UI behaviour; `REAL_MODEL=1` separately enables real supported-answer and abstention checks. CI excludes held-out evaluation and model downloads.

Executed results will be recorded in implementation-log.md after each run.
