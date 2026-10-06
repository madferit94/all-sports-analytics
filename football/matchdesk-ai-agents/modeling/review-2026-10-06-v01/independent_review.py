import csv,json,hashlib,math,sys,subprocess
from pathlib import Path
from datetime import date,datetime,timezone
from collections import Counter,defaultdict
sys.dont_write_bytecode=True
import numpy as np
D=Path(__file__).resolve().parent; M=D.parent; REPO=M.parent
BASE=next(p for p in REPO.parents if p.name=='ai-agent-planning-2026-10-06-v01')
DS=BASE/'source-unified-2026-10-06-v01'; RUN=M/'runs/2026-10-06-v01'
sys.path.insert(0,str(M));import train_baseline as code
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
load=lambda p:list(csv.DictReader(p.open(encoding='utf-8-sig')))
checks=[];failures=[]
def check(name,expected,actual,tol=None):
 ok=abs(expected-actual)<=tol if tol is not None else expected==actual
 item={'name':name,'expected':expected,'actual':actual,'passed':bool(ok)};checks.append(item)
 if not ok:failures.append(item)
def save(name,obj):
 with (D/name).open('x',encoding='utf-8') as f:json.dump(obj,f,ensure_ascii=False,indent=2)
completed=load(DS/'completed_matches.csv');scheduled=load(DS/'scheduled_matches.csv')
manifest=read(RUN/'input_manifest.json');hist=read(RUN/'historical_features.json');future=read(RUN/'future_inputs.json');model=read(RUN/'model.json');stored=read(RUN/'metrics.json')
for f in manifest['files']:check('Input SHA256 '+f['name'],f['sha256'],hashlib.sha256((DS/f['name']).read_bytes()).hexdigest())
check('Completed input size',2399,len(completed));check('Scheduled input size',641,len(scheduled));check('Last completed date','2026-09-20',max(r['source_date'] for r in completed));check('Dataset refreshed',False,manifest['dataset_refreshed']);check('Class order',['home','draw','away'],model['class_order'])
# Independent feature reconstruction by scanning dated team records, rather than calling build_features.
team_rows=defaultdict(list)
for r in completed:
 if r['source_date']<manifest['cutoff_date']:
  for side in ['home','away']:team_rows[(r['league'],r[side+'_team_key'])].append(r)
for key in team_rows:team_rows[key].sort(key=lambda r:(r['source_date'],r['match_key']))
index={r['match_key']:r for r in completed+scheduled}
feature_errors=[];history_errors=[];label_errors=[]
for item in hist+future:
 r=index[item['match_key']]; sides=[]
 for side in ['home','away']:
  t=r[side+'_team_key'];prior=[p for p in team_rows[(r['league'],t)] if p['source_date']<r['source_date'] and p['source_date']<manifest['cutoff_date']][-5:]
  want_keys=[p['match_key'] for p in prior]
  if item['history_keys'][side]!=want_keys:history_errors.append(item['match_key']+' '+side)
  if not prior:vector=[1.3]*5+[0.,30.]
  else:
   stats=[]
   for p in prior:
    h=p['home_team_key']==t;gf=float(p['home_goals' if h else 'away_goals']);ga=float(p['away_goals' if h else 'home_goals']);xf=float(p['home_xg' if h else 'away_xg']);xa=float(p['away_xg' if h else 'home_xg'])
    stats.append([3 if gf>ga else 1 if gf==ga else 0,xf,xa,gf,ga])
   vector=np.asarray(stats).mean(axis=0).tolist()+[float(len(prior)),float(min((date.fromisoformat(r['source_date'])-date.fromisoformat(prior[-1]['source_date'])).days,60))]
  sides.append(vector)
 expected=[v for pair in zip(*sides) for v in pair]+[float(r['league']=='EPL')]
 if not np.allclose(expected,item['features'],atol=1e-12,rtol=0):feature_errors.append(item['match_key'])
 if 'label' in item:
  expected_label=0 if float(r['home_goals'])>float(r['away_goals']) else 1 if float(r['home_goals'])==float(r['away_goals']) else 2
  if item['label']!=expected_label:label_errors.append(item['match_key'])
check('Independent feature rows checked',2401,len(hist+future));check('Feature mismatches',[],feature_errors);check('History key/date mismatches',[],history_errors);check('Label mismatches',[],label_errors)
parts={s:[r for r in hist if r['season']==s] for s in ['2023/24','2024/25','2025/26','2026/27']}
check('Split sizes',{'2023/24':760,'2024/25':760,'2025/26':760,'2026/27':119},{s:len(v) for s,v in parts.items()})
for a,b in zip(list(parts)[:-1],list(parts)[1:]):check('Strict chronology '+a+' to '+b,True,max(r['date'] for r in parts[a])<min(r['date'] for r in parts[b]))
x=np.asarray([r['features'] for r in hist]);scale=x.std(axis=0);scale[scale<1e-8]=1
check('Final model training-only mean error',0.,float(np.max(np.abs(x.mean(axis=0)-model['mean']))),1e-12);check('Final model training-only scale error',0.,float(np.max(np.abs(scale-model['scale']))),1e-12)
# Independent prediction expression from serialized coefficients.
def independent_probs(m,rs):
 a=np.asarray([r['features'] for r in rs]);a=(a-np.array(m['mean']))/np.array(m['scale']);logits=np.c_[np.ones(len(a)),a]@np.array(m['weights']);logits-=np.max(logits,axis=1,keepdims=True);e=np.exp(logits);return e/e.sum(axis=1,keepdims=True)
fp=independent_probs(model,future);csvpred=load(RUN/'predictions.csv');pred_index={r['match_key']:r for r in csvpred}
check('Prediction finite/range',True,bool(np.isfinite(fp).all() and (fp>=0).all() and (fp<=1).all()));check('Probability sum max error',0.,float(abs(fp.sum(axis=1)-1).max()),1e-12)
for row,p in zip(future,fp):
 want=np.array([float(pred_index[row['match_key']][c]) for c in ['home','draw','away']]);check('Reload '+row['match_key']+' maximum error',0.,float(abs(want-p).max()),1e-12)
# Own metric definitions, including unscaled three-class Brier and top-label ECE.
def measures(rs,p):
 labels=np.array([r['label'] for r in rs]);onehot=np.eye(3)[labels];hit=(p.argmax(1)==labels);conf=p.max(1);ece=0
 for i in range(10):
  mask=(conf>=i/10)&(conf<(i+1)/10 if i<9 else conf<=1)
  if mask.any():ece+=mask.sum()/len(rs)*abs(hit[mask].mean()-conf[mask].mean())
 return {'n':len(rs),'accuracy':float(hit.mean()),'log_loss':float(-sum(math.log(max(float(p[i,y]),1e-15)) for i,y in enumerate(labels))/len(rs)),'brier_sum_of_three_classes':float(np.square(p-onehot).sum(1).mean()),'expected_calibration_error_10bins':float(ece)}
def own_baseline(tr,rs):
 freq={l:np.array([sum(r['label']==c and r['league']==l for r in tr)+1 for c in range(3)],dtype=float) for l in {r['league'] for r in tr}}
 return np.array([freq[r['league']]/sum(freq[r['league']]) for r in rs])
reg=stored['chosen_regularization'];check('Reg chosen solely from validation',min(stored['trials'],key=lambda t:t['validation']['log_loss'])['regularization'],reg)
performance={}
for name,tr,ts in [('untouched_test_2025_26',parts['2023/24']+parts['2024/25'],parts['2025/26']),('followup_2026_27',parts['2023/24']+parts['2024/25']+parts['2025/26'],parts['2026/27'])]:
 fitted=code.fit(tr,reg);pp=independent_probs(fitted,ts);bp=own_baseline(tr,ts);performance[name]={}
 tx=np.array([r['features'] for r in tr]);check(name+' train-only scaler mean max error',0.,float(abs(tx.mean(0)-np.array(fitted['mean'])).max()),1e-12)
 for kind,p in [('model',pp),('league_frequency_baseline',bp)]:
  vals=measures(ts,p);performance[name][kind]=vals
  for metric,value in vals.items():check(name+' '+kind+' '+metric,stored[name][kind][metric],value,1e-11)
 for league in {r['league'] for r in ts}:
  idx=[i for i,r in enumerate(ts) if r['league']==league];subset=[ts[i] for i in idx]
  for kind,p in [('model',pp),('league_frequency_baseline',bp)]:
   for metric,value in measures(subset,p[idx]).items():check(name+' '+league+' '+kind+' '+metric,stored[name]['by_league'][league][kind][metric],value,1e-11)
# Actual source perturbation: own result and same date result excluded, earlier result influences feature.
target=hist[500];changed=[dict(r) for r in completed]
for r in changed:
 if r['source_date']==target['date']:r['home_goals']='10.0';r['away_goals']='0.0';r['home_xg']='9.0'
perturbed,_=code.build_features(changed,scheduled,manifest['cutoff_date']);lookup={r['match_key']:r for r in perturbed};check('Actual same-date perturbation feature unchanged',target['features'],lookup[target['match_key']]['features'])
command=[sys.executable,'-B','-m','unittest','discover','-s',str(M/'tests'),'-v'];proc=subprocess.run(command,capture_output=True,text=True,encoding='utf-8');check('Existing tests return code',0,proc.returncode)
save('test-execution.json',{'command':command,'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr})
save('independent-checks.json',{'checker':'/root/validation','observed_at':datetime.now(timezone.utc).isoformat(),'checks':checks,'failures':failures,'performance':performance,'prediction_recomputed':fp.tolist(),'class_order':['home','draw','away'],'limitation':'Feature reconstruction and metric formulas independent; evaluation coefficient refit uses reviewed original fitter. Not an independent algorithm implementation.'})
print(json.dumps({'checks':len(checks),'failures':len(failures),'performance':performance},ensure_ascii=True))
