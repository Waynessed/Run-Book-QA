import os
from pathlib import Path

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://runbookqa:local-demo-only@localhost/runbookqa")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
MODEL = "qwen2.5:1.5b"
MODEL_DIGEST = "65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBED_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RERANK_REVISION = "233902d25c440f23af6f7d6e94d2946bac0bee0a"
CONFIG_PATH = Path(os.getenv("CONFIG_PATH", "/config/retrieval.json"))
CORPUS_PATH = Path(os.getenv("CORPUS_PATH", "/corpus"))
REPORT_PATH = Path(os.getenv("REPORT_PATH", "/reports"))
