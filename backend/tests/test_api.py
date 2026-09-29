import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.generation import ModelError

client=TestClient(app)

@pytest.mark.parametrize('question',['',' '*3,'x'*1001])
def test_api_rejects_invalid_question_before_model(question):
    result=client.post('/v1/ask',json={'question':question})
    assert result.status_code==422

def test_api_model_failure_is_explicit(monkeypatch):
    import app.main as module
    def fail(request):raise ModelError('Local model timed out after 120 seconds')
    monkeypatch.setattr(module,'ask',fail)
    response=client.post('/v1/ask',json={'question':'What should I check?'})
    assert response.status_code==503 and 'timed out' in response.json()['detail']

def test_api_rejects_unknown_mode():
    assert client.post('/v1/ask',json={'question':'Question','retrieval_mode':'magic'}).status_code==422

def test_api_keeps_raw_repair_attempts_out_of_public_metadata(monkeypatch):
    import app.main as module
    from app.schemas import AskResponse
    value=AskResponse(status='answered',claims=[dict(text='Check the audience.',citation_ids=['P1'])],reason='',request_id='test',passages=[],retrieval_mode='hybrid',corpus_version='test',model_version='test',latency_ms=10,
        generation_details={'attempts':[{'response':'INJECTED_VALUE','validation_error':'raw INJECTED_VALUE','validation_error_kind':'claim_policy','eval_count':15,'total_duration':100}]})
    monkeypatch.setattr(module,'ask',lambda request:value)
    response=client.post('/v1/ask',json={'question':'Check auth'})
    assert response.status_code==200 and 'INJECTED_VALUE' not in response.text
    assert response.json()['generation_details']['attempts']==[{'validation_error_kind':'claim_policy','eval_count':15,'total_duration':100}]
    assert 'INJECTED_VALUE' in value.generation_details['attempts'][0]['response']
