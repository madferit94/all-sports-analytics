"""Exploratory prior-season RAW table proxy ablation, not official standings.

Same rows / model family / original regularization as prematch-v2. No tuning
on the reused evaluation season. Existing production files are never changed.
"""
import argparse, collections, hashlib, importlib.util, json
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
V2 = ROOT / 'prematch-v2-2026-10-06-v01'
spec = importlib.util.spec_from_file_location('prematch_v2', V2/'train.py')
v2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v2)
base = v2.base
EXTRA = ['home_previous_raw_rank', 'away_previous_raw_rank',
         'home_previous_table_missing', 'away_previous_table_missing']

def build_tables(matches):
    groups = collections.defaultdict(list)
    for r in matches: groups[(r['league'], r['season'])].append(r)
    tables = {}
    for (league, season), group in sorted(groups.items()):
        if len(group) != 380: continue  # Incomplete seasons never become final tables.
        clubs = collections.defaultdict(lambda: dict(matches=0, points=0, gf=0, ga=0))
        names = {}
        seen = set()
        for r in group:
            if r['match_key'] in seen: raise ValueError('duplicate match')
            seen.add(r['match_key'])
            hg, ag = base.goals(r['home_goals']), base.goals(r['away_goals'])
            for side, gf, ga in [('home', hg, ag), ('away', ag, hg)]:
                team=r[f'{side}_team_key']; names[team]=r[f'{side}_team_name']; c=clubs[team]
                c['matches']+=1; c['gf']+=gf; c['ga']+=ga; c['points']+=3 if gf>ga else 1 if gf==ga else 0
        if len(clubs)!=20 or any(c['matches']!=38 for c in clubs.values()):
            raise ValueError('A 380-match season is not complete round robin')
        ordered=sorted(clubs,key=lambda k:(-clubs[k]['points'],-(clubs[k]['gf']-clubs[k]['ga']),-clubs[k]['gf'],k))
        table=[]
        for position, team in enumerate(ordered,1):
            c=clubs[team]
            tied=[k for k in ordered if (clubs[k]['points'],clubs[k]['gf']-clubs[k]['ga'],clubs[k]['gf']) == (c['points'],c['gf']-c['ga'],c['gf'])]
            table.append(dict(team_key=team,team_name=names[team],raw_proxy_position=position,
                **c,gd=c['gf']-c['ga'],unresolved_exact_tie=len(tied)>1))
        tables[(league,season)]=dict(league=league,season=season,latest_match_date=max(r['source_date'] for r in group),
            completed_matches=len(group),table_type='RAW_POINTS_GD_GF_PROXY_NOT_OFFICIAL',
            standings_adjustments_applied=False,official_tiebreakers_applied=False,clubs=table)
    return tables

def augment(rows,tables):
    out=[]; checks=[]
    for r in rows:
        year=int(r['season'][:4]); previous=f'{year-1}/{str(year)[-2:]}'
        table=tables.get((r['league'],previous))
        if table and table['latest_match_date']>=r['date']:
            raise ValueError('Prior table not available before match date')
        ranks={c['team_key']:c['raw_proxy_position'] for c in table['clubs']} if table else {}
        ranksides=[]; missing=[]
        for side in ['home','away']:
            rank=ranks.get(r[f'{side}_team_key'])
            ranksides.append((rank-1)/19 if rank is not None else .5)
            missing.append(float(rank is None))
        extra=ranksides+missing
        out.append(r|dict(features=r['features']+extra))
        checks.append(dict(match_key=r['match_key'],season=r['season'],league=r['league'],previous_season=previous,
            prior_table_date=table['latest_match_date'] if table else None,home_missing=bool(missing[0]),away_missing=bool(missing[1])))
    return out,checks

def evaluate(model,rows):
    p=base.predict(model,rows)
    return dict(overall=base.metrics(rows,p),by_league={league:base.metrics(
        [r for r in rows if r['league']==league],p[[i for i,r in enumerate(rows) if r['league']==league]])
        for league in sorted({r['league'] for r in rows})})

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--dataset',type=Path,required=True); args=parser.parse_args()
    old=json.loads((V2/'historical-features.json').read_text(encoding='utf-8'))
    old_metrics=json.loads((V2/'metrics.json').read_text(encoding='utf-8'))
    tables=build_tables(base.load_csv(args.dataset/'completed_matches.csv'))
    new,audit=augment(old,tables)
    train_old=[r for r in old if r['season']=='2023/24']; train_new=[r for r in new if r['season']=='2023/24']
    val_old=[r for r in old if r['season']=='2024/25']; val_new=[r for r in new if r['season']=='2024/25']
    reg=old_metrics['chosen_regularization']
    # Demonstrate the initial tuning training season cannot learn these variables.
    m0=base.fit(train_old,reg); m1=base.fit(train_new,reg)
    tuning_max_delta=float(np.max(np.abs(base.predict(m0,val_old)-base.predict(m1,val_new))))
    extra_weights=np.asarray(m1['weights'])[-4:]
    assert np.ptp(np.asarray([r['features'][-4:] for r in train_new]),axis=0).max()==0
    assert np.max(np.abs(extra_weights))==0 and tuning_max_delta<1e-12
    # Original final training rows allow a cautious retrospective ablation.
    fit_old=train_old+val_old; fit_new=train_new+val_new
    baseline=base.fit(fit_old,reg); augmented=base.fit(fit_new,reg)
    baseline['features']=v2.FEATURES; augmented['features']=v2.FEATURES+EXTRA
    saved=json.loads((V2/'evaluation-model.json').read_text(encoding='utf-8'))
    replay_delta=float(np.max(np.abs(base.predict(saved,old)-base.predict(baseline,old))))
    assert replay_delta<1e-12
    scores={}
    for season in ['2025/26','2026/27']:
        a=[r for r in old if r['season']==season]; b=[r for r in new if r['season']==season]
        original=evaluate(baseline,a); added=evaluate(augmented,b)
        scores[season]=dict(original=original,with_prior_raw_rank_proxy=added,
            delta_added_minus_original={k:added['overall'][k]-original['overall'][k]
                for k in ['accuracy','log_loss','brier_sum_of_three_classes','expected_calibration_error_10bins']})
    availability={}
    for season in sorted({r['season'] for r in audit}):
        group=[r for r in audit if r['season']==season]
        availability[season]=dict(matches=len(group),home_missing=sum(r['home_missing'] for r in group),
            away_missing=sum(r['away_missing'] for r in group),both_known=sum(not r['home_missing'] and not r['away_missing'] for r in group))
    report=dict(agent_id='analyst',producer_id='/root/rank_ablation',run_id=OUT.name,
        match_key='ALL_HISTORICAL_MATCHES',status='EXPLORATORY_NOT_ADOPTED',model_accepted=False,
        original_model_preserved=True,website_unchanged=True,transfermarkt_inputs='NOT_COLLECTED_NOT_USED',
        prior_feature_status='DERIVED_RAW_TABLE_PROXY_NOT_OFFICIAL_LEAGUE_POSITION',
        evaluation_status='RETROSPECTIVE_REUSED_EVALUATION_NOT_NEW_UNTOUCHED_TEST',
        fixed_original_regularization=reg,new_hyperparameter_search=False,
        initial_training_season='2023/24',final_training_seasons=['2023/24','2024/25'],
        extra_features=EXTRA,missing_rank_default=.5,missing_flag_explicit=True,promotion_status='UNKNOWN_NOT_INFERRED',
        availability=availability,initial_training_extra_feature_weights=extra_weights.tolist(),
        initial_tuning_prediction_max_abs_delta=tuning_max_delta,original_model_replay_max_abs_delta=replay_delta,
        scores=scores,limitations=[
            '2022/23 standings unavailable; added columns are constant in initial tuning training.',
            'Raw standings omit disciplinary points deductions and official league tiebreakers.',
            'Missing prior top-division history does not confirm promotion; no lower division rank fabricated.',
            'Reused 2025/26 and 2026/27 after feature hypothesis; not fresh held-out evidence.',
            'Single reused season and partial monitoring season cannot establish reliable future improvement.',
            'Higher confidence values do not imply greater accuracy or calibrated probabilities.'],
        input_hashes=[dict(name=f,sha256=hashlib.sha256(path.read_bytes()).hexdigest()) for f,path in [
            ('completed_matches.csv',args.dataset/'completed_matches.csv'),
            ('historical-features.json',V2/'historical-features.json'),('evaluation-model.json',V2/'evaluation-model.json')]])
    for name,value in [('derived-raw-tables.json',list(tables.values())),('analyst-report.json',report),
                       ('augmented-evaluation-model.json',augmented),('availability-audit.json',audit)]:
        with (OUT/name).open('x',encoding='utf-8') as f: json.dump(value,f,ensure_ascii=False,indent=2)
    print(json.dumps(dict(availability=availability,initial_tuning_max_delta=tuning_max_delta,scores=scores),ensure_ascii=False))

if __name__=='__main__': main()
