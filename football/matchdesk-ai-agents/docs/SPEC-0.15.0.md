# MatchLab 0.15.0 / F1 0.3.0

사용자정정: 단순기록시뮬레이션을 예측레이스와실제진행비교로변경. 이전F1v03/축구0.14보존,새F1v04/축구v36.

- 종료16GP comparison기본탭: 예측순위연출판/실제랩진행판/공식중간순위/최종순위차이및DNF/DNS/DSQ.
- 각GP시작전끝난경기만train,first19→last34학습GP. 동일10과거지표,모델/스케일러각GP마다다시fit. 대상·이후결과학습제외. actualposition/laps순위연출예측입력사용금지.
- 입력공개시점한계: 당해GP명단은경기후수집,당시경기전공개시점미검증. 과거재현평가와당시예측발표구분.
- 예측차량은예상최종순위시각표현: 물리주행·랩별추월/피트예측아님. 실제차량도GPS가아닌유효랩기록보간,결측정지.
- OpenF1position16GP8100행:sourcehash·session/driver/time검사,latest sample time<=currenttime. 원본range이상값4행보존·표시제외. GP장시간지연경우예정session_end넘은기록보존.
- 결과25%top1/logloss2.7249/Brier0.9483/continuousrankMAE2.950/uniqueorderMAE3.713. 최근우승기준대비일부열세. 원래6GP홀드아웃대체아님.
- 예정7예측바이트보존/취소2불생성/한영종목전환/축구2399기록641예측보존.
- 실행주체: f1_model분석,f1_replay시각화,root통합,f1_verifier독립검증,f1_director최종제한명시내부결재. 참가자확인전/GitHub미전송.

## 검증 근거
- 독립1333PASS:historical214/position225/comparison547/mount208/UI139. 이상위치첫실패보고보존, 수정재검증별도.
- root실브라우저498×544:44차선/22표행/Play64%진행/End100%최종순위/한영/가로넘침없음/최종details기본접힘/errorlog없음.
- 제작자834모델검사·356시각화검사와독립검사를구분. 실제사용자확인전.
