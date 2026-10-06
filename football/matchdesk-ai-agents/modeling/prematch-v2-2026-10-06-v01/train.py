"""Stored-record prematch model; no current season totals or live API inputs."""
import argparse, collections, hashlib, importlib.util, json, math
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('baseline', ROOT/'train_baseline.py')
base = importlib.util.module_from_spec(spec); spec.loader.exec_module(base)
METRICS = ['points','gf','ga','xgf','xga','npxgf','npxga','deep','deep_allowed','ppda','ppda_allowed']
NEUTRAL = dict(zip(METRICS,[1.35,1.4,1.4,1.4,1.4,1.25,1.25,7,7,12,12]))
FEATURES = [f'{side}_{metric}' for side in ['home','away'] for metric in METRICS+['current_count','last5_count','previous_count','cold_start','league_gap_days']]+['is_epl']
CLASS_ORDER = ['home','draw','away']

def average(rows, metric, default):
    values = [r[metric] for r in rows if r.get(metric) is not None]
    return sum(values)/len(values) if values else default

def side_features(history, league_history, league, team, season, day):
    records = history[(league,team)]
    current = [r for r in records if r['season']==season]
    previous_season = f'{int(season[:4])-1}/{str(int(season[:4]))[-2:]}'
    previous = [r for r in records if r['season']==previous_season]
    recent = current[-5:]
    league_records = league_history[league]
    values = []
    missing=[]
    for metric in METRICS:
        league_mean = average(league_records,metric,NEUTRAL[metric])
        previous_values = [r[metric] for r in previous if r.get(metric) is not None]
        prior = (sum(previous_values)+8*league_mean)/(len(previous_values)+8)
        current_values = [r[metric] for r in current if r.get(metric) is not None]
        season_mean = (sum(current_values)+8*prior)/(len(current_values)+8)
        recent_values = [r[metric] for r in recent if r.get(metric) is not None]
        smoothed_recent = (sum(recent_values)+3*season_mean)/(len(recent_values)+3)
        values.append(smoothed_recent)
        if len(recent_values)<len(recent): missing.append(metric)
    gap=min(120,(base.date.fromisoformat(day)-base.date.fromisoformat(records[-1]['date'])).days) if records else 120
    values += [float(min(len(current),38)),float(len(recent)),float(min(len(previous),38)),float(not previous and len(current)<5),float(gap)]
    evidence=dict(current_matches=len(current),previous_season_matches=len(previous),recent_keys=[r['key'] for r in recent],
        recent_dates=[r['date'] for r in recent],prior_status='previous_season_shrunk_to_league' if previous else 'league_prior_no_previous_season',
        promotion_status='UNKNOWN_NOT_INFERRED_FROM_MISSING_HISTORY',missing_recent_metrics=missing)
    return values,evidence

def build_features(completed, scheduled, team_stats, cutoff_date):
    stats={(r['match_key'],r['team_key']):r for r in team_stats}
    if len(stats)!=len(team_stats): raise ValueError('Duplicate team match stats')
    history=collections.defaultdict(list); league_history=collections.defaultdict(list); days=collections.defaultdict(list)
    seen=set()
    for r in completed:
        if r['match_key'] in seen: raise ValueError('Duplicate match key')
        seen.add(r['match_key'])
        if r['source_date']<cutoff_date: days[r['source_date']].append(r)
    def make(r):
        h,he=side_features(history,league_history,r['league'],r['home_team_key'],r['season'],r['source_date'])
        a,ae=side_features(history,league_history,r['league'],r['away_team_key'],r['season'],r['source_date'])
        return dict(match_key=r['match_key'],date=r['source_date'],league=r['league'],season=r['season'],
            home_team=r['home_team_name'],away_team=r['away_team_name'],home_team_key=r['home_team_key'],away_team_key=r['away_team_key'],
            features=h+a+[float(r['league']=='EPL')],evidence=dict(home=he,away=ae))
    def add(r,team,is_home):
        s=stats[(r['match_key'],team)]
        fields=['points','goals_for','goals_against','xg_for','xg_against','npxg_for','npxg_against','deep','deep_allowed']
        values={m:float(s[f]) if s[f] else None for m,f in zip(METRICS,fields)}
        for m,num,den in [('ppda','ppda_att','ppda_def'),('ppda_allowed','ppda_allowed_att','ppda_allowed_def')]:
            values[m]=float(s[num])/float(s[den]) if s[num] and s[den] and float(s[den])>0 else None
        if any(v is not None and (not math.isfinite(v) or v<0) for v in values.values()): raise ValueError('Invalid statistic')
        values.update(key=r['match_key'],date=r['source_date'],season=r['season'])
        history[(r['league'],team)].append(values);league_history[r['league']].append(values)
    rows=[]
    for day in sorted(days):
        batch=sorted(days[day],key=lambda r:r['match_key'])
        for r in batch:
            item=make(r);hg=base.goals(r['home_goals']);ag=base.goals(r['away_goals'])
            item['label']=0 if hg>ag else 1 if hg==ag else 2; rows.append(item)
        for r in batch:
            add(r,r['home_team_key'],True);add(r,r['away_team_key'],False)
    # All future records use the same observed snapshot: no invented results update history.
    future=[make(r) for r in scheduled if r['source_date']>=cutoff_date]
    return rows,future

def fit(rows,reg):
    model=base.fit(rows,reg);model['features']=FEATURES
    return model

def evaluate(model,train,rows):
    p=base.predict(model,rows); baseline=base.baseline(train,rows)
    return dict(model=base.metrics(rows,p),league_frequency_baseline=base.metrics(rows,baseline),
        by_league={league:dict(model=base.metrics([r for r in rows if r['league']==league],p[[i for i,r in enumerate(rows) if r['league']==league]]),
            league_frequency_baseline=base.metrics([r for r in rows if r['league']==league],baseline[[i for i,r in enumerate(rows) if r['league']==league]])) for league in sorted({r['league'] for r in rows})})

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--dataset',type=Path,required=True);parser.add_argument('--cutoff-date',default='2026-10-06');args=parser.parse_args()
    out=Path(__file__).parent
    rows,future=build_features(base.load_csv(args.dataset/'completed_matches.csv'),base.load_csv(args.dataset/'scheduled_matches.csv'),base.load_csv(args.dataset/'team_match_stats.csv'),args.cutoff_date)
    train=[r for r in rows if r['season']=='2023/24'];val=[r for r in rows if r['season']=='2024/25'];test=[r for r in rows if r['season']=='2025/26'];monitor=[r for r in rows if r['season']=='2026/27']
    trials=[]
    for reg in [.001,.01,.1,1.]:
        model=fit(train,reg); trials.append(dict(regularization=reg,validation=base.metrics(val,base.predict(model,val))))
    reg=min(trials,key=lambda t:t['validation']['log_loss'])['regularization']
    frozen=fit(train+val,reg)
    scores=dict(training_season='2023/24',tuning_season='2024/25',trials=trials,chosen_regularization=reg,
        frozen_training=['2023/24','2024/25'],untouched_test_2025_26=evaluate(frozen,train+val,test),monitor_2026_27=evaluate(frozen,train+val,monitor),
        model_accepted=False,adoption='PENDING_INDEPENDENT_REVIEW',statmuse_pass_features='EXCLUDED_NO_PREMATCH_HISTORICAL_AVAILABILITY')
    model=fit(rows,reg);model.update(model_id='prematch-v2-2026-10-06-v01',cutoff_date=args.cutoff_date,training_matches=len(rows),training_last_date=max(r['date'] for r in rows),model_accepted=False,probability_status='EXPERIMENTAL_NOT_ADOPTED')
    probabilities=base.predict(model,future)
    assert len(future)==641 and np.allclose(probabilities.sum(axis=1),1) and np.isfinite(probabilities).all()
    predictions=[]
    for r,p in zip(future,probabilities):
        predictions.append({k:v for k,v in r.items() if k!='features'}|dict(probabilities=dict(zip(CLASS_ORDER,map(float,p))),model_id=model['model_id'],cutoff_date=args.cutoff_date,training_last_date=model['training_last_date'],status='EXPERIMENTAL_NOT_ADOPTED',source_date_is_verified_kickoff=False))
    manifest=dict(producer_id='/root/prediction_v2',agent_id='analyst',run_id=model['model_id'],completed_matches=len(rows),future_matches=len(future),dataset_refreshed=False,
        inputs=[dict(name=n,sha256=hashlib.sha256((args.dataset/n).read_bytes()).hexdigest()) for n in ['completed_matches.csv','scheduled_matches.csv','team_match_stats.csv']],
        feature_groups=dict(attack=['gf','xgf','npxgf','deep'],defense=['ga','xga','npxga','deep_allowed'],pressing_pass_proxy=['ppda','ppda_allowed'],form=['points','last5_count']),
        excludes=['StatMuse current/season-final passing totals','lineups','market value','odds','injuries','uncollected actual passing accuracy'],
        prior_policy='8 league pseudo-games for previous season; 8 previous-prior pseudo-games for current season; last5 shrunk with 3 season-mean pseudo-games',
        initial_league_prior=NEUTRAL,same_day_policy='Strict dates: all same-day features computed before any same-day results added',
        cold_start='No previous-season data is unknown-history proxy, not confirmed promotion; league prior never fabricates lower division records',
        future_policy='All scheduled fixtures use one stored cutoff snapshot; later fixtures become stale without refresh')
    for name,value in [('model.json',model),('evaluation-model.json',frozen),('metrics.json',scores),('input-manifest.json',manifest),('future-predictions.json',dict(class_order=CLASS_ORDER,model_id=model['model_id'],cutoff_date=args.cutoff_date,model_accepted=False,predictions=predictions)),('historical-features.json',rows)]:
        with (out/name).open('x',encoding='utf-8') as f:json.dump(value,f,ensure_ascii=False,separators=(',',':'))
    print(json.dumps(dict(rows=len(rows),future=len(future),reg=reg,test=scores['untouched_test_2025_26'],monitor=scores['monitor_2026_27']),ensure_ascii=False))
if __name__=='__main__':main()
