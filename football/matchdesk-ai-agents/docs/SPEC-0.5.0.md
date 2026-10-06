# MatchDesk 0.5.0 · 한·영 사이트 / Bilingual site

사용자 요청: 선정한 두 리그에 디자인이 모두 반영되었는지 확인하고 영어 사이트도 제공합니다.

## 범위와 구현

- 프리미어리그 27개·라리가 29개 팀: 현재와 과거 시즌에 수집된 팀의 합계입니다. 현 시즌 참가팀 수를 뜻하지 않습니다. 두 리그 모두 같은 8비트 화면·팀 색·24×24 로고 표시 방식입니다.
- [한국어 기본 화면](../index.html)과 [영어 기본 화면](../index.en.html). [v16 한국어](../visualization-design-2026-10-06-v16/index.html)·[v16 영어](../visualization-design-2026-10-06-v16/index.en.html)를 보존합니다.
- 영어판: 메뉴·날짜/장소/결과/시즌 필터·검색·표·차트 설명·오류·빈 자료 안내·접근성 이름·47개 지표 이름/의미/읽는 법을 제공합니다.
- 영어 이름·설명·원본 코드로 지표 검색 가능. PKC는 페널티킥 실점이 아닌 허용 횟수이며 TKL-LM은 최종 수비 태클입니다. SH-BLK의 공격/수비 방향 미확인 상태도 번역에 유지합니다.
- 상단 한국어/English 링크. 팀 상세 주소의 팀 선택은 유지합니다. 언어 전환은 별도 HTML 이동이므로 시즌 등 기타 필터는 기본값으로 돌아갑니다.
- 통계 값·팀/경기 식별자·날짜·로고 주소·리그 범위는 보존합니다. 영어 자료의 차이는 지표 표시용 이름·설명·단위입니다.
- 2,399 완료 경기·641 예정 경기·4,798 팀 경기 상세·160 팀 시즌 합계·47개 지표. 마지막 완료일 2026-09-20. 이번 변경에서 자료 갱신은 하지 않았습니다.

## 실행 검증 / Evidence

한국어 Node VM 40개 및 영어 15개 검사 통과. 영어 검사는 두 리그의 팀 상세, 팀 주소 유지, 47개 번역, 영어 검색·말풍선·필터·오류 안내, 표시용 번역 외 자료 동일성, 기본 파일 동일성을 검사합니다.

검사 환경은 화면 구성 요소를 대신하는 가짜 객체입니다. 실제 브라우저 배치, 터치 조작, 외부 이미지/글꼴 로딩과 시각적 품질을 확인한 것은 아닙니다. 참가자 확인 전입니다.

English acceptance: both selected leagues retain the pixel design. English includes all visitor UI and 47 metric definitions. Language links retain a selected team hash; other filters reset. Korean/English statistical data match except translated metric metadata. 40 Korean and 15 English Node VM checks passed. Real-browser rendering and human confirmation remain pending.

## 공개 범위

사용자가 앞서 승인한 GitHub 푸시·머지 범위에 영어판 코드와 문서를 포함합니다. 공개 저장소에 HTML·번역·검증 자료를 게시합니다. 비밀값·개인 작업일지·관리자 원본 자료는 제외합니다. 웹 호스팅, 관리자 인증, 모델 개선은 이번 요구 범위에 포함되지 않습니다.
