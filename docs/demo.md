# Local demo

Run `./scripts/bootstrap.ps1` from the repository. It starts private database/model services, pulls Qwen, builds API/UI, downloads embedding/reranking models, ingests the corpus and checks readiness. Open http://127.0.0.1:5174. Run `./scripts/demo.ps1` for a command-line 401 question.

Try API 401, container restarting, exhausted database connections, rollback and incident escalation. Click a citation to see the retrieved section and full current document. Unsupported examples: office Wi-Fi password and payroll taxes. Model failures are displayed as errors.

Troubleshooting: `docker compose ps`, `docker compose logs api ollama`. First model downloads need internet and several GB of disk; use a CPU host with at least 8 GB available RAM (16 GB recommended). Generation timeout is 120 seconds per attempt. No GPU or paid API required. Docker Desktop must be running.

Document update and measured comparisons will be added after verification.
