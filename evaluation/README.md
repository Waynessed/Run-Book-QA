# Dataset provenance

Thirty fictional Northstar runbooks are original repository content. Logs, domains, services, configuration values and incident notes are synthetic. Each file declares a stable ID/version/title. The initial ten were authored before first-demo tuning; the additional twenty and final labels were authored before confidence calibration.

Initial twenty development cases are preserved in development-initial.json. dataset.json is the authoritative final label file; scripts/author-expansion.py is the historical authoring helper, not a launch/reindex step. Narrow expected facts and one document-injection question were refined during label authoring before held-out generation. Re-running the historical authoring helper would overwrite those editorial labels; do not use it to regenerate the final dataset.

Split grouping is by document/topic family for supported/adversarial cases, and separate unsupported topics. Development has twelve supported document families; test has eighteen different families. The normal CI manifest contains IDs/groups/categories/splits but no held-out question text. Normal CI does not generate held-out answers. Calibration selects only development rows; no test outputs are used to choose threshold, prompt or retrieval settings.

The implementing assistant authored the dataset and necessarily saw its contents. This is a held-out execution discipline, not an independently blinded benchmark. Unsupported questions are mostly clearly unrelated office/business topics; results do not measure abstention on difficult near-domain gaps. Shared runbook boilerplate and templated question phrasing further limit generalization claims.
