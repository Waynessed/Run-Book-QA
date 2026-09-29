# Local demo

Run `./scripts/bootstrap.ps1` from the repository. It starts private database/model services, pulls Qwen, builds API/UI, downloads embedding/reranking models, ingests the corpus and checks readiness. Open http://127.0.0.1:5174. Run `./scripts/demo.ps1` for a command-line 401 question.

Try API 401, container restarting, exhausted database connections, rollback and incident escalation. Click a citation to see the retrieved section and full current document. Unsupported examples: office Wi-Fi password and payroll taxes. Model failures are displayed as errors.

Troubleshooting: `docker compose ps`, `docker compose logs api ollama`. First model downloads need internet and several GB of disk; use a CPU host with at least 8 GB available RAM (16 GB recommended). Generation timeout is 120 seconds per attempt. No GPU or paid API required. Docker Desktop must be running.

The document replacement and first full development comparison have been verified. The UI reads the saved reviewed report and names its split/reviewer. The corrected development comparison is complete and reviewed. Held-out generation completed 180 outputs; review is paused at 177/180. The raw comparison shows unreviewed semantic fields, and the final live package remains pending.
## Document replacement demo
Run `./scripts/document-update.ps1`. The original db-pool version 1 advised a pool maximum of ten; version 2 advises six. The script ingests the update and checks current source and every active chunk for version 2 and absence of the obsolete phrase. The repository now contains the demonstrated version 2. The replacement regression test independently creates disposable version 1/2 fixtures on every test run.

Development evaluation: `./scripts/evaluate.ps1 -Split development`. The threshold is already calibrated; `./scripts/calibrate.ps1` deliberately rejects an existing freeze and must not be used to tune against test results. Held-out runs require a frozen configuration and `./scripts/evaluate.ps1 -Freeze -Split test -AllowHeldOut`. Read the implementation log before rerunning because a frozen run must keep its code/corpus/dataset/configuration fingerprints unchanged.
