import json
import math
import os
import platform
import statistics
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from importlib.metadata import version
from .db import Session
from .ingest import digest, corpus_version
from .retrieval import retrieve
from .service import ask
from .schemas import AskRequest
from .generation import SYSTEM_PROMPT, model_metadata, ModelError
from .settings import REPORT_PATH, CONFIG_PATH, CORPUS_PATH, EMBED_REVISION, RERANK_REVISION, GENERATION_OPTIONS

DATASET_PATH = Path(os.getenv('DATASET_PATH', '/evaluation/dataset.json'))

def load_cases(split):
    cases=json.loads(DATASET_PATH.read_text())
    validate_dataset(cases)
    return [c for c in cases if c['split']==split]

def validate_dataset(cases):
    if len(cases)!=100 or len({c['id'] for c in cases})!=100:
        raise ValueError('Dataset must have 100 unique stable IDs')
    expected={('development','answerable'):24,('development','unsupported'):8,('development','adversarial'):8,('test','answerable'):36,('test','unsupported'):12,('test','adversarial'):12}
    if Counter((c['split'],c['category']) for c in cases)!=Counter(expected):
        raise ValueError('Dataset category/split counts differ from the handoff')
    groups={}
    for c in cases:
        if c['group'] in groups and groups[c['group']]!=c['split']:
            raise ValueError('Related questions cross splits')
        groups[c['group']]=c['split']
        if c['category']=='unsupported' and not c['expected_abstention']:
            raise ValueError('Unsupported label must abstain')
        if not c['expected_abstention'] and not (c['expected_facts'] and c['supporting_sections']):
            raise ValueError('Supported labels require facts and sources')

def file_manifest():
    files={str(p.relative_to(Path('/app'))):digest(p.read_text()) for p in sorted(Path('/app/app').glob('*.py'))}
    files['requirements.lock']=digest(Path('/app/requirements.lock').read_text())
    files['retrieval.json']=digest(CONFIG_PATH.read_text())
    files['dataset.json']=digest(DATASET_PATH.read_text())
    files['corpus_files']=digest(''.join(p.name+digest(p.read_text()) for p in sorted(CORPUS_PATH.glob('*.md'))))
    return files

def freeze():
    config=json.loads(CONFIG_PATH.read_text())
    if config['threshold'] is None:
        raise ValueError('Calibrate before freezing')
    with Session() as session: frozen_corpus=corpus_version(session)
    manifest={'date':datetime.now(timezone.utc).isoformat(),'git_commit':os.getenv('GIT_COMMIT','unknown'),'files':file_manifest(),'corpus_hash':frozen_corpus,'generator':model_metadata()}
    save_json(REPORT_PATH/'freeze.json',manifest)
    return manifest

def save_json(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value,indent=2),encoding='utf-8')
    temporary.replace(path)

def calibrate():
    if (REPORT_PATH/'freeze.json').exists():
        raise ValueError('Configuration is frozen; archive/reset intentionally before further tuning')
    with Session() as session: calibration_corpus=corpus_version(session)
    rows=[]
    for c in load_cases('development'):
        if c['category']=='adversarial':continue
        with Session() as s: candidates=retrieve(s,c['question'],'hybrid')
        rows.append({'id':c['id'],'category':c['category'],'score':candidates[0].score if candidates else -100.0})
    with Session() as session:
        if corpus_version(session)!=calibration_corpus: raise ValueError('Corpus changed during calibration; rerun on a stable index')
    thresholds=[min(r['score'] for r in rows)-1]+sorted({r['score'] for r in rows})+[max(r['score'] for r in rows)+1]
    choices=[]
    for threshold in thresholds:
        coverage=sum(r['score']>=threshold for r in rows if r['category']=='answerable')/24
        abstention=sum(r['score']<threshold for r in rows if r['category']=='unsupported')/8
        choices.append(dict(threshold=threshold,answerable_retrieval_coverage=coverage,unsupported_retrieval_abstention=abstention,balanced_accuracy=(coverage+abstention)/2,meets_targets=coverage>=.8 and abstention>=.9))
    eligible=[r for r in choices if r['meets_targets']] or choices
    selected=max(eligible,key=lambda r:(r['balanced_accuracy'],r['answerable_retrieval_coverage'],-r['threshold']))
    report={'date':datetime.now(timezone.utc).isoformat(),'split':'development','corpus_hash':calibration_corpus,'dataset_hash':digest(DATASET_PATH.read_text()),'git_commit':os.getenv('GIT_COMMIT','unknown'),'model_revision':RERANK_REVISION,'selected':selected,'scores':rows,'sweep':choices,'note':'Retrieval gate calibration only; generation may further abstain. Scores are not probabilities.'}
    save_json(REPORT_PATH/'calibration.json',report)
    return selected

def metric_rows(rows):
    answerable=[r for r in rows if r['category']=='answerable']
    unsupported=[r for r in rows if r['category']=='unsupported']
    adversarial=[r for r in rows if r['category']=='adversarial']
    citations=[v for r in rows for v in r.get('citation_validity',[])]
    latencies=sorted(r['latency_ms'] for r in rows)
    return {'recall_at_5':statistics.mean(r['evidence_recall_at_5'] for r in answerable),
            'unsupported_abstention':sum(r.get('output',{}).get('status')=='abstained' for r in unsupported)/len(unsupported),
            'answerable_coverage':sum(r.get('output',{}).get('status')=='answered' for r in answerable)/len(answerable),
            'valid_citation_rate':statistics.mean(citations) if citations else None,
            'adversarial_marker_failures':sum(bool(r['forbidden_marker_hits']) for r in adversarial),
            'median_latency_ms':statistics.median(latencies),'p95_latency_ms':latencies[math.ceil(.95*len(latencies))-1],
            'model_errors':sum('error' in r for r in rows),'repair_attempts':sum(r.get('output',{}).get('repair_attempted',False) for r in rows),
            'answer_correctness':None,'supported_claim_rate':None,'semantic_review_status':'pending'}

def evaluate(split):
    if split=='test':
        frozen=json.loads((REPORT_PATH/'freeze.json').read_text())
        if frozen['files']!=file_manifest():raise ValueError('Frozen files changed; held-out run rejected')
        if frozen['git_commit']!=os.getenv('GIT_COMMIT'):raise ValueError('Git revision differs from frozen manifest')
    cases=sorted(load_cases(split),key=lambda c:(c['group'],c['id']))
    with Session() as s: corpus_hash=corpus_version(s)
    if split=='test' and frozen['corpus_hash']!=corpus_hash: raise ValueError('Active index differs from frozen corpus')
    report={'status':'running','date':datetime.now(timezone.utc).isoformat(),'split':split,
            'git_commit':os.getenv('GIT_COMMIT','unknown'),'corpus_hash':corpus_hash,
            'dataset_hash':digest(DATASET_PATH.read_text()),'manifest':file_manifest(),
            'generator':model_metadata(),'generator_options':GENERATION_OPTIONS,'prompt':SYSTEM_PROMPT,
            'config':json.loads(CONFIG_PATH.read_text()),'model_revisions':{'embedding':EMBED_REVISION,'reranker':RERANK_REVISION},
            'dependencies':{p:version(p) for p in ['fastapi','pydantic','sqlalchemy','psycopg','sentence-transformers','transformers','torch','numpy','pgvector']},
            'environment':{'platform':platform.platform(),'cpu_count':os.cpu_count(),'runtime':json.loads(Path('/config/runtime.json').read_text())},'modes':{},'rows':[]}
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    path=REPORT_PATH/f'{split}-{stamp}.json'
    for mode in ['keyword','semantic','hybrid']:
        for c in cases:
            started=time.perf_counter()
            with Session() as s: evidence=retrieve(s,c['question'],mode,limit=5)
            found={f'{p.document_id}:{p.section_id}' for p in evidence}
            expected=set(c['supporting_sections'])
            row={'mode':mode,'case_id':c['id'],'category':c['category'],'question':c['question'],
                 'expected_facts':c['expected_facts'],'supporting_sections':c['supporting_sections'],
                 'retrieved':[p.model_dump() for p in evidence],
                 'evidence_recall_at_5':len(expected&found)/len(expected) if expected else None}
            try:
                result=ask(AskRequest(question=c['question'],retrieval_mode=mode))
                row['output']=result.model_dump()
                ids={p.id for p in result.passages}
                row['citation_validity']=[identity in ids for claim in result.claims for identity in claim.citation_ids]
            except ModelError as exc:
                row['error']=str(exc)
                row['citation_validity']=[]
            answer_text=' '.join(claim['text'] for claim in row.get('output',{}).get('claims',[]))+' '+row.get('output',{}).get('reason','')
            row['forbidden_marker_hits']=[v for v in c['forbidden_behaviours'] if v.lower() in answer_text.lower()]
            row['latency_ms']=round((time.perf_counter()-started)*1000,2)
            report['rows'].append(row)
            save_json(path.with_suffix('.pending.json'),report)
            print(f'{split} {mode} {c["id"]}: {row.get("output",{}).get("status", "error")} ({row["latency_ms"]:.0f} ms)',flush=True)
        report['modes'][mode]=metric_rows([r for r in report['rows'] if r['mode']==mode])
    with Session() as session:
        if corpus_version(session)!=corpus_hash: raise ValueError('Corpus changed during evaluation; partial outputs retained, final report rejected')
    if report['manifest']!=file_manifest(): raise ValueError('Configuration changed during evaluation; final report rejected')
    report['status']='complete'
    save_json(path,report);save_json(REPORT_PATH/'latest.json',report)
    annotations=[{'mode':r['mode'],'case_id':r['case_id'],'fact_correctness':None,'supported_claims':None,'claim_count':len(r.get('output',{}).get('claims',[])),'adversarial_failure':None,'notes':''} for r in report['rows']]
    save_json(path.with_name(path.stem+'-annotations.json'),{'rubric':'/docs/scoring-rubric.md','reviewer':None,'rows':annotations})
    summary=['# '+split+' evaluation','',f'Git: {report["git_commit"]}', '', '| Mode | Recall@5 | Unsupported abstention | Answerable coverage | p95 ms | Errors |','|---|---:|---:|---:|---:|---:|']
    for mode,m in report['modes'].items():summary.append(f'| {mode} | {m["recall_at_5"]:.3f} | {m["unsupported_abstention"]:.3f} | {m["answerable_coverage"]:.3f} | {m["p95_latency_ms"]:.0f} | {m["model_errors"]} |')
    path.with_suffix('.md').write_text('\n'.join(summary)+'\n\nSemantic correctness and support await rubric-based review.\n')
    return {'report':str(path),'modes':report['modes']}
