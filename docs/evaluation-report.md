# Evaluation report — development checkpoint

## First complete comparison, before instruction validation correction

Run: development-20260929T122416Z; Git 5579119; same corpus, dataset, generator and settings for all modes. Forty cases per mode, 120 outputs. Raw report: reports/development-20260929T122416Z.json. Recorded rubric annotations: reports/development-20260929T122416Z-annotations.json. Reviewed report: reports/development-20260929T122416Z-reviewed.json.

| Mode | Recall@5 | Fact score | Claim support | Valid citation IDs | Unsupported abstention | Answerable coverage | Adversarial failures | Median / p95 seconds | Errors |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Keyword | 87.5% | 65.0% | 90.5% | 100% | 100% | 91.7% | 1/8 | 25.6 / 50.9 | 0 |
| Semantic | 100% | 71.3% | 93.3% | 100% | 100% | 91.7% | 1/8 | 15.0 / 42.6 | 1 |
| Hybrid | 100% | 70.0% | 93.9% | 100% | 100% | 95.8% | 3/8 | 23.2 / 52.9 | 1 |

Fact score averages the fixed 0/0.5/1 rubric over all forty labelled cases, including unsupported and adversarial cases. Claim support counts generated claims only. IDs being valid does not establish support or correct instruction handling. Review was performed by the implementing assistant with source inspection; it is model-assisted semantic review, not independent human ground truth.

Hybrid improved retrieval and delivery coverage but regressed on instruction-following failures. An imported unapproved note was copied into answers. Semantic and hybrid each had a latency-question error after two 300-token responses ended as incomplete JSON. Generic boilerplate and irrelevant extra advice also appeared; see docs/development-findings.md and individual annotation notes. Concurrent frontend builds/checks on the shared CPU host may influence timings; these are local end-to-end measurements, not an isolated benchmark.

Development retrieval calibration separately accepted 24/24 answerable and rejected 8/8 unsupported cases at threshold 0.7685428857803345 (reports/calibration.json). That gate measurement is not generation accuracy.

## Next

A development-only correction will add a narrow instruction-override output validator, safer public trace/error handling, stronger relevant-evidence prompting and a bounded generation-budget adjustment. A fresh full comparison will verify that configuration before freeze. No held-out generation or configuration freeze has occurred. Handoff targets remain goals.
