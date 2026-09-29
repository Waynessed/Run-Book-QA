"""Real model schema smoke with deliberately irrelevant stored evidence (development only)."""
import json,time
from pathlib import Path
from sqlalchemy import select
from app.db import Session,Chunk,Document
from app.schemas import Passage
from app.generation import generate

with Session() as session:
    chunk=session.scalars(select(Chunk).where(Chunk.document_id=='auth-401',Chunk.section_id=='authentication-checks')).first()
    doc=session.get(Document,chunk.document_id)
    passage=Passage(id='P1',chunk_id=chunk.id,document_id=doc.id,title=doc.title,version=doc.version,heading=chunk.heading,section_id=chunk.section_id,text=chunk.text,score=0)
question='What is the office Wi-Fi password?'
started=time.perf_counter()
answer,model,repair,trace=generate(question,[passage])
result={'question':question,'evidence':[passage.model_dump()],'output':answer.model_dump(),'model_digest':model,'repair_attempted':repair,'generation_details':trace,'latency_ms':(time.perf_counter()-started)*1000}
Path('/reports/conditional-schema-forced-abstention.json').write_text(json.dumps(result,indent=2))
assert answer.status=='abstained' and not answer.claims
print(json.dumps({'status':answer.status,'latency_ms':result['latency_ms'],'repair_attempted':repair}))
