from functools import lru_cache
from sentence_transformers import SentenceTransformer, CrossEncoder
from .settings import EMBED_MODEL, EMBED_REVISION, RERANK_MODEL, RERANK_REVISION

@lru_cache(maxsize=1)
def embedder():
    model = SentenceTransformer(EMBED_MODEL, revision=EMBED_REVISION, device="cpu")
    model.max_seq_length = 384
    return model

@lru_cache(maxsize=1)
def reranker():
    return CrossEncoder(RERANK_MODEL, revision=RERANK_REVISION, device="cpu")
