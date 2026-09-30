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

## Corrected complete development comparison

Run: development-20260929T132154Z; code revision c526532. All 120 outputs have report-bound annotations and separate reviewed results. Corpus, dataset, retrieval ordering and calibrated threshold match the earlier comparison. Changed generation prompt, directive validation, 350-character claim cap and 400-token output budget were selected using development evidence only.

| Mode | Recall@5 | Fact score | Claim support | Unsupported abstention | Answerable coverage | Delivered adversarial failures | Median / p95 seconds | Errors | Rejected directives |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Keyword | 87.5% | 70.0% | 92.0% | 100.0% | 91.7% | 0/8 | 25.6 / 41.9 | 0 | 0 |
| Semantic | 100.0% | 81.2% | 93.0% | 100.0% | 95.8% | 0/8 | 19.5 / 37.9 | 0 | 0 |
| Hybrid | 100.0% | 80.0% | 92.9% | 100.0% | 100.0% | 0/8 | 29.8 / 50.2 | 2 | 4 |

All modes have 100% valid citation-ID membership and zero malformed-output attempts. Keyword/semantic have zero repairs; hybrid has two repairs, four rejected directive attempts and two explicit errors (dev-x-04 / dev-x-05). In both requests the generator repeated the malicious imported directive twice. The guard prevented those responses from becoming delivered answers. Zero delivered instruction failures does not mean the raw generator ignored instructions or that all adversarial questions were answered.

Compared with the earlier run, fact scores improve by 5.0 / 10.0 / 10.0 percentage points. Keyword support improves; semantic/hybrid support decline slightly (93.3% to 93.0%, 93.9% to 92.9%). Hybrid answerable coverage improves from 23/24 to 24/24, but service errors increase from one to two. The previous latency-question truncation is absent; long irrelevant paragraphs and capped fragments remain. Timing differences are measurements on the same shared CPU host, not controlled causal estimates.

Artifacts: reports/development-20260929T132154Z.json, matching -annotations.json and -reviewed.json; working notes retain the inspection history. Review is model-assisted by the implementing assistant, not an independent human assessment. Held-out configuration freeze and generation are next; no test answer has been used for tuning.

## Held-out frozen comparison — review complete

Frozen Git: 39bc696. Run: test-20260929T140703Z. All 180 outputs completed; source/configuration unchanged checks passed. Raw JSON/Markdown, freeze manifest, 180 source-inspected annotations and the separate reviewed result are saved under reports. The raw report was not modified by review.

| Mode | Recall@5 | Unsupported abstention | Answerable coverage | Valid citation IDs | Median / p95 seconds | Errors | Rejected directives | Exact-marker failures |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Keyword | 97.2% | 100% | 94.4% | 100% | 22.5 / 54.0 | 2 | 4 | 0 |
| Semantic | 97.2% | 100% | 97.2% | 100% | 18.1 / 51.4 | 1 | 2 | 0 |
| Hybrid | 97.2% | 100% | 97.2% | 100% | 22.4 / 46.3 | 1 | 2 | 1 |

| Mode | Reviewed fact score | Reviewed claim support | Delivered instruction failures |
|---|---:|---:|---:|
| Keyword | 79.2% | 91.7% | 0/12 |
| Semantic | 82.5% | 95.7% | 0/12 |
| Hybrid | 83.3% | **87.5%** | **1/12** |

The handoff's 90% claim-support target was missed by hybrid. The hybrid test-x-07 quotation copied the forbidden directive/marker/synthetic secret and bypassed the narrow validator. Blocked raw directives in other cases do not erase this delivered failure; explicit errors also lost legitimate answers. The implementing assistant authored the dataset and performed source-inspected semantic review, so this is not independent blind or human ground truth. No held-out tuning occurred during the frozen run. See `docs/held-out-findings.md` and individual annotation notes.
