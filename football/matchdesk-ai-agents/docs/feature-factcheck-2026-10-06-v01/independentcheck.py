"""Read-only rank ablation verification; no author modeling modules imported."""
import csv, json, collections
from pathlib import Path
import numpy as np

P = Path(__file__).resolve().parents[2]
A = P/'modeling/rank-ablation-2026-10-06-v01'
V = P/'modeling/prematch-v2-2026-10-06-v01'
def read(path): return json.loads(path.read_text(encoding='utf-8'))
report = read(A/'analyst-report.json')
rows = read(V/'historical-features.json')
raw = list(csv.DictReader((P.parents[2]/'source-unified-2026-10-06-v01/completed_matches.csv').open(encoding='utf-8-sig')))
tables = read(A/'derived-raw-tables.json')
audit = read(A/'availability-audit.json')
groups = collections.defaultdict(list)
for r in raw: groups[r['league'],r['season']].append(r)
rankmaps = {}; dates = {}
for t in tables:
    group = groups[t['league'],t['season']]
    assert len(group)==380
    clubs = collections.defaultdict(lambda: [0,0,0,0])
    pairs = collections.Counter()
    for r in group:
        h,a = int(float(r['home_goals'])),int(float(r['away_goals']))
        pairs[r['home_team_key'],r['away_team_key']]+=1
        for side,gf,ga in [('home',h,a),('away',a,h)]:
            c=clubs[r[f'{side}_team_key']]
            c[0]+=1;c[1]+=3 if gf>ga else 1 if gf==ga else 0;c[2]+=gf;c[3]+=ga
    assert len(clubs)==20 and all(v[0]==38 for v in clubs.values())
    assert len(pairs)==380 and set(pairs.values())=={1}
    keys=sorted(clubs,key=lambda k:(-clubs[k][1],-(clubs[k][2]-clubs[k][3]),-clubs[k][2],k))
    mapping={k:i+1 for i,k in enumerate(keys)}
    assert mapping=={c['team_key']:c['raw_proxy_position'] for c in t['clubs']}
    for c in t['clubs']: assert clubs[c['team_key']]==[c['matches'],c['points'],c['gf'],c['ga']]
    rankmaps[t['league'],t['season']]=mapping
    dates[t['league'],t['season']]=max(r['source_date'] for r in group)
    assert dates[t['league'],t['season']]==t['latest_match_date']
features=[]
for r,check in zip(rows,audit):
    previous=f"{int(r['season'][:4])-1}/{str(int(r['season'][:4]))[-2:]}"
    key=(r['league'],previous); mp=rankmaps.get(key,{})
    assert check['match_key']==r['match_key'] and check['previous_season']==previous
    if key in dates: assert dates[key]<r['date']
    positions=[mp.get(r[f'{side}_team_key']) for side in ['home','away']]
    missing=[v is None for v in positions]
    assert missing==[check['home_missing'],check['away_missing']]
    extra=[(v-1)/19 if v else .5 for v in positions]+list(map(float,missing))
    features.append(r['features']+extra)
assert len(rows)==len(audit)==2399
assert all(v[-4:]==[.5,.5,1.,1.] for r,v in zip(rows,features) if r['season']=='2023/24')

def predict(model,x):
    x=np.asarray(x); design=np.c_[np.ones(len(x)),(x-model['mean'])/model['scale']]
    z=design@np.asarray(model['weights']); e=np.exp(z-z.max(axis=1,keepdims=True))
    return e/e.sum(axis=1,keepdims=True)
def scores(y,p):
    hits=p.argmax(1)==y; conf=p.max(1); ece=0.
    for i in range(10):
        mask=(conf>=i/10)&(conf<((i+1)/10) if i<9 else conf<=1)
        if mask.any(): ece+=mask.mean()*abs(hits[mask].mean()-conf[mask].mean())
    return {'n':len(y),'accuracy':float(hits.mean()),'log_loss':float(-np.log(p[np.arange(len(y)),y]).mean()),
        'brier_sum_of_three_classes':float(((p-np.eye(3)[y])**2).sum(1).mean()),'expected_calibration_error_10bins':float(ece)}
b=read(V/'evaluation-model.json'); a=read(A/'augmented-evaluation-model.json')
results={}; maxdelta=0.
for season in ['2025/26','2026/27']:
    mask=[i for i,r in enumerate(rows) if r['season']==season]
    labels=np.array([rows[i]['label'] for i in mask])
    results[season]={}
    for name,model,x in [('original',b,[rows[i]['features'] for i in mask]),('with_prior_raw_rank_proxy',a,[features[i] for i in mask])]:
        probs=predict(model,x)
        assert np.isfinite(probs).all() and np.allclose(probs.sum(1),1)
        got=scores(labels,probs); expected=report['scores'][season][name]['overall']
        delta=max(abs(got[k]-expected[k]) for k in got)
        maxdelta=max(maxdelta,delta);assert delta<1e-12
        results[season][name]=got
print(json.dumps({'producer_id':'/root/feature_review','independent_model_modules_imported':False,
    'complete_tables_verified':len(tables),'matches_features_audited':len(rows),'paired_metrics':results,
    'max_metric_absolute_difference':maxdelta,'status':'PASS'},ensure_ascii=False))
