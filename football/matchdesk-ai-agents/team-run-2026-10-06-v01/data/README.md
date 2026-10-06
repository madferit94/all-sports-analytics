# 데이터·선수단 역할 실행 결과

실제 실행 주체: `/root/data_analysis`. 실행 ID: `team-run-2026-10-06-v01`.

대상은 Arsenal–Leeds `understat:31230`, Malaga–Espanyol `understat:30845`입니다. Understat 기본 경기·일정·xG와 StatMuse 추가 통계 정책은 변경하지 않았습니다.

## 수집 결과

보조 기록 24개 중 16개를 수집하고, 미래 경기 실제 선발·포메이션 8개는 `MISSING`으로 남겼습니다. 계약 검사 24개 오류 0개이며, 이 검사는 제공처 정보의 절대 정확성을 인증하지 않습니다.

| 팀 | 최근 실제 선발 경기 키 | 명목 포메이션 | 선수단 스냅샷 인원 | 2026-06-01 추정 선수단 가치 |
|---|---|---|---:|---:|
| Arsenal | understat:31224 | 4-2-3-1 | 24 | EUR 1,230,000,000 |
| Leeds | understat:31225 | 3-5-2 | 30 | EUR 346,030,000 |
| Malaga | understat:30835 | 4-1-4-1 | 28 | EUR 27,200,000 |
| Espanyol | understat:30834 | 4-2-3-1 | 25 | EUR 124,200,000 |

선수단 구성은 10월 6일 조회 스냅샷입니다. 사이트가 정확한 발효일을 표시하지 않아 `effective_date_basis`에 조회일 기준임을 명시했습니다. 6월 시장가치와 10월 선수단은 서로 다른 시점이며 전력·확률로 직접 환산하지 않습니다. 시장가치는 제공처 표시 금액의 반올림된 추정치입니다. 현재 시장가치 열은 평가 기준일이 명시되지 않아 수집값으로 채택하지 않았습니다.

선발 자료: Arsenal은 Sky 경기 종료 후 명단, Leeds는 FotMob, Malaga는 Sky 명단 및 LaLiga 명목 포메이션, Espanyol은 LaLiga 공식 경기 페이지입니다. 일부 선수명은 제공처의 약칭을 보존했고 통합 선수 ID는 아직 없습니다. 포메이션은 명목 시작 배치이며 경기 중 전술을 확정하는 자료가 아닙니다.

선수단 자료: Leeds·Malaga·Espanyol은 구단 공식 명단, Arsenal은 Transfermarkt입니다. Arsenal 공식 `men/players` 경로가 404여서 접근 실패를 `source_manifest.json`에 기록하고 공개 선수단 표로 대체했습니다.

## 실제 조회와 접근 제한

최초 제한된 로컬 네트워크 요청은 Windows 소켓 권한 오류로 차단됐습니다. 허용된 공개 페이지 읽기 실행에서는 원문 텍스트 13개를 확보했습니다. 저장은 렌더링 텍스트만 수행했고 script/style 및 사이트 실행 설정은 제거했습니다. 원문 경로·조회 시각·일부 SHA256은 source_manifest.json과 dated_source_manifest.json에 있습니다.

Arsenal 포메이션은 별도 웹 조회 발췌도 보존했습니다. 그 FotMob 응답은 46:32 시점의 오래된 라이브 스냅샷이므로 해당 점수·통계는 가져오지 않았습니다. 시작 선발은 Sky 경기 종료 명단과 대조했습니다.

## 산출물

- `context_records.json`: 전체 24개 기록과 사실·수집 상태
- `lineups_formations.json`, `squads.json`, `dated_market_values.json`: 단계별 자료
- `context_validation.json`: `context_cli.validate_records` 실행 결과
- `reports.json`: 대상 2경기의 data 역할 보고
- `../analysis/recent_form.json`: 실제 Understat 최근 5경기 계산
- `../analysis/README.md`: 해석과 사용 제한

계약 검사 성공과 별개로 참가자 확인 전입니다. 새 보조 자료는 설명 근거로만 사용하며 예측 입력이나 승리 확률은 생성하지 않았습니다.
