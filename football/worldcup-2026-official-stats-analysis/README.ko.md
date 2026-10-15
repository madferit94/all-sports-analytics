# 2026 FIFA 월드컵 공식 기록 분석

[English](README.md) | [한국어](README.ko.md)

2026 FIFA 월드컵의 팀 단위 FIFA Match Centre 데이터로 만든 기술(記述) 분석 노트북 모음입니다.

## 노트북

1. `01_field_tilt_proxy_analysis.ipynb` - 필드 틸트 대리 지표와 슈팅 생성 효율.
2. `02_champion_profile_analysis.ipynb` - 우승팀 프로필 순위 비교.
3. `03_progression_quality_analysis.ipynb` - 영역 확보와 라인을 깨는 전진의 질.
4. `04_final_third_zone_dominance_mplsoccer.ipynb` - mplsoccer로 본 최종 3분의 1 지역 진입 경로와 구역 장악.
5. `05_off_ball_movement_analysis.ipynb` - 받으러 들어가는 움직임과 패스 받기 접근성.
6. `06_Possession_vs_Directness_Analysis_fixed.ipynb` - 점유 스타일 vs 최종 3분의 1 지역 직선 접근.
7. `07_reception_to_shot_conversion_analysis.ipynb` - 패스 받은 뒤 슈팅까지, 박스 안 마무리 전환율.
8. `08_defensive_shot_suppression_analysis.ipynb` - 수비의 슈팅 억제 대리 지표.

## 데이터

노트북은 정리된 입력 CSV가 아래 위치에 있다고 가정합니다:

`data/fifa_worldcup_2026/site_scrape/site_official_stats_team_wide_flagged.csv`

원본·정리 데이터 파일은 이 업로드에 포함되어 있지 않습니다. 노트북을 다시 실행하려면 직접 추가해 주세요.

## 지표 설명

- 필드 틸트 대리 지표 = 팀의 최종 3분의 1 지역 진입 / 양 팀 최종 3분의 1 지역 진입 합계 x 100.
- 최종 3분의 1 직선성 = 최종 3분의 1 지역 진입 / 성공한 패스 x 100.
- 패스 받기 접근성 = 미드필드·수비 라인 사이에서 받은 횟수 + 수비 뒷공간에서 받은 횟수.
- 진입 대비 슈팅 허용률 = 허용한 슈팅 / 상대에게 허용한 최종 3분의 1 지역 진입 x 100.

FIFA가 직접 제공한 지표가 아니면 모두 설명용 대리 지표입니다.

## 꼭 알아둘 점

- 벨기에 vs 이집트 경기는 FIFA가 Live Statistics만 제공해서 전체 기록 분석에서 제외했습니다.
- 팀별 경기 수가 3~8경기로 달라, 경기 수가 적은 팀은 값이 크게 흔들릴 수 있습니다.
- xG, 슈팅 위치, 경기 상황(스코어), 상대 전력은 보정하지 않았습니다.
- 순위는 현상을 설명할 뿐, 원인을 뜻하지 않습니다.

## 출처

FIFA Match Centre, FIFA 공식 전체 기록(Official Stats)만 사용.
