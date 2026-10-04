"""저장 원본·분석·PPT 독립 대조. 실시간 제공자 검증은 포함하지 않습니다."""
from pathlib import Path
from collections import Counter,defaultdict
import json,csv,math,hashlib,zipfile,xml.etree.ElementTree as ET
import pandas as pd,numpy as np
import io,posixpath,re,os
start=Path(__file__).resolve().parent
ROOT=next(p for p in [start,*start.parents] if (p/'raw_manifest.json').exists() and (p/'analysis').is_dir())
AN=ROOT/'analysis';PPT=ROOT/'presentation/Beyond_Goals_EN_Landscape_verified.pptx'
REPO=ROOT
RAW=Path(os.environ.get('UNDERSTAT_RAW_CACHE',str(ROOT)))
if not (RAW/'data/raw/leagues/EPL_2025.json').exists():
 raise FileNotFoundError('Full raw-cache verification requires the original snapshot. Set UNDERSTAT_RAW_CACHE to its project directory. For CSV-only checks, run verify_saved_data.py from the project root.')
OUT=ROOT/'verification';OUT.mkdir(exist_ok=True)
latest=json.loads((AN/'latest_results.json').read_text());result=AN/latest['en']
checks=[];issues=[]
def check(name,condition,evidence):
 checks.append({'check':name,'status':'pass' if condition else 'fail','evidence':evidence})
 if not condition:issues.append({'severity':'high','issue':name,'evidence':evidence})
def loadcsv(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def same(a,b):
 if b is None:return a==''
 if str(a)==str(b):return True
 try:return math.isclose(float(a),float(b),rel_tol=1e-12,abs_tol=1e-10)
 except (ValueError,TypeError):return False
# 1. 파일 출처와 디코딩 원본 해시 검증.
manifest=json.loads((AN/'data/input_manifest.json').read_text())
for f in manifest['files']:
 check('input_hash:'+f['file'],hashlib.sha256((AN/'data/input'/f['file']).read_bytes()).hexdigest()==f['sha256'],f['sha256'])
raw_manifest=json.loads((REPO/'raw_manifest.json').read_text());bad=[]
for f in raw_manifest:
 p=RAW/f['path'];m=json.loads(p.with_suffix('.meta.json').read_text())
 if hashlib.sha256(p.read_bytes()).hexdigest()!=f['sha256'] or m['sha256_decoded_json']!=f['sha256']:bad.append(f['path'])
check('raw_hashes_and_retrieval_metadata',not bad,{'files':len(raw_manifest),'mismatches':bad})
# 2. 원본 리그·경기·출전·슈팅 기록 재구성.
players=loadcsv(REPO/'data/processed/all_players_league_season.csv');fixtures=loadcsv(REPO/'data/processed/league_matches.csv')
appearances=loadcsv(AN/'data/input/player_match_records.csv');shots=loadcsv(AN/'data/input/shot_events.csv')
fixture_map={r['match_id']:r for r in fixtures};raw_players={};raw_fixtures={}
for league in ['EPL','La_liga','Bundesliga','Serie_A','Ligue_1']:
 d=json.loads((RAW/f'data/raw/leagues/{league}_2025.json').read_text())
 for r in d['players']:raw_players[(league,r['id'])]=r
 for r in d['dates']:raw_fixtures[r['id']]=(league,r)
badplayers=[]
for r in players:
 original=raw_players.get((r['league'],r['id']))
 if original is None or any(not same(r[k],v) for k,v in original.items()):badplayers.append((r['league'],r['id']))
check('league_summary_raw_reconciliation',not badplayers and len(raw_players)==len(players),{'rows':len(players),'mismatch_keys':badplayers})
badfixtures=[]
for r in fixtures:
 l,o=raw_fixtures[r['match_id']]
 if l!=r['league'] or not o['isResult'] or o['datetime']!=r['date'] or not same(o['goals']['h'],r['home_goals']) or not same(o['goals']['a'],r['away_goals']):badfixtures.append(r['match_id'])
check('fixture_raw_reconciliation',not badfixtures and len(fixtures)==len(raw_fixtures),{'fixtures':len(fixtures),'mismatches':badfixtures})
raw_ap={};raw_sh={};duplicates=[]
for p in sorted((RAW/'data/raw/players').glob('*.json')):
 if p.name.endswith('.meta.json'):continue
 d=json.loads(p.read_text());pid=str(d['player']['id'])
 for m in sorted(d['matches'],key=lambda r:int(r['roster_id'])):
  if m['id'] not in fixture_map:continue
  k=(pid,m['id'])
  if k in raw_ap:
   first=raw_ap[k]
   check('duplicate_payload:'+':'.join(k),{a:b for a,b in m.items() if a!='roster_id'}=={a:b for a,b in first.items() if a!='roster_id'},m['roster_id'])
   duplicates.append(k)
  else:raw_ap[k]=m
 for s in d['shots']:
  if s['match_id'] in fixture_map:raw_sh[s['id']]=s
badap=[]
for r in appearances:
 o=raw_ap.get((r['player_id'],r['id']))
 if o is None or any(not same(r.get(k),v) for k,v in o.items()):badap.append((r['player_id'],r['id']))
check('appearance_raw_reconstruction',not badap and len(appearances)==len(raw_ap),{'canonical_rows':len(raw_ap),'duplicates_retained_in_evidence':len(duplicates),'mismatches':badap})
badshots=[]
for r in shots:
 o=raw_sh.get(r['id'])
 if o is None or any(not same(r.get(k),v) for k,v in o.items()):badshots.append(r['id'])
check('shot_raw_reconstruction',not badshots and len(shots)==len(raw_sh),{'events':len(shots),'mismatch_ids':badshots})
# 3. 데이터 품질과 이벤트 기반 선수 지표 독립 계산.
profiles=pd.read_csv(AN/'data/input/striker_scatter_ready.csv');ap=pd.DataFrame(appearances);ev=pd.DataFrame(shots)
K=['league','season','player_id']
for frame in [profiles]:frame['season']=frame.season.astype(str);frame['player_id']=frame.player_id.astype(str)
check('profile_keys_and_completeness',not profiles.duplicated(K).any() and profiles[K+['minutes','non_penalty_shots','npshots_per90','npxg_per_shot']].notna().all().all(),{'players':len(profiles)})
check('event_and_appearance_unique_keys',not ev.duplicated('id').any() and not ap.duplicated(K+['id']).any(),{'events':len(ev),'appearances':len(ap)})
orphans=[(r['player_id'],r['match_id']) for r in shots if (r['player_id'],r['match_id']) not in raw_ap]
check('all_event_appearance_links',not orphans,{'orphan_events':len(orphans)})
check('event_ranges',ev[['X','Y','xG']].astype(float).ge(0).all().all() and ev[['X','Y','xG']].astype(float).le(1).all().all(), 'X,Y,xG in [0,1]')
check('penalty_own_goal_flags',((ev.is_penalty=='True')==(ev.situation=='Penalty')).all() and ((ev.counts_as_attempt=='False')==(ev.result=='OwnGoal')).all(),{'own_goal_events':int(ev.result.eq('OwnGoal').sum())})
np_ev=ev[ev.situation.ne('Penalty')&ev.result.ne('OwnGoal')].copy();np_ev['xG']=np_ev.xG.astype(float)
totals=np_ev.groupby(K).agg(event_shots=('id','size'),event_xg=('xG','sum'),event_goals=('result',lambda x:x.eq('Goal').sum())).reset_index()
ap['time']=ap.time.astype(int);ap_tot=ap.groupby(K).agg(event_minutes=('time','sum'),event_appearances=('id','size')).reset_index()
computed=profiles.merge(totals,on=K,validate='one_to_one').merge(ap_tot,on=K,validate='one_to_one')
computed['computed_volume']=computed.event_shots/computed.event_minutes*90
computed['computed_quality']=computed.event_xg/computed.event_shots
computed['computed_production']=computed.event_xg/computed.event_minutes*90
check('all_cohort_metrics_from_events',len(computed)==len(profiles) and np.allclose(computed.non_penalty_shots,computed.event_shots) and np.allclose(computed.non_penalty_goals,computed.event_goals) and np.allclose(computed.shot_sum_npxg,computed.event_xg) and np.allclose(computed.minutes,computed.event_minutes) and np.allclose(computed.npshots_per90,computed.computed_volume) and np.allclose(computed.npxg_per_shot,computed.computed_quality) and np.allclose(computed.npxg_per90,computed.computed_production),{'cohort_rows':len(computed),'cohort_minutes':int(computed.minutes.sum()),'cohort_np_shots':int(computed.event_shots.sum())})
# Position-based cohort from canonical appearances, then compare selected keys.
audit=pd.read_csv(AN/'data/input/forward_candidate_audit.csv',dtype={'player_id':str,'season':str});badrole=[]
for _,r in audit.iterrows():
 m=ap[(ap.league==r.league)&(ap.player_id==r.player_id)];total=m.time.sum();known=m.loc[m.position!='Sub','time'].sum();fw=m.loc[m.position=='FW','time'].sum()
 if int(r.known_position_minutes)!=known or int(r.cf_assigned_minutes)!=fw:badrole.append(r.player_id)
check('duplicate_affected_candidate_exclusion',audit.loc[audit.source_duplicate_appearance_rows.gt(0),'qc_pass'].eq(False).all() and not profiles.player_id.isin(audit.loc[audit.source_duplicate_appearance_rows.gt(0),'player_id']).any(),{'affected_candidate_rows':int(audit.source_duplicate_appearance_rows.gt(0).sum())})
check('recorded_position_minutes',not badrole,{'candidate_rows':len(audit),'mismatches':badrole})
expected_role=np.where(audit.known_position_minutes/audit.minutes.replace(0,np.nan)>=.5,np.where(audit.cf_assigned_minutes/audit.known_position_minutes.replace(0,np.nan)>=.5,'central_forward_candidate','other_forward_or_mixed_role'),'insufficient_known_position')
check('position_classification_rule',(audit.role_classification==expected_role).all(),'Known position minutes ≥50% of total; FW minutes ≥50% of known position minutes')
selected=audit[(audit.role_classification=='central_forward_candidate')&audit.minutes.ge(900)&audit.non_penalty_shots.gt(0)&audit.qc_pass.eq(True)]
check('cohort_filter_reproduction',set(map(tuple,selected[K].values))==set(map(tuple,profiles[K].values)),{'selected_rows':len(selected),'excluded_failed_qc':int(audit.qc_pass.ne(True).sum())})
# 4. 영한 결과·순위·대표 선정·무슈팅 처리 대조.
output=pd.read_csv(result/'player_profiles.csv',dtype={'player_id':str,'season':str});median_v=output.npshots_per90.median();median_q=output.npxg_per_shot.median()
groups=np.select([output.npshots_per90.ge(median_v)&output.npxg_per_shot.ge(median_q),output.npshots_per90.ge(median_v)&output.npxg_per_shot.lt(median_q),output.npshots_per90.lt(median_v)&output.npxg_per_shot.ge(median_q)],['high_volume_high_quality','high_volume_low_quality','low_volume_high_quality'],default='low_volume_low_quality')
check('four_quadrant_classification',(output.profile_group==groups).all(),{'volume_median':median_v,'quality_median':median_q})
qv=float(np.quantile(output.npshots_per90,.75));qq=float(np.quantile(output.npxg_per_shot,.75))
strong=output[output.non_penalty_shots.ge(50)&output.npshots_per90.ge(qv)&output.npxg_per_shot.ge(qq)]
actual_strong=pd.read_csv(result/'both_measures_standouts.csv',dtype={'player_id':str})
check('global_upper_quartile_standouts',set(zip(strong.league,strong.player_id))==set(zip(actual_strong.league,actual_strong.player_id)) and np.allclose(actual_strong.volume_q75,qv) and np.allclose(actual_strong.quality_q75,qq),{'players':strong.player_name.tolist(),'volume_q75':qv,'quality_q75':qq})
check('output_metric_formula',np.allclose(output.goals_minus_npxg,output.non_penalty_goals-output.shot_sum_npxg) and np.allclose(output.conversion_pct,output.non_penalty_goals/output.non_penalty_shots*100),'NP goals - event xG; conversion NP goals/shots')
for f in ['player_profiles.csv','league_summary.csv','representative_players.csv','match_consistency.csv','player_match_analysis.csv','shot_volume_ranking.csv','chance_quality_ranking.csv','goals_above_xg_ranking.csv','league_metric_representatives.csv','both_measures_standouts.csv']:
 check('bilingual_parity:'+f,(AN/latest['en']/f).read_bytes()==(AN/latest['ko']/f).read_bytes(),'Exact CSV byte comparison')
reps=pd.read_csv(result/'representative_players.csv');expected=[];scale=output[['npshots_per90','npxg_per_shot']].std()
for g,x in output.groupby('profile_group'):
 eligible=x[x.non_penalty_shots>=50].copy();center=x[['npshots_per90','npxg_per_shot']].median();eligible['distance']=((eligible[['npshots_per90','npxg_per_shot']]-center)/scale).pow(2).sum(axis=1)
 chosen=eligible.sort_values(['distance','player_id','league']).iloc[0];expected.append((chosen.league,chosen.player_name))
check('four_case_selection',set(expected)==set(zip(reps.league,reps.player_name)),expected)
league_reps=pd.read_csv(result/'league_metric_representatives.csv',dtype={'player_id':str,'season':str});pool=output[output.non_penalty_shots>=50]
expected_league=pool.sort_values(['league','npxg_per90','minutes','player_id'],ascending=[True,False,False,True]).groupby('league').head(1)
check('league_representative_selection',set(zip(league_reps.league,league_reps.player_id))==set(zip(expected_league.league,expected_league.player_id)),league_reps[['league','player_name','npxg_per90']].to_dict('records'))
for filename,metric,frame in [('shot_volume_ranking','npshots_per90',output),('chance_quality_ranking','npxg_per_shot',pool),('goals_above_xg_ranking','goals_minus_npxg',pool)]:
 x=pd.read_csv(result/(filename+'.csv'),dtype={'player_id':str});values=list(x[metric]);valid=x[metric].is_monotonic_decreasing and all(int(r.metric_rank)==1+sum(v>r[metric] for v in values) for _,r in x.iterrows()) and set(zip(x.league,x.player_id))==set(zip(frame.league,frame.player_id));check('metric_rank:'+filename,valid,{'rows':len(x)})
match=pd.read_csv(result/'player_match_analysis.csv',dtype={'player_id':str,'season':str,'match_id':str});cons=pd.read_csv(result/'match_consistency.csv',dtype={'player_id':str,'season':str})
by_match=np_ev.groupby(K+['match_id']).agg(raw_np_shots=('id','size'),raw_np_xg=('xG','sum')).reset_index();j=match.merge(by_match,on=K+['match_id'],how='left',validate='one_to_one').fillna({'raw_np_shots':0,'raw_np_xg':0})
check('zero_shot_appearance_reconstruction',np.allclose(j.np_shots,j.raw_np_shots) and np.allclose(j.np_xg,j.raw_np_xg),'All appearances retained; absent NP event totals become 0')
long=j[j.time>=60].groupby(K).agg(n=('match_id','size'),zero=('raw_np_shots',lambda x:x.eq(0).sum())).reset_index();j2=cons.merge(long,on=K,validate='one_to_one')
check('60plus_zero_shot_rates',np.allclose(j2.matches_60plus,j2.n) and np.allclose(j2.no_np_shot_60plus,j2.zero) and np.allclose(j2.no_np_shot_60plus_pct,j2.zero/j2.n*100),'Condition is ≥60 minutes played per appearance, not a rolling 60-minute window')
# 5. PPT 차트 순서에 따라 차트 값과 포함 워크북 대조.
NS={'c':'http://schemas.openxmlformats.org/drawingml/2006/chart','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
def series(t):return t.findall('.//c:ser',NS)
def vals(s,axis):
 p=s.find('c:'+axis,NS)
 return [] if p is None else [float(v.text) for v in p.findall('.//c:numCache/c:pt/c:v',NS)+p.findall('.//c:numLit/c:pt/c:v',NS)]
def compare_chart(number,expected_series):
 actual=series(charts[number]);valid=len(actual)==len(expected_series);details=[]
 for i,(x,y) in enumerate(expected_series):
  if i>=len(actual):valid=False;continue
  s=actual[i];av=vals(s,'yVal') or vals(s,'val');ax=vals(s,'xVal')
  ok=len(av)==len(y) and np.allclose(av,y,rtol=1e-10,atol=1e-11)
  if x is not None:ok=ok and len(ax)==len(x) and np.allclose(ax,x,rtol=1e-10,atol=1e-11)
  valid=valid and ok;details.append({'series':i,'points':len(av),'match':bool(ok)})
 check('ppt_chart_'+str(number),valid,details)
with zipfile.ZipFile(PPT) as z:
 charts={int(n.split('chart')[-1].split('.')[0]):ET.fromstring(z.read(n)) for n in z.namelist() if '/charts/chart' in n and n.endswith('.xml')}
 slide_text={i:' '.join(ET.fromstring(z.read(f'ppt/slides/slide{i}.xml')).itertext()) for i in range(1,14)}
 # Expected ordering mirrors the analytic row order, independently of deck_data.json.
 leagues=['EPL','La_liga','Bundesliga','Serie_A','Ligue_1'];ss=[(output.loc[output.league==l,'npshots_per90'].tolist(),output.loc[output.league==l,'npxg_per_shot'].tolist()) for l in leagues]
 compare_chart(1,ss);compare_chart(3,ss);compare_chart(2,[(None,[int((output.league==l).sum()) for l in leagues])])
 compare_chart(4,[(output.npshots_per90.tolist(),output.npxg_per_shot.tolist())]+[([r.npshots_per90],[r.npxg_per_shot]) for _,r in league_reps.iterrows()])
 rp=reps.merge(output[K+['player_name']],on=['league','player_name'],validate='one_to_one')
 compare_chart(5,[([r.npshots_per90],[r.npxg_per_shot]) for _,r in rp.iterrows()]+[([median_v,median_v],[.06,.27]),([1,3.6],[median_q,median_q])])
 ss=[(output.loc[output.league==l,'expected_conversion_pct'].div(100).tolist(),output.loc[output.league==l,'conversion_pct'].div(100).tolist()) for l in leagues]
 compare_chart(6,ss+[([0,.33],[0,.33])])
 compare_chart(7,[(None,[round(output.loc[output.league==l,'npshots_per90'].median(),2) for l in leagues])])
 compare_chart(8,[(None,[round(output.loc[output.league==l,'npxg_per_shot'].median(),3) for l in leagues])])
 allp=pd.DataFrame(players);allp['goals']=allp.goals.astype(int);allp=allp.rename(columns={'id':'player_id'});leaders=allp[allp.goals==allp.groupby('league').goals.transform('max')]
 leaders=leaders[['league','player_id','goals']].merge(output,on=['league','player_id'],suffixes=('_src',''),validate='one_to_one').set_index('league').loc[leagues].reset_index()
 check('five_scoring_leaders',len(leaders)==5 and (leaders.goals_src==leaders.goals).all(),leaders[['player_name','league','goals']].to_dict('records'))
 compare_chart(9,[(None,leaders.non_penalty_goals.tolist()),(None,(leaders.goals-leaders.non_penalty_goals).tolist())])
 compare_chart(10,[([r.npshots_per90],[r.npxg_per_shot]) for _,r in leaders.iterrows()])
 for i,(_,r) in enumerate(rp.iterrows()):
  sh=np_ev[(np_ev.league==r.league)&(np_ev.player_id==r.player_id)]
  compare_chart(11+i,[(sh.loc[sh.result.ne('Goal'),'X'].astype(float).tolist(),sh.loc[sh.result.ne('Goal'),'Y'].astype(float).tolist()),(sh.loc[sh.result.eq('Goal'),'X'].astype(float).tolist(),sh.loc[sh.result.eq('Goal'),'Y'].astype(float).tolist())])
 composition=[]
 for part in ['Head','LeftFoot','RightFoot','OtherBodyPart']:
  values=[]
  for _,r in rp.iterrows():
   sh=np_ev[(np_ev.league==r.league)&(np_ev.player_id==r.player_id)];values.append(sh.shotType.eq(part).sum()/len(sh))
  composition.append((None,values))
 compare_chart(15,composition)
 matches=[]
 for i,(_,r) in enumerate(rp.iterrows()):
  m=match[(match.league==r.league)&(match.player_id==r.player_id)]
  matches.append(([i+1+(q%7-3)*.028 for q in range(len(m))],m.np_xg.tolist()))
 compare_chart(16,matches)
 check('removed_footer_and_author',all('SAVED 03 OCT' not in t and 'Minseob Eom' not in t for t in slide_text.values()),'13 slides visible text')
 check('case_selection_explanation','quadrant' in slide_text[5] and 'nearest' in slide_text[5] and 'illustrative' in slide_text[5],slide_text[5])
 # Native embedded workbook numeric values must agree with their cached chart coordinates.
 workbook_points=0;workbook_errors=[]
 for number,t in charts.items():
  part=f'ppt/slides/charts/chart{number}.xml';rels=ET.fromstring(z.read(f'ppt/slides/charts/_rels/chart{number}.xml.rels'))
  ex=t.find('.//c:externalData',NS);rid=ex.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
  target=next(r.get('Target') for r in rels if r.get('Id')==rid);target=posixpath.normpath(posixpath.join(posixpath.dirname(part),target))
  with zipfile.ZipFile(io.BytesIO(z.read(target))) as wb:
   sheet=ET.fromstring(wb.read('xl/worksheets/sheet1.xml'));WN={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
   cells={c.get('r'):c.find('s:v',WN).text for c in sheet.findall('.//s:c',WN) if c.find('s:v',WN) is not None}
   for nr in t.findall('.//c:numRef',NS):
    formula=nr.find('c:f',NS).text;bounds=re.findall(r'\$?([A-Z]+)\$?(\d+)',formula.split('!')[-1]);cache=nr.findall('c:numCache/c:pt',NS)
    if len(bounds)!=2:workbook_errors.append((number,formula));continue
    col,start=bounds[0];lastcol,end=bounds[1]
    for point in cache:
     idx=int(point.get('idx'));cell=col+str(int(start)+idx);v=point.find('c:v',NS).text;workbook_points+=1
     if col!=lastcol or int(start)+idx>int(end) or not same(cells.get(cell),v):workbook_errors.append((number,formula,cell))
 check('embedded_workbook_numeric_values',not workbook_errors,{'numeric_cache_values':workbook_points,'workbooks':len(charts),'errors':workbook_errors})
 check('visible_league_representative_values',all(r.player_name in slide_text[4] and f'{r.npshots_per90:.2f} shots/90' in slide_text[4] and f'{r.npxg_per_shot:.3f} xG/shot' in slide_text[4] and f'{r.npxg_per90:.3f} xG/90' in slide_text[4] for _,r in league_reps.iterrows()),'Five names and fifteen rounded metrics checked')
 check('leader_superlative_claims',leaders.loc[leaders.npshots_per90.idxmax(),'league']=='La_liga' and leaders.loc[leaders.npxg_per_shot.idxmax(),'league']=='EPL','Highest volume Mbappe; highest quality Haaland, among five leaders')
 check('league_median_claim',output.groupby('league').npxg_per_shot.median().idxmax()=='EPL','Premier League cohort highest median xG/shot')

penalty_labels=series(charts[9])[1].findall('c:dLbls/c:dLbl',NS)
check('penalty_native_labels_disabled',len(penalty_labels)==5 and all(x.find('c:showVal',NS) is not None and x.find('c:showVal',NS).get('val')=='0' for x in penalty_labels),'Five native labels hidden; four explicit positive labels retained; zero omitted')
check('ppt_native_chart_and_slide_counts',len(charts)==16 and len(slide_text)==13,{'charts':len(charts),'slides':len(slide_text)})
# Visible claims recomputed from original numerators. Rounding tolerance applies only to display.
check('visible_key_findings',round(leaders.loc[leaders.league=='La_liga','npshots_per90'].iloc[0],2)==4.70 and round(leaders.loc[leaders.league=='EPL','npxg_per_shot'].iloc[0],3)==.213 and round(leaders.loc[leaders.league=='Ligue_1','goals_minus_npxg'].iloc[0],2)==5.31 and round(composition[0][1][3]*100,1)==41.7, 'Mbappe 4.70; Haaland .213; Lepaul +5.31; Pellegrino headers 41.7%')
# Visual QA findings recorded separately after rendering.
summary={'status':'pass' if not issues else 'needs_review','checks':checks,'issues':issues,'scope':'Saved snapshot internal consistency and source-file reconstruction, not live provider or xG model calibration.',
 'counts':{'raw_files':len(raw_manifest),'fixtures':len(fixtures),'league_player_rows':len(players),'detail_players':len(list((RAW/'data/raw/players').glob('[0-9]*.json')))-len(list((RAW/'data/raw/players').glob('[0-9]*.meta.json'))),'appearances':len(appearances),'shot_events':len(shots),'cohort_players':len(profiles),'cohort_appearances':len(match),'cohort_np_shots':int(computed.event_shots.sum()),'source_duplicate_rows':len(duplicates),'season_scope':sorted(ev.season.unique().tolist()),'appearance_date_range':[min(ap.date),max(ap.date)],'null_assisted_player_events':sum(r.get('player_assisted') is None for r in raw_sh.values())},
 'latest_results':latest,'ppt_sha256':hashlib.sha256(PPT.read_bytes()).hexdigest()}
(OUT/'pipeline_validation.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,default=lambda x:x.item() if hasattr(x,'item') else str(x)))
print(json.dumps({'status':summary['status'],'checks':len(checks),'failed_checks':[x['check'] for x in checks if x['status']=='fail'],'counts':summary['counts']},ensure_ascii=False))
