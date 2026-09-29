# Current state — paused at user request

Pause checkpoint: 2026-09-29 15:12 UTC (2026-09-30 Sydney). The checkpoint commit is the repository HEAD, recorded by `git log -1`. Frozen evaluation revision: 39bc6969de03549d1cf5d7e7d86aee1a21496ffc; model/validator code checkpoint c526532. User authorized pushes to Waynessed/Run-Book-QA on codex/runbookqa.

## Completed and preserved

RQ-00/RQ-01 real local model demo, RQ-02 30 runbooks/100 grouped labels/atomic replacement, and RQ-03 complete development comparisons and calibrated abstention are verified. Corrected development run c526532 has all 120 applied annotations and raw/reviewed reports.

RQ-04 held-out generation **completed just before this pause**. All 180 real outputs are saved in reports/test-20260929T140703Z.json; its final unchanged-file/corpus checks passed and host evaluator exited zero. Docker Compose top confirms only API startup/uvicorn remain, no evaluator. The initial process check using ps failed because the slim container lacks ps; Docker top supplied the actual confirmation. Demo services remain running at http://127.0.0.1:5174 and API http://127.0.0.1:8081.

Raw held-out measurements for keyword/semantic/hybrid: Recall@5 35/36 (97.22%) each; unsupported abstention 12/12 each; answerable coverage 34/36, 35/36, 35/36; citation-ID membership 100%; explicit errors 2, 1, 1; rejected directive attempts 4, 2, 2; malformed-output attempts zero. Hybrid has one delivered exact-marker/quoted-instruction failure (test-x-07). Never describe the system as generally injection-resistant.

## Review and remaining work

**177/180 semantic annotations are recorded but the held-out annotation application is not complete.** The report-bound annotation file now preserves those 177 values and leaves three rows null. Working notes: reports/test-review-working.json. Remaining: hybrid test-a-33, test-a-34, test-x-11. Do not invent their semantic scores. Raw latest.json exposes pending semantic review; no reviewed test report exists yet.

Keyword/semantic provisional source-inspected fact scores are 79.17%/82.5% and support 91.67%/95.65%; these are not yet published through the all-row annotation helper. Hybrid support/fact aggregate remains unfinalized. docs/held-out-findings.md records failures, including the quoted directive bypass, wrong citations, missed facts and relevance-gate false negatives.

Resume by reviewing the three remaining saved outputs, then applying the exact report-bound annotations with scripts/apply-annotations.py. No new evaluation is needed to finish this review. Keep the frozen settings unchanged; no tuning followed test exposure. Final REAL_MODEL browser run/screenshot, live scripts/final-demo.ps1 and complete final documentation/package remain unexecuted. The script is syntax checked and now saves explicit HTTP failures. Earlier real browser demo and current deterministic browser checks were executed separately.

## Verified engineering checks

- 33 backend/database/API/evaluation tests passed; four deterministic Playwright scenarios and frontend build passed.
- Three real correction smoke checks and complete cached bootstrap passed; active index contains 30 documents and 61 chunks.
- Atomic db-pool v1 -> v2 update verified: current pool maximum six, obsolete current guidance removed.
- GitHub Actions passed at frozen revision 39bc696 (run 36580172289), and at code checkpoint c526532.
- CPU runtime: 8 CPUs and about 7.6 GiB assigned to Docker; pinned Qwen 2.5 1.5B Q4_K_M, embedding/reranker revisions, images and dependency locks.

## Launch and reproduction

After reading records: `./scripts/bootstrap.ps1`, then `./scripts/demo.ps1`; open http://127.0.0.1:5174. First launch downloads models. Do not restart or reindex merely to finish annotation of saved outputs.

The original frozen manifest is reports/freeze.json and belongs to Git 39bc696. This pause commit changes documentation/report records only. Future measurement at a later HEAD must intentionally archive/preserve the original freeze and freeze the unchanged configuration again, or use the original frozen revision; it is a repeat measurement after exposure, not a new blind benchmark. Never tune on test outputs. Evaluator has no partial-run resume, but this run is already complete.

Resume-oriented portfolio wording is saved in docs/resume-entry.md. It uses only verified implementation and structural metrics; no final answer-accuracy, production, scalability, AWS or deployment claim.
