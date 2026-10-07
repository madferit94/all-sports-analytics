# v04 독립검토: 범위 내 내부준비 가능·한계 있음

생산자와 다른 reviewer `/root/f1_verifier`, 2026-10-07. v04 verification파일만 소유하고 production파일을 변경하지 않았습니다.

## 완료 범위 / 실제 대조값
1333개 독립검사 PASS: 역사예측214,position225,비교순수상태547,mount208,UI139.
16개 완료GP의훈련종료<대상시작·자기경기제외·10피처과거자료독립재계산·확률합1·22명고유순위·actual정답분리·로그손실및순위MAE직접재계산일치. 예정7개기존예측파일바이트동일.
position16GP8100행의manifest해시·session/driver연결·중복없음·기존실제결과및모든이전records불변. 비교0/25/50/75/100%에서미래position시간참조없음,최종공식결과,결측추론표시. mount재생·seek·끝·reset·숨김pause·해제,한영routing·예정/취소·최신모듈및4payload일치.

## 발견과 조치
원본22명인데position23 이상값4행(11234:1,11299:2,11307:1)발견,position-independent-v01 FAIL보존. 제작자comparison.js에이상샘플표시차단·invalid_position_sample·lap_inference별표대체추가. 원본23은보존. 독립격리position23입력fallback/flag/원본보존통과,position-v02는이상4행을알려진결측취급하고재검사PASS. 정상데이터라고재분류하지않았습니다.
모든GP순위샘플중시작전22행. 예정종료이후11299:72/11353:11/11731:443행. 예정종료시각과지연된실제경기종료가다를수있으므로원본시간범위는관찰값으로보존하고현재리플레이시각이후샘플배제를검증했습니다.

## 근거 파일
SPEC-v04-independent.ko.md 실행전기대값. check-historical-independent.py/check-position-independent.py/check-comparison-independent.cjs/check-comparison-mount-independent.cjs/check-ui-independent.cjs 실행. 각각JSON에기대값/실제값/판정. reviewer-summary-v04-v01.json은보고서와최종피검파일SHA256을기록합니다.

## 미확인과 필요한 판단
회고적순차학습모델이며당시미리공개한실시간예측이아닙니다. target참가자메타데이터는경기후수집되었고경기전공개시점미확인. 왼쪽차량은최종예상순위연출이며물리적랩페이스·추월예측아닙니다. 오른쪽진행은공식position샘플과랩시간보간이며GPS아님. 실제브라우저가로넘침및이미지·사용자확인은이reviewer가직접수행하지않았습니다. 상위root브라우저근거는추가보고받으면별도주체로연결합니다. 전체기존사이트·모델성능보장을통과판정하지않습니다. 참가자확인전.

후속: 설명기본접힘수정후comparison547/mount208/UI139재실행PASS,총1333유지·최종해시갱신. root작성browser-observations-2026-10-07-v01.json읽음:498x544에서44차선/22표행/Play64%차량이동/End100%종료/문서가로넘침없음/영문확인. 스크린샷browser-comparison-2026-10-07-v01.png은root출처. 이reviewer브라우저직접조작과구분하며새기본접힘화면최종브라우저는root후속중.
