"""Meaningful self-checks; independent review is a separate agent."""
import json
from pathlib import Path
import numpy as np
import experiment as exp

root=Path(__file__).resolve().parent
report=json.loads((root/'analyst-report.json').read_text(encoding='utf-8'))
tables=json.loads((root/'derived-raw-tables.json').read_text(encoding='utf-8'))
audit=json.loads((root/'availability-audit.json').read_text(encoding='utf-8'))
old=json.loads((exp.V2/'historical-features.json').read_text(encoding='utf-8'))
model=json.loads((root/'augmented-evaluation-model.json').read_text(encoding='utf-8'))
mapping={(r['league'],r['season']):r for r in tables}
augmented,_=exp.augment(old,mapping)
checks=[]
def check(name,condition):
    checks.append(dict(name=name,passed=bool(condition)))
    assert condition,name
check('all six tables are complete 380/20/38', len(tables)==6 and all(
    t['completed_matches']==380 and len(t['clubs'])==20 and all(c['matches']==38 for c in t['clubs']) for t in tables))
check('incomplete current season not treated as final',not any(t['season']=='2026/27' for t in tables))
check('no table data at or after target match',all(a['prior_table_date'] is None or a['prior_table_date']<r['date'] for a,r in zip(audit,old)))
check('all 2023 training prior ranks explicitly missing',all(a['home_missing'] and a['away_missing'] for a in audit if a['season']=='2023/24'))
check('initial constant extra coefficient zero',np.max(np.abs(report['initial_training_extra_feature_weights']))==0)
check('initial validation effect zero',report['initial_tuning_prediction_max_abs_delta']<1e-12)
check('original frozen v2 reproduced',report['original_model_replay_max_abs_delta']<1e-12)
check('fixed reg no new tuning',model['regularization']==.1 and report['new_hyperparameter_search'] is False)
for season in ['2025/26','2026/27']:
    selected=[r for r in augmented if r['season']==season]
    probs=exp.base.predict(model,selected)
    computed=exp.base.metrics(selected,probs)
    stored=report['scores'][season]['with_prior_raw_rank_proxy']['overall']
    check(season+' stored probabilities finite normalized',np.isfinite(probs).all() and np.allclose(probs.sum(axis=1),1))
    check(season+' actual metrics replay',all(abs(computed[k]-stored[k])<1e-12 for k in
        ['accuracy','log_loss','brier_sum_of_three_classes','expected_calibration_error_10bins']))
fake=old[0]|dict(date='2023-01-01',season='2024/25')
blocked=False
try:exp.augment([fake],mapping)
except ValueError:blocked=True
check('synthetic future table leakage rejected',blocked)
check('experimental provenance honest',report['model_accepted'] is False and
      report['evaluation_status']=='RETROSPECTIVE_REUSED_EVALUATION_NOT_NEW_UNTOUCHED_TEST' and
      all(t['standings_adjustments_applied'] is False and t['official_tiebreakers_applied'] is False for t in tables))
result=dict(producer_id='/root/rank_ablation',independent=False,passed=len(checks),failed=0,checks=checks)
with (root/'check-result.json').open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps(result))
