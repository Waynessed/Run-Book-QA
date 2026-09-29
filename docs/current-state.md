# Current state — development comparison reviewed; correction next

Resumed 2026-09-29 12:24 UTC from local pause checkpoint 5579119. Code checkpoint e31a76f is pushed to https://github.com/Waynessed/Run-Book-QA on codex/runbookqa. The user requested continuing the remaining stages. The first complete corrected-schema development comparison from 5579119 is saved and reviewed. A further development-only instruction-validation correction is next.

## Completed and verified

- RQ-00/RQ-01: first real local model demo delivered early. UI http://127.0.0.1:5174; API http://127.0.0.1:8081. Real browser supported-answer/source/abstention checks passed; the browser error scenario used a deterministic fixture.
- RQ-02: thirty original runbooks, one hundred grouped labels (40 development / 60 test), atomic db-pool v1 -> v2 replacement verified, original source characters preserved in chunks.
- RQ-03 partially complete: keyword, semantic and hybrid retrieval, reranking, shared confidence gate, conditional generation schema and raw failed-response traces implemented. First full development comparison completed and reviewed; the next corrected configuration needs its own complete comparison.
- Latest backend/database/API/evaluation suite: 21 passed in 7.11s. Updated deterministic browser suite: 4 passed in 12.3s, including reviewed/unreviewed comparison provenance. No new tests were needed for this documentation-only pause checkpoint.
- Development retrieval calibration: threshold 0.7685428857803345; 24/24 answerable accepted and 8/8 unsupported rejected. These are retrieval-gate measurements, not generation accuracy.
- Real conditional-schema smoke: correct cited issuer/audience claim, empty reason, zero repairs, 27,903.59 ms. Forced irrelevant-evidence generation: abstained, zero claims, zero repairs, 12,390.17 ms. Reports retain raw traces.

## Evaluation history and active run

The earlier ca7857d diagnostic run was interrupted after 31 saved outputs for response-contract corrections. Its tracked raw archive is `reports/development-diagnostic-20260929.json`; partial semantic inspection is `reports/development-diagnostic-annotations.json`. The old ignored `.pending.json` is also still present. These are diagnostic evidence, not a completed comparison.

The corrected development run at e31a76f was stopped with SIGTERM at the user's request. Its host evaluation script exited with `Evaluation failed` because of that intentional stop. No completed case or new pending/final report was saved from this corrected run. A process check at the pause confirmed zero active evaluation processes. On resumption, Docker services and the pinned model were ready with 61 indexed chunks. The fresh development evaluator completed 120 outputs with unchanged-file/corpus checks. No evaluation is active. Raw and reviewed reports plus all annotations are preserved under development-20260929T122416Z.

RQ-04 has not started: configuration is not frozen, held-out generation has not run, final semantic scores and final demo package remain pending. The frontend image was rebuilt on resumption, including the committed comparison columns. Compose also recreated API before evaluation began; an immediate readiness request raced startup and failed, then the subsequent readiness check succeeded. Whole-script bootstrap has not yet been verified end to end. Remote engineering CI passed at e31a76f and 167cbc7.

## Launch and next steps

Read `AGENTS.md`, `RUNBOOKQA_HANDOFF.md`, this record, the implementation log and walkthrough; check Git status before edits. From the repository directory:

```powershell
docker compose ps
docker compose up -d --build web
./scripts/demo.ps1
./scripts/evaluate.ps1 -Split development
```

The evaluator starts a fresh complete 120-output run (40 development cases across three modes); it does not resume partial files. Do not change backend/corpus/configuration or restart API during that run. If Docker services are unavailable, use `./scripts/bootstrap.ps1`; its individual setup steps were verified, but the complete script has not yet been exercised end to end.

Next: implement and verify the observed instruction-validation/trace/budget corrections using development cases, then execute and annotate a fresh full development comparison. Then freeze configuration, explicitly run held-out evaluation and finish final demo/documentation. Do not tune on held-out outputs.

Other commands: `./scripts/test.ps1`, `./scripts/verify-first-demo.ps1`, `./scripts/document-update.ps1` (update already applied). Annotation application was successfully exercised on all 120 completed development outputs; see `docs/review.md`.

Runtime pins are in `config/runtime.json`, `backend/app/settings.py`, dependency locks, Compose and Dockerfiles. Observed hardware: 8 CPUs, 7.6 GiB; local CPU Qwen 1.5B Q4_K_M. Active corpus fingerprint: f52a788b7c3a40916d84fe801640d03dda8f70a3aceb7dc1fa5c16ea88d47b53. Dataset fingerprint: d3b4b55d75919d8a7dfa34230f7d2fd907b658284b7040243ecaca61ef9d04c4.

First complete development hybrid measurements: Recall@5 100%, fact score 70%, supported claims 93.9%, coverage 95.8%, unsupported abstention 100%, three adversarial failures and one model error. These are pre-correction development results, not held-out achievements. See docs/evaluation-report.md.
