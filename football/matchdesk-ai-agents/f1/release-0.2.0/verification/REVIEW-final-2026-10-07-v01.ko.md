# 독립 reviewer: 내부 검토 가능 / 실험 모델 한계 있음

2026-10-07, `/root/f1_verifier` 실행. 생산자와 별개입니다. 저장 verification-evidence와 MatchDesk reviewer skill/protocol 적용. 기능 수정은 하지 않았습니다. 최종 결재·공개 업로드는 상위 담당자 판단입니다.

## 완료 범위 / 실제 대조값
- 데이터 16검사 PASS: GP25=종료16/예정7/취소2, 실제완료 참가자·결과22행, 예정·취소 실제기록 없음, raw112SHA256일치, v02 원본시즌데이터바이트동일, 결측랩타임111유지. Bahrain GP 말레이시아 개최 공식 F1 race 페이지 독립조회. Sepang key12와 취소Sakhir63 분리,원본BRN표기보존.
- 모델 156검사 PASS: 피처10개를 저장역사자료에서 독립재계산하여 모든학습예제와예정7GP값 일치. 모든과거레이스종료<대상시작. train29/holdout6/serving35,훈련/검증겹침없음,마지막6GP검증,예정7개만22명/합계1/미확정명단안내.
- 모델 실제 확률오차: 로그손실 모델3.119464529091759 / 최근승비율기준2.9699472884626945 / 균등3.0910424533583156. 낮을수록 좋으므로 모델이 두 기준보다 열세입니다. Brier 모델0.8645732081859369 / 최근승0.9713220164609054 / 균등0.9545454545454547. 우승 top1 모델33.333% / 최근승11.667% / 균등4.545%,동률에균등정답점수를주는명시정책 적용. 검증6개뿐이며 정확도나확률보장불가.
- 리플레이 순수timeline101검사·mount가상DOM208검사 PASS: 종료16GP22명,최종원본순위,미출발·리타이어·종료정지,결측구간정지,seek범위/동일입력재현,play/reset/탭숨김pause/destroy프레임및이벤트해제. location16GP모두HTTP404: 실제GPS영상이아닌도식과랩시각보간재구성입니다.
- UI 독립가상DOM137검사 PASS: 최종HTML3payload원본동일·JS구문,전체25/필터,한영완료replay라우팅,예정22명표/10지표/미확정참가자안내,취소예측없음,축구언어별링크,Sepang표시,뒤로해제.

## 발견과 조치
최초독립모델검사v01은동률최대확률의첫선수를무조건선택하는검사기준때문에FAIL10개였습니다. 제작자가기록한동률균등점수정책과대조하여검사코드수정후같은입력v02가PASS했습니다. 실패v01을보존했습니다. 앱수정오류로기록하지않습니다.
사전제작메시지의9971결과누락을받아상위메시지에9971제외를전달했으나실제excluded=[]·drivers19/results19입니다. 이를즉시정정했습니다. 원본자료의당시출전자공개시점은별도검증되지않습니다.

## 근거 파일
실행전SPEC-independent-review-2026-10-07-v01.ko.md. check-data-independent.py/check-model-independent.py/check-replay-independent.cjs/check-replay-mount-independent.cjs/check-ui-independent.cjs 재실행가능. JSON기대값·실제값·판정은각*-independent*.json. 통합요약reviewer-summary-2026-10-07-v01.json은 검사총618개 및피검파일해시를기록합니다. 공식웹확인official-venue-source-2026-10-07-v01.json.

## 미확인과 필요한 판단
실제브라우저레이아웃·원격이미지·사용자확인은이reviewer가수행하지않았으며가상DOM과구분합니다. 예측순위MAE2.530은생산자측정값이며이reviewer가직렬화모델로독립재실행하지않았습니다. 전체자료진실성·미래모델성능·확률보정·역사출전자공개시각·독립재학습은인증하지않습니다. 모델확률오차열세를화면/README에명시한실험제공범위로만내부준비가능합니다. 참가자확인전.

후속: 최종한영실험모델·단순기준보다확률오차열세안내가추가된HTML로UI137검사PASS 재확인. 피검해시갱신.

추가발견: root 실브라우저에서 range step=1이소수점duration끝에못도달하여FINISH미표시. worker가step=any·입력clamp·최종상태listcache구분수정. 독립timeline101/mount208PASS 재실행(stepany16GP검사추가). 가상DOM은브라우저range의실제정규화동작을재현하지않으므로root End실브라우저후속확인필요. root브라우저관측은browser-observations-2026-10-07-v01.json이며이reviewer직접확인과구분.

최종후속: 재생성index로독립UI137PASS재실행,summary피검SHA갱신. root실브라우저관측보고:11234 End후value=max4885.787,81:25·종료,1 RUS L57 HARD완주. 이는root메시지에서전달받은AI브라우저관측이며reviewer직접조작이아닙니다. screenshot browser-replay-2026-10-07-v02.png보고됨,관측JSONv02는갱신시점아직미저장. 참가자확인전.
