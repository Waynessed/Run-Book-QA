# Step index for later explanations

Read each named log entry and the indicated Git revision before explaining a step. Later fixes may change current behaviour; distinguish that from the behaviour at the historical checkpoint.

| Step | What actually happened | Revision/evidence |
|---|---|---|
| RQ-00-A | Empty repo inspection; Docker permission correction; runtime/dependency scaffold | 2f03dba |
| RQ-00-B | Real Qwen READY response and hardware/runtime inspection | RQ-00 verification log; config/runtime.json |
| RQ-01-A | Ten runbooks, initial labels, ingestion, keyword retrieval, structured generation, UI | 2f03dba |
| RQ-01-B | Alembic import failure corrected; real index and database tests | a42b005 |
| RQ-01-C | False abstention diagnosed; schema-aware prompt and P1 citation aliases | a42b005; first-demo outputs |
| RQ-01-D | Real API/browser/source/unsupported acceptance | a42b005; reports/first-demo-answer.json |
| RQ-01-E | Wrong citation support observed; original-character offset chunking correction | a42b005; corrected index logs |
| RQ-02-A | Corpus expansion, grouped labels and structural manifest | 59c53c1 |
| RQ-02-B | Atomic pool guidance update v1->v2 demonstrated | 59c53c1; reports/document-update.json |
| RQ-02-C | Evaluation/raw reports/rubric and freeze interfaces implemented | 59c53c1 |
| RQ-03-A | Three retrieval modes and shared confidence gate integrated | 1003bae |
| RQ-03-B | Development threshold selected and index/config snapshot guards added | ca7857d; reports/calibration.json |
| RQ-03-C | Partial development diagnostic, 31 outputs and recorded semantic failures | ca7857d; reports/development-diagnostic-20260929.json |
| RQ-03-D | Conditional generation schema and failed raw traces verified | e31a76f; conditional-schema smoke reports |
| RQ-03-E | User-requested pause; corrected comparison stopped before saving a case | Pause log/current-state; full comparison remains pending |
| RQ-03-F | First complete three-mode development run and 120 recorded annotations | 5579119 run; reports/development-20260929T122416Z-reviewed.json |
| RQ-03-G | Narrow directive validation, safe live-answer traces and generation budget correction | Correction log; engineering verification 33 passed; real comparison pending |
| RQ-04 | Freeze, held-out evaluation and final demo | Pending |

- **RQ-03-H**: complete c526532 comparison and 120 applied annotations: reports/development-20260929T132154Z.*; docs/evaluation-report.md. Next RQ-04 freezes this unchanged backend/configuration before test generation.

- **RQ-04-A**: freeze at 39bc696, reports/freeze.json; test-20260929T140703Z serial comparison and reports/test-review-working.json recorded rubric notes. Backend/configuration unchanged after held-out exposure.

- **RQ-04 pause** (2026-09-29 15:12 UTC): complete 180 raw outputs at 39bc696; 177 annotations recorded, three null; no evaluator active. docs/current-state.md lists remaining rows and unexecuted final-demo/browser steps. docs/resume-entry.md records evidence-backed resume wording.

- **RQ-04-B** (2026-10-01): completed all 180 report-bound annotations and applied the reviewed held-out report. Hybrid support 87.5% missed target; one delivered quoted instruction remains. `reports/test-20260929T140703Z-reviewed.json`, `docs/evaluation-report.md`. Docker Desktop unavailable for current live demo verification.
