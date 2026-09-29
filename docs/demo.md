# Local demo

Run `./scripts/bootstrap.ps1` from the repository. It starts private database/model services, pulls Qwen, builds API/UI, downloads embedding/reranking models, ingests the corpus and checks readiness. Open http://127.0.0.1:5174. Run `./scripts/demo.ps1` for a command-line 401 question.

Try API 401, container restarting, exhausted database connections, rollback and incident escalation. Click a citation to see the retrieved section and full current document. Unsupported examples: office Wi-Fi password and payroll taxes. Model failures are displayed as errors.

Troubleshooting: `docker compose ps`, `docker compose logs api ollama`. First model downloads need internet and several GB of disk; use a CPU host with at least 8 GB available RAM (16 GB recommended). Generation timeout is 120 seconds per attempt. No GPU or paid API required. Docker Desktop must be running.

The document replacement has been verified. A full measured comparison is being executed; until its final report is saved, the UI has no aggregate results to show.
## Document replacement demo
Run `./scripts/document-update.ps1`. The original db-pool version 1 advised a pool maximum of ten; version 2 advises six. The script ingests the update and checks current source and every active chunk for version 2 and absence of the obsolete phrase. The repository now contains the demonstrated version 2. The replacement regression test independently creates disposable version 1/2 fixtures on every test run.

Evaluation: `./scripts/calibrate.ps1`, `./scripts/evaluate.ps1 -Split development`. Held-out runs require a frozen configuration and `./scripts/evaluate.ps1 -Freeze -Split test -AllowHeldOut`. Read the implementation log before rerunning because a frozen run must keep its code/corpus/dataset/configuration fingerprints unchanged.
