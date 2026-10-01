"""Build a public, finite preview from saved real development-run outputs."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports/development-20260929T132154Z-reviewed.json"
ANNOTATIONS = ROOT / "reports/development-20260929T132154Z-annotations.json"
HELD_OUT = ROOT / "reports/test-20260929T140703Z-reviewed.json"
DESTINATION = ROOT / "frontend/src/recorded-demo.json"
CASE_IDS = ("dev-a-01", "dev-a-03", "dev-a-04", "dev-u-01")
MODES = ("keyword", "semantic", "hybrid")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    report, annotations, held_out = read(REPORT), read(ANNOTATIONS), read(HELD_OUT)
    by_case = {(row["case_id"], row["mode"]): row for row in report["rows"]}
    judgments = {(row["case_id"], row["mode"]): row for row in annotations["rows"]}
    examples, documents = [], {}
    for case_id in CASE_IDS:
        for mode in MODES:
            row = by_case[(case_id, mode)]
            judgment = judgments[(case_id, mode)]
            output = row["output"]
            assert output and output["status"] in ("answered", "abstained")
            assert len(output["claims"]) == judgment["claim_count"]
            for passage in output["passages"]:
                document_id = passage["document_id"]
                source = (ROOT / "corpus" / f"{document_id}.md").read_text(encoding="utf-8")
                assert f"id: {document_id}\n" in source
                assert f"version: {passage['version']}\n" in source
                documents[document_id] = {
                    "title": passage["title"],
                    "version": passage["version"],
                    "markdown": source,
                }
            examples.append({
                "case_id": case_id,
                "mode": mode,
                "question": row["question"],
                "answer": {key: output[key] for key in (
                    "status", "claims", "reason", "passages", "latency_ms",
                    "retrieval_mode", "model_version", "corpus_version"
                )},
                "review": {key: judgment[key] for key in (
                    "fact_correctness", "supported_claims", "claim_count", "notes"
                )},
            })
    payload = {
        "kind": "recorded-development-preview",
        "source_report": REPORT.name,
        "source_git_commit": report["git_commit"],
        "reviewer": annotations["reviewer"],
        "examples": examples,
        "documents": documents,
        "evaluation": {
            "status": held_out["status"],
            "split": held_out["split"],
            "git_commit": held_out["git_commit"],
            "row_count": len(held_out["rows"]),
            "modes": held_out["modes"],
        },
    }
    DESTINATION.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(examples)} recorded answers and {len(documents)} source documents to {DESTINATION}")


if __name__ == "__main__":
    main()
