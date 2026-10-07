"""Time-ordered result-history prototype. No target race timing is an input."""
from pathlib import Path
from datetime import datetime,timezone
import json,math,hashlib,unicodedata,joblib
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression,Ridge
ROOT=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
def instant(s):return datetime.fromisoformat(s.replace('Z','+00:00'))
def identity(d):return ''.join(c for c in unicodedata.normalize('NFKD',d['full_name']).casefold() if c.isalpha())
LABELS={
 'recent5_finish_score':{'ko':'최근 5경기 완주 순위 점수','en':'Last-five finishing score'},
 'recent5_points':{'ko':'최근 5경기 평균 포인트','en':'Last-five mean points'},
 'recent5_win_rate':{'ko':'최근 5경기 우승 비율','en':'Last-five win rate'},
 'recent5_podium_rate':{'ko':'최근 5경기 포디움 비율','en':'Last-five podium rate'},
 'recent5_nonfinish_rate':{'ko':'최근 5경기 미완주·미출발·실격 비율','en':'Last-five DNF/DNS/DSQ rate'},
 'season_finish_score':{'ko':'해당 시즌 이전 경기 순위 점수','en':'Season-to-date finishing score'},
 'team_recent5_finish_score':{'ko':'팀 최근 5개 GP 순위 점수','en':'Team last-five GP finishing score'},
 'team_recent5_win_rate':{'ko':'팀 최근 5개 GP 우승 비율','en':'Team last-five GP win rate per entrant'},
 'circuit_past_finish_score':{'ko':'같은 서킷 이전 경기 순위 점수','en':'Earlier same-circuit finishing score'},
 'circuit_past_win_rate':{'ko':'같은 서킷 이전 우승 비율','en':'Earlier same-circuit win rate'},
}
FEATURES=list(LABELS)
def mean(rows,key,default):return float(np.mean([x[key] for x in rows])) if rows else float(default)
def features(d,s,history):
    own=[x for x in history if x['identity']==identity(d)];recent=own[-5:]
    season=[x for x in own if x['year']==s['year']]
    teamall=[x for x in history if x['team']==d['team_name']]
    keys=list(dict.fromkeys(x['session_key'] for x in teamall))[-5:]
    team=[x for x in teamall if x['session_key'] in keys]
    circ=[x for x in own if x['circuit_key']==s['circuit_key']]
    # Fixed neutral priors, blended with a strength of two observations; not fitted on future rows.
    smooth=lambda rows,key,prior:(sum(x[key] for x in rows)+2*prior)/(len(rows)+2)
    f={'recent5_finish_score':smooth(recent,'score',.5),'recent5_points':smooth(recent,'points',4),
       'recent5_win_rate':smooth(recent,'win',.05),'recent5_podium_rate':smooth(recent,'podium',.15),
       'recent5_nonfinish_rate':smooth(recent,'nonfinish',.15),'season_finish_score':smooth(season,'score',.5),
       'team_recent5_finish_score':smooth(team,'score',.5),'team_recent5_win_rate':smooth(team,'win',.05),
       'circuit_past_finish_score':smooth(circ,'score',.5),'circuit_past_win_rate':smooth(circ,'win',.05)}
    refs=own+teamall
    audit={'driver_prior_races':len(own),'same_circuit_prior_races':len(circ),
           'latest_source_end':max([x['end'] for x in refs],default=None),'cold_start':not own}
    return f,audit
def append_race(r,history):
    s=r['session'];ds={d['driver_number']:d for d in r['records']['drivers']};n=len(r['records']['session_result'])
    for result in r['records']['session_result']:
        d=ds.get(result['driver_number']);position=result.get('position')
        if not d:continue
        bad=any(result.get(k) for k in ('dnf','dns','dsq'))
        history.append({'identity':identity(d),'team':d['team_name'],'year':s['year'],'session_key':s['session_key'],
          'circuit_key':s['circuit_key'],'end':s['date_end'],'score':(n-float(position or n))/(n-1),
          'points':float(result.get('points') or 0),'win':int(position==1),'podium':int(position is not None and position<=3),
          'nonfinish':int(bad)})
def probabilities(clf,x):
    z=clf.decision_function(x);z=z-np.max(z);p=np.exp(z);return p/p.sum()
season=load(ROOT.parent/'data/season-2026.json')
races=load(ROOT/'historical-2025.json')['races']+[r for r in season['races'] if r['state']=='completed']
races.sort(key=lambda r:r['session']['date_start'])
history=[];examples=[]
for i,r in enumerate(races):
    s=r['session'];result={x['driver_number']:x for x in r['records']['session_result']}
    drivers=r['records']['drivers']
    n=len(drivers)
    assert sum(result.get(d['driver_number'],{}).get('position')==1 for d in drivers)==1
    rows=[]
    for d in drivers:
        f,a=features(d,s,history)
        assert a['latest_source_end'] is None or instant(a['latest_source_end'])<instant(s['date_start'])
        target=result.get(d['driver_number'],{});y=int(target.get('position')==1) if target else None
        rank=float(target['position']) if target.get('position') is not None else None
        rows.append({'driver_number':d['driver_number'],'identity':identity(d),'features':f,'audit':a,'win':y,'rank_score':(rank-1)/(n-1) if rank is not None else None,'missing_result_position':rank is None})
    examples.append({'session_key':s['session_key'],'start':s['date_start'],'year':s['year'],'rows':rows,'warmup':i<5,'complete_winner_labels':all(row['win'] is not None for row in rows)})
    append_race(r,history)
completed2026=[e for e in examples if e['year']==2026 and e['complete_winner_labels']]
holdkeys={e['session_key'] for e in completed2026[-6:]}
train=[e for e in examples if not e['warmup'] and e['complete_winner_labels'] and e['session_key'] not in holdkeys]
hold=[e for e in examples if e['session_key'] in holdkeys]
def fit(examples):
    rows=[r for e in examples for r in e['rows']];x=np.array([[r['features'][k] for k in FEATURES] for r in rows])
    clf=make_pipeline(StandardScaler(),LogisticRegression(C=1,max_iter=1000,random_state=7))
    ranker=make_pipeline(StandardScaler(),Ridge(alpha=10))
    clf.fit(x,[r['win'] for r in rows]);valid=[i for i,r in enumerate(rows) if r['rank_score'] is not None]
    ranker.fit(x[valid],[rows[i]['rank_score'] for i in valid]);return clf,ranker
clf,ranker=fit(train);evaluations=[]
for e in hold:
    x=np.array([[r['features'][k] for k in FEATURES] for r in e['rows']]);y=np.array([r['win'] for r in e['rows']]);p=probabilities(clf,x)
    baseline=np.array([r['features']['recent5_win_rate'] for r in e['rows']]);baseline/=baseline.sum()
    uniform=np.ones(len(y))/len(y)
    entry={'session_key':e['session_key'],'winner_driver_number':e['rows'][int(y.argmax())]['driver_number']}
    for name,q in [('model',p),('recent_win_baseline',baseline),('uniform',uniform)]:
        entry[name]={'log_loss':float(-np.log(q[y.argmax()])),'multiclass_brier':float(np.sum((q-y)**2)),
         'top1_correct':float(1/np.sum(np.isclose(q,q.max(),rtol=0,atol=1e-14))) if np.isclose(q[y.argmax()],q.max(),rtol=0,atol=1e-14) else 0.,'probabilities':q.tolist()}
    valid=[i for i,r in enumerate(e['rows']) if r['rank_score'] is not None]
    entry['expected_rank_mae']=float(np.mean(np.abs((np.clip(ranker.predict(x)[valid],0,1)-np.array([e['rows'][i]['rank_score'] for i in valid]))*(len(y)-1))))
    evaluations.append(entry)
summary={name:{key:float(np.mean([e[name][key] for e in evaluations])) for key in ('log_loss','multiclass_brier','top1_correct')} for name in ('model','recent_win_baseline','uniform')}
metrics={'model':'standardized logistic winner scores normalized within each race; ridge finishing percentile',
 'hyperparameters':{'logistic_C':1,'max_iter':1000,'ridge_alpha':10,'prior_strength':2,'warmup':5},
 'input_sha256':{str(f.relative_to(ROOT.parent)).replace('\\','/'):hashlib.sha256(f.read_bytes()).hexdigest() for f in [ROOT.parent/'data/season-2026.json',ROOT/'historical-2025.json']},
 'feature_count':len(FEATURES),'features':LABELS,'train_races':len(train),'warmup_races':5,'holdout_races':len(hold),
 'train_session_keys':[e['session_key'] for e in train],'holdout_session_keys':sorted(holdkeys),'excluded_incomplete_result_session_keys':[e['session_key'] for e in examples if not e['complete_winner_labels']],
 'holdout_metrics':summary,'holdout_rank_mae':float(np.mean([e['expected_rank_mae'] for e in evaluations])),
 'evaluation':evaluations,'top1_tie_policy':'Uniform credit across equal maximum-probability entrants; uniform baseline top1 equals 1/field size.','holdout_tuned':False,'serving_refit_after_evaluation':True,'evaluation_protocol':'Fixed last-six completed 2026 races; model frozen for all six; rolling history updates after each actual completed race.',
 'limitations':['Small 2025–2026 sample and 2026 regulation change','Probabilities uncalibrated; race normalization is not empirical calibration','No qualifying grid, future weather, target laps, or race-final standings used','Expected rank is a continuous estimate, not a unique assigned finishing position','Future roster assumed from latest completed GP, not officially confirmed']}
save(ROOT/'modelmetrics.json',metrics)
# Final serving models refit only after untouched holdout evaluation.
serving=[e for e in examples if not e['warmup'] and e['complete_winner_labels']];finalclf,finalrank=fit(serving)
joblib.dump({'classifier':finalclf,'ranker':finalrank,'features':FEATURES},ROOT/'model.joblib')
latest=max([r for r in season['races'] if r['state']=='completed'],key=lambda r:r['session']['date_end'])
roster=latest['records']['drivers'];outputs={}
for r in season['races']:
    if r['state']!='scheduled':continue
    s=r['session'];fs=[features(d,s,history) for d in roster];x=np.array([[f[k] for k in FEATURES] for f,a in fs]);p=probabilities(finalclf,x)
    ranks=1+np.clip(finalrank.predict(x),0,1)*(len(roster)-1)
    outputs[str(s['session_key'])]={'session_key':s['session_key'],'meeting_name':r['meeting']['meeting_name'],
      'circuit_key':s['circuit_key'],'circuit_name':s['circuit_short_name'],'start':s['date_start'],
      'as_of':season['summary']['as_of'],'roster_assumption':'Latest completed GP driver list; future entries unconfirmed',
      'roster_source_session_key':latest['session']['session_key'],'drivers':[{'driver_number':d['driver_number'],
       'name':d['full_name'],'team':d['team_name'],'team_colour':d.get('team_colour'),
       'win_probability':float(p[i]),'expected_rank':float(ranks[i]),'features':fs[i][0],'history':fs[i][1]} for i,d in enumerate(roster)]}
    outputs[str(s['session_key'])]['drivers'].sort(key=lambda d:-d['win_probability'])
save(ROOT/'predictions.json',{'version':'0.2.0','model_id':'f1-logistic-history-2026-10-07-v01','feature_labels':LABELS,'races':outputs,'metrics':summary})
save(ROOT/'feature-audit.json',{'examples':examples,'strict_prior_end_before_target_start':True,'target_performance_features_used':False})
print(json.dumps({'train':len(train),'holdout':len(hold),'serving':len(serving),'scheduled':len(outputs),'metrics':summary},indent=2))
