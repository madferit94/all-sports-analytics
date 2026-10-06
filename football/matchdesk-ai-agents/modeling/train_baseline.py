"""Time-ordered, pre-match multinomial logistic baseline using NumPy only."""
import argparse,csv,hashlib,json,math
from collections import defaultdict,deque
from datetime import date,datetime,timezone
from pathlib import Path
import numpy as np

FEATURES=['home_points5','away_points5','home_xgf5','away_xgf5',
 'home_xga5','away_xga5','home_gf5','away_gf5','home_ga5','away_ga5',
 'home_history_count','away_history_count','home_league_gap_days','away_league_gap_days','is_epl']
CLASS_ORDER=['home','draw','away']

def load_csv(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def goals(value):
    number=float(value)
    if not math.isfinite(number) or number<0 or not number.is_integer():raise ValueError('Goals must be a nonnegative integer')
    return int(number)

def side_features(history,league,team,day):
    previous=list(history[(league,team)])[-5:]
    if not previous:return [1.3,1.3,1.3,1.3,1.3,0.,30.],[]
    count=len(previous)
    values=[sum(p[k] for p in previous)/count for k in ['points','xgf','xga','gf','ga']]
    gap=(date.fromisoformat(day)-date.fromisoformat(previous[-1]['date'])).days
    return values+[float(count),float(min(gap,60))],[p['key'] for p in previous]

def feature_row(r,history):
    league=r['league'];day=r['source_date']
    home,hkeys=side_features(history,league,r['home_team_key'],day)
    away,akeys=side_features(history,league,r['away_team_key'],day)
    vector=[v for pair in zip(home,away) for v in pair]+[float(league=='EPL')]
    return dict(match_key=r['match_key'],date=day,league=league,season=r['season'],
                home_team=r['home_team_name'],away_team=r['away_team_name'],features=vector,
                history_keys=dict(home=hkeys,away=akeys))

def add_result(r,history):
    gf=goals(r['home_goals']);ga=goals(r['away_goals']);xgf=float(r['home_xg']);xga=float(r['away_xg'])
    if min(gf,ga,xgf,xga)<0 or not all(math.isfinite(v) for v in [xgf,xga]):raise ValueError('Invalid result '+r['match_key'])
    for team,a,b,x,y in [(r['home_team_key'],gf,ga,xgf,xga),(r['away_team_key'],ga,gf,xga,xgf)]:
        history[(r['league'],team)].append(dict(key=r['match_key'],date=r['source_date'],gf=a,ga=b,xgf=x,xga=y,points=3 if a>b else 1 if a==b else 0))

def build_features(completed,scheduled,cutoff_date):
    history=defaultdict(lambda:deque(maxlen=5));days=defaultdict(list);seen=set()
    for row in completed:
        if row['match_key'] in seen:raise ValueError('Duplicate match '+row['match_key'])
        seen.add(row['match_key']);date.fromisoformat(row['source_date'])
        if row['source_date']>=cutoff_date:continue
        days[row['source_date']].append(row)
    output=[]
    for day in sorted(days):
        batch=sorted(days[day],key=lambda r:r['match_key'])
        # Compute every input first. Only then make the day's results available.
        for r in batch:
            item=feature_row(r,history);hg=goals(r['home_goals']);ag=goals(r['away_goals'])
            item['label']=0 if hg>ag else 1 if hg==ag else 2;output.append(item)
        for r in batch:add_result(r,history)
    future=[]
    for r in scheduled:
        if r['source_date']>=cutoff_date:future.append(feature_row(r,history))
    return output,future

def softmax(logits):
    z=logits-np.max(logits,axis=1,keepdims=True);exp=np.exp(z)
    return exp/exp.sum(axis=1,keepdims=True)

def fit(rows,regularization):
    x=np.asarray([r['features'] for r in rows]);y=np.asarray([r['label'] for r in rows])
    mean=x.mean(axis=0);scale=x.std(axis=0);scale[scale<1e-8]=1
    design=np.column_stack([np.ones(len(x)),(x-mean)/scale]);weights=np.zeros((design.shape[1],3))
    target=np.eye(3)[y]
    # Conservative fixed learning rate bounded by curvature; deterministic fitting.
    curvature=np.linalg.eigvalsh(design.T@design/len(x)).max()
    lr=0.8/(curvature+regularization)
    iterations=0
    for iterations in range(4000):
        gradient=design.T@(softmax(design@weights)-target)/len(x)
        gradient[1:]+=regularization*weights[1:]
        if np.max(np.abs(gradient))<1e-7:break
        weights-=lr*gradient
    return dict(type='multinomial_logistic_numpy',features=FEATURES,class_order=CLASS_ORDER,
                mean=mean.tolist(),scale=scale.tolist(),weights=weights.tolist(),regularization=regularization,iterations=iterations+1)

def predict(model,rows):
    x=np.asarray([r['features'] for r in rows],dtype=float)
    if not len(x):return np.empty((0,3))
    design=np.column_stack([np.ones(len(x)),(x-np.asarray(model['mean']))/np.asarray(model['scale'])])
    return softmax(design@np.asarray(model['weights']))

def metrics(rows,probs):
    if not rows:return None
    y=np.asarray([r['label'] for r in rows]);truth=np.eye(3)[y]
    confidence=probs.max(axis=1);hits=(probs.argmax(axis=1)==y)
    bins=[];ece=0.
    for i in range(10):
        mask=(confidence>=i/10)&(confidence<(i+1)/10 if i<9 else confidence<=1)
        if mask.any():
            accuracy=float(hits[mask].mean());conf=float(confidence[mask].mean());n=int(mask.sum())
            bins.append(dict(lower=i/10,n=n,accuracy=accuracy,mean_confidence=conf));ece+=n/len(y)*abs(accuracy-conf)
    return dict(n=len(y),accuracy=float(hits.mean()),log_loss=float(-np.log(np.clip(probs[np.arange(len(y)),y],1e-15,1)).mean()),
                brier_sum_of_three_classes=float(np.square(probs-truth).sum(axis=1).mean()),
                expected_calibration_error_10bins=ece,calibration_bins=bins)

def baseline(train,test):
    counts=defaultdict(lambda:np.ones(3))
    for row in train:counts[row['league']][row['label']]+=1
    return np.asarray([counts[row['league']]/counts[row['league']].sum() for row in test])

def evaluation(train,test,reg):
    model=fit(train,reg);probs=predict(model,test);base=baseline(train,test)
    result=dict(model=metrics(test,probs),league_frequency_baseline=metrics(test,base),by_league={})
    for league in sorted({r['league'] for r in test}):
        index=[i for i,r in enumerate(test) if r['league']==league];subset=[test[i] for i in index]
        result['by_league'][league]=dict(model=metrics(subset,probs[index]),league_frequency_baseline=metrics(subset,base[index]))
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--dataset',type=Path,required=True);parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--cutoff-date',required=True);args=parser.parse_args()
    date.fromisoformat(args.cutoff_date)
    completed=load_csv(args.dataset/'completed_matches.csv');scheduled=load_csv(args.dataset/'scheduled_matches.csv')
    rows,future=build_features(completed,scheduled,args.cutoff_date)
    train=[r for r in rows if r['season']=='2023/24'];validation=[r for r in rows if r['season']=='2024/25'];test=[r for r in rows if r['season']=='2025/26'];ongoing=[r for r in rows if r['season']=='2026/27']
    if min(len(train),len(validation),len(test))<500:raise ValueError('Full historical dataset required; demonstration subset is too small.')
    trials=[]
    for reg in [0.001,0.01,0.1]:
        m=fit(train,reg);score=metrics(validation,predict(m,validation));trials.append(dict(regularization=reg,validation=score))
    reg=min(trials,key=lambda t:t['validation']['log_loss'])['regularization']
    scores=dict(tuning_train_season='2023/24',tuning_validation_season='2024/25',trials=trials,chosen_regularization=reg,
                untouched_test_2025_26=evaluation(train+validation,test,reg),
                followup_2026_27=evaluation(train+validation+test,ongoing,reg),
                model_accepted=False,note='Exploratory evaluation, not independent model adoption; no hyperparameter selection on test/followup.')
    model=fit(rows,reg);model.update(training_matches=len(rows),training_last_date=max(r['date'] for r in rows),cutoff_date=args.cutoff_date,numpy_version=np.__version__)
    chosen=[r for r in future if r['match_key'] in {'understat:31230','understat:30845'}]
    probs=predict(model,chosen)
    if len(chosen)!=2:raise ValueError('Representative future fixtures missing.')
    if not np.all(np.isfinite(probs)) or not np.allclose(probs.sum(axis=1),1,atol=1e-10):raise ValueError('Invalid probabilities')
    args.out.mkdir(parents=True,exist_ok=False)
    def save(name,value):
        with (args.out/name).open('x',encoding='utf-8') as f:json.dump(value,f,ensure_ascii=False,indent=2)
    save('metrics.json',scores);save('model.json',model);save('historical_features.json',rows);save('future_inputs.json',chosen)
    save('input_manifest.json',dict(cutoff_date=args.cutoff_date,observed_at=datetime.now(timezone.utc).isoformat(),
        files=[dict(name=n,sha256=hashlib.sha256((args.dataset/n).read_bytes()).hexdigest()) for n in ['completed_matches.csv','scheduled_matches.csv']],
        completed_matches=len(rows),future_candidates=len(future),latest_completed_date=model['training_last_date'],dataset_refreshed=False,
        excluded_features=['StatMuse season snapshots','current squad','market value','availability news','future actual lineups','odds'],
        same_day_policy='All same-date results withheld until date batch inputs are computed.',
        fallback='No-history fixed neutral values=1.3, history_count=0, league_gap=30; real missing context is never filled as confirmed facts.',
        league_gap_notice='Calendar gap between recorded league matches, not actual rest days.',model_accepted=False,independent_review='PENDING'))
    with (args.out/'predictions.csv').open('x',encoding='utf-8',newline='') as f:
        writer=csv.writer(f);writer.writerow(['match_key','source_date','league','home_team','away_team','home','draw','away','status'])
        for r,p in zip(chosen,probs):writer.writerow([r['match_key'],r['date'],r['league'],r['home_team'],r['away_team'],*map(float,p),'EXPERIMENTAL_STORED_SNAPSHOT_NOT_ADOPTED'])
    print(json.dumps(dict(output=str(args.out),historical_matches=len(rows),reg=reg,test=scores['untouched_test_2025_26']['model'],baseline=scores['untouched_test_2025_26']['league_frequency_baseline'],future_predictions=len(chosen)),ensure_ascii=True))
if __name__=='__main__':main()
