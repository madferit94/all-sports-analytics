# v08 실제 시간 배속: 증분 범위 독립검증 통과

reviewer /root/f1_verifier,2026-10-07. 생산자별도,저장지침적용,verification만작성했습니다.

완료범위/대조값: 총1861PASS(보존6/realtime1701/UI154). v07경기·지도·완료/예정예측및기존actualhelper2파일바이트동일.16GP8배속독립제어RAF wall1초→기록cursor진행0.25·0.5·1·2·4·10·30·60초.1배속+1000ms/0.25배속+250ms/0.5배속+500ms/60배속+60000ms 정확히대조. old압축60초기준기대값은사용하지않았습니다. 기본1selected·옵션8개,paused변경시커서시계정지·resume60배속1초+60기록초·seek50%/reset0·양지도22marker같은커서갱신·cleanup검사. 예정7지도는1초에phase1/180이며180초예측연출안내확인. 최신embedded/payload/한영UI154PASS.

발견과조치: 이전1배속은전체기록을60초로압축하는기준이어서너무빠르게느껴질수있었습니다. 생산자가종료GP에서는실제기록duration을분모로사용하도록바꿨고독립기대값과일치했습니다. 미래GP는기록이없으므로180초연출로명시한범위입니다. 개별차량물리속도까지같아지는변경이나새랩페이스예측모델로주장하지않습니다.

근거파일:SPEC-v08-realtime-independent.ko.md/check-preservation-independent.py/check-realtime-independent.cjs/check-ui-independent.cjs 및각JSON,reviewer-summary-v08-v01.json에피검파일SHA. root작성browser-observations-v01.json읽고별도주체SHA연결. 옵션/default1/0.5선택Play요청/tooltip관측은root실제브라우저보고이고reviewer직접조작아닙니다.

미확인: 사용자화면이랩비교로이동하여root후속pause브라우저검사는중단됐고사용자조작을보존했습니다. 브라우저일부분확인을전체완료로확대하지않습니다. 실제스톱워치속도측정은미실행,정확비율은독립제어RAF근거입니다. 기존모델성능/원본자료전체재인증이아니며참가자확인전입니다.
