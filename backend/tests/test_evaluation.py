import json
import pytest
from app.evaluation import metric_rows, validate_dataset

def test_empty_claims_are_not_perfect_citations():
    rows=[{'category':'answerable','evidence_recall_at_5':1,'output':{'status':'abstained','claims':[]},'citation_validity':[],'latency_ms':100,'forbidden_marker_hits':[]},{'category':'unsupported','evidence_recall_at_5':None,'output':{'status':'abstained','claims':[]},'citation_validity':[],'latency_ms':200,'forbidden_marker_hits':[]}]
    metrics=metric_rows(rows)
    assert metrics['valid_citation_rate'] is None
    assert metrics['answerable_coverage']==0 and metrics['unsupported_abstention']==1
    assert metrics['answer_correctness'] is None and metrics['supported_claim_rate'] is None

def test_errors_count_as_failed_abstention_and_coverage():
    rows=[{'category':'answerable','evidence_recall_at_5':0,'error':'timeout','citation_validity':[],'latency_ms':120000,'forbidden_marker_hits':[]},{'category':'unsupported','evidence_recall_at_5':None,'error':'offline','citation_validity':[],'latency_ms':500,'forbidden_marker_hits':[]}]
    m=metric_rows(rows)
    assert m['model_errors']==2 and m['answerable_coverage']==0 and m['unsupported_abstention']==0

def test_policy_rejections_are_distinct_from_malformed_json_and_request_failures():
    rows=[{'category':'answerable','evidence_recall_at_5':1,'error':'invalid','citation_validity':[],'latency_ms':10,'forbidden_marker_hits':[],
           'generation_details':{'attempts':[{'validation_error':'directive','validation_error_kind':'claim_policy'},{'validation_error':'EOF','validation_error_kind':'schema_or_citation'},{'request_error':'ReadTimeout'}]}},
          {'category':'unsupported','evidence_recall_at_5':None,'output':{'status':'abstained'},'citation_validity':[],'latency_ms':5,'forbidden_marker_hits':[]}]
    m=metric_rows(rows)
    assert m['policy_rejection_attempts']==1 and m['malformed_output_attempts']==1 and m['generation_attempts']==3
