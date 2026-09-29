import os
import uuid
from pathlib import Path
import pytest
from sqlalchemy import select
from app.db import Session, Document, Chunk
from app.ingest import ingest
from app.retrieval import retrieve

pytestmark=pytest.mark.skipif(os.getenv('RUN_DB_TESTS')!='1',reason='Requires migrated PostgreSQL; set RUN_DB_TESTS=1')

def test_atomic_replacement_and_unchanged_skip(tmp_path,monkeypatch):
    import app.ingest as module
    from test_core import Tokenizer
    class Embedder:
        tokenizer=Tokenizer()
        calls=0
        def encode(self, texts, **kw):
            import numpy as np
            self.calls+=1
            return np.array([[1.0]+[0.0]*383 for _ in texts])
    model=Embedder();monkeypatch.setattr(module,'embedder',lambda:model)
    identity='fixture-'+uuid.uuid4().hex
    path=tmp_path/'runbook.md'
    def write(version,value):path.write_text(f'---\nid: {identity}\nversion: {version}\ntitle: Fixture\n---\n## Checks\n{value}')
    try:
        write('1','obsolete advice')
        assert ingest([path])['changed']==1
        assert ingest([path])['unchanged']==1 and model.calls==1
        write('1','different advice')
        with pytest.raises(ValueError,match='Bump version'):ingest([path])
        write('2','current advice')
        assert ingest([path])['changed']==1
        with Session() as s:
            chunks=s.scalars(select(Chunk).where(Chunk.document_id==identity)).all()
            assert all(c.version=='2' and 'obsolete' not in c.text for c in chunks)
            assert any(p.document_id==identity for p in retrieve(s,'current advice','keyword'))
            assert not any(p.document_id==identity for p in retrieve(s,'obsolete advice','keyword') if 'obsolete' in p.text)
        write('3','failed advice')
        def fail(*a,**kw):raise RuntimeError('embedding failed')
        monkeypatch.setattr(model,'encode',fail)
        with pytest.raises(RuntimeError):ingest([path])
        with Session() as s:assert s.get(Document,identity).version=='2'
    finally:
        with Session.begin() as s:
            doc=s.get(Document,identity)
            if doc:s.delete(doc)
