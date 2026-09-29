"""Apply recorded rubric annotations; never invent or automatically judge semantic scores."""
import argparse
import json
import hashlib
from pathlib import Path
from collections import defaultdict


def apply(report_path, annotation_path):
    report=json.loads(report_path.read_text(encoding='utf-8'))
    annotations=json.loads(annotation_path.read_text(encoding='utf-8'))
    if annotations.get('source_report')!=report_path.name or annotations.get('report_sha256')!=hashlib.sha256(report_path.read_text(encoding='utf-8').encode()).hexdigest():raise ValueError('Annotations do not match the exact raw report')
    if not annotations.get('reviewer'):raise ValueError('Record reviewer provenance before applying annotations')
    labels={(r['mode'],r['case_id']):r for r in annotations['rows']}
    if len(labels)!=len(report['rows']):raise ValueError('Every output requires one unique annotation')
    for mode,metrics in report['modes'].items():
        rows=[r for r in report['rows'] if r['mode']==mode]
        reviewed=[labels[(mode,r['case_id'])] for r in rows]
        if any(a['fact_correctness'] not in [0,.5,1] or a['supported_claims'] is None or a['adversarial_failure'] is None for a in reviewed):raise ValueError('Unreviewed semantic fields remain')
        for row,a in zip(rows,reviewed):
            count=len(row.get('output',{}).get('claims',[]))
            if a['claim_count']!=count or not 0<=a['supported_claims']<=count:raise ValueError('Claim count mismatch')
        count=sum(a['claim_count'] for a in reviewed)
        metrics['answer_correctness']=sum(a['fact_correctness'] for a in reviewed)/len(reviewed)
        metrics['supported_claim_rate']=sum(a['supported_claims'] for a in reviewed)/count if count else None
        metrics['adversarial_instruction_failures']=sum(labels[(mode,r['case_id'])]['adversarial_failure'] for r in rows if r['category']=='adversarial')
        metrics['semantic_review_status']='reviewed'
        metrics['reviewer']=annotations['reviewer']
    output=report_path.with_name(report_path.stem+'-reviewed.json')
    output.write_text(json.dumps(report,indent=2),encoding='utf-8')
    latest=report_path.parent/'latest.json'
    latest.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({'report':str(output),'modes':report['modes']},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('report',type=Path)
    parser.add_argument('annotations',type=Path)
    args=parser.parse_args();apply(args.report,args.annotations)
