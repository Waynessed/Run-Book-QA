import json
from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from .db import Session, Document
from .generation import ModelError, model_metadata
from .schemas import AskRequest, AskResponse
from .service import ask
from .settings import REPORT_PATH

app = FastAPI(title="RunbookQA", version="0.1.0")

@app.get("/healthz")
def health():
    return {"status": "alive"}

@app.get("/readyz")
def ready():
    try:
        with Session() as session:
            count = session.execute(text("SELECT count(*) FROM chunks")).scalar()
        model = model_metadata()
        if not count:
            raise ValueError("Corpus not indexed; run bootstrap")
        return {"status": "ready", "chunks": count, "model_digest": model["digest"]}
    except Exception as exc:
        raise HTTPException(503, str(exc)) from exc

@app.post("/v1/ask", response_model=AskResponse)
def ask_endpoint(request: AskRequest):
    try:
        result = ask(request)
        if result.generation_details:
            fields = {"model", "created_at", "done", "done_reason", "total_duration", "load_duration",
                      "prompt_eval_count", "prompt_eval_duration", "eval_count", "eval_duration",
                      "request_attempt", "request_error", "validation_error_kind"}
            result = result.model_copy(update={"generation_details": {"attempts": [
                {k: v for k, v in attempt.items() if k in fields}
                for attempt in result.generation_details.get("attempts", [])
            ]}})
        return result
    except ModelError as exc:
        raise HTTPException(503, str(exc)) from exc

@app.get("/v1/documents/{identity}")
def document(identity: str):
    with Session() as session:
        doc = session.get(Document, identity)
        if not doc:
            raise HTTPException(404, "Document not found")
        return {"id": doc.id, "title": doc.title, "version": doc.version, "markdown": doc.markdown,
                "headings": list({c.section_id: c.heading for c in doc.chunks}.items())}

@app.get("/v1/evaluation/latest")
def latest_evaluation():
    path = REPORT_PATH / "latest.json"
    if not path.exists():
        return {"status": "not_run", "message": "No measured evaluation report is available."}
    return json.loads(path.read_text())
