"""Recalculate reported metrics without using the training metric function."""
import json, math
from pathlib import Path
HERE=Path(__file__).resolve().parent
scores=json.loads((HERE/'metrics.json').read_text(encoding='utf-8'))
rows=json.loads((HERE/'evaluation-predictions.json').read_text(encoding='utf-8'))
features=json.loads((HERE/'historical-features.json').read_text(encoding='utf-8'))
model=json.loads((HERE/'model.json').read_text(encoding='utf-8'))
assert len(features)==2399 and len(rows)==879 and len(model['features'])==61
assert scores['chosen_regularization']==min(scores['trials'],key=lambda t:t['validation']['log_loss'])['regularization']
verified=[]
for season in ['2025/26','2026/27']:
    subset=[r for r in rows if r['season']==season]
    for field,label in [('existing','existing_33'),('candidate','candidate_61')]:
        accuracy=sum(max(range(3),key=lambda i:r[field][i])==r['label'] for r in subset)/len(subset)
        loss=-sum(math.log(r[field][r['label']]) for r in subset)/len(subset)
        brier=sum(sum((p-int(i==r['label']))**2 for i,p in enumerate(r[field])) for r in subset)/len(subset)
        for k,v in [('accuracy',accuracy),('log_loss',loss),('brier_sum_of_three_classes',brier)]:assert abs(scores['evaluation'][season][label][k]-v)<1e-12
        verified.append(dict(season=season,model=label,n=len(subset),accuracy=accuracy,log_loss=loss,brier=brier))
lines=['# 경기 기록 모델 실험 결과 · v01','',
       '확보된 경기 기록을 시즌 평균·최근5경기 평균으로 분리한 모델입니다. 확정 목록 전체를 반영한 모델은 아닙니다. 웹 모델 변경·배포 없음. 기존 파일 보존. 참가자 확인 전.','',
       '|구간|경기 수|기존 정답률|새 정답률|기존 확률 오차|새 확률 오차|','|---|---:|---:|---:|---:|---:|']
for season,result in scores['evaluation'].items():
    for group,pair in [('전체',result),*list(result['by_league'].items()),('이전 시즌 기록 없음',result['missing_previous']),('시즌 초반',result['early_season'])]:
        old,new=pair['existing_33'],pair['candidate_61']
        if not old:continue
        lines.append(f"|{season} {group}|{old['n']}|{old['accuracy']:.2%}|{new['accuracy']:.2%}|{old['log_loss']:.6f}|{new['log_loss']:.6f}|")
lines += ['', '확률 오차(log loss)는 작을수록 좋습니다. 전체 Brier 오차 및 확률 보정 오차도 metrics.json에 기록했습니다.', '',
          '## 실제 입력과 제외','',
          '- 홈/원정 각각: 경기당 승점·득점·실점·xG·상대xG·페널티 제외xG·상대페널티 제외xG·DEEP·DEEP허용·PPDA·상대PPDA의 보정된 최근5경기값11개와 보정된 현재시즌값11개.',
          '- 각각 현재/최근/이전 시즌 경기 수·이전 기록 부족 여부·리그 경기 간격5개, 보정한 최근 승무패 비율3개. 홈/원정 각30개+리그1개=61개.',
          '- 시즌 누적 StatMuse47종은 사용하지 않았습니다. 경기별 슈팅·유효슈팅·차단·클리어링·태클·경합은 아직 미확보이며 포함하지 않았습니다.', '',
          '## 누수 방지와 실제 검증','',
          '- 경기 당일을 포함한 이후 결과·지표를 변조해도 해당 날짜까지 입력이 그대로임을 확인했습니다.',
          '- cutoff 뒤의 미래 종료 경기 추가에도 모든 기존 입력이 그대로였습니다. 시즌/리그 평균도 엄격히 이전 날짜 기록만 사용합니다.',
          '- 평균·표준편차는 학습행만 사용. 설정 선택은2024/25검증구간만 사용. 같은날 모든 입력 생성 후 결과를 넣습니다.',
          '- run.py 자동검사13개 통과. 별도 verify_results.py에서 저장한879개 예측의 정답률·log loss·Brier 재계산과 일치.',
          '- 새로운 입력과 정규화 설정이 함께 변경됐습니다. 새 모델 정규화 강도는1.0, 기존은0.1입니다. 개선을 한 지표의 효과로 단정할 수 없습니다.', '',
          '## 판단과 남은 한계','',
          '- 탐색 결과에서 전체 확률 오차는 개선됐으나 정식 채택하지 않았습니다. 리그별·자료 부족 구간 결과를 함께 봐야 합니다.',
          '- 2025/26·2026/27은 이미 이전 실험에서 관찰한 자료입니다. 신규 미사용 평가나 앞으로의 실제 성능 보장이 아닙니다.',
          '- 출처 날짜 기준 검사를 통과한 것이며, 실제 킥오프 시간대·연기/재개·과거 원문 수정 이력 검증까지 완료한 것은 아닙니다.',
          '- 자료 마지막 경기2026-09-20. 경기별 추가 지표 확보와 향후 결과를 보기 전에 고정한 예측 평가가 필요합니다.',
          '- 코드/모델/검사만 새 버전에 저장했으며 웹 확률·8비트 움직임은 변경하지 않았습니다.', '',
          '재현: 새 버전 폴더에서 run.py --dataset <원본폴더> 실행. 생성결과가 있는 폴더의 재실행은 중단됩니다. 결과 재확인: python verify_results.py.']
for name,value in [('verification-recalculated.json',dict(status='PASS',recalculated=verified,subject='AI local recalculation, not an independent agent review')),('RESULTS.ko.md','\n'.join(lines)+'\n')]:
    with (HERE/name).open('x',encoding='utf-8') as f:
        if isinstance(value,str):f.write(value)
        else:json.dump(value,f,ensure_ascii=False,indent=2)
print('PASS: 879 predictions recalculated; temporal configuration checked; results written.')
