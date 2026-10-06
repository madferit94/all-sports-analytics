"""Evidence gate, not an LLM judge and not human deployment authorization."""
import json,argparse,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def decide(bundle,base=None):
    base=Path(base or ROOT.parent).resolve();reports=bundle.get('reports',{});mode=bundle.get('mode','analysis');required=['data','analysis','validation','operations']
    if mode in ['prediction','web']:required+=['prediction','model-evaluation']
    if mode=='web':required+=['visualization']
    if mode not in ['analysis','prediction','web']:return {'decision':'REJECT','reasons':['UNKNOWN_MODE'],'human_release_authorized':False}
    hold=[];reject=[]
    for role in required:
        r=reports.get(role)
        if not r:hold.append('MISSING_REPORT_'+role);continue
        for field in ['run_id','match_key','role','producer_id','status','summary','evidence','issues']:
            if field not in r:reject.append('REPORT_FIELD_MISSING_'+role+'_'+field)
        if not isinstance(r.get('issues',[]),list):reject.append('INVALID_ISSUES_'+role)
        elif any(isinstance(issue,dict) and issue.get('severity') in ['BLOCKER','ERROR'] for issue in r.get('issues',[])):reject.append('UNRESOLVED_BLOCKING_ISSUE_'+role)
        if r.get('role')!=role or r.get('run_id')!=bundle.get('run_id') or r.get('match_key')!=bundle.get('match_key'):reject.append('REPORT_IDENTITY_MISMATCH_'+role)
        if not r.get('producer_id'):reject.append('PRODUCER_REQUIRED_'+role)
        if r.get('status')=='FAILED':reject.append('FAILED_'+role)
        elif r.get('status')!='DONE':hold.append('NOT_DONE_'+role)
        if not r.get('evidence'):hold.append('NO_EVIDENCE_'+role)
        for ev in r.get('evidence',[]):
            path=ev.get('path') if isinstance(ev,dict) else None
            if not path:reject.append('INVALID_EVIDENCE_'+role);continue
            target=(base/path).resolve()
            if not target.is_relative_to(base) or not target.is_file():reject.append('EVIDENCE_NOT_FOUND_OR_OUTSIDE_SCOPE_'+role)
    producer_ids={reports[r].get('producer_id') for r in ['data','prediction','analysis','visualization'] if r in reports}
    validator=reports.get('validation',{}).get('producer_id')
    if validator and validator in producer_ids:reject.append('SELF_VALIDATION_NOT_INDEPENDENT')
    evaluator=reports.get('model-evaluation',{}).get('producer_id')
    if mode in ['prediction','web'] and evaluator and evaluator==reports.get('prediction',{}).get('producer_id'):reject.append('SELF_EVALUATION_NOT_INDEPENDENT')
    reviewer=bundle.get('reviewer_id')
    if not reviewer:hold.append('FINAL_REVIEWER_REQUIRED')
    elif reviewer in producer_ids or reviewer in [validator,evaluator]:reject.append('FINAL_REVIEWER_NOT_INDEPENDENT')
    if mode in ['prediction','web']:
        probs=reports.get('prediction',{}).get('probabilities')
        if not isinstance(probs,dict) or set(probs)!= {'home','draw','away'}:hold.append('PROBABILITIES_UNAVAILABLE')
        elif any(not isinstance(v,(int,float)) or isinstance(v,bool) or not math.isfinite(v) or not 0<=v<=1 for v in probs.values()) or abs(sum(probs.values())-1)>1e-6:reject.append('INVALID_PROBABILITIES')
        if reports.get('model-evaluation',{}).get('model_accepted') is not True:hold.append('MODEL_NOT_ACCEPTED')
    return {'decision':'REJECT' if reject else 'HOLD' if hold else 'APPROVE','reasons':reject+hold,'mode':mode,'display_probabilities':not reject and not hold and mode in ['prediction','web'],'human_release_authorized':False,'note':'Rules check only. Final agent must inspect evidence content. Human model adoption/policy/deployment decisions remain separate.'}
def main():
    p=argparse.ArgumentParser();p.add_argument('input');a=p.parse_args();r=decide(json.loads(Path(a.input).read_text(encoding='utf-8')));print(json.dumps(r,indent=2));return 0 if r['decision']=='APPROVE' else 1
if __name__=='__main__':raise SystemExit(main())
