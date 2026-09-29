# Current state — resumed development comparison

Resumed 2026-09-29 12:24 UTC from local pause checkpoint 5579119. Code checkpoint e31a76f is pushed to https://github.com/Waynessed/Run-Book-QA on codex/runbookqa. The user requested continuing the remaining stages. The corrected full development comparison is now running from 5579119.

## Completed and verified

- RQ-00/RQ-01: first real local model demo delivered early. UI http://127.0.0.1:5174; API http://127.0.0.1:8081. Real browser supported-answer/source/abstention checks passed; the browser error scenario used a deterministic fixture.
- RQ-02: thirty original runbooks, one hundred grouped labels (40 development / 60 test), atomic db-pool v1 -> v2 replacement verified, original source characters preserved in chunks.
- RQ-03 partially complete: keyword, semantic and hybrid retrieval, reranking, shared confidence gate, conditional generation schema and raw failed-response traces implemented. Full development comparison remains incomplete.
- Latest backend/database/API/evaluation suite: 21 passed in 7.11s. Deterministic browser suite: 3 passed in 7.4s. No new tests were needed for this documentation-only pause checkpoint.
- Development retrieval calibration: threshold 0.7685428857803345; 24/24 answerable accepted and 8/8 unsupported rejected. These are retrieval-gate measurements, not generation accuracy.
- Real conditional-schema smoke: correct cited issuer/audience claim, empty reason, zero repairs, 27,903.59 ms. Forced irrelevant-evidence generation: abstained, zero claims, zero repairs, 12,390.17 ms. Reports retain raw traces.

## Evaluation history and active run

The earlier ca7857d diagnostic run was interrupted after 31 saved outputs for response-contract corrections. Its tracked raw archive is `reports/development-diagnostic-20260929.json`; partial semantic inspection is `reports/development-diagnostic-annotations.json`. The old ignored `.pending.json` is also still present. These are diagnostic evidence, not a completed comparison.

The corrected development run at e31a76f was stopped with SIGTERM at the user's request. Its host evaluation script exited with `Evaluation failed` because of that intentional stop. No completed case or new pending/final report was saved from this corrected run. A process check at the pause confirmed zero active evaluation processes. On resumption, Docker services and the pinned model were ready with 61 indexed chunks. The fresh development evaluator is now active; keep its backend, corpus and settings fixed.

RQ-04 has not started: configuration is not frozen, held-out generation has not run, final semantic scores and final demo package remain pending. The frontend image was rebuilt on resumption, including the committed comparison columns. Compose also recreated API before evaluation began; an immediate readiness request raced startup and failed, then the subsequent readiness check succeeded. Whole-script bootstrap and remote CI have not been verified as successful.

## Launch and next steps

Read `AGENTS.md`, `RUNBOOKQA_HANDOFF.md`, this record, the implementation log and walkthrough; check Git status before edits. From the repository directory:

```powershell
docker compose ps
docker compose up -d --build web
./scripts/demo.ps1
./scripts/evaluate.ps1 -Split development
```

The evaluator starts a fresh complete 120-output run (40 development cases across three modes); it does not resume partial files. Do not change backend/corpus/configuration or restart API during that run. If Docker services are unavailable, use `./scripts/bootstrap.ps1`; its individual setup steps were verified, but the complete script has not yet been exercised end to end.

Next: complete development comparison, inspect semantic correctness/support with report-bound annotations, record failures and finalize settings. Then freeze configuration, explicitly run held-out evaluation and finish final demo/documentation. Do not tune on held-out outputs.

Other commands: `./scripts/test.ps1`, `./scripts/verify-first-demo.ps1`, `./scripts/document-update.ps1` (update already applied). Annotation application is implemented but has not been exercised on a completed comparison report; see `docs/review.md`.

Runtime pins are in `config/runtime.json`, `backend/app/settings.py`, dependency locks, Compose and Dockerfiles. Observed hardware: 8 CPUs, 7.6 GiB; local CPU Qwen 1.5B Q4_K_M. Active corpus fingerprint: f52a788b7c3a40916d84fe801640d03dda8f70a3aceb7dc1fa5c16ea88d47b53. Dataset fingerprint: d3b4b55d75919d8a7dfa34230f7d2fd907b658284b7040243ecaca61ef9d04c4.
