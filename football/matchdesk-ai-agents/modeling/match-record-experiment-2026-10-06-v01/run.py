"""Exploratory match-record features, using strict pre-date histories only."""
import argparse, collections, copy, hashlib, importlib.util, json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'prematch-v2-2026-10-06-v01'
spec = importlib.util.spec_from_file_location('v2', OLD/'train.py')
v2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v2)
base = v2.base
original_side = v2.side_features
FEATURES = [f'{side}_{name}' for side in ['home','away'] for name in
            [f'recent_{m}' for m in v2.METRICS]+[f'season_{m}' for m in v2.METRICS]+
            ['current_count','last5_count','previous_count','cold_start','league_gap_days','win5_ratio','draw5_ratio','loss5_ratio']]+['is_epl']

def expanded_side(history, league_history, league, team, season, day):
    recent_vector, evidence = original_side(history, league_history, league, team, season, day)
    records = history[(league,team)]
    current = [r for r in records if r['season']==season]
    prior_season = f'{int(season[:4])-1}/{str(int(season[:4]))[-2:]}'
    previous = [r for r in records if r['season']==prior_season]
    seasonal=[]
    for metric in v2.METRICS:
        league_mean=v2.average(league_history[league],metric,v2.NEUTRAL[metric])
        pv=[r[metric] for r in previous if r.get(metric) is not None]
        prior=(sum(pv)+8*league_mean)/(len(pv)+8)
        cv=[r[metric] for r in current if r.get(metric) is not None]
        seasonal.append((sum(cv)+8*prior)/(len(cv)+8))
    recent=current[-5:]
    # Missing recent WDL is a league-frequency prior, not fabricated results.
    league_rows=league_history[league]
    priors=[(sum(r['points']==p for r in league_rows)+1)/(len(league_rows)+3) for p in [3,1,0]]
    ratios=[(sum(r['points']==p for r in recent)+3*prior)/(len(recent)+3) for p,prior in zip([3,1,0],priors)]
    evidence['all_history_max_date']=max((r['date'] for r in records),default=None)
    evidence['league_history_max_date']=max((r['date'] for r in league_rows),default=None)
    assert all(r['date']<day for r in records+league_rows)
    return recent_vector[:11]+seasonal+recent_vector[11:]+ratios,evidence

def build(completed,stats):
    v2.side_features=expanded_side
    try:return v2.build_features(completed,[],stats,'2026-10-06')[0]
    finally:v2.side_features=original_side

def write(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:json.dump(value,f,ensure_ascii=False,indent=2)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--dataset',type=Path,required=True);args=parser.parse_args()
    if (HERE/'metrics.json').exists():raise SystemExit('Existing results preserved: use a new version folder.')
    files=[args.dataset/n for n in ['completed_matches.csv','team_match_stats.csv','team_season_additional_stats.csv']]+[OLD/n for n in ['train.py','model.json','evaluation-model.json','metrics.json']]
    hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    completed=base.load_csv(args.dataset/'completed_matches.csv');stats=base.load_csv(args.dataset/'team_match_stats.csv')
    oldrows=v2.build_features(completed,[],stats,'2026-10-06')[0]
    rows=build(completed,stats)
    checks=[]
    def check(name,condition,details):
        checks.append(dict(name=name,passed=bool(condition),details=details))
        if not condition:raise AssertionError(name)
    check('exact_match_alignment',[r['match_key'] for r in rows]==[r['match_key'] for r in oldrows],dict(matches=len(rows)))
    check('feature_schema',len(FEATURES)==61 and all(len(r['features'])==61 and np.isfinite(r['features']).all() for r in rows),dict(features=FEATURES))
    check('all_history_strictly_before',all(not value or value<r['date'] for r in rows for side in ['home','away'] for field,value in r['evidence'][side].items() if field.endswith('_max_date')),dict(policy='source-date strict; same-day excluded'))
    check('last5_strictly_before',all(len(r['evidence'][s]['recent_dates'])<=5 and all(d<r['date'] for d in r['evidence'][s]['recent_dates']) for r in rows for s in ['home','away']),dict(max_recent=5))
    # Rebuild after changing current/same-date and all later goals and match statistics.
    pivot='2025-08-16';changed_matches=copy.deepcopy(completed);changed_stats=copy.deepcopy(stats)
    changed_keys={r['match_key'] for r in completed if r['source_date']>=pivot}
    for r in changed_matches:
        if r['match_key'] in changed_keys:r['home_goals']='9';r['away_goals']='0'
    numeric=['points','goals_for','goals_against','xg_for','xg_against','npxg_for','npxg_against','deep','deep_allowed','ppda_att','ppda_def','ppda_allowed_att','ppda_allowed_def']
    for r in changed_stats:
        if r['match_key'] in changed_keys:
            for field in numeric:r[field]='9'
    mutant=build(changed_matches,changed_stats)
    prefix=[(r['match_key'],r['features']) for r in rows if r['date']<=pivot]
    check('current_and_future_mutation_invariance',prefix==[(r['match_key'],r['features']) for r in mutant if r['date']<=pivot],dict(pivot=pivot,compared_matches=len(prefix),changed_matches=len(changed_keys)))
    extra=copy.deepcopy(completed[0]);extra.update(match_key='leak-probe',source_date='2026-10-07')
    check('after_cutoff_record_invariance',build(completed+[extra],stats)==rows,dict(extra_date='2026-10-07'))
    train=[r for r in rows if r['season']=='2023/24'];val=[r for r in rows if r['season']=='2024/25']
    trials=[]
    for reg in [.001,.01,.1,1.]:
        model=base.fit(train,reg);trials.append(dict(regularization=reg,validation=base.metrics(val,base.predict(model,val))))
    reg=min(trials,key=lambda t:t['validation']['log_loss'])['regularization']
    model=base.fit(train+val,reg);model['features']=FEATURES
    model.update(model_id=HERE.name,model_accepted=False,status='EXPLORATORY_PARTIAL_FEATURES_NOT_ADOPTED')
    matrix=np.asarray([r['features'] for r in train+val]);scale=matrix.std(axis=0);scale[scale<1e-8]=1
    check('train_only_standardization',np.allclose(model['mean'],matrix.mean(axis=0)) and np.allclose(model['scale'],scale),dict(training_seasons=['2023/24','2024/25']))
    oldmodel=json.loads((OLD/'evaluation-model.json').read_text(encoding='utf-8'))
    oldmetrics=json.loads((OLD/'metrics.json').read_text(encoding='utf-8'))
    result=dict(exploratory=True,full_agreed_feature_set=False,dataset_refreshed=False,chosen_regularization=reg,trials=trials,evaluation={},feature_count=61)
    prediction_rows=[]
    for season,oldkey in [('2025/26','untouched_test_2025_26'),('2026/27','monitor_2026_27')]:
        subset=[r for r in rows if r['season']==season];oldsubset=[r for r in oldrows if r['season']==season]
        candidate=base.predict(model,subset);control=base.predict(oldmodel,oldsubset)
        check('probabilities_'+season,np.isfinite(candidate).all() and (candidate>=0).all() and (candidate<=1).all() and np.allclose(candidate.sum(axis=1),1),dict(n=len(subset)))
        control_metrics=base.metrics(oldsubset,control)
        check('reproduce_existing_'+season,all(abs(control_metrics[k]-oldmetrics[oldkey]['model'][k])<1e-10 for k in ['accuracy','log_loss','brier_sum_of_three_classes']),dict(n=len(subset),metrics=control_metrics))
        result['evaluation'][season]=dict(existing_33=control_metrics,candidate_61=base.metrics(subset,candidate),by_league={})
        for league in sorted({r['league'] for r in subset}):
            idx=[i for i,r in enumerate(subset) if r['league']==league];group=[subset[i] for i in idx]
            result['evaluation'][season]['by_league'][league]=dict(existing_33=base.metrics(group,control[idx]),candidate_61=base.metrics(group,candidate[idx]))
        for group_name,criterion in [('missing_previous',lambda r:any(r['evidence'][s]['previous_season_matches']==0 for s in ['home','away'])),('early_season',lambda r:any(r['evidence'][s]['current_matches']<5 for s in ['home','away']))]:
            idx=[i for i,r in enumerate(subset) if criterion(r)]
            result['evaluation'][season][group_name]=dict(existing_33=base.metrics([subset[i] for i in idx],control[idx]),candidate_61=base.metrics([subset[i] for i in idx],candidate[idx]))
        for r,p,c in zip(subset,candidate,control):prediction_rows.append({k:r[k] for k in ['match_key','date','season','league','home_team','away_team','label']}|dict(candidate=p.tolist(),existing=c.tolist()))
    snapshot_headers=base.load_csv(args.dataset/'team_season_additional_stats.csv')[0].keys()
    excluded=[x for x in snapshot_headers if x.startswith('statmuse_')]
    check('no_snapshot_columns_in_features',not any(x.startswith('statmuse_') for x in FEATURES),dict(excluded_columns=list(excluded),reason='No pre-match match-level historical availability'))
    check('original_files_preserved',all(hashlib.sha256(p.read_bytes()).hexdigest()==hashes[str(p)] for p in files),dict(file_count=len(files)))
    write('model.json',model);write('metrics.json',result);write('evaluation-predictions.json',prediction_rows);write('historical-features.json',rows)
    write('checks.json',dict(checks=checks,passed=len(checks),failed=0,subject='AI automated checks; no independent reviewer or participant confirmation'))
    write('input-manifest.json',dict(inputs=[dict(name=p.name,sha256=hashes[str(p)]) for p in files],excluded_season_snapshot_fields=list(excluded),same_day_policy='all-date-batch features before results',missing_feature_policy='exclude unavailable match-level stats, never fabricate',evaluation_status='Retrospective exploratory; previously inspected holdout periods',remaining=['source kickoff/correction history unverified','no prospective untouched outcome test','partial agreed metrics only'],numpy_version=np.__version__))
    print(json.dumps(dict(reg=reg,checks=len(checks),evaluation={s:{m:{k:v[k] for k in ['n','accuracy','log_loss','brier_sum_of_three_classes','expected_calibration_error_10bins']} for m,v in r.items() if m in ['existing_33','candidate_61']} for s,r in result['evaluation'].items()})))

if __name__=='__main__':main()
