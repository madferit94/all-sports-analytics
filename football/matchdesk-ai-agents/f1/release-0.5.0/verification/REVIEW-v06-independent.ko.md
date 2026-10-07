# v06 드라이버 진행 지표·전체 차량 표시: 범위 내 내부준비 가능

검사주체 `/root/f1_verifier`, 생산자별도. 2026-10-07. 저장 reviewer skill/protocol·verification-evidence 적용. production수정없고v06 verification만작성.

## 완료 범위 / 실제 대조값
총6902개 독립검사PASS: 원본보존4 / 시간별history6344 / mount400 / UI154.
- v05와경기·지도·완료16회고예측·미래7예측바이트동일. 새로운수집/재학습성공으로주장하지않습니다.
- 종료16GP22드라이버3시점(0/50/100%)1056snapshot:과거position개수·완료lap개수·pit진입개수·lap완료시각·pit완료시각·마지막완료랩실제원본대조.
- 격리입력: position정확cursor포함/미래+1ms제외, lap.end==cursor포함/미완료·결측lap제외, pitdate<=cursor진입/레이스전·미래pit제외, 진입1초에총28초소요값미표시·진행중,진입+28초경계후총시간표시,미확보pit_count null. 피트레인총시간을정차stop_duration으로바꿔표시하지않음.
- 기본전체22차량/모든차량alpha1(희미화없음),일시정지selected1대,재생시자동all22복귀·선택드라이버정보유지,드라이버변경시카드이름갱신. 재생·seek끝·reset·숨김pause·destroy/viewchange이벤트해제대조.
- 예정7GP의기록진행은없다고표시하고예측값만제공. 한영카드/전체25라우팅·5payload원본동일·최신JSembedded·예정중복표숨김·취소예측금지·축구언어링크검사.

## 발견과 조치
상위가피트진입일1초후총28초값이먼저표시될수있는후행값누출위험을지적했습니다. 생산자는pit.completed=date+lane_duration<=cursor를분리하고진입중에는값대신진행중을표시했습니다. 독립순수함수와실제UI렌더가상DOM경계시험둘다통과. SPEC에사전기대값추가기록.
검사초기v06미복제source-manifest를서비스필수보존대상으로가정해파일경로실행오류. 실제서비스4파일보존으로좁혀재실행PASS했고원본수집근거는v05에서보존되는자료로구분했습니다. 앱기능실패로기록하지않습니다.

## 근거 파일
SPEC-v06-independent.ko.md. check-preservation-independent.py/check-history-independent.cjs/check-dashboard-mount-independent.cjs/check-ui-independent.cjs 재실행가능. JSON에기대값/실제값/판정/주체, reviewer-summary-v06-v01.json에검사6902개및피검파일SHA256을기록합니다.

## 미확인과 필요한 판단
가상DOM/canvas계측은실제브라우저레이아웃검사가아닙니다. 최종원본결과표는정적비교정답이며진행순위·완료랩차트와별도로취급했습니다. GPS2명/나머지20명재구성·2025참조지도·순위연출예측기존한계는유지됩니다. 미래실제텔레메트리없는것을새로확보한것처럼표시하지않습니다. 사용자확인전. root실브라우저관측은별도주체근거를받으면연결합니다. 기존모델전체성능재인증범위아닙니다.

최종후속: coverage.pit.status=HTTP_404빈배열격리입력에서pit_count=null검사추가PASS. 직후source SVG축숫자21px대비index14/15px불일치UIv01 FAIL1개보존. 최신축숫자확대포함assemble후같은조건UIv02 154PASS,summary모든피검SHA갱신. 최종6902PASS입니다.
root browser-observations-v01.json실제읽고별도주체SHA연결:기본all22,선택Max·single후Playall전환·선택유지,중간순위6/29랩MEDIUM/pit1/완료L28 83.44s,End6/57랩HARD/pit2/L57 83.53s,차트변경·예정Singapore실제없음·498폭가로넘침없음. 이는root브라우저관측이고이reviewer직접조작아닙니다. screenshot은마지막coverage-null전캡처로한계명시됨,참가자확인전.
