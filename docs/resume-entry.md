# RunbookQA resume entry — verified checkpoint

Based on implementation through the 2026-09-29 pause. Held-out generation is complete; final semantic review and final-demo execution remain pending. The retrieval metric below is 35/36 labelled evidence sections found in the top five results in each tested mode; it is not generated-answer accuracy.

## A. Top 4 strongest aspects

### 1. Full-Stack Application Engineering

**Why:** Shows ownership of a working application across API, interface and local deployment.

**Evidence:** FastAPI/Pydantic APIs, React/TypeScript source inspection and abstention UI, real Ollama generation, Docker Compose with localhost exposure and private database/model services. First real browser demo and cached bootstrap executed.

**Resume bullet:** Built a Dockerized runbook assistant with FastAPI, React/TypeScript and Ollama, exposing local APIs and inspectable citations for generated answers.

### 2. Retrieval Architecture & Measured Evaluation

**Why:** Demonstrates search engineering and measured outcomes beyond a language-model wrapper.

**Evidence:** PostgreSQL full-text ranking, exact pgvector cosine search, reciprocal rank fusion, MiniLM reranking, development-calibrated abstention and configuration freeze. Complete held-out raw comparison measured 97.22% evidence Recall@5 on 36 answerable questions in each mode; semantic review is still unfinished.

**Resume bullet:** Implemented keyword, semantic and hybrid retrieval with pgvector and MiniLM reranking, measuring 97.2% evidence Recall@5 on 36 held-out answerable questions.

### 3. Transactional Data Ingestion & Version Integrity

**Why:** Shows backend reliability through concrete consistency and update decisions.

**Evidence:** Heading-aware source-preserving chunking, embedding-tokenizer budgets, content hashes, embeddings built before replacement, advisory locks, atomic SQLAlchemy/PostgreSQL transactions and repeatable-read retrieval snapshots. Verified db-pool version replacement removes obsolete active guidance; unchanged documents skip embedding.

**Resume bullet:** Designed heading-aware ingestion with content hashes and atomic PostgreSQL transactions, preventing mixed-version retrieval and redundant embedding of unchanged documents.

### 4. Testing, CI & Reproducibility

**Why:** Demonstrates verification habits, automated checks and traceable experiments.

**Evidence:** 33 backend/database/API/evaluation pytest tests and four deterministic Playwright scenarios passed; GitHub Actions passed at frozen revision 39bc696. Pinned dependencies/models/images, 100 grouped labels, freeze manifests, raw outputs and report-bound annotations. Real model runs are recorded separately from CI fixtures.

**Resume bullet:** Automated GitHub Actions checks with 33 pytest tests and four Playwright scenarios, plus frozen evaluations across a 100-question labelled dataset.

## B. Recommended final resume entry

**RunbookQA — Local Engineering-Support Assistant**

- Built a Dockerized runbook assistant with FastAPI, React/TypeScript and Ollama, exposing local APIs and inspectable citations for generated answers.
- Implemented keyword, semantic and hybrid retrieval with pgvector and MiniLM reranking, measuring 97.2% evidence Recall@5 on 36 held-out answerable questions.
- Designed heading-aware ingestion with content hashes and atomic PostgreSQL transactions, preventing mixed-version retrieval and redundant embedding of unchanged documents.
- Automated GitHub Actions checks with 33 pytest tests and four Playwright scenarios, plus frozen evaluations across a 100-question labelled dataset.

Evidence limits: local deployment only; no AWS, user counts, production/scalability, independent answer-quality or general injection-resistance claim. Test authoring exposure and observed failures are recorded in docs/evaluation-report.md and docs/held-out-findings.md.
