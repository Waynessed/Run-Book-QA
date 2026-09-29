"""Real development-only checks for the measured directive and truncation failures."""
from app.evaluation import load_cases, save_json
from app.generation import ModelError
from app.service import ask
from app.schemas import AskRequest
from app.settings import REPORT_PATH, GENERATION_OPTIONS

cases = {c['id']: c for c in load_cases('development')}
record = {'split': 'development', 'options': GENERATION_OPTIONS, 'rows': []}
for identity, mode in [('dev-a-01', 'hybrid'), ('dev-x-01', 'hybrid'), ('dev-a-09', 'semantic')]:
    case = cases[identity]
    row = {'case_id': identity, 'mode': mode, 'question': case['question']}
    try:
        result = ask(AskRequest(question=case['question'], retrieval_mode=mode))
        row['output'] = result.model_dump()
    except ModelError as error:
        row['error'] = str(error)
        row['generation_details'] = {'attempts': error.traces}
    record['rows'].append(row)
    save_json(REPORT_PATH / 'development-correction-smoke.json', record)
    print(identity, row.get('output', {}).get('status', 'error'), flush=True)
