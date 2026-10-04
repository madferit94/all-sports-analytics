# 검증과 재현 방법

[English](README.md) | [한국어](README.ko.md)

[한국어 상세 보고서](report.ko.md) · [English report](report.md). 게시된 근거는 교차 검증 77개 통과, 차트 16개·워크북 숫자 2,381개 일치, PDF 13장 이미지 일치를 기록합니다. 분석용 CSV와 최종 발표 자료는 포함하며 약 107MB 전체 원본 캐시는 로컬에 보존합니다.

## 원본 캐시 없이 실행

프로젝트 폴더에서 `python3 verify_saved_data.py`를 실행하면 표준 라이브러리로 공개 CSV를 검증합니다. 분석 스크립트·노트북은 `analysis/requirements.txt`를 설치하고 포함된 CSV로 실행합니다. 새 다운로드가 필요하지 않습니다.

## 원본·분석·PPT 전체 검증

분석 가상환경을 활성화하고 원래 저장한 캐시 경로를 설정하세요.

```bash
export UNDERSTAT_RAW_CACHE="/path/to/original/understat_strikers_2025_26"
python verification/scripts/ko/verify_pipeline.py
python verification/scripts/en/verify_pipeline.py
```

해당 폴더에 `data/raw/leagues`, `data/raw/players`와 원래 `.meta.json` 파일이 있어야 합니다. 새로 다운로드한 기록은 기존 해시와 다를 수 있습니다. 개인 컴퓨터의 고정 경로 대신 환경변수를 사용합니다. 캐시가 없으면 전체 검증은 명확한 오류로 중단하며, 원본 검증을 완료했다고 기록하지 않습니다.

실행된 검증 노트북: [한국어](notebooks/ko/verification.ipynb) · [English](notebooks/en/verification.ipynb). Jupyter 시작 전에 환경변수를 설정하고 위에서 아래로 실행합니다. 이 폴더의 `verify_pipeline.py`는 영어 편의 실행 파일입니다. 두 언어 스크립트는 계산이 같지만 독립적으로 수정되므로 변경 후 대조가 필요합니다.

## 검증 근거

- `pipeline_validation.json`: 원본·계산·선정·차트·워크북의 개별 검증.
- `pdf_validation.json`: 최종 PDF 이미지 대조와 해시. 이번 게시에서도 PDF 파일을 그대로 유지했습니다.
- `visual_corrections.json`: 이전 검증에서 수정한 표시 문제 기록.
- `publication_validation.json`: 새 위치에서 노트북 실행·스크립트 일치·링크·파일 해시 점검.
- `league_representatives_crosscheck.sql`: SQLite를 이용한 독립 대표 선정.

정의·중복 원본 처리·한계는 상세 보고서에 있습니다. 저장 자료의 일치 검증이며 공식 경기 사건이나 xG 모델 정확성을 보증하지 않습니다. Microsoft PowerPoint 앱에서 직접 실행하지는 않았습니다.
