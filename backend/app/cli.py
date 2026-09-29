import argparse
import json
from .settings import CORPUS_PATH
from .ingest import ingest

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["ingest", "models", "evaluate", "calibrate", "freeze"])
    parser.add_argument("--split", choices=["development", "test"], default="development")
    parser.add_argument("--allow-held-out", action="store_true")
    parser.add_argument("--rebuild-index", action="store_true")
    args = parser.parse_args()
    if args.command == "ingest":
        print(json.dumps(ingest(sorted(CORPUS_PATH.glob("*.md")), args.rebuild_index)))
    elif args.command == "models":
        from .models import embedder, reranker
        embedder(); reranker()
        print("Embedding and reranking models ready")
    else:
        from .evaluation import evaluate, calibrate, freeze
        if args.split == "test" and not args.allow_held_out:
            parser.error("Held-out run requires --allow-held-out and frozen configuration")
        print(json.dumps(calibrate() if args.command == "calibrate" else freeze() if args.command == "freeze" else evaluate(args.split), indent=2))

if __name__ == "__main__":
    main()
