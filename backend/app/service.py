import json
import time
import uuid
from sqlalchemy import text
from .db import Session
from .ingest import corpus_version
from .retrieval import retrieve, context_passages
from .generation import generate
from .schemas import AskResponse, GeneratedAnswer
from .settings import CONFIG_PATH, MODEL, MODEL_DIGEST

def ask(request):
    started = time.perf_counter()
    # Repeatable-read keeps retrieval and corpus metadata on one document snapshot.
    with Session() as session:
        session.execute(text("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"))
        version = corpus_version(session)
        candidates = retrieve(session, request.question, request.retrieval_mode)
        passages = context_passages(candidates)
    threshold = json.loads(CONFIG_PATH.read_text()).get("threshold") if CONFIG_PATH.exists() else None
    confidence = candidates[0].score if candidates and request.retrieval_mode == "hybrid" else None
    repair = False
    model_version = f"{MODEL}@{MODEL_DIGEST} (generation skipped)"
    if not passages or (confidence is not None and threshold is not None and confidence < threshold):
        answer = GeneratedAnswer(status="abstained", claims=[], reason="The indexed runbooks do not provide sufficiently relevant evidence.")
    else:
        answer, model_version, repair = generate(request.question, passages)
    return AskResponse(**answer.model_dump(), request_id=str(uuid.uuid4()), passages=passages,
                       retrieval_mode=request.retrieval_mode, corpus_version=version, model_version=model_version,
                       latency_ms=round((time.perf_counter() - started) * 1000, 2),
                       retrieval_confidence=confidence, repair_attempted=repair)
