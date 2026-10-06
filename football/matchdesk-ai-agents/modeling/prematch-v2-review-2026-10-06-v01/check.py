"""Independent arithmetic reconstruction: never imports the author's model code."""
import csv, datetime, hashlib, json, math, re
from collections import Counter
from pathlib import Path
import numpy as np

OUT=Path(__file__).parent
P=OUT.parents[1]
D=P.parents[2]/'source-unified-2026-10-06-v01'
A=P/'modeling/prematch-v2-2026-10-06-v01'
checks=[]
def read(name):
    with (D/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def load(path):return json.loads(path.read_text(encoding='utf-8'))
def check(name,expected,actual,ok):
    checks.append(dict(name=name,expected=expected,actual=actual,status='PASS' if ok else 'FAIL'))

completed=read('completed_matches.csv');scheduled=read('scheduled_matches.csv');stats=read('team_match_stats.csv')
historical=load(A/'historical-features.json');bundle=load(A/'future-predictions.json');manifest=load(A/'input-manifest.json');model=load(A/'model.json');frozen=load(A/'evaluation-model.json');metrics=load(A/'metrics.json')
ordered=sorted(completed,key=lambda r:(r['source_date'],r['match_key']))
check('Full dataset cardinality',[2399,641,4798],[len(completed),len(scheduled),len(stats)], [len(completed),len(scheduled),len(stats)]==[2399,641,4798])
check('Input file digests',True,all(hashlib.sha256((D/i['name']).read_bytes()).hexdigest()==i['sha256'] for i in manifest['inputs']),all(hashlib.sha256((D/i['name']).read_bytes()).hexdigest()==i['sha256'] for i in manifest['inputs']))
columns=['points','goals_for','goals_against','xg_for','xg_against','npxg_for','npxg_against','deep','deep_allowed']
neutral=np.array([1.35,1.4,1.4,1.4,1.4,1.25,1.25,7,7,12,12],dtype=float)
keys=['points','gf','ga','xgf','xga','npxgf','npxga','deep','deep_allowed','ppda','ppda_allowed']
lookup={(r['match_key'],r['team_key']):r for r in stats}
record=[]
for r in ordered:
    for team in (r['home_team_key'],r['away_team_key']):
        s=lookup[r['match_key'],team];values=[float(s[c]) if s[c] else math.nan for c in columns]
        for n,d in [('ppda_att','ppda_def'),('ppda_allowed_att','ppda_allowed_def')]:values.append(float(s[n])/float(s[d]) if s[n] and s[d] and float(s[d])>0 else math.nan)
        record.append(dict(league=r['league'],team=team,date=r['source_date'],season=r['season'],key=r['match_key'],v=np.array(values)))
def features(r,future=False):
    # Future games all consume one observed snapshot, never predicted results.
    before=[t for t in record if t['date']<(bundle['cutoff_date'] if future else r['source_date'])]
    league=[t for t in before if t['league']==r['league']]
    league_mean=np.nanmean(np.array([t['v'] for t in league]),axis=0) if league else neutral.copy()
    league_mean=np.where(np.isfinite(league_mean),league_mean,neutral)
    result=[];ev={}
    for side in ['home','away']:
        team=[t for t in league if t['team']==r[side+'_team_key']]
        current=[t for t in team if t['season']==r['season']]
        year=int(r['season'][:4]);previous=[t for t in team if t['season']==f'{year-1}/{str(year)[-2:]}'];recent=current[-5:]
        def smooth(rows,prior,strength):
            matrix=np.array([t['v'] for t in rows]) if rows else np.empty((0,len(keys)))
            return (np.nansum(matrix,axis=0)+strength*prior)/(np.isfinite(matrix).sum(axis=0)+strength)
        prior=smooth(previous,league_mean,8);season=smooth(current,prior,8);smoothed=smooth(recent,season,3)
        gap=min(120,(datetime.date.fromisoformat(r['source_date'])-datetime.date.fromisoformat(team[-1]['date'])).days) if team else 120
        result.extend(smoothed.tolist()+[min(len(current),38),len(recent),min(len(previous),38),int(not previous and len(current)<5),gap])
        ev[side]=dict(current_matches=len(current),previous_season_matches=len(previous),recent_keys=[t['key'] for t in recent],recent_dates=[t['date'] for t in recent])
    return result+[int(r['league']=='EPL')],ev

generated=[];max_error=0;ev_errors=0
for r,h in zip(ordered,historical):
    f,e=features(r);generated.append(f);max_error=max(max_error,float(np.max(np.abs(np.array(f)-h['features']))))
    for side in e:
        for key,value in e[side].items():ev_errors+=h['evidence'][side][key]!=value
check('Independent historical features from strictly earlier CSV dates','2399 × 33, error < 1e-10',dict(shape=[len(generated),len(generated[0])],max_abs_error=max_error),max_error<1e-10)
check('Historical recent keys / previous counts / same-day exclusion',0,ev_errors,ev_errors==0)
check('Historical result labels',True,all(h['label']==(0 if float(r['home_goals'])>float(r['away_goals']) else 1 if float(r['home_goals'])==float(r['away_goals']) else 2) and h['match_key']==r['match_key'] for r,h in zip(ordered,historical)),all(h['label']==(0 if float(r['home_goals'])>float(r['away_goals']) else 1 if float(r['home_goals'])==float(r['away_goals']) else 2) and h['match_key']==r['match_key'] for r,h in zip(ordered,historical)))
future_features=[];future_evidence_errors=0
predictions={r['match_key']:r for r in bundle['predictions']}
for r in scheduled:
    f,e=features(r,True);future_features.append(f);h=predictions[r['match_key']]
    for side in e:
        for key,value in e[side].items():future_evidence_errors+=h['evidence'][side][key]!=value
    future_evidence_errors+=any(h[k]!=r[k] for k in ['league','season','home_team_key','away_team_key']) or h['date']!=r['source_date']
check('Scheduled fixture identities and cutoff histories',0,future_evidence_errors,future_evidence_errors==0)
def predict(m,xx):
    x=(np.array(xx)-m['mean'])/m['scale'];design=np.concatenate([np.ones((len(x),1)),x],axis=1);logits=design@np.array(m['weights']);weights=np.exp(logits-logits.max(axis=1)[:,None]);return weights/weights.sum(axis=1)[:,None]
future_probs=predict(model,future_features);stored=np.array([[predictions[r['match_key']]['probabilities'][c] for c in ['home','draw','away']] for r in scheduled]);difference=float(np.max(np.abs(future_probs-stored)))
check('Independent softmax reproduces all 641 probabilities','error < 1e-12',difference,difference<1e-12)
check('Outcome order and normalized finite probability',True,bool(np.isfinite(stored).all() and (stored>=0).all() and (stored<=1).all() and np.max(abs(stored.sum(axis=1)-1))<1e-12 and bundle['class_order']==['home','draw','away']),bool(np.isfinite(stored).all() and (stored>=0).all() and (stored<=1).all() and np.max(abs(stored.sum(axis=1)-1))<1e-12 and bundle['class_order']==['home','draw','away']))
seasons=Counter(h['season'] for h in historical)
check('Separated season sample counts',{'2023/24':760,'2024/25':760,'2025/26':760,'2026/27':119},dict(seasons),dict(seasons)=={'2023/24':760,'2024/25':760,'2025/26':760,'2026/27':119})
training=[i for i,h in enumerate(historical) if h['season'] in ['2023/24','2024/25']];xx=np.array(generated)[training];scale=xx.std(axis=0);scale[scale<1e-8]=1
check('Frozen normalization fitted on train/validation only','max error < 1e-12',float(max(np.max(abs(xx.mean(axis=0)-frozen['mean'])),np.max(abs(scale-frozen['scale'])))),np.allclose(xx.mean(axis=0),frozen['mean'],rtol=0,atol=1e-12) and np.allclose(scale,frozen['scale'],rtol=0,atol=1e-12))
best=min(metrics['trials'],key=lambda t:t['validation']['log_loss'])['regularization']
check('Tuning rule uses validation loss',best,metrics['chosen_regularization'],best==metrics['chosen_regularization']==frozen['regularization']==model['regularization'])
def measures(indices,p):
    y=np.array([historical[i]['label'] for i in indices]);hits=p.argmax(axis=1)==y;confidence=p.max(axis=1);ece=0
    for j in range(10):
        mask=(confidence>=j/10)&(confidence<((j+1)/10) if j<9 else confidence<=1)
        if mask.any():ece+=mask.mean()*abs(hits[mask].mean()-confidence[mask].mean())
    return dict(n=len(indices),accuracy=float(hits.mean()),log_loss=float(-np.log(p[np.arange(len(y)),y]).mean()),brier_sum_of_three_classes=float(((p-np.eye(3)[y])**2).sum(axis=1).mean()),expected_calibration_error_10bins=float(ece))
metric_errors=[];actual_metrics={}
for season,key in [('2025/26','untouched_test_2025_26'),('2026/27','monitor_2026_27')]:
    ix=[i for i,h in enumerate(historical) if h['season']==season];pp=predict(frozen,np.array(generated)[ix]);baseline=[]
    for i in ix:
        counts=np.ones(3)
        for j in training:
            if historical[j]['league']==historical[i]['league']:counts[historical[j]['label']]+=1
        baseline.append(counts/counts.sum())
    baseline=np.array(baseline);actual_metrics[key]={}
    for league in [None,'EPL','La_liga']:
        pos=[k for k,i in enumerate(ix) if league is None or historical[i]['league']==league];subset=[ix[k] for k in pos];section=metrics[key] if league is None else metrics[key]['by_league'][league]
        for label,prob in [('model',pp),('league_frequency_baseline',baseline)]:
            value=measures(subset,prob[pos]);actual_metrics[key][str(league)+'/'+label]=value
            metric_errors.extend(abs(value[m]-section[label][m]) for m in value)
check('Independent test/monitor/league metrics and baseline arithmetic','max error < 1e-12',max(metric_errors),max(metric_errors)<1e-12)
features_names=model['features']
check('Excluded season snapshots and passing accuracy',False,any('statmuse' in s.lower() or 'pass_accuracy' in s.lower() for s in features_names),not any('statmuse' in s.lower() or 'pass_accuracy' in s.lower() for s in features_names))
check('Not adopted and no invented promotion status',True,bundle['model_accepted'] is False and model['model_accepted'] is False and all(p['evidence'][side]['promotion_status']=='UNKNOWN_NOT_INFERRED_FROM_MISSING_HISTORY' for p in bundle['predictions'] for side in ['home','away']),bundle['model_accepted'] is False and model['model_accepted'] is False and all(p['evidence'][side]['promotion_status']=='UNKNOWN_NOT_INFERRED_FROM_MISSING_HISTORY' for p in bundle['predictions'] for side in ['home','away']))
for name in ['index.html','index.en.html']:
    text=(P/name).read_text(encoding='utf-8');match=re.search(r'<script[^>]+id="prematch-predictions-v22"[^>]*>(.*?)</script>',text,re.S)
    embedded=json.loads(match.group(1)) if match else None
    public_bundle={**bundle,'predictions':[{k:v for k,v in p.items() if k!='evidence'} for p in bundle['predictions']]}
    check(name+' embedded public predictions equal model output (history evidence omitted)',True,embedded==public_bundle,embedded==public_bundle)
out=dict(producer_id='/root/independent_model_review',independent=True,scope='CSV arithmetic, stored model and generated HTML; no browser',passed=sum(c['status']=='PASS' for c in checks),failed=sum(c['status']=='FAIL' for c in checks),checks=checks,recalculated_metrics=actual_metrics)
(OUT/'independent-checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(passed=out['passed'],failed=out['failed'],max_feature_error=max_error,max_probability_error=difference,metrics_error=max(metric_errors))))
raise SystemExit(bool(out['failed']))
