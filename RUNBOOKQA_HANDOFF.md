# RunbookQA — Implementation Handoff

## 1. Instruction to the implementing Codex session

Implement this project in the current repository. This repository is dedicated
to RunbookQA and is independent of the job-search and ClipFlow repositories.

Priority:
1. Deliver a working local question → evidence → answer demo.
2. Add retrieval comparisons, abstention and meaningful evaluation.
3. Complete tests and portfolio documentation.

Proceed through the stages below without waiting for approval for routine
implementation choices. Preserve existing user changes.

The user wants to learn the implementation later. Maintain the implementation
records below while building. Chat history is not the sole source of truth.

Never describe stubbed responses, planned features, unexecuted evaluations or
aspirational accuracy targets as completed achievements.

## 2. Product and success criteria

Build an engineering-support assistant that answers from a fictional company's
runbooks and displays the passages supporting its answer.

Examples:
- "The API returns 401 after deployment. What should I check?"
- "Why is the container restarting?"
- "How do I investigate exhausted database connections?"
- "What is our policy for a situation the documents do not cover?"

The final demo must show:
1. A supported answer with inspectable citations.
2. An unsupported question and abstention.
3. A document update that removes obsolete guidance.
4. A retrieval comparison and measured evaluation results.
5. An adversarial document containing instructions the assistant should ignore.

First-demo acceptance:
- A real local language model generates the answer.
- Retrieved passages come from the stored corpus.
- Citations open the actual source sections.
- Model failure is shown honestly; no silently substituted canned answer.

## 3. Fixed scope and stack

Backend: Python, FastAPI, Pydantic, SQLAlchemy/Alembic, psycopg.
Database: PostgreSQL with pgvector.
Embeddings: sentence-transformers/all-MiniLM-L6-v2.
Reranker: cross-encoder/ms-marco-MiniLM-L-6-v2.
Generator: Ollama qwen2.5:1.5b.
Frontend: React, TypeScript and Vite.
Environment: Docker Compose, CPU-compatible defaults.
Tests: pytest and Playwright.
CI: GitHub Actions.

Pin dependency versions, model revisions/digests and container configuration.
Record exact versions and hardware assumptions.

Architecture:
Markdown → ingestion → PostgreSQL text/vector index
Question → retrieval → reranking → local LLM → validated answer/citations
Labelled questions → evaluation CLI → JSON/Markdown comparison reports

Local ports:
- Frontend: 5174.
- API: 8081.
- Bind exposed services to localhost.
- PostgreSQL and Ollama stay inside the Docker network.

No paid APIs, public deployment, model fine-tuning or GPU requirement.
Single-workspace corpus.
No autonomous tools, shell execution, infrastructure changes or real credentials.
No user accounts or multitenancy in v1.

## 4. Corpus and indexing

Final corpus:
- 30 original Markdown runbooks, approximately 250–500 words each.
- Fictional services and synthetic logs/configuration.
- Topics: deployment/rollback, Docker/Kubernetes, authentication/API errors,
  database connections, monitoring and incident escalation.
- Stable document ID, version, title and section headings.

Do not copy large third-party documentation into the corpus.

Chunking:
- Heading-aware chunks, approximately 300 tokens with 50-token overlap.
- Use the embedding model's tokenizer.
- Store document ID/version, heading, chunk ID, content hash and source text.
- Preserve heading context when splitting long sections.

Document replacement:
- Detect changes using content hashes.
- Build updated chunks/embeddings before changing the active document.
- Replace the active document version and its chunks atomically.
- Retrieval must not mix obsolete and current versions.
- Unchanged documents must not be embedded again.

Use exact vector search for this small corpus.
Approximate indexing is outside v1.

## 5. Interfaces and answer behaviour

POST /v1/ask
Input:
- question.
- retrieval_mode: keyword, semantic or hybrid.
- Default: hybrid.

Output:
- request ID.
- answered or abstained status.
- Answer as at most three short claims.
- Citation IDs attached to each claim.
- Supporting passages and document versions.
- Retrieval mode, corpus version, model version and latency.

Other interfaces:
- GET /v1/documents/{id}: current document and headings.
- GET /v1/evaluation/latest: most recent saved report.
- GET /healthz and /readyz.
- CLI ingest: index/replace the corpus.
- CLI evaluate: execute a configuration against development or test questions.

Limit questions to 1,000 characters.
Use a 120-second model timeout.
Malformed model output gets at most one repair attempt.
Timeouts/unavailable models return explicit errors, not fabricated answers.

Retrieval:
1. Keyword baseline: PostgreSQL full-text ranking.
2. Semantic baseline: cosine similarity using exact pgvector search.
3. Hybrid:
   - Retrieve up to 20 candidates from each baseline.
   - Merge using reciprocal rank fusion with k=60.
   - Rerank the best 20 merged candidates.
   - Send the best three passages, at most 1,200 context tokens, to the generator.

Generation:
- Temperature 0; record actual model/runtime configuration.
- Structured output validated with Pydantic.
- Cite only passage IDs present in the supplied context.
- Treat retrieved documents as evidence, not instructions.
- Ask the generator to abstain when the evidence is insufficient.

Validate citation IDs deterministically.
Do not claim this proves semantic correctness: supporting claims requires evaluation.

Confidence:
- Use the best reranker score as a retrieval-confidence signal, not a probability.
- Calibrate its threshold using development questions only.
- Select a threshold that meets ≥90% unsupported abstention while retaining
  ≥80% answerable coverage on development data, when achievable.
- If no threshold meets both, choose the best balanced accuracy and document
  the unmet target.
- Below threshold, abstain before generation.
- The generator may also abstain.

## 6. UI

One compact interface:
- Question input and retrieval-mode selector.
- Answer or explicit abstention.
- Clickable source passages, document titles and versions.
- Latency and retrieval mode.
- Evaluation comparison table.
- Sample question buttons.

Do not spend time on a complex design system, chat history or user settings.
Show a clear model-download/loading/error state.

## 7. Evaluation dataset and measurements

Final dataset: 100 labelled questions.
- 60 answerable.
- 20 unsupported.
- 20 adversarial.

Split:
- Development: 24 answerable, 8 unsupported, 8 adversarial.
- Held-out test: 36 answerable, 12 unsupported, 12 adversarial.

Keep related questions/paraphrases in the same split.

Each case records:
- Stable case ID and category.
- Question.
- Expected answer facts or expected abstention.
- Supporting document/section IDs when applicable.
- Adversarial behaviour that must not occur.

Create labels before tuning.
Do not use held-out cases to select prompts, thresholds or retrieval settings.
Freeze the configuration before the final held-out run.
Document any exposure or later tuning that invalidates that distinction.

Compare keyword, semantic and hybrid modes using the same corpus and generator.

Metrics:
- Evidence Recall@5.
- Answer correctness against labelled facts.
- Supported-claim rate.
- Valid citation rate.
- Correct abstention on unsupported questions.
- Answerable coverage, so universal abstention cannot look successful.
- Adversarial instruction-following failures.
- Median/p95 response latency.

Automatically check IDs, retrieval results, schemas and exact expectations where
appropriate. Manually inspect factual correctness and citation support using a
recorded rubric. Do not present an LLM judge as unquestionable ground truth.

Targets:
- Recall@5 ≥90% on answerable held-out questions.
- Correct abstention ≥90% on unsupported held-out questions.
- Supported-claim rate ≥90%.
- Answerable coverage ≥80%.

Targets are not guarantees. Report actual results and failures.
No claim of general prompt-injection immunity.

## 8. Implementation stages

### RQ-00 — Scaffold and model setup
- Inspect the repository and available Docker/Node tools.
- Create Compose services, migrations and dependency locks.
- Add scripts/bootstrap.ps1 and scripts/demo.ps1.
- Bootstrap downloads required models, waits for readiness and reports failures.
- Establish the implementation records.
- Verify a real model response before building the product around it.

Acceptance: database, model and API readiness work.
If hardware/downloads block the model, report the precise blocker; do not fake it.

### RQ-01 — First vertical demo
- Author 10 initial runbooks.
- Implement ingestion and keyword retrieval.
- Implement structured generation and citation validation.
- Build the small UI.
- Add five clearly answerable sample questions and two unsupported examples.
- Create an initial development-only set of 20 cases.

Acceptance: browser question produces a real grounded answer and inspectable sources.
Deliver this first demo immediately.

Planning estimate: RQ-00 + RQ-01 approximately 10–15 focused hours,
excluding unusually slow downloads.

### RQ-02 — Complete corpus and evaluation foundations
- Expand to 30 runbooks and the final 100-case dataset.
- Preserve initial development examples within the development split.
- Implement atomic document-version replacement.
- Add evaluation CLI, scoring rubric and raw-report format.
- Keep held-out questions out of tuning commands and normal CI.

Acceptance: dataset splits validate; indexing updates remove obsolete content.

### RQ-03 — Retrieval comparison and abstention
- Implement semantic and hybrid retrieval.
- Add reranking.
- Calibrate confidence using development data.
- Compare approaches and inspect failure cases.
- Add adversarial corpus examples and regression tests.

Acceptance: reproducible development reports for all three modes.
Record improvements or regressions honestly.

### RQ-04 — Final test and demo package
- Freeze prompt, corpus and retrieval configuration.
- Run held-out evaluations.
- Save raw outputs, scores and manual annotations.
- Add UI comparison table.
- Add Playwright supported-answer/abstention smoke tests.
- Complete documentation and demo script.

Acceptance: final demo works and evaluation is reproducible.
Include at least five analysed failures or limitations.

Total original scope estimate: approximately 55 hours.
Prioritise completing the first real demo before expanding features.

## 9. Test strategy

Normal CI:
- Chunking and ingestion tests.
- Document-version replacement.
- Retrieval tests using a small fixed fixture corpus.
- API schema and citation validation.
- Timeout/error handling.
- Generator stub for deterministic engineering tests.
- UI tests with deterministic backend fixtures where necessary.

Model integration:
- Run locally with the real pinned generator.
- Label results separately from stubbed CI tests.
- Record response latency and malformed-output frequency.
- Final demo and held-out evaluation must use real generation.

Required scenarios:
- Supporting section retrieved and cited.
- Unknown question abstains.
- Invented citation rejected.
- Document update removes obsolete chunk.
- Instructions embedded in evidence are not followed in tested cases.
- Model timeout is visible.
- Dataset case IDs and split membership remain stable.

Evaluation reports must include:
- Git commit.
- Corpus and dataset hashes.
- Model/dependency versions.
- Retrieval/prompt configuration.
- Run date and environment.
- Per-question outputs and aggregate metrics.

## 10. Implementation records for future learning

Create and maintain:

AGENTS.md
- Tell future agents to read the plan, current state and implementation log.
- Require documentation to track actual implementation.
- Require claims and explanations to distinguish code, tests and assumptions.

docs/implementation-log.md
For every RQ stage or meaningful correction:
- Step ID and UTC date.
- Goal and actual changes.
- Files and named functions/types.
- Control/data flow.
- Design reasoning.
- Commands/tests and observed results.
- Deviations, limitations and pending work.
- Local Git commit hash when available.

docs/decisions.md
- Explain chunking, model selection, hybrid retrieval, reranking,
  confidence calibration, citation validation and evaluation splitting.

docs/walkthrough.md
- Explain actual ingestion, retrieval, generation, validation and scoring.
- Reference stable function names and relative paths.
- Show representative code excerpts.
- Explain which checks establish structure and which require semantic judgement.

docs/current-state.md
- Current stage/HEAD, model availability, exact launch commands,
  verified/unverified features and next task.

docs/demo.md
- Bootstrap and demo commands.
- Sample questions and expected evidence.
- Document-update example.
- Model failure troubleshooting.

docs/evaluation-report.md
- Comparison table, scoring rubric, measured results and error analysis.
- Link raw machine-readable reports and annotations.

After a verified stage, make a local commit if Git is available and writable.
Do not push without user instruction.
If commits cannot be made, record that explicitly.

At completion, report:
- First-demo and final-demo status.
- Exact launch/demo commands.
- Tests and evaluations actually executed.
- Model/runtime requirements.
- Measured results and limitations.
- Where the implementation records are stored.

For a future question such as "Explain RQ-03", inspect the implementation log,
relevant code revision, tests and evaluation configuration before answering.
Explain the actual implementation rather than reconstructing it from this plan.

## 11. Primary references

pgvector:
https://github.com/pgvector/pgvector

Retrieve and rerank:
https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html

Ollama model family:
https://ollama.com/library/qwen2.5