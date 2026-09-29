# Current state — development reviewed; ready to freeze

Code checkpoint c526532 committed and pushed to Waynessed/Run-Book-QA, branch codex/runbookqa. The user resumed from pause checkpoint 5579119. First local demo was delivered before corpus expansion. UI http://127.0.0.1:5174; API http://127.0.0.1:8081.

## Current stage

RQ-00/RQ-01 working real local demo and RQ-02 corpus/dataset/atomic replacement are verified. RQ-03 first full comparison at 5579119 completed and received 120 recorded rubric annotations. Its hybrid results: Recall@5 100%, fact score 70%, claim support 93.9%, answerable coverage 23/24, unsupported abstention 8/8, three instruction-following failures, one model error. Raw/reviewed reports and all annotations remain under reports/development-20260929T122416Z.*. These are development results, not held-out achievements.

The observed directive copying and 300-token JSON truncation motivated c526532: narrow instruction-override validators for claims/reasons, stronger evidence/relevance prompt, claim cap 350 characters, generation budget 400 tokens, safe POST answer trace/error metadata and separate policy-rejection metrics. Corpus, dataset, retrieval ordering and threshold are unchanged. No general injection-resistance claim.

The fresh c526532 development comparison completed and all 120 report-bound annotations were applied. Hybrid Recall@5 100%, fact score 80%, support 92.9%, answerable coverage 24/24, unsupported abstention 8/8, zero delivered instruction failures, two explicit errors and four rejected raw directive attempts. Keyword/semantic fact scores 70%/81.25%; support 92%/92.98%. Zero malformed-output attempts in all modes. Raw generator instruction failures remain; the guard blocks delivery in the two error cases. Next: commit this reviewed checkpoint, freeze unchanged backend/corpus/retrieval/generation settings and run held-out evaluation. RQ-04 freeze/test has not begun. Final demo live execution awaits reviewed test results.

## Verification

- Backend/database/API/evaluation: 33 tests passed in 11.50s; one locked upstream AnyIO deprecation warning.
- Frontend build and 4 deterministic browser tests passed (11.3s), including review provenance and rejected-directive display.
- Real correction smoke: supported 401 and mixed-injection 401 both answered with correct P1 citations, zero repairs (83.2s cold/shared build; 29.1s warm). Previously truncated latency case returned complete JSON in 57.4s, zero repairs; extra irrelevant text and a capped fragment remain limitations. Raw traces: reports/development-correction-smoke.json.
- Whole cached-stack bootstrap passed: exact Qwen digest ready, embedding/reranker loaded, ingestion changed=0/unchanged=30, 61 chunks ready. Original downloads were verified earlier; a clean empty-machine full run has not been repeated.
- Atomic db-pool v1 -> v2 replacement verified; current pool maximum six; old current guidance removed. Source characters preserved.
- Development retrieval gate threshold 0.7685428857803345 accepted 24/24 answerable and rejected 8/8 unsupported cases. This is gate calibration, not answer correctness.
- First real browser supported/source/abstention checks passed earlier; browser error scenario uses a fixture. Remote CI at c526532 passed (GitHub Actions run 36574536932).

## Commands

From the repository directory:

```powershell
./scripts/bootstrap.ps1
./scripts/demo.ps1
./scripts/test.ps1
./scripts/evaluate.ps1 -Split development
```

The evaluator starts a fresh complete run; it does not resume partial files. Inspect records and Git status before edits. Current progress files are atomic *.pending.json files (ignored by Git); archive them explicitly if a future pause interrupts the run. The historical 31-output ca7857d diagnostic is already tracked separately. The e31a76f corrected run stopped at the prior user pause before saving any cases.

After a reviewed development run and committed final settings: `./scripts/evaluate.ps1 -Freeze -Split test -AllowHeldOut`. Do not tune using test outputs. Apply report-bound annotations with scripts/apply-annotations.py; inspect claims/evidence with scripts/inspect-evaluation.py. Final demo: ./scripts/final-demo.ps1, only after a complete reviewed test report.

Runtime pins: config/runtime.json, backend/app/settings.py, dependency locks, Compose and Dockerfiles. Observed resources: 8 CPUs, 7.6 GiB, CPU Qwen 1.5B Q4_K_M. Corpus fingerprint f52a788b7c3a40916d84fe801640d03dda8f70a3aceb7dc1fa5c16ea88d47b53; dataset fingerprint d3b4b55d75919d8a7dfa34230f7d2fd907b658284b7040243ecaca61ef9d04c4.
