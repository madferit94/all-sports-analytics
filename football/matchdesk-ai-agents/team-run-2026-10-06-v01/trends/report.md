# 최근 팀 동향 담당 실제 실행

- 실행: team-run-2026-10-06-v01 / 담당 주체: /root/trends
- 대상: Arsenal–Leeds understat:31230, Málaga–Espanyol understat:30845
- 관측 시각: 2026-10-06T06:31:53.086268+00:00 (한국 날짜 2026-10-06)
- 상태: DONE(검색·기록 수행), 전체 최신 동향 확보는 부분 MISSING.
- 기록 25개: COLLECTED 10, MISSING 14, BLOCKED 1.
- 구조 검사: True. 사실의 완전성 인증이나 다음 경기 출전 확정은 아님.

| 팀 | 실제 확인 | 제한 |
|---|---|---|
| Arsenal | 리그 공식 기사 10/5 기준 Havertz 부상 대표팀 철수, Konsa 대표팀 철수 | Leeds전 결장 확정 없음. 구단 뉴스 목록 403. |
| Leeds | 공식 10/5 기사 Tanaka 대표팀 소집 4회 출전 | Arsenal전 선발·출전 가능 확정 아님. |
| Málaga | 공식 훈련 기사 Juan Cruz 점진적 단체 합류, Cajuste·Murillo·Aaron Ochoa·Lobete 회복 중 | 기사 발행시각 미표기. 문맥 사건일 10/5 추정, 결장 확정 금지. |
| Espanyol | 공식 9/14 기자회견 Manolo González 확인 | 오래된 근거. 당시 Jofre 제외를 다음 Málaga전 상태로 재사용하지 않음. |

미수집: 네 팀의 완전한 부상·징계·출전 가능 명단, 최신 경기 전 기자회견, 최근 이적 자료, Arsenal·Leeds 현재 감독의 최신 공식 근거. 발행시각 오프셋이 확인되지 않은 뉴스는 news 계약에 MISSING으로 남겼습니다. 네 팀 모두 무부상/무징계라고 해석할 수 없습니다.

정확한 날짜·시각이 검증되지 않은 자료는 과거 모델 입력에 사용하지 않습니다. 이번 자료 전체는 설명용 보조 근거이며 확률 계산에 반영하지 않았습니다. 공식 기사에 적힌 경기 날짜는 문맥 파악에만 사용했으며 Understat 기본 일정은 바꾸지 않았습니다.

원문은 web 도구로 실제 읽었습니다. 별도 Python 재조회는 Windows 네트워크 권한 오류로 실패했고 각 *-metadata.json에 그 실패를 보존했습니다. 원문 HTML 저장 성공이라고 주장하지 않습니다. source-evidence.json은 읽은 웹 텍스트를 사람이 검토할 수 있게 옮긴 요약·25단어 이하 짧은 발췌입니다.

## 출처

- [arsenal 공식 근거](https://www.premierleague.com/en/news/4727187) — 공개 날짜: 2026-10-05 / 시각 정밀도: DATE_ONLY
- [leeds 공식 근거](https://www.leedsunited.com/en/news/tanaka-helps-blue-samurai-to-kirin-cup-success) — 공개 날짜: 2026-10-05 / 시각 정밀도: DATE_ONLY
- [malaga 공식 근거](https://www.malagacf.com/noticias/vuelta-al-trabajo-para-preparar-el-malagaespanyol) — 공개 날짜: 미확인 / 시각 정밀도: UNVERIFIED
- [espanyol 공식 근거](https://campaigns.rcdespanyol.com/es/noticia/un-rival-muy-complicado/20751) — 공개 날짜: 2026-09-14 / 시각 정밀도: LOCAL_TIME_WITHOUT_SOURCE_OFFSET
