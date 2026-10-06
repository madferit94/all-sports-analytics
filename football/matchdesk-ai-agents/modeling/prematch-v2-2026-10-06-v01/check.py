"""Executable author checks; independent review is separately assigned."""
import collections, copy, json
from pathlib import Path
import numpy as np
import train

P=Path(__file__).parent
# P -> modeling -> matchdesk -> football -> git workspace -> project
dataset=P.parents[4]/'source-unified-2026-10-06-v01'
completed=train.base.load_csv(dataset/'completed_matches.csv')
scheduled=train.base.load_csv(dataset/'scheduled_matches.csv')
stats=train.base.load_csv(dataset/'team_match_stats.csv')
rows,future=train.build_features(completed,scheduled,stats,'2026-10-06')
checks=[]
def check(name,condition):
    assert condition,name
    checks.append(dict(name=name,status='PASS'))
check('actual full stored dataset and 641 scheduled fixtures',len(rows)==2399 and len(future)==641)
check('finite feature vectors and correct model feature dimensions',all(len(r['features'])==len(train.FEATURES) and np.isfinite(r['features']).all() for r in rows+future))
check('all recent evidence strictly before target including same day exclusion',all(d<r['date'] for r in rows+future for side in ['home','away'] for d in r['evidence'][side]['recent_dates']))
check('input order independent',train.build_features(list(reversed(completed)),scheduled,list(reversed(stats)),'2026-10-06')== (rows,future))
target=sorted(completed,key=lambda r:(r['source_date'],r['match_key']))[100]
modified=copy.deepcopy(completed)
for r in modified:
    if r['match_key']==target['match_key']:r['home_goals']='9';r['away_goals']='0'
rerows,_=train.build_features(modified,scheduled,stats,'2026-10-06')
check('target result cannot change its own or earlier feature vectors',all(a['features']==b['features'] for a,b in zip(rows,rerows) if a['date']<=target['source_date']))
past,past_future=train.build_features(completed,scheduled,stats,'2025-01-01')
check('cutoff excludes future completed results',all(r['date']<'2025-01-01' for r in past) and all(d<'2025-01-01' for r in past_future for s in ['home','away'] for d in r['evidence'][s]['recent_dates']))
changed_stats=copy.deepcopy(stats);changed_stats[0]['ppda_def']='0'
zrows,_=train.build_features(completed,scheduled,changed_stats,'2026-10-06')
check('zero PPDA denominator handled without infinity or fake zero ratio',all(np.isfinite(r['features']).all() for r in zrows))
h=collections.defaultdict(list);lh=collections.defaultdict(list)
features,evidence=train.side_features(h,lh,'EPL','new-team','2026/27','2026-10-10')
check('cold start uses explicit league fallback and unknown promotion status',np.allclose(features[:len(train.METRICS)],list(train.NEUTRAL.values())) and evidence['promotion_status'].startswith('UNKNOWN') and features[-2]==1)
model=json.loads((P/'model.json').read_text(encoding='utf-8'))
export=json.loads((P/'future-predictions.json').read_text(encoding='utf-8'))
probs=train.base.predict(model,future)
check('export reproducible from actual trained weights',np.allclose(probs,np.array([list(p['probabilities'].values()) for p in export['predictions']]),rtol=0,atol=1e-12))
check('probabilities normalized and not adopted',np.allclose(probs.sum(axis=1),1) and (probs>=0).all() and export['model_accepted'] is False)
check('no passing accuracy feature invented',not any('pass_accuracy' in f or 'statmuse' in f.lower() for f in train.FEATURES))
result=dict(producer_id='/root/prediction_v2',independent_review=False,passed=len(checks),checks=checks)
path=P/'check-result.json'
if path.exists():
    assert json.loads(path.read_text(encoding='utf-8'))==result,'New result differs: preserve previous evidence and write a new version'
else:
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result))
