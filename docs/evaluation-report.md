# Evaluation report — incomplete at pause

As of 2026-09-29, no complete three-mode generation comparison or held-out evaluation exists. Handoff targets remain goals. The final 100-case grouped dataset is in evaluation/dataset.json; rubric and review instructions are in docs/scoring-rubric.md and docs/review.md.

| Executed check | Observed result | Evidence |
|---|---|---|
| Development retrieval-gate calibration | Threshold 0.7685428857803345; 24/24 answerable accepted, 8/8 unsupported rejected | reports/calibration.json |
| Real conditional-schema supported smoke | Correct cited issuer/audience claim; empty reason; zero repairs; 27,903.59 ms | reports/conditional-schema-smoke-answer.json |
| Real forced irrelevant-evidence smoke | Abstained; zero claims; zero repairs; 12,390.17 ms | reports/conditional-schema-forced-abstention.json |
| Earlier development diagnostic | 31 saved outputs, intentionally interrupted; semantic failures inspected | reports/development-diagnostic-20260929.json; reports/development-diagnostic-annotations.json |

Calibration measures retrieval acceptance, not answer correctness. Smoke timings are individual requests, not aggregate median/p95. Diagnostic annotations are implementing-assistant inspection, not independent human ground truth. See docs/development-findings.md for six analysed examples.

The corrected e31a76f development run was stopped at the user's request before saving a case. Next: fresh complete development comparison, report-bound semantic annotation, freeze, explicitly allowed held-out run and final comparison table. Raw errors and repairs remain part of the reported outcomes.
