# v05 지도 비교: 증분 범위 내부준비 가능·한계 있음

reviewer `/root/f1_verifier`, 2026-10-07. verification-evidence 및 저장 MatchDesk reviewer 지침 적용. production파일 수정하지 않았습니다. v05 verification만 작성했습니다.

## 완료 범위 / 실제 대조값
독립1456검사 PASS: 보존3 / 원본지도자료533 / 지도상태521 / mount245 / UI154.
보존: v04경기자료·완료16회고예측·미래7예측바이트동일. 지도/GPS가모델입력으로추가되지않음을서비스예측파일불변으로대조했습니다. 기존모델전체학습을재인증하지않습니다.
원본: 완료16GP각2명좌표·예정7개2025참조,총23지도46요청. 압축원문SHA/응답행수/선수session키/순서/유한좌표/각다운샘플원본일치/원본2초초과공백양끝보존/한랩윤곽원본xy일치. 예측참조2025메타원본SHA및동일circuit key·참조날짜<미래시작대조. 피트인·아웃제외정상랩16개검사. 실패source없음.
지도: 실제GPS선택2명만표시,나머지랩재구성구분·22마커·시간/좌표유한·viewport변환·지도불명/서킷불일치타원대체없음. 보간전체간격2000ms허용/2001·4000거부,큰공백의정확한원본시점은측정값허용,범위밖외삽없음.
컨트롤:16GP재생·시간진행·seek끝·reset·숨김pause·destroy이벤트/프레임해제. 예정7지도는2025참고문구·실제GPS범례없음·표22명·추가실제canvas없음. 최종HTML5payload와원본일치·최신module·JS구문·한영25GP라우팅·예정중복표숨김·취소예측없음·축구언어링크대조.

## 발견과 조치
첫builder코드는양옆각2초를허용해전체4초보간가능했습니다. root규칙의샘플간격<=2초와대조하여생산자에게보고했고전체간격<=2000ms로수정된경계검사를통과했습니다.
수집중초안HTML은maps/module동기화불일치2개FAIL(v01),이후피트랩지도교체로maps불일치(v02)발견. 최종자료고정·재assemble후동일UI검사v03 PASS입니다. v01원본증거는original.json.gz압축으로바이트보존하고요약JSON에canonicalhash를남겼습니다. 실패를삭제하지않았습니다.
윤곽11245러셀10랩피트인→9랩/11731러셀9랩피트인→11랩을자료담당이정상랩으로수정했고독립원본xy및피트구간제외확인. 나머지실제샘플/모델변경없음.
예정지도2025참고표시누락을보고하여기본문구·현재레이아웃동일공식미확인안내·실제GPS범례숨김을반영한최종module검사PASS.

## 근거 파일
실행전SPEC-map-independent-v01.ko.md. check-preservation-independent.py/check-map-data-independent.py/check-map-state-independent.cjs/check-map-mount-independent.cjs/check-ui-independent.cjs 재실행가능. 각JSON은기대값·실제값·주체기록. reviewer-summary-v05-v01.json은1456검사및최종artifactSHA를기록합니다.

## 미확인과 필요한 판단
OpenF1 x/y는위도·경도나미터단위로확인한좌표가아닙니다. 완료GP각2명만실제위치이며나머지20명은랩기록보간. 미래지도는2025같은circuit key참고윤곽이며2026레이아웃불변공식검증아님. 예측움직임은최종순위연출이고랩타임/추월물리모델아닙니다. 원본위치큰공백을GPS로이어그리지않고재구성표시합니다.
root메시지의AI브라우저관측(2canvas/가로넘침없음/Play63%13:58/RUS L37/GPS2/22)은이reviewer직접브라우저검사와분리했습니다. 최종브라우저JSON은대기중. 사용자확인전이며기존전체사이트·미래모델확률을새로보장하지않습니다.
