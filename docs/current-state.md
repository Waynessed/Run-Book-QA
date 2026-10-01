# Current state — recruiter preview in progress

Updated 2026-10-01 (Sydney). Active branch: `codex/runbookqa`. The original held-out evaluation was frozen at `39bc6969de03549d1cf5d7e7d86aee1a21496ffc`; its raw report and freeze manifest remain preserved. Development commits and pushes to Waynessed/Run-Book-QA are authorized.

## Completed evidence

- A real local Qwen-backed API and React UI previously answered questions with inspectable source passages and abstained on unsupported questions. The repository contains 30 original fictional runbooks, 100 grouped labelled questions, atomic document replacement, three retrieval modes, and a calibrated relevance gate.
- The 180 saved held-out model outputs in `reports/test-20260929T140703Z.json` now have all 180 source-inspected annotations. `scripts/apply-annotations.py` verified report identity and claim counts, wrote `reports/test-20260929T140703Z-reviewed.json`, and updated `reports/latest.json`. The raw report is unchanged. Review was performed by the implementing assistant, not an independent human reviewer.
- Frozen keyword / semantic / hybrid Recall@5 was 35/36 (97.2%) in each mode; unsupported abstention was 12/12 in each; answerable coverage was 34/36, 35/36, 35/36. Source-inspected fact scores were 79.2%, 82.5%, 83.3%; claim support was 91.7%, 95.7%, **87.5%**. Hybrid missed the handoff's 90% claim-support target. All cited IDs were supplied evidence IDs, which does not establish semantic support.
- Frozen hybrid delivered one quoted instruction/marker in test-x-07. Other attempted directives were rejected and in some cases produced explicit errors. No general prompt-injection-resistance claim is justified. See `docs/held-out-findings.md`.
- Earlier engineering verification: 33 backend/database/API/evaluation tests, four deterministic browser scenarios, frontend build, cached bootstrap and real model smokes passed. The final real-model browser screenshot and `scripts/final-demo.ps1` have not yet executed.

## Immediate work and environment

On 2026-10-01, `docker compose ps` could not connect to the Docker engine pipe. Docker Desktop was launched from its installed executable, but a later elevated check still found no Linux engine pipe. This prevents current live API/browser verification until its engine becomes available. It does not invalidate saved evaluation outputs.

The finite recorded preview has been built from 12 real saved development responses, original source Markdown and separately labelled frozen aggregate metrics. Its normal and recorded Vite builds passed; four existing fixture browser tests and the new recorded-preview browser test passed. Preview screenshots were inspected. GitHub Pages was observed disabled in repository settings before enabling the Actions publishing source. Backend pytest was not available outside Docker; CI verification of the post-test validator change is pending.

The original frozen result must not be overwritten or recast as a measurement of later fixes. The broader quote-copy guard is a post-test code revision; its generic regression checks are engineering tests, not a fresh independent held-out score. Keep held-out cases out of tuning and ordinary CI.

## Reproduce locally

Start Docker Desktop, run `./scripts/bootstrap.ps1`, then `./scripts/demo.ps1`; open http://127.0.0.1:5174. First launch downloads pinned models. After readiness, run `REAL_MODEL=1` Playwright from `frontend` and `./scripts/final-demo.ps1`; inspect actual responses and screenshot. The original frozen raw/reviewed reports are already complete; do not rerun held-out evaluation just to demonstrate the UI.
