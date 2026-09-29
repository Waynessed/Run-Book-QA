# Current state

RQ-00/RQ-01 in progress. No working demo verified yet. Repository began with only the untracked handoff and an empty Git history. Docker requires elevated execution because the sandbox identity cannot open the Docker named pipe. Elevated Docker works (Desktop 4.92.0, Engine 29.8.0, linux/amd64). Host Node 24.21.0, Python 3.14.7; product uses pinned container runtimes.

Implemented: Compose, initial migration, heading chunking, atomic replacement, keyword/semantic/hybrid retrieval code, structured Ollama generation with citation checks, compact React UI, ten original runbooks, initial twenty development labels. Features remain unverified until model/database/browser checks run.

Launch: `./scripts/bootstrap.ps1`; demo: `./scripts/demo.ps1`. Model downloads and container builds in progress. Next: verify real Qwen response, ingest and browser answer; commit/push milestone. Later: expand corpus/dataset, calibration, evaluation, manual review and final package.
