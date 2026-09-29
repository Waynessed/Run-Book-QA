# Current state

RQ-03 in progress. First real local demo passed and was delivered before expansion. UI http://127.0.0.1:5174, API http://127.0.0.1:8081. Thirty original runbooks indexed, including db-pool v2 with obsolete guidance removed. One hundred stable grouped labels: development 24 answerable/8 unsupported/8 adversarial, test 36/12/12. All twenty initial examples retained in development. Exact source characters are preserved using tokenizer offsets.

Branch codex/runbookqa; commits 2f03dba (scaffold), a42b005 (first demo), 59c53c1 (corpus/evaluation foundations), 1003bae (retrieval/confidence integration) pushed. Next checkpoint records stable calibration. Runtime/image pins in config/runtime.json, compose.yaml and Dockerfiles. Actual full generator digest is checked at runtime. CPU Docker resources: 8 cores, 7.6 GiB.

Executed: real supported API answer (39.4s) and real source/abstention browser checks; 19 backend/database/API/evaluation tests passed; deterministic UI smoke 3 passed; real browser mode 3 passed (model error case intentionally stubbed). Verified changed=1/unchanged=29 document update and no obsolete active chunks. Stable development-only calibration threshold 0.7685428858 accepts 24/24 answerable retrievals and rejects 8/8 unsupported retrievals. This is not generated-answer accuracy.

Launch: `./scripts/bootstrap.ps1`; CLI demo: `./scripts/demo.ps1`; engineering suite: `./scripts/test.ps1`; comparison: `./scripts/evaluate.ps1 -Split development`; document update: `./scripts/document-update.ps1` (already applied). Real UI tests: `$env:REAL_MODEL='1'; cd frontend; npm.cmd run test:e2e`.

Known failures: initial false abstention, a wrongly supported citation in first successful answer, corrected migration import path/source decoding/prompt-envelope regression. All documented in implementation-log.md. Development generation comparison and held-out measurements are pending. Next: run full development comparison, inspect outputs against rubric, freeze configuration, execute held-out run and complete demo/docs. Do not restart API or change corpus/config/code during an active evaluation.
