# Current state

First working demo delivered (RQ-01): real Qwen supported answer, stored evidence/source endpoint, unsupported abstention and real browser smoke checks passed on 2026-09-29 UTC. Local UI http://127.0.0.1:5174; API http://127.0.0.1:8081. Stack is running. Scaffold commit 2f03dba pushed to origin/codex/runbookqa; next milestone commit pending corrected-index verification.

Commands: `./scripts/bootstrap.ps1`, `./scripts/demo.ps1`, `./scripts/verify-first-demo.ps1`. Engineering tests: `./scripts/test.ps1`; real browser tests: `$env:REAL_MODEL='1'; cd frontend; npm.cmd run test:e2e`.

Verified: 10 runbooks (about 300 words each), 20 initial development labels; database migration/embedding ingestion; real PostgreSQL replacement and embedding-skip tests; 10 backend/database tests; 3 deterministic browser tests; 3 browser checks in real mode (error check remains stubbed); real Qwen readiness, supported response and unsupported abstention. Runtime: Docker CPU 8 cores / 7.6 GiB, generator Q4_K_M; pins in config/runtime.json and image digests in Compose/Dockerfiles.

Quality limitation observed: false abstention in two earlier prompt attempts, and one wrongly attached supporting citation in the first successful response. No claim of semantic accuracy or injection immunity. Source-preserving offset chunking and more explicit citation prompt are now implemented; corrected index must be rebuilt/verified.

Current work: RQ-02 corpus/dataset/evaluation foundations. Next: rebuild index with original source characters, expand to 30 documents and 100 labels, validate splits, then calibrate and compare retrieval with real inference. Held-out evaluation has not run.
