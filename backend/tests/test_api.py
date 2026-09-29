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
