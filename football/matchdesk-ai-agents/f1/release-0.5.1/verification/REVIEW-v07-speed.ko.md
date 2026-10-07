# v07 공통 배속: 증분 범위 검증 통과

reviewer /root/f1_verifier,생산자별도,2026-10-07. 저장 reviewer/protocol·verification-evidence 적용. v07 verification만작성.

완료 범위 / 실제 대조값: 독립417PASS(보존6/배속257/UI154). v06경기·지도·완료/예정예측및기존actual replay/comparison바이트동일.16GP예측회전척도=유효완료랩max;없으면세션결과랩수fallback,예정·모두없으면3회전연출. 호주유효57/결과58불일치에서실제재생끝과맞는57우선확인.
제어RAF 같은1초후진행량1/60·2/60·4/60,정확비율1:2:4. 두canvas동일커서에서22차량갱신. paused배속변경은커서/시계정지,재개4x진행량4/60. seek50%·reset0의실제KST시계는원래timeline기준과동일. 한영공통배속label/최신module·5payload/한영라우팅검사PASS.

발견과 조치: 고정3회전예측연출을실제재생유효랩수척도로교체한생산자코드만검토했습니다. 공통배속은동일시각커서를의미하며모든개별차량이같은물리적속도로주행한다는뜻아닙니다. 기존예측순위조기종료연출·실제랩시각차이는그대로이며새물리랩페이스모델로주장하지않습니다.

근거 파일: SPEC-v07-speed-independent.ko.md,check-preservation-independent.py,check-speed-independent.cjs,check-ui-independent.cjs 및각JSON. reviewer-summary-v07-v01.json에피검파일/보고서SHA. root작성browser-observations-v01.json읽고별도주체SHA연결:4x선택재생후pause/공통4유지/phase0.4309645·기록L25반영보고. reviewer실제브라우저직접조작아님.

미확인: 프레임타임제어자동검사이며실브라우저스톱워치속도측정아닙니다.1x는기존압축재생기준으로실시간1초=경기1초라고인증하지않습니다. 기존전체모델성능·데이터를다시인증하는범위아님. 참가자확인전.
