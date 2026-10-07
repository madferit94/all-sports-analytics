"""Preserve v01 report and repair the missing La_liga aggregation in v02."""
import json, math
from pathlib import Path
HERE=Path(__file__).resolve().parent
rows=json.loads((HERE/'evaluation-predictions.json').read_text(encoding='utf-8'))
metrics=json.loads((HERE/'metrics.json').read_text(encoding='utf-8'))
def measure(rs,field):
    return dict(n=len(rs),accuracy=sum(max(range(3),key=lambda i:r[field][i])==r['label'] for r in rs)/len(rs),log_loss=-sum(math.log(r[field][r['label']]) for r in rs)/len(rs),brier_sum_of_three_classes=sum(sum((p-int(i==r['label']))**2 for i,p in enumerate(r[field])) for r in rs)/len(rs))
table=[]
for season,result in metrics['evaluation'].items():
    rs=[r for r in rows if r['season']==season];result['by_league']={}
    for league in sorted({r['league'] for r in rs}):
        group=[r for r in rs if r['league']==league]
        pair=dict(existing_33=measure(group,'existing'),candidate_61=measure(group,'candidate'))
        result['by_league'][league]=pair
        a,b=pair['existing_33'],pair['candidate_61']
        table.append(f"|{season} {league}|{a['n']}|{a['accuracy']:.2%}|{b['accuracy']:.2%}|{a['log_loss']:.6f}|{b['log_loss']:.6f}|")
    assert sum(p['candidate_61']['n'] for p in result['by_league'].values())==len(rs)
    for field in ['existing_33','candidate_61']:
        for key in ['accuracy','log_loss','brier_sum_of_three_classes']:
            weighted=sum(p[field][key]*p[field]['n'] for p in result['by_league'].values())/len(rs)
            assert abs(weighted-result[field][key])<1e-12
original=(HERE/'RESULTS.ko.md').read_text(encoding='utf-8')
text=original+'\n## v02 리그별 집계 정정\n\n초기 보고서가 LaLiga와 실제 데이터 La_liga 표기를 다르게 처리하여 라리가 행을 누락했습니다. 전체 평가·모델·예측값은 변경하지 않았습니다. 원 v01 결과를 보존하고 리그별 집계만 보완했습니다. 새 metrics-v02.json이 리그별 평가 기준입니다.\n\n|구간|경기 수|기존 정답률|새 정답률|기존 확률 오차|새 확률 오차|\n|---|---:|---:|---:|---:|---:|\n'+'\n'.join(table)+'\n\n두 리그 표본 합계와 가중 지표가 전체 평가와 일치함을 검증했습니다.\n'
for name,value in [('metrics-v02.json',metrics),('RESULTS.ko.v02.md',text)]:
    with (HERE/name).open('x',encoding='utf-8') as f:
        if isinstance(value,str):f.write(value)
        else:json.dump(value,f,ensure_ascii=False,indent=2)
print('\n'.join(table));print('PASS league counts and weighted metrics; original report preserved.')
