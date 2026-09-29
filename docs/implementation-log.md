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
## RQ-03 / 2026-09-29 UTC — Retrieval and abstention integration

`retrieve` supports exact cosine semantic search, PostgreSQL keyword ranking and hybrid RRF(k=60) across twenty candidates per baseline, followed by cross-encoder reranking of twenty merged candidates. `service.ask` applies the best reranker-score gate to all modes without changing baseline ordering. Hybrid is now the UI default, matching the API default. Model revisions/digest and image digests are pinned; actual generation options are centralized in settings.GENERATION_OPTIONS and written in reports.

Updated prompt after development-only first-demo observations: prefer one direct short claim, leave answered reason empty, permit reuse of the correct citation. Schema and evidence precede the question in the JSON envelope. Serial evaluation orders cases by group/ID so related questions can reuse Ollama's prompt prefix cache; this scheduling is recorded and identical for all modes. No held-out outputs have been inspected or used for tuning.

Added API boundary/503 tests and evaluation denominator tests (universal abstention cannot score perfect coverage or citation rate; errors count as failed outcomes). Full database suite: 19 passed in 20.15s. One upstream AnyIO BlockingPortal deprecation warning; locked runtime works.

A recalibration attempt was interrupted when API restart terminated its docker-exec process. The host script reported Calibration failed; no successful new report or threshold application was claimed. Re-running after restart/tests finish. Avoid restarting the API or changing corpus while an in-container evaluation/calibration process is active.

Measured development comparison and semantic review are pending. Retrieval calibration's preliminary 100%/100% scores must not be presented as generation accuracy.
## RQ-03 calibration verified / 2026-09-29 UTC

Stable final-corpus calibration completed: threshold 0.7685428857803345, answerable retrieval-gate coverage 24/24, unsupported retrieval-gate abstention 8/8, balanced accuracy 1.0. Corpus fingerprint f52a788b7c3a40916d84fe801640d03dda8f70a3aceb7dc1fa5c16ea88d47b53; dataset fingerprint d3b4b55d75919d8a7dfa34230f7d2fd907b658284b7040243ecaca61ef9d04c4; calibration source revision 1003bae. Full threshold sweep and scores saved in reports/calibration.json; host script applied the threshold to config/retrieval.json. These measurements exclude generation.

Strengthened freeze/evaluation provenance: freeze records the active database corpus fingerprint and exact model metadata. Held-out checks require the active index to match; all evaluations reject source/configuration/corpus changes during the run while preserving partial outputs. Preparing the first full development comparison; prompt/configuration now fixed for that run.
## RQ-03 ongoing development inspection / 2026-09-29 UTC

Full development run began at backend revision ca7857d. First observed 429 keyword output was supported (81.3s), while a related paraphrase gave the same correct fact with a wrong attached source. Later warm 401 cases took 20.2s and 13.0s and cited the exact issuer/audience evidence correctly. Failed 503/restart/adversarial variants are recorded in docs/development-findings.md and reports/development-review-working.json. Aggregate measurements remain pending.

Added scripts/apply-annotations.py and docs/review.md. Annotation application requires a named reviewer, all fields, unique output IDs and matching claim counts; raw reports remain intact. UI table now includes factual correctness and supporting-claim rates, showing Unreviewed until annotations exist. Added question/data provenance and a stable docs/step-index.md for future step explanations. These documentation/UI changes do not alter the active evaluation's backend/prompt/corpus/configuration.

Final hybrid-default UI deterministic smoke: 3 passed in 7.4s. No real model requests were added to the active serial evaluation.
## RQ-03 response-contract correction / 2026-09-29 UTC

Stopped the diagnostic development run after 31 saved outputs to fix an observed contract defect before spending more inference on it. Archived every saved row in reports/development-diagnostic-20260929.json with status interrupted_for_response_contract_correction. This is a partial diagnostic run, not a completed three-mode comparison. The host reported Evaluation failed because the intentional API restart terminated docker-exec. No held-out generation occurred.

Observed defects: answered reasons contained extra uncited assertions despite the prompt asking for an empty reason; rollback and an adversarial scheduler response remained status/claims-inconsistent after the allowed repair. Tightened `GeneratedAnswer.consistent`: answered reason must be empty. Added `generation.response_schema`, a oneOf union enforcing answered/nonempty claims/empty reason versus abstained/empty claims at generation time, retaining the citation enum. Pydantic still independently validates the result, and one repair/error handling remains.

Confirmed oneOf and const support in the exact pinned Ollama 0.6.8 JSON-schema grammar converter: https://raw.githubusercontent.com/ollama/ollama/v0.6.8/llama/llama.cpp/common/json-schema-to-grammar.cpp (oneOf branch at line 796, const at 807). Added regression tests for uncited reason rejection and conditional grammar. Real smoke verification and a complete fresh development comparison are next. Historical RQ-01 successful traces preserved as first-demo-answer-rq01.json / first-demo-abstention-rq01.json before new smoke attempts.
## RQ-03 conditional-schema verification / 2026-09-29 UTC

The tightened schema passed 21 backend/database/API/evaluation tests (13.15s initially, 7.11s after trace retention changes; one locked upstream deprecation warning). Real 401 API smoke passed with one correct P1-supported issuer/audience claim, empty reason, zero repairs and 27,903.59 ms latency. It also verified current source versions and unsupported abstention. Saved current schema smoke separately in conditional-schema-smoke-answer.json / conditional-schema-smoke-abstention.json; restored canonical first-demo historical files so earlier log references remain accurate. Future smoke runs use current-smoke filenames.

`ModelError` now retains actual failed-response traces and whether repair was attempted. `evaluate` saves those on errors and measures malformed-output attempts as well as total generation attempts. The repair prompt keeps previous output and validation error in a JSON data envelope. This addresses the diagnostic run's incomplete raw error trace retention; older diagnostic errors retain only their recorded validation messages and must be described that way.

A forced-irrelevant-evidence real model check is running to exercise the abstained schema branch independently of the retrieval confidence gate. It uses an initial development unsupported question and the actual stored auth-401 passage; no held-out question is involved.
## RQ-03 corrected grammar accepted / 2026-09-29 UTC

Real forced-irrelevant-evidence smoke returned abstained with zero claims, zero repair attempts, and 12,390.17 ms latency. Evidence was the actual stored authentication section; the unsupported Wi-Fi question comes from initial development labels. Full response/trace: reports/conditional-schema-forced-abstention.json. Conditional answered and abstained branches are now both exercised with real pinned Qwen.

Annotation templates now identify the exact raw report filename and SHA-256; scripts/apply-annotations.py rejects mismatched reports. Archived earlier partial semantic inspections separately as development-diagnostic-annotations.json and initialized a fresh working review for the corrected full run. Earlier diagnostic output supports failure analysis only and is not included in final comparison metrics.

## RQ-03 pause checkpoint / 2026-09-29 06:47 UTC

User requested saving progress, a coherent local commit and stopping until later. Code checkpoint e31a76f (conditional schema, failed traces, report-bound annotations) was committed and pushed before this pause. Earlier pushed milestones: 2f03dba, a42b005, 59c53c1, 1003bae, ca7857d.

Stopped the corrected development evaluator with SIGTERM to its in-container process (PID 16), preserving the running API and index. The host scripts/evaluate.ps1 session exited 1 with Evaluation failed as a consequence of this intentional stop. No new corrected-run pending/final file or completed case had been saved. Docker process inspection confirmed Active evaluation processes: []; compose ps showed API, web, database and Ollama still up, database healthy. The historical 31-output diagnostic archive and its annotations remain intact. No held-out generation or freeze was executed.

Updated docs/current-state.md and docs/walkthrough.md with exact verified/unverified status, stop semantics and resume commands. Corrected stale active-run text in docs/step-index.md, docs/development-findings.md and docs/evaluation-report.md. No product code changed and no additional model requests were made for this checkpoint. Latest actual checks remain 21 backend tests, 3 deterministic browser checks, real conditional answered/abstained smoke and development-only retrieval calibration; full generation comparison remains pending.

Resume from a fresh development evaluation, not from the historical partial file: inspect records/Git status, check Docker, rebuild the web image for the committed comparison columns, then scripts/evaluate.ps1 -Split development. The evaluator has no partial-run resume mechanism. Complete comparison and semantic inspection before freezing and explicitly allowing held-out evaluation. This pause documentation is committed locally after e31a76f; its hash is available in Git history. Work stops here until the user resumes.

## RQ-03 resumed comparison / 2026-09-29 12:24 UTC

User requested continuation from local checkpoint 5579119. Git working tree was clean. Docker services remained running; compose up -d --build web rebuilt both web and its API dependency, recreating them before evaluation began. The first immediate readiness request failed during startup; the next check succeeded with 61 chunks and the exact pinned Qwen digest. Started scripts/evaluate.ps1 -Split development at Git 5579119. Backend/corpus/configuration remain fixed throughout the run. First keyword case returned answered in 17.0s; aggregates remain pending.

Added scripts/inspect-evaluation.py to display recorded questions, labels, claims and attached evidence for rubric inspection without assigning automatic scores. Updated review/demo/decision records and current-state to reflect resumption. No held-out generation or final freeze yet.

Resumed UI engineering smoke: npm run test:e2e passed 3 deterministic tests in 23.8s against the rebuilt UI. Provisional manual inspection of the first seven saved development outputs is recorded in reports/development-review-working.json. A correct rate-limit answer still attached generic handover evidence (zero supported claims); a 503 answer mixed relevant checks with unrelated but source-supported 401 advice. These are preserved failures, not a reason to change the active configuration mid-run.

## RQ-03 comparison display verification / 2026-09-29 UTC

The UI now shows review provenance, valid-citation membership rate, manually reviewed adversarial instruction failures, model-error count and median latency alongside the initial comparison table. Pending semantic fields remain Unreviewed; ID membership is explicitly distinguished from support. Added a deterministic browser regression for pending versus reviewed measurements. Rebuilt only web with --no-deps to preserve the evaluator; build passed, four Playwright tests passed in 12.3s. A host npm build attempt from the repository root failed because package.json is under frontend; the container build ran in its proper directory and succeeded.

GitHub Actions inspections confirmed successful engineering checks at e31a76f (run 36532622467) and resumed checkpoint 167cbc7 (run 36568317448). Source/API/corpus/retrieval configuration were unchanged during the active comparison; concurrent frontend build/browser work may influence observed latency on this shared host, so timings are local end-to-end measurements, not an isolated hardware benchmark.

The corrected keyword baseline completed all 40 development cases: Recall@5 0.875, unsupported abstention 8/8, answerable coverage 22/24, valid citation membership 1.0, one marker failure, zero model errors/repairs/malformed attempts, median 25,607.555 ms and p95 50,864.03 ms. These are provisional per-mode measurements saved in the still-running pending report; semantic/support review is separately recorded and the full three-mode report remains pending. Semantic mode is now active. The observed keyword injection failure is described in docs/development-findings.md.

Prepared scripts/final-demo.ps1 (Ask-DemoQuestion) for live supported/unsupported queries, current db-pool v2 source, saved comparison and a live replay of the completed report's document-injection case. It refuses a missing/unreviewed held-out report, so it cannot expose that question during development tuning. PowerShell parser check passed; live execution remains pending. The script saves actual answers and explicitly avoids treating marker absence alone as semantic support or general resistance. Also pinned the CI PostgreSQL image to the already verified Compose digest; CI verification for that change is pending.

Semantic baseline completed 40 development cases: Recall@5 1.0, unsupported abstention 8/8, answerable coverage 22/24, citation membership 1.0, one marker failure, one model error, two repair attempts, three malformed attempts, median 14,979.24 ms and p95 42,557.05 ms. The failed latency case exhausted num_predict=300 on both attempts (done_reason=length), leaving truncated JSON; raw traces are preserved. This illustrates that conditional grammar constrains valid continuations but cannot guarantee completion within the token budget. Hybrid now running; final aggregates/review pending.

## RQ-03-F first complete development comparison / 2026-09-29 UTC

The 5579119 run completed 120 outputs and passed unchanged-file/corpus checks. Applied all 120 source-inspected annotations using scripts/apply-annotations.py; the filename/SHA binding and claim-count validation passed. Raw report, annotations, reviewed report and Markdown summary are retained. Reviewed latest.json now feeds the UI. Keyword/semantic/hybrid fact scores: 0.65/0.7125/0.70; supported-claim rates: 0.9047619/0.9333333/0.9387755. Hybrid Recall@5 1.0, answerable coverage 23/24, unsupported abstention 8/8, three instruction failures, one model error, median 23.248s and p95 52.917s. Keyword/semantic had one instruction failure each. No claim of general resistance or independent human scoring.

Observed corrections to pursue using development outputs: reject explicit role/instruction-override directives in claims/reasons, keep failed raw traces internal to evaluation, remove raw validation input from outward ModelError detail, strengthen relevance/quotation rules and cap short claims while raising the output budget from its observed 300-token truncation. No backend/configuration change occurred during this completed run. A fresh comparison is required after those changes, before any held-out run. CI at 033bf7a also passed (run 36568969740).

## RQ-03-G directive validation and generation completion / 2026-09-29 UTC

First complete comparison checkpoint aa466ae committed and pushed with raw/reviewed reports and all 120 annotations before any correction. Implemented schemas.validate_reply_text / Claim.no_instruction_override / GeneratedAnswer.no_instruction_override with a narrow non-marker-specific imperative pattern. It rejects directive forms observed in development, including abstention reasons, while tests preserve negated warnings and ordinary operational advice. Strengthened SYSTEM_PROMPT relevance and instruction-quotation rules, set claim text cap 350 and GENERATION_OPTIONS.num_predict 400. Corpus, labels, retrieval ordering and confidence threshold unchanged.

Generation tags claim-policy versus schema/citation rejections, retains raw validation traces, records HTTP failure attempts, and gives an explicit generic invalid-output error without echoing raw input. main.ask_endpoint projects trace metadata to safe timing/error fields; service.ask still returns full internal traces for evaluation. Evaluation adds policy_rejection_attempts separately from malformed_output_attempts. UI adds recorded rejected-directive counts, showing Not recorded for historical reports. Prepared backend/development_smoke.py for real development-only normal/known-injection/previously-truncated cases.

After the completed comparison, restarted API and ran real-DB engineering suite: 33 passed in 11.50s, one locked upstream AnyIO deprecation warning. New tests cover directive/negation boundaries, reason enforcement, successful repair with preserved rejected trace, safe outward error, safe public answer metadata and rejection/error denominators. Real correction smoke is now running; fresh complete development comparison still required. No held-out generation or freeze.

Real correction smoke completed: dev-a-01 hybrid answered with correctly supported issuer/audience and header/expiry/clock checks, zero repairs, 83,216.53 ms (cold process/model work plus concurrent web build); dev-x-01 hybrid answered the legitimate same checks without marker or secret, zero repairs, 29,135.03 ms; dev-a-09 semantic returned complete valid JSON, zero repairs, 57,441.33 ms, 255 generated tokens. All actual responses/traces saved in reports/development-correction-smoke.json. The latency answer includes irrelevant extra source text and a claim ending at the 350-character limit, so this verifies completion, not perfect usefulness or prose. Both claims in the mixed 401 answer cite the exact P1 authentication section.

Frontend build passed and updated four deterministic browser tests passed in 11.3s, including rejected-directive visibility. Whole cached-stack bootstrap is being exercised before the fresh comparison; no active evaluator is running during service restart/build.

Whole scripts/bootstrap.ps1 passed on the existing cached stack: Qwen manifest/digest verified, API/web builds succeeded, embedding/reranking models loaded, ingestion changed=0/unchanged=30, readiness 61 chunks with exact pinned digest. This verifies the complete cached launch path; original model downloads were separately verified earlier, but a fresh empty-machine whole-script run was not repeated.

## RQ-03-H fresh corrected comparison / 2026-09-29 UTC

Committed/pushed c526532 after 33 engineering tests, four UI fixtures, three real targeted checks and cached bootstrap succeeded. Started a fresh full development comparison at that revision. App source/corpus/configuration stay fixed through completion. The earlier full report remains an immutable pre-correction comparison, with annotations and failures preserved.

GitHub Actions at c526532 completed successfully (run 36574536932). Keyword and semantic corrected comparisons finished with zero errors/repairs/invalid-output attempts, no delivered adversarial failures in rubric inspection, and unsupported abstention 8/8 each. Keyword reviewed fact score 0.70 and support 0.92; semantic 0.8125 and 0.92982456. These are interim completed-mode measurements; hybrid and final report binding remain pending. Historical pause prose in walkthrough is now explicitly dated to avoid confusing it with current state.

Corrected hybrid dev-x-04 still generated the imported instruction/marker/secret directive twice. Both raw responses were rejected by claim_policy validation, and the outward result was an explicit ModelError. This is executed evidence of the narrow guard blocking delivery, not evidence of an immune generator. The request receives correctness zero because its legitimate rollback question is unanswered. Raw attempt traces remain in the evaluation; no synthetic fallback or configuration change was made.

## RQ-03-H complete reviewed correction / 2026-09-29 UTC

The c526532 run completed all 120 outputs, with unchanged manifest/corpus verified. Applied all 120 annotations successfully; helper verified report SHA, unique identities and actual claim counts. Hybrid fact score 0.80, support 0.92857143, Recall@5 1.0, coverage 24/24, unsupported abstention 8/8, zero delivered instruction failures, two explicit errors, four claim-policy rejections, zero malformed-output attempts; median 29.777s/p95 50.233s. Keyword/semantic fact scores 0.70/0.8125 and support 0.92/0.92982456. Raw responses, notes, annotations, reviewed reports and comparison are preserved separately.

The prompt/budget/validator combination improves development fact scores and removes observed JSON truncation; semantic/hybrid support slightly regresses. Two hybrid requests still generate the malicious directive on both attempts, blocked with visible errors. No held-out tuning or generation yet. Configuration is now final for the held-out measurement; remaining work is freeze/test/review and final demo/package. Expanded README and corrected historical/current documentation status.

The observed blocked hybrid requests exposed a final-demo recording gap: Invoke-RestMethod could terminate before saving its response bundle. Ask-DemoQuestion now records HTTP/transport errors as explicit error objects, so final-demo.json preserves a failing demonstration. Marker absence is not counted as success when the request errors. PowerShell parser passed; live final-demo execution remains pending. This script adjustment does not change the frozen model/retrieval configuration.
