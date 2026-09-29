# How to review an evaluation

Open a final report and its matching annotation template. Compare each question and expected fact with the generated claims and attached source passages. Use docs/scoring-rubric.md. Fill fact_correctness, supported_claims, adversarial_failure and notes for every mode/case. Set reviewer to a descriptive name and provenance (for example, independent human review or implementing-assistant review).

For a compact view of exact recorded claims and attached evidence, run `python scripts/inspect-evaluation.py reports/<run>.json --start 0 --stop 10`. This prints existing data without assigning scores. It can also inspect an atomic pending file while a run progresses; only final report-bound annotations should be applied.

Run `python scripts/apply-annotations.py reports/<run>.json reports/<run>-annotations.json`. It rejects missing fields, duplicate IDs and incorrect claim counts. It writes a separate reviewed report and updates the latest UI report. Raw outputs remain intact. This operation changes measurements attached to the run; it does not change the generator or retrieval configuration.

No second-model judge is used. Implementing-assistant annotations must be described as model-assisted semantic inspection and are subject to independent human disagreement. A reviewer should not treat valid IDs, exact marker absence or the confidence score as proof of factual support.
