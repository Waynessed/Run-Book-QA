"""Print recorded answers and their attached evidence for rubric-based inspection."""
import argparse
import json
from pathlib import Path


def inspect(path, start=0, stop=None, compact=False):
    report = json.loads(path.read_text(encoding="utf-8"))
    print(f"{path.name}: {report['status']}; {len(report['rows'])} outputs; Git {report['git_commit']}")
    seen = set()
    for index, row in enumerate(report["rows"][start:stop], start):
        output = row.get("output", {})
        print(f"\n[{index}] {row['mode']} {row['case_id']} ({row['category']})")
        print("Question:", row["question"])
        print("Expected:", json.dumps(row["expected_facts"], ensure_ascii=False))
        print("Result:", output.get("status", "error"), output.get("reason", row.get("error", "")))
        passages = {p["id"]: p for p in output.get("passages", [])}
        for claim in output.get("claims", []):
            print("Claim:", claim["text"], "Cites:", claim["citation_ids"])
        cited = {i for c in output.get("claims", []) for i in c["citation_ids"]}
        for identity in sorted(cited):
            passage = passages.get(identity)
            if compact and passage:
                key = passage.get("chunk_id", passage["id"])
                print("Evidence:", identity, key)
                if key not in seen:
                    print(passage["text"])
                    seen.add(key)
            else:
                print("Evidence:", identity, json.dumps(passage, ensure_ascii=False))
        print("Markers:", row["forbidden_marker_hits"], "Latency ms:", row["latency_ms"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--stop", type=int)
    parser.add_argument("--compact", action="store_true", help="Print each distinct evidence chunk once")
    args = parser.parse_args()
    inspect(args.report, args.start, args.stop, args.compact)
