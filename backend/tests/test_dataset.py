import json
from pathlib import Path
from collections import Counter

def evaluation_root():
    return Path('/evaluation') if Path('/evaluation').exists() else Path(__file__).resolve().parents[2]/'evaluation'

def test_dataset_manifest_stable_splits():
    root=evaluation_root()
    cases=json.loads((root/'manifest.json').read_text())['cases']
    assert len(cases)==100 and len({c['id'] for c in cases})==100
    assert Counter((c['split'],c['category']) for c in cases)=={('development','answerable'):24,('development','unsupported'):8,('development','adversarial'):8,('test','answerable'):36,('test','unsupported'):12,('test','adversarial'):12}
    groups={}
    for c in cases:
        assert c['group'] not in groups or groups[c['group']]==c['split']
        groups[c['group']]=c['split']
    initial=json.loads((root/'development-initial.json').read_text())
    assert all(any(c['id']==d['id'] and c['split']=='development' for c in cases) for d in initial)

def test_source_text_preserves_case_and_punctuation():
    from app.ingest import Source,chunk_source
    from test_core import Tokenizer
    value='AUTH_ISSUER=https://identity.northstar.invalid\nMixedCase_Value=42'
    result=chunk_source(Source('exact','1','Exact','## Checks\n'+value),Tokenizer())
    assert result[0]['text'].split('\n',1)[1]==value
