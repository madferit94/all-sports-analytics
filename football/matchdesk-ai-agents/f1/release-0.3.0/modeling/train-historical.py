"""Retrospective, expanding-window forecasts; never import train.py's execution."""
from pathlib import Path
import ast,json,hashlib
ROOT=Path(__file__).resolve().parent
# Select declarations only. The original script's reading/fitting/output statements are not executed.
source=(ROOT/'train.py').read_text(encoding='utf8');tree=ast.parse(source)
declarations=[]
for node in tree.body:
    if isinstance(node,(ast.Import,ast.ImportFrom,ast.FunctionDef)):
        declarations.append(node)
    elif isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'ROOT','LABELS','FEATURES'} for t in node.targets):
        declarations.append(node)
namespace={'__file__':str(ROOT/'train.py')}
exec(compile(ast.Module(body=declarations,type_ignores=[]),'train-declarations','exec'),namespace)
load=namespace['load'];save=namespace['save'];instant=namespace['instant'];features=namespace['features'];append_race=namespace['append_race'];fit=namespace['fit'];probabilities=namespace['probabilities'];identity=namespace['identity'];np=namespace['np'];FEATURES=namespace['FEATURES']
season=load(ROOT.parent/'data/season-2026.json')
all_races=load(ROOT/'historical-2025.json')['races']+[r for r in season['races'] if r['state']=='completed']
all_races.sort(key=lambda r:r['session']['date_start'])
projection=[{'session':r['session'],'drivers':r['records']['drivers'],'session_result':r['records']['session_result']} for r in all_races]
input_fingerprint={'scope':'Ordered session metadata, driver metadata and race results only; target lap/position telemetry not read as features.',
 'sha256':hashlib.sha256(json.dumps(projection,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8')).hexdigest()}
history=[];examples=[];outputs={};evaluation=[];cutoff_tests=[]
for i,race in enumerate(all_races):
    s=race['session'];ds=race['records']['drivers'];results={v['driver_number']:v for v in race['records']['session_result']};n=len(ds);rows=[]
    for d in ds:
        f,a=features(d,s,history);target=results.get(d['driver_number']);position=target.get('position') if target else None
        assert a['latest_source_end'] is None or instant(a['latest_source_end'])<instant(s['date_start'])
        rows.append({'driver_number':d['driver_number'],'features':f,'audit':a,'win':int(position==1) if target else None,'rank_score':(float(position)-1)/(n-1) if position is not None else None})
    if s['year']==2026:
        eligible=[e for e in examples if not e['warmup'] and e['complete_winner_labels'] and instant(e['end'])<instant(s['date_start'])]
        assert eligible and all(e['session_key']!=s['session_key'] for e in eligible)
        clf,ranker=fit(eligible)
        x=np.array([[row['features'][k] for k in FEATURES] for row in rows]);p=probabilities(clf,x);expected=1+np.clip(ranker.predict(x),0,1)*(n-1)
        pred=[]
        for j,d in enumerate(ds):
            pred.append({'driver_number':d['driver_number'],'name':d['full_name'],'team':d['team_name'],'team_colour':d.get('team_colour'),
             'win_probability':float(p[j]),'expected_rank':float(expected[j]),'features':rows[j]['features'],'history':rows[j]['audit']})
        unique=sorted(pred,key=lambda d:(d['expected_rank'],-d['win_probability'],d['driver_number']))
        order=[d['driver_number'] for d in unique]
        ranks={num:place+1 for place,num in enumerate(order)}
        for d in pred:d['predicted_rank']=ranks[d['driver_number']]
        winner=next(j for j,d in enumerate(ds) if results.get(d['driver_number'],{}).get('position')==1)
        y=np.array([int(j==winner) for j in range(n)])
        baseline=np.array([row['features']['recent5_win_rate'] for row in rows]);baseline/=baseline.sum()
        metrics={}
        for name,q in [('model',p),('recent_win_baseline',baseline),('uniform',np.ones(n)/n)]:
            tied=np.isclose(q,q.max(),atol=1e-14,rtol=0)
            metrics[name]={'log_loss':float(-np.log(q[winner])),'multiclass_brier':float(np.sum((q-y)**2)),
             'top1_correct':float(1/tied.sum()) if tied[winner] else 0.}
        valid=[j for j,d in enumerate(ds) if results.get(d['driver_number'],{}).get('position') is not None]
        metrics['expected_rank_mae']=float(np.mean([abs(expected[j]-float(results[ds[j]['driver_number']]['position'])) for j in valid]))
        metrics['unique_order_rank_mae']=float(np.mean([abs(ranks[ds[j]['driver_number']]-float(results[ds[j]['driver_number']]['position'])) for j in valid]))
        metrics['actual_winner_driver_number']=ds[winner]['driver_number'];metrics['actual_winner_probability']=float(p[winner])
        actual=[{'driver_number':d['driver_number'],'name':d['full_name'],'team':d['team_name'],
         'position':results.get(d['driver_number'],{}).get('position'),'dnf':results.get(d['driver_number'],{}).get('dnf'),
         'dns':results.get(d['driver_number'],{}).get('dns'),'dsq':results.get(d['driver_number'],{}).get('dsq'),
         'number_of_laps':results.get(d['driver_number'],{}).get('number_of_laps'),'points':results.get(d['driver_number'],{}).get('points')} for d in ds]
        latest_end=max(e['end'] for e in eligible)
        cutoff_tests.append({'target_session_key':s['session_key'],'target_start':s['date_start'],'training_session_keys':[e['session_key'] for e in eligible],'training_latest_end':latest_end,
         'training_races':len(eligible),'training_cutoff_pass':instant(latest_end)<instant(s['date_start']),
         'source_feature_cutoff_pass':all(row['audit']['latest_source_end'] is None or instant(row['audit']['latest_source_end'])<instant(s['date_start']) for row in rows)})
        outputs[str(s['session_key'])]={'session_key':s['session_key'],'meeting_name':race['meeting']['meeting_name'],'circuit_key':s['circuit_key'],'circuit_name':s['circuit_short_name'],'target_start':s['date_start'],
         'prediction_type':'retrospective expanding-window refit using pre-race completed results only',
         'drivers':pred,'predicted_order':order,'actual':{'drivers':actual,'winner_driver_number':ds[winner]['driver_number']},'metrics':metrics,
         'training':cutoff_tests[-1],'prediction_animation':'Final predicted order only: symbolic animation, no predicted lap-by-lap model',
         'roster_assumption':'Target session drivers metadata acquired after race; retrospective entrant list, pre-race publication time unverified'}
        evaluation.append(metrics)
    examples.append({'session_key':s['session_key'],'start':s['date_start'],'end':s['date_end'],'year':s['year'],'rows':rows,'warmup':i<5,'complete_winner_labels':all(row['win'] is not None for row in rows)})
    # Append target results only after its predictions and evaluation have been created.
    append_race(race,history)
aggregate={name:{metric:float(np.mean([e[name][metric] for e in evaluation])) for metric in ['log_loss','multiclass_brier','top1_correct']} for name in ['model','recent_win_baseline','uniform']}
aggregate['expected_rank_mae']=float(np.mean([e['expected_rank_mae'] for e in evaluation]));aggregate['unique_order_rank_mae']=float(np.mean([e['unique_order_rank_mae'] for e in evaluation]))
save(ROOT/'historical-predictions.json',{'version':'0.3.0','model_id':'f1-walk-forward-history-2026-10-07-v01','input_fingerprint':input_fingerprint,'feature_labels':namespace['LABELS'],'races':outputs,'metrics':aggregate,
 'evaluation':'Retrospective walk-forward evaluation; not live predictions recorded before races or a fresh untouched prospective test.',
 'limitations':['Target entrant metadata collected after race; publication cutoff not independently verified','Final-order illustration is not a physical lap/pace forecast','No target laps/target results in prediction inputs; actual results stored separately after prediction','Small single-season sample; probabilities uncalibrated; rule changes and missing qualifying/weather apply']})
save(ROOT/'historical-feature-audit.json',{'input_fingerprint':input_fingerprint,'cutoff_tests':cutoff_tests,'examples':examples,'shared_declaration_source_sha256':hashlib.sha256(source.encode()).hexdigest()})
print(json.dumps({'completed_GP_predictions':len(outputs),'metrics':aggregate},indent=2))
