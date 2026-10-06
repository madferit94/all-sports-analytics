"""Validate five actual owners, then apply the preserved capability gate."""
import json, argparse
from pathlib import Path
from approval_gate import decide as capability_decide
ROOT=Path(__file__).resolve().parents[1]
ASSIGNMENTS={r['id']:set(r['capabilities']) for r in json.loads((ROOT/'team.json').read_text(encoding='utf-8'))['roles']}

def decide(bundle,base=None):
    errors=[]; reports={}; owners={}
    agents=bundle.get('agents')
    if not isinstance(agents,list):
        return dict(decision='REJECT',reasons=['AGENT_REPORTS_LIST_REQUIRED'],human_release_authorized=False,display_probabilities=False)
    for agent in agents:
        if not isinstance(agent,dict):errors.append('INVALID_AGENT_REPORT');continue
        ident=agent.get('agent_id'); producer=agent.get('producer_id')
        if ident not in ASSIGNMENTS:errors.append('UNKNOWN_AGENT');continue
        if ident in owners:errors.append('DUPLICATE_AGENT_'+ident)
        owners[ident]=producer
        if not isinstance(producer,str) or not producer.strip():errors.append('PRODUCER_REQUIRED_'+ident)
        if agent.get('run_id')!=bundle.get('run_id') or agent.get('match_key')!=bundle.get('match_key'):errors.append('AGENT_IDENTITY_MISMATCH_'+ident)
        parts=agent.get('reports')
        if not isinstance(parts,list):errors.append('CAPABILITY_REPORTS_LIST_REQUIRED_'+ident);continue
        for r in parts:
            if not isinstance(r,dict):errors.append('INVALID_CAPABILITY_REPORT_'+ident);continue
            role=r.get('role')
            if role not in ASSIGNMENTS[ident]:errors.append('WRONG_AGENT_FOR_'+str(role));continue
            if role in reports:errors.append('DUPLICATE_CAPABILITY_'+role)
            if r.get('producer_id')!=producer:errors.append('REPORT_PRODUCER_MISMATCH_'+role)
            reports[role]=r
    producer_ids=list(owners.values())
    if any(producer_ids.count(p)>1 for p in producer_ids if p):errors.append('AGENTS_NOT_DISTINCT')
    if errors:return dict(decision='REJECT',reasons=sorted(set(errors)),human_release_authorized=False,display_probabilities=False)
    legacy=dict(run_id=bundle.get('run_id'),match_key=bundle.get('match_key'),mode=bundle.get('mode','analysis'),reviewer_id=owners.get('director'),reports=reports)
    result=capability_decide(legacy,base=base)
    result['owner_map']=owners
    result['note']='Five-agent ownership checked. Rules do not certify source truth or authorize human release.'
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('input');args=parser.parse_args()
    result=decide(json.loads(Path(args.input).read_text(encoding='utf-8')))
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if result['decision']=='APPROVE' else 1
if __name__=='__main__':raise SystemExit(main())
