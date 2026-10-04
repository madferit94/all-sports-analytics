# 수집 데이터·Python·PPT 교차 검증

## 수치와 선정 결과는 일치하며, 표시 문제는 수정했습니다

저장된 원본 데이터부터 분석 결과와 최종 PPT까지 77개 검증 항목이 통과했습니다. PPT의 16개 차트와 포함된 워크북의 숫자 2,381개를 분석 결과와 대조했습니다. 게시용 PDF 13장의 이미지 픽셀도 최종 PPT 렌더링과 일치합니다.

판정은 **저장된 데이터 범위에서 공유 가능**입니다. 실제 경기 기록 또는 Understat xG 모델의 외부 정확성을 보증하는 검증은 아닙니다.

## 계산 오류는 발견하지 않았고, 세 가지 표시 문제를 정리했습니다

슈팅 위치 차트의 반복 눈금을 수정했고, PowerPoint에서 페널티 숫자가 중복될 가능성을 제거했습니다. 반올림된 수치의 곱을 정확한 등식처럼 보여주던 표기도 고쳤습니다. 원본 데이터와 선수 선정 결과는 바뀌지 않았습니다.

### 수정한 표시 문제

| 항목 | 심각도 | 이전 상태 | 수정 |
| --- | --- | --- | --- |
| 대표 선수 수치 표기 | 낮음 | 반올림한 두 수치의 곱을 정확한 등식처럼 표시 | 수치별로 독립 표기. 계산은 반올림 전 원본 값 사용 |
| 슈팅 위치 PDF 눈금 | 낮음 | 자동 눈금과 반올림으로 0.6 등 같은 표시가 반복됨 | 차트 폭 조정. 0.50~1.00 눈금으로 구분. 원본 좌표 유지 |
| 페널티 득점 라벨 | 중간 | 양수 라벨이 PowerPoint에서 중복 표시될 가능성 | 기본 라벨 모두 숨김, 양수 4개만 명시. 0 표시 제거 유지 |

## 리그별 대표 5명의 수치가 PPT와 같은지 확인했습니다

그래프는 각 리그의 대표 선수 1명씩을 보여줍니다. 오른쪽일수록 90분당 슈팅 빈도가 높고, 위쪽일수록 슈팅당 평균 xG가 높습니다. 아래 표의 세 수치는 최종 PPT의 표시값과 일치합니다. 대표 선정은 두 지표의 전체 상위 25% 기준과 달리, 리그 안에서 비페널티 xG/90이 가장 높은 선수를 고르는 방식입니다.

대표 선수 산점도는 최종 PPT의 4번째 슬라이드에서 확인하실 수 있습니다. 보고서에서는 정확한 수치를 아래 표로 대조합니다.

### 리그별 대표의 PPT 표시값

| 리그 | 선수 | 비페널티 슈팅 | 슈팅/90 | xG/슈팅 | xG/90 |
| --- | --- | --- | --- | --- | --- |
| Bundesliga | Harry Kane | 108 | 4.08 | 0.197 | 0.802 |
| La Liga | Robert Lewandowski | 60 | 3.31 | 0.231 | 0.764 |
| Ligue 1 | Pierre-Emerick Aubameyang | 60 | 2.60 | 0.259 | 0.674 |
| Premier League | Erling Haaland | 121 | 3.66 | 0.213 | 0.778 |
| Serie A | Nikola Krstovic | 99 | 5.00 | 0.158 | 0.792 |

## 데이터 범위와 지표 정의

2025/26 시즌의 저장된 Understat 스냅샷입니다. 원본 JSON 1,018개, 경기 1,752개, 리그별 선수 요약 2,775행, 상세 출전 기록 18,128행, 슈팅 이벤트 24,185개를 확인했습니다. 상세 수집은 전방 선수 후보 중심이며 전체 2,775명 모두의 상세 슈팅을 수집한 자료는 아닙니다.

최종 분석 대상은 중앙 공격수 후보 181명, 출전 기록 5,204개, 비페널티 슈팅 8,847개입니다. 페널티와 자책골 이벤트를 제외하고, 다른 세트피스는 포함합니다. 슈팅 지표는 FW로 기록된 경기뿐 아니라 해당 리그·시즌의 모든 출전 포지션을 포함합니다.

- 슈팅 빈도 = 비페널티 슈팅 ÷ 출전시간 × 90
- 기회 질 = 비페널티 슈팅 xG 합계 ÷ 슈팅 수
- 기대 슈팅 생산량 = 비페널티 슈팅 xG 합계 ÷ 출전시간 × 90
- 실제 전환율 = 비페널티 득점 ÷ 비페널티 슈팅
- 초과 득점 = 비페널티 득점 − 비페널티 슈팅 xG 합계

## 저장된 원본에서 계산을 다시 구성했습니다

원본 JSON과 수집 메타데이터의 SHA-256 해시를 확인하고, 경기·선수 요약·출전·슈팅 기록을 다시 구성해 CSV와 대조했습니다. SHA-256은 파일 내용이 달라졌는지 확인하는 값이며 원천 사실의 정확성을 보증하지는 않습니다.

이벤트에서 슈팅 수·득점·xG를 다시 집계하고, 출전 기록에서 시간을 합산했습니다. 선수 선정, 순위·동률 처리, 리그별 중앙값, 신체 부위 비중, 경기별 xG와 60분 이상 출전 경기의 무슈팅 비율을 확인했습니다. 영어·한글 노트북은 새 커널에서 각각 16개 코드 셀을 다시 실행했고, 주요 CSV가 두 언어에서 일치합니다.

마지막으로 PPT의 16개 차트 캐시와 포함된 16개 워크북의 숫자를 대조했습니다. PDF는 최종 PPT에서 렌더링한 이미지를 사용했고, 13개 페이지의 이미지 픽셀이 일치합니다.

### 개별 검증 결과

| 검증 항목 | 결과 | 근거 |
| --- | --- | --- |
| 60plus_zero_shot_rates | 통과 | "Condition is ≥60 minutes played per appearance, not a rolling 60-minute window" |
| all_cohort_metrics_from_events | 통과 | {"cohort_rows": 181, "cohort_minutes": 314600, "cohort_np_shots": 8847} |
| all_event_appearance_links | 통과 | {"orphan_events": 0} |
| appearance_raw_reconstruction | 통과 | {"canonical_rows": 18128, "duplicates_retained_in_evidence": 12, "mismatches": []} |
| bilingual_parity:both_measures_standouts.csv | 통과 | "Exact CSV byte comparison" |
| bilingual_parity:chance_quality_ranking.csv | 통과 | "Exact CSV byte comparison" |
| bilingual_parity:goals_above_xg_ranking.csv | 통과 | "Exact CSV byte comparison" |
| bilingual_parity:league_metric_representatives.csv | 통과 | "Exact CSV byte comparison" |
| bilingual_parity:league_summary.csv | 통과 | "Exact CSV byte comparison" |
| bilingual_parity:match_consistency.csv | 통과 | "Exact CSV byte comparison" |
| bilingual_parity:player_match_analysis.csv | 통과 | "Exact CSV byte comparison" |
| bilingual_parity:player_profiles.csv | 통과 | "Exact CSV byte comparison" |
| bilingual_parity:representative_players.csv | 통과 | "Exact CSV byte comparison" |
| bilingual_parity:shot_volume_ranking.csv | 통과 | "Exact CSV byte comparison" |
| case_selection_explanation | 통과 | "Why these four case studies? One central example from each shot-profile quadrant, with at least 50 non-penalty shots. Hugo Ekitike High volume · High xG/shot Ante Budimir High volume · Low xG/shot Rasmus Højlund Low volume · High xG/shot Mateo Pellegrino Low volume · Low xG/shot Why these four? To compare shot locations, body-part mix and match variation across contrasting profiles. Split the cohort at both medians, then choose the player nearest each quadrant’s median after scaling the metrics. These are illustrative cases. High and low are relative to the cohort, not overall ability grades." |
| cohort_filter_reproduction | 통과 | {"selected_rows": 181, "excluded_failed_qc": 12} |
| duplicate_affected_candidate_exclusion | 통과 | {"affected_candidate_rows": 12} |
| duplicate_payload:11401:29482 | 통과 | "784933" |
| duplicate_payload:12160:29482 | 통과 | "784971" |
| duplicate_payload:12322:29482 | 통과 | "784957" |
| duplicate_payload:13700:29482 | 통과 | "784927" |
| duplicate_payload:13701:29482 | 통과 | "784925" |
| duplicate_payload:13705:29482 | 통과 | "784931" |
| duplicate_payload:13996:29482 | 통과 | "784967" |
| duplicate_payload:14173:29482 | 통과 | "784941" |
| duplicate_payload:14393:29482 | 통과 | "784929" |
| duplicate_payload:5656:29482 | 통과 | "784968" |
| duplicate_payload:770:29482 | 통과 | "784972" |
| duplicate_payload:8187:29482 | 통과 | "784969" |
| embedded_workbook_numeric_values | 통과 | {"numeric_cache_values": 2381, "workbooks": 16, "errors": []} |
| event_and_appearance_unique_keys | 통과 | {"events": 24185, "appearances": 18128} |
| event_ranges | 통과 | "X,Y,xG in [0,1]" |
| five_scoring_leaders | 통과 | [{"player_name": "Erling Haaland", "league": "EPL", "goals": 27}, {"player_name": "Kylian Mbappe-Lottin", "league": "La_liga", "goals": 25}, {"player_name": "Harry Kane", "league": "Bundesliga", "goals": 36}, {"player_name": "Lautaro Martínez", "league": "Serie_A", "goals": 17}, {"player_name": "Esteban Lepaul", "league": "Ligue_1", "goals": 21}] |
| fixture_raw_reconciliation | 통과 | {"fixtures": 1752, "mismatches": []} |
| four_case_selection | 통과 | [["EPL", "Hugo Ekitike"], ["La_liga", "Ante Budimir"], ["Serie_A", "Rasmus Højlund"], ["Serie_A", "Mateo Pellegrino"]] |
| four_quadrant_classification | 통과 | {"volume_median": 2.464840858623242, "quality_median": 0.1579359607263044} |
| global_upper_quartile_standouts | 통과 | {"players": ["Serhou Guirassy", "Patrik Schick", "Erling Haaland", "Benjamin Sesko", "Ferrán Torres", "Alexander Sørloth", "Robert Lewandowski"], "volume_q75": 2.87109375, "quality_q75": 0.1976654265075922} |
| input_hash:forward_candidate_audit.csv | 통과 | "cf27c7821fbd6584f99a858290582b4119d20dbc66c18f3876986921b6f8813c" |
| input_hash:player_match_records.csv | 통과 | "e5d3dd3b84edb3f4f14f309a1e2df800fcbd6277f86bcc6fc24b3b9170eca0f2" |
| input_hash:shot_events.csv | 통과 | "04533747c93d7b94858b460f0ef5bb9d68bcc89fe09c1f8b7b9242ce219987ab" |
| input_hash:striker_scatter_ready.csv | 통과 | "4f60944eae691622626517c244bf05c18fda01fdff77870ac2ea120d54b9a31b" |
| leader_superlative_claims | 통과 | "Highest volume Mbappe; highest quality Haaland, among five leaders" |
| league_median_claim | 통과 | "Premier League cohort highest median xG/shot" |
| league_representative_selection | 통과 | [{"league": "EPL", "player_name": "Erling Haaland", "npxg_per90": 0.7779655817986165}, {"league": "La_liga", "player_name": "Robert Lewandowski", "npxg_per90": 0.764004570140612}, {"league": "Bundesliga", "player_name": "Harry Kane", "npxg_per90": 0.8016770556920542}, {"league": "Serie_A", "player_name": "Nikola Krstovic", "npxg_per90": 0.7921103954446962}, {"league": "Ligue_1", "player_name": "Pierre-Emerick Aubameyang", "npxg_per90": 0.6737361387183518}] |
| league_summary_raw_reconciliation | 통과 | {"rows": 2775, "mismatch_keys": []} |
| metric_rank:chance_quality_ranking | 통과 | {"rows": 85} |
| metric_rank:goals_above_xg_ranking | 통과 | {"rows": 85} |
| metric_rank:shot_volume_ranking | 통과 | {"rows": 181} |
| output_metric_formula | 통과 | "NP goals - event xG; conversion NP goals/shots" |
| penalty_native_labels_disabled | 통과 | "Five native labels hidden; four explicit positive labels retained; zero omitted" |
| penalty_own_goal_flags | 통과 | {"own_goal_events": 8} |
| position_classification_rule | 통과 | "Known position minutes ≥50% of total; FW minutes ≥50% of known position minutes" |
| ppt_chart_1 | 통과 | [{"series": 0, "points": 33, "match": true}, {"series": 1, "points": 38, "match": true}, {"series": 2, "points": 30, "match": true}, {"series": 3, "points": 50, "match": true}, {"series": 4, "points": 30, "match": true}] |
| ppt_chart_10 | 통과 | [{"series": 0, "points": 1, "match": true}, {"series": 1, "points": 1, "match": true}, {"series": 2, "points": 1, "match": true}, {"series": 3, "points": 1, "match": true}, {"series": 4, "points": 1, "match": true}] |
| ppt_chart_11 | 통과 | [{"series": 0, "points": 54, "match": true}, {"series": 1, "points": 11, "match": true}] |
| ppt_chart_12 | 통과 | [{"series": 0, "points": 84, "match": true}, {"series": 1, "points": 11, "match": true}] |
| ppt_chart_13 | 통과 | [{"series": 0, "points": 47, "match": true}, {"series": 1, "points": 12, "match": true}] |
| ppt_chart_14 | 통과 | [{"series": 0, "points": 64, "match": true}, {"series": 1, "points": 8, "match": true}] |
| ppt_chart_15 | 통과 | [{"series": 0, "points": 4, "match": true}, {"series": 1, "points": 4, "match": true}, {"series": 2, "points": 4, "match": true}, {"series": 3, "points": 4, "match": true}] |
| ppt_chart_16 | 통과 | [{"series": 0, "points": 28, "match": true}, {"series": 1, "points": 37, "match": true}, {"series": 2, "points": 33, "match": true}, {"series": 3, "points": 37, "match": true}] |
| ppt_chart_2 | 통과 | [{"series": 0, "points": 5, "match": true}] |
| ppt_chart_3 | 통과 | [{"series": 0, "points": 33, "match": true}, {"series": 1, "points": 38, "match": true}, {"series": 2, "points": 30, "match": true}, {"series": 3, "points": 50, "match": true}, {"series": 4, "points": 30, "match": true}] |
| ppt_chart_4 | 통과 | [{"series": 0, "points": 181, "match": true}, {"series": 1, "points": 1, "match": true}, {"series": 2, "points": 1, "match": true}, {"series": 3, "points": 1, "match": true}, {"series": 4, "points": 1, "match": true}, {"series": 5, "points": 1, "match": true}] |
| ppt_chart_5 | 통과 | [{"series": 0, "points": 1, "match": true}, {"series": 1, "points": 1, "match": true}, {"series": 2, "points": 1, "match": true}, {"series": 3, "points": 1, "match": true}, {"series": 4, "points": 2, "match": true}, {"series": 5, "points": 2, "match": true}] |
| ppt_chart_6 | 통과 | [{"series": 0, "points": 33, "match": true}, {"series": 1, "points": 38, "match": true}, {"series": 2, "points": 30, "match": true}, {"series": 3, "points": 50, "match": true}, {"series": 4, "points": 30, "match": true}, {"series": 5, "points": 2, "match": true}] |
| ppt_chart_7 | 통과 | [{"series": 0, "points": 5, "match": true}] |
| ppt_chart_8 | 통과 | [{"series": 0, "points": 5, "match": true}] |
| ppt_chart_9 | 통과 | [{"series": 0, "points": 5, "match": true}, {"series": 1, "points": 5, "match": true}] |
| ppt_native_chart_and_slide_counts | 통과 | {"charts": 16, "slides": 13} |
| profile_keys_and_completeness | 통과 | {"players": 181} |
| raw_hashes_and_retrieval_metadata | 통과 | {"files": 1018, "mismatches": []} |
| recorded_position_minutes | 통과 | {"candidate_rows": 1042, "mismatches": []} |
| removed_footer_and_author | 통과 | "13 slides visible text" |
| shot_raw_reconstruction | 통과 | {"events": 24185, "mismatch_ids": []} |
| visible_key_findings | 통과 | "Mbappe 4.70; Haaland .213; Lepaul +5.31; Pellegrino headers 41.7%" |
| visible_league_representative_values | 통과 | "Five names and fifteen rounded metrics checked" |
| zero_shot_appearance_reconstruction | 통과 | "All appearances retained; absent NP event totals become 0" |

## 알려진 원본 이상과 남아 있는 검증 한계

- 원본 출전 중복 12건은 roster_id만 달랐습니다. 별도 이상 기록을 보존하고, 영향을 받은 후보 12행을 최종 분석에서 제외했습니다.
- 슈팅 이벤트의 도움 선수 이름 5,688건은 원본부터 null입니다. CSV의 빈칸과 대조했고, 이번 지표 계산에는 사용하지 않습니다.
- 출전 날짜 범위는 2025년 8월 15일~2026년 5월 24일이며 시즌 값은 2025입니다. 실시간 변경·정정 기록은 이번 검증 범위에 포함하지 않았습니다.
- “60분 이상 무슈팅”은 해당 경기에서 60분 이상 출전하고 비페널티 슈팅이 0회라는 뜻입니다. 연속 60분 구간을 추적한 지표가 아닙니다. 산점도는 모든 출전 경기를 표시합니다.
- 실제 영상·공식 경기 기록과의 별도 대조, Understat xG 모델의 보정·정확성 검증, 팀·상대·리그 수준 보정은 수행하지 않았습니다.
- Microsoft PowerPoint 앱에서 직접 열어 확인하지 않았습니다. OOXML 구조·캐시·워크북과 자체 렌더링은 확인했습니다. 기존 LibreOffice 변환은 산점도 호환성 문제가 있어 게시에는 제공한 PDF를 사용하세요.

## 게시할 파일과 다음 검증

게시에는 [최종 PDF](../presentation/Beyond_Goals_EN_Landscape_verified.pdf), 수정에는 같은 이름의 PPTX를 사용하세요. 기존 v3는 검증 전 표시 상태를 보존한 이전 버전입니다. 데이터나 선정 기준을 바꾸면 노트북을 다시 실행하고 PPT도 다시 대조해야 합니다.

추가 확인이 필요하다면 공식 경기 기록으로 득점·출전시간을 대조하고, 여러 시즌에서 같은 지표가 유지되는지 확인하는 것이 다음 단계입니다.

## 이 자료만으로 답할 수 없는 질문

높은 xG/shot이 선수 움직임 때문인지 팀 전술 때문인지, 골−xG 차이가 다음 시즌에도 유지될지, 다른 리그로 옮겨도 같은 성과를 낼지는 이번 데이터만으로 확정할 수 없습니다.
