from typing import Literal
from pydantic import BaseModel, Field, ConfigDict, model_validator

class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    retrieval_mode: Literal["keyword", "semantic", "hybrid"] = "hybrid"

    @model_validator(mode="after")
    def nonblank(self):
        self.question = self.question.strip()
        if not self.question:
            raise ValueError("Question must contain text")
        return self

class Claim(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(min_length=1, max_length=600)
    citation_ids: list[str] = Field(min_length=1, max_length=3)

class GeneratedAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["answered", "abstained"]
    claims: list[Claim] = Field(max_length=3)
    reason: str = Field(max_length=600)

    @model_validator(mode="after")
    def consistent(self):
        if (self.status == "answered") != bool(self.claims):
            raise ValueError("Answered needs claims; abstained must have no claims")
        return self

class Passage(BaseModel):
    id: str
    chunk_id: str = ""
    document_id: str
    title: str
    version: str
    heading: str
    section_id: str
    text: str
    score: float

class AskResponse(GeneratedAnswer):
    request_id: str
    passages: list[Passage]
    retrieval_mode: str
    corpus_version: str
    model_version: str
    latency_ms: float
    retrieval_confidence: float | None = None
    repair_attempted: bool = False
    generation_details: dict | None = None

def validate_citations(answer: GeneratedAnswer, passages: list[Passage]):
    allowed = {p.id for p in passages}
    if any(c not in allowed for claim in answer.claims for c in claim.citation_ids):
        raise ValueError("Model invented a citation ID")
    return answer
