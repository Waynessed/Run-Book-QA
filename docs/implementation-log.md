# Implementation log

## RQ-00 / 2026-09-29 UTC — Scaffold and runtime preparation

Goal: establish the smallest real local demo. Read the handoff and inspected the empty repository. Preserved the handoff. Docker pipe access failed under sandbox; elevated execution confirmed a working Linux engine. Git commands need a per-command `-c safe.directory=D:/Projects/RunBookQA` override because repository ownership differs from the sandbox account. User explicitly authorized pushes.

Files: compose.yaml, backend/Dockerfile, backend/requirements.in, backend/migrations, scripts/bootstrap.ps1, scripts/demo.ps1, AGENTS.md. Runtime downloads started. Backend lock resolution uses Python 3.12.10 and uv 0.7.3 in Docker. Models use immutable Hugging Face revisions and Ollama digest verification; container digests will be recorded after pulling.

## RQ-01 / 2026-09-29 UTC — First vertical slice implementation

Files/functions: app/ingest.py (`read_source`, `chunk_source`, `ingest`, `corpus_version`); app/retrieval.py (`retrieve`, `reciprocal_rank_fusion`, `context_passages`); app/generation.py (`generate`, `model_metadata`); app/schemas.py (`GeneratedAnswer`, `validate_citations`); app/service.py (`ask`); frontend/src/main.tsx (`App`); corpus/*.md; evaluation/development-initial.json.

Flow: original Markdown -> tokenizer-aware heading chunks -> CPU embeddings prepared before transaction -> PostgreSQL documents/chunks -> keyword retrieval -> three passages -> Ollama schema-constrained JSON -> Pydantic and citation membership validation -> answer UI -> current source endpoint. Repeatable-read query transactions keep corpus metadata and chunks consistent during updates. Evidence is JSON-encoded as untrusted data. HTTP failures and timeouts become explicit 503 errors; malformed output permits one repair attempt.

Reasoning: retain fixed-stack storage from the first slice; use exact vector search for the small corpus; build replacement chunks before deleting old content; keep source text and document version inspectable. Keyword terms use OR after PostgreSQL stopword/stem normalization because AND across a full natural-language question suppresses useful matches. Semantic/hybrid code is present early but not claimed verified.

Observed commands: Docker version and Git remote checks succeeded with elevation; no remote refs existed. Corpus authoring created ten synthetic runbooks and twenty development-only labels before tuning. Pending: dependency locks, real model response, database migration, ingestion, browser verification, tests, commit hash and push.
## RQ-00 verification / 2026-09-29 UTC

Local commit: 2f03dba (scaffold checkpoint). Qwen downloaded successfully; `docker compose exec -T ollama ollama run qwen2.5:1.5b 'Reply with the word READY only.'` returned READY from real CPU inference. Docker resources: 8 CPUs, 8,212,049,920 bytes RAM; model resident footprint reported 1.4 GB, CPU 100%. First load took 22.11 seconds according to Ollama logs. UI TypeScript/Vite production build passed. API dependency installation still in progress.

Correction: npm audit found initial Vite/Playwright advisories. Updated to Vite 6.4.3 and Playwright 1.63.0, then lock-only install reported zero vulnerabilities. Verified reranker revision via Hugging Face API: 233902d25c440f23af6f7d6e94d2946bac0bee0a.

Push was rejected by automatic approval review because the configured remote destination was not explicitly confirmed. Asked user to confirm Waynessed/Run-Book-QA; pushes pending that reply. Local implementation continues.
## RQ-00 records correction / 2026-09-29 UTC

User confirmed the exact GitHub destination. `git push -u origin codex/runbookqa` succeeded. First checkpoint is now on origin. Pinned database, Ollama, Python and Node image digests in Compose/Dockerfiles after inspecting pulled digests. Added config/runtime.json with observed hardware/runtime assumptions. Patched frontend production build passed with Vite 6.4.3. Added CI and Playwright engineering smoke tests; those tests have not run yet. API image export remains in progress (dependency installation succeeded).
## RQ-01 correction and test / 2026-09-29 UTC

API startup failed with `ModuleNotFoundError: app` inside Alembic. Added `prepend_sys_path = .` to backend/alembic.ini and a read-only backend bind mount for local iteration. Restarted the API; migration succeeded and UI readiness became available. `docker compose exec -T api python -m app.cli ingest` returned changed=10, unchanged=0 from real MiniLM embeddings. `docker compose exec -T -e RUN_DB_TESTS=1 api pytest -q`: 10 passed in 5.66s, two cache warnings from read-only source mount. Disabled the pytest cache provider to avoid those warnings. Tests include a real PostgreSQL update that removes obsolete chunks, unchanged embedding skip, and embedding failure preserving the active version.

First browser UI is reachable and reports local model/corpus ready. Submitted the real supported question; awaiting generation and source inspection. Playwright deterministic smoke execution started.
## RQ-01 real-model correction / 2026-09-29 UTC

First browser question retrieved auth-401 / Authentication checks but Qwen abstained incorrectly, saying the evidence did not directly address the question. Observed end-to-end latency: 113.7s. This is an actual failed supported-answer attempt and does not meet first-demo acceptance. No substitute answer was used.

Changed `generation.SYSTEM_PROMPT` to explicitly recognize symptom/procedure matches and request concrete short checks; serialized only evidence ID/text to reduce irrelevant metadata. Reduced maximum generated tokens from 500 to 300 and retained the model in memory between requests. Added `AskResponse.generation_details` to preserve actual Ollama responses and timing counters for later diagnosis/evaluation. A first scripted retry raced API restart and returned ResponseEnded; added health polling to the verification script before requests. Re-run in progress.
## RQ-01 schema/citation correction / 2026-09-29 UTC

The revised real-model verification still returned abstained on the supported 401 question; acceptance remains unmet. The verification script originally saved only successful answers, so that retry's raw trace was not retained. Corrected it to save every returned attempt before asserting acceptance.

`retrieval.context_passages` now gives context passages short request-local IDs P1/P2/P3, preserving the permanent stored identity in `Passage.chunk_id`. `generation.generate` includes the actual JSON schema in the prompt and constrains citation strings with an enum of supplied IDs. Long chunk identifiers and an implicit response format were unnecessary burdens for the small generator. Deterministic membership validation remains; constraining IDs is still not semantic support validation. Real retry in progress.
## RQ-01 accepted first demo / 2026-09-29 UTC

`scripts/verify-first-demo.ps1` passed: real Qwen returned two claims for the 401 question, actual stored sections were retrievable with matching document versions, and the Wi-Fi question abstained. Supported run: 39,369.52 ms, zero repair attempts. Ollama trace: 1,012 prompt tokens; prompt evaluation 26.96s; 121 generated tokens; generation 10.92s; warm load 0.028s. Full output and timings: reports/first-demo-answer.json. Unsupported output: reports/first-demo-abstention.json.

`REAL_MODEL=1 npm run test:e2e` passed all three browser tests in 38.1s. Supported answer + actual source endpoint took 32.7s; unsupported abstention took 1.8s; error test deliberately used a deterministic 503 fixture (1.1s). First working demo delivered to user at localhost:5174 before corpus expansion. This acceptance demonstrates the real question/evidence/model/source flow, not high semantic accuracy.

Semantic review of that first answer: claim 1 cites Authentication checks correctly; claim 2 cites Verification and handover although the exact release-configuration comparison is in Authentication checks. This is a citation-support failure despite valid IDs. Prompt updated to allow multiple claims citing the same source and to cite the passage actually containing the fact. Requires further measured review.

Further correction found during passage inspection: decoding uncased WordPiece tokens changed source casing and punctuation (AUTH_ISSUER and URL formatting). `chunk_source` now uses tokenizer offset mappings to slice original characters. Added explicit `--rebuild-index` for index-algorithm changes without altering unchanged source document versions. Routine ingestion still skips unchanged embeddings. `corpus_version` now includes chunk hashes as well as document hashes so an index rebuild changes the recorded corpus fingerprint. Real browser acceptance above used the earlier index; corrected index verification is next.
## RQ-02 / 2026-09-29 UTC — Corpus, labels and evaluation foundations

Goal: complete the corpus and author labels before confidence tuning. Added twenty original runbooks using scripts/author-expansion.py (now thirty total), final evaluation/dataset.json and a question-free structural manifest for normal CI. Dataset has 40 development / 60 test cases and all requested category counts. Kept the twenty initial IDs and questions in development. Grouped related questions and adversarial variants by document; no group crosses splits. Corpus word-count validation: all thirty in 250–500 range. Webhook signature runbook contains a synthetic adversarial imported note; its text is evidence to ignore, not an instruction to this implementing session.

Implemented `evaluation.validate_dataset`, `load_cases`, `metric_rows`, `evaluate`, `calibrate`, `freeze`, `file_manifest`, `save_json`. Evaluation saves source candidates, real model outputs/traces, ID/recall checks, failures, timing, environment/configuration and explicit null semantic-review scores. Annotation templates and docs/scoring-rubric.md separate semantic judgement from deterministic structure. Test execution requires explicit allow-held-out plus an unchanged frozen manifest and Git revision. Pending files are written atomically after every case; final reports are saved only when all cases finish.

First-demo commit a42b005 pushed successfully. The subsequent source-preserving reindex succeeded (changed=10). A regression stub expected the entire prompt to be one JSON value and failed after the schema was appended as text: 1 failed, 9 passed. Corrected the production prompt to carry response_schema inside the JSON envelope. That change makes the evidence/schema structure inspectable and aligns the stub with the real payload; rerun pending. Expanded-corpus ingestion and development-only calibration now running.

Quality/comparison decision: all modes use the same calibrated reranker confidence gate. Keyword and semantic keep baseline ordering; their best score over the first three context candidates supplies confidence. Hybrid uses its highest reranked score. The threshold is calibrated on hybrid development candidates, so baseline coverage may regress; report this explicitly. This is not a probability.
## RQ-02 verified replacement / 2026-09-29 UTC

`scripts/document-update.ps1` changed db-pool source version 1 -> 2 and current pool guidance 10 -> 6 connections per replica. Real ingestion returned changed=1, unchanged=29. The current document endpoint and all stored chunks were verified to contain only v2 and no obsolete current-guidance phrase. Saved source in reports/document-update.json. Existing synthetic alert mentioning an old pool setting remains an example of an invalid configuration, not current guidance.

Expanded backend suite: 12 passed in 8.45s, including exact original source casing/punctuation, question-free dataset split manifest, and atomic replacement. Preliminary development calibration selected 0.7685428858, accepting 100% of answerable retrievals and rejecting 100% of unsupported retrievals. This is gate performance only, not model answer correctness. It ran around the document-update demonstration; it will be rerun against the stable final index. Added start/end corpus fingerprint checks to reject concurrent changes in later calibration runs.

Routine correction: a Windows Python editing helper hit the host's GBK default on a UTF-8 frontend file. Reissued those file edits explicitly as UTF-8. Product containers use the pinned Linux runtime. No user text was lost.
