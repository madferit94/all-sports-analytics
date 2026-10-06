"""Promote existing work to 0.9.0 without rewriting historical snapshots."""
from pathlib import Path
import json

p=Path(__file__).resolve().parents[1]
if (p/'VERSION').read_text(encoding='utf8').strip()!='0.8.0':
    raise SystemExit('This one-time promotion requires 0.8.0; do not rewrite an existing release.')
backup=p/'docs/publication_manifest-0.8.0.json'
if not backup.exists():
    backup.write_bytes((p/'publication_manifest.json').read_bytes())
(p/'VERSION').write_text('0.9.0\n',encoding='utf8')
selection=json.loads((p/'viewer_selection.json').read_text(encoding='utf8'))
selection.update(release='0.9.0',versioned_viewer='visualization-design-2026-10-06-v23/index.html',experimental_prediction_implemented=True,prediction_model='prematch-v2-2026-10-06-v01',prediction_status='EXPERIMENTAL_NOT_ADOPTED',simulation_version='pixel-v2-2026-10-06-v01',players_per_team=11)
# Configured credentials and live-account access are runtime state, not public configuration.
selection['model_adopted']=False
selection['ai_model_connected']=False
(p/'viewer_selection.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

for lang in ('md','ko.md'):
    path=p/f'README.{lang}'
    text=path.read_text(encoding='utf8')
    text=text.replace('**Release 0.8.0','**Release 0.9.0').replace('**버전 0.8.0','**버전 0.9.0')
    text=text.replace('[versioned v19](visualization-design-2026-10-06-v19/index.html)','[versioned v23](visualization-design-2026-10-06-v23/index.html)').replace('[v19 버전](visualization-design-2026-10-06-v19/index.html)','[v23 버전](visualization-design-2026-10-06-v23/index.html)')
    text=text.replace('docs/SPEC-0.8.0.md','docs/SPEC-0.9.0.md')
    text=text.replace('node visualization-design-2026-10-06-v19/','node visualization-design-2026-10-06-v23/')
    text=text.replace('UI v01–v19 are preserved. Release 0.8.0 provides Korean index.html and English index.en.html identical to their v19 snapshots;','UI v01–v23 are preserved. Release 0.9.0 provides Korean index.html and English index.en.html identical to their v23 snapshots;')
    text=text.replace('화면 v01~v19을 보존하며 이번 버전은 0.8.0입니다. 한국어 index.html과 영어 index.en.html은 v19의 각 언어 화면과 동일합니다.','화면 v01~v23을 보존하며 이번 버전은 0.9.0입니다. 한국어 index.html과 영어 index.en.html은 v23의 각 언어 화면과 동일합니다.')
    text=text.replace('and probabilities are not shown in the viewer. Automatic refresh, administrator authentication, prediction API, hosting and a new five-agent runtime run are not implemented.','and the first model is not adopted. The newer experimental v2 probabilities are displayed with an explicit non-adopted status. Automatic refresh, administrator authentication and hosting are not implemented.')
    text=text.replace('사이트에 예측 확률을 표시하지 않습니다. 자동 갱신·관리자 로그인·예측 API(프로그램 간 연결 창구)·공개 서비스·통합 5인 팀 재실행은 미구현입니다.','최신 실험 v2의 확률은 미채택 표시와 함께 화면에 제공합니다. 자동 갱신·관리자 로그인·공개 서비스는 미구현입니다.')
    text=text.replace('No shot-coordinate dataset is available; the pixel pitch is decorative.','No shot-coordinate dataset is available; player motion and goals in the replay are illustrative.')
    text=text.replace('슈팅 좌표 자료는 없으며 픽셀 경기장 그림은 장식입니다.','슈팅 좌표 자료는 없으며 재생의 움직임과 득점 시간은 연출입니다.')
    if lang=='md':
        intro='0.9.0: Experimental pre-match probabilities with attack/defence/pressing/recent-five features and cold-start smoothing; illustrated 8-bit replay now has **11 players per team (one goalkeeper + ten outfield players)**. Preserve v20 AI error messages, v21 result colours, v22 first replay and v23 player-count correction. [Model](modeling/prematch-v2-2026-10-06-v01/README.md) · [Feature fact check](docs/feature-factcheck-2026-10-06-v01/RESULTS.ko.md) · [Release SPEC](docs/SPEC-0.9.0.md). Predictions are **EXPERIMENTAL_NOT_ADOPTED**; replay is not real footage.\n\n'
        rows=['AI request error handling','Loss/draw colour contrast','Experimental probabilities and illustrated replay','Eleven players per team; goalkeeper and ten outfield players']
    else:
        intro='0.9.0: 공격·수비·압박·최근 5경기와 데이터 부족 보정을 이용한 실험 확률·8비트 재생을 추가하고 **각 팀 11명(골키퍼 1명·필드 선수 10명)**으로 수정했습니다. v20 오류 안내·v21 승패 색상·v22 첫 재생·v23 인원 수정을 보존합니다. [모델](modeling/prematch-v2-2026-10-06-v01/README.ko.md) · [변수 팩트 체크](docs/feature-factcheck-2026-10-06-v01/RESULTS.ko.md) · [이번 SPEC](docs/SPEC-0.9.0.md). 확률은 **실험·정식 미채택**이며 재생은 가상 연출입니다.\n\n'
        rows=['AI 요청 오류 안내 개선','패배 붉은색·무승부 노란색 가독성','실험 승부 확률·가상 재생','각 팀 골키퍼 1명·필드 선수 10명']
    marker='**Day13' if lang=='md' else '**Day13'
    text=text.replace(marker,intro+marker,1)
    text+='\n'+''.join(f'| [v{n}](visualization-design-2026-10-06-v{n}/index.html) · [English](visualization-design-2026-10-06-v{n}/index.en.html) | {label} |\n' for n,label in zip(range(20,24),rows))
    # Code check totals are version-specific evidence, not browser verification.
    text=text.replace('44 Korean + 19 English Node VM checks passed;','Versioned Node VM checks are preserved;').replace('한국어 44개·영어 19개 코드 동작 검사 통과.','버전별 코드 동작 검사 결과를 보존했습니다.')
    text=text.replace('Node runs 40 calculation/navigation/interaction checks with a DOM stub.','Node checks calculations/navigation/interactions with a DOM stub.').replace('화면은 Node에서 화면 요소를 흉내 내는 검사로 계산·검색·이동·말풍선과 로고 렌더링 40항목을 확인합니다.','화면은 Node에서 화면 요소를 흉내 내는 검사로 계산·검색·이동·말풍선과 로고 렌더링을 확인합니다.')
    path.write_text(text,encoding='utf8')

path=p/'CHANGELOG.md'
text=path.read_text(encoding='utf8')
entry='''## 0.9.0 — 2026-10-06

- Preserve v20 improved AI errors, v21 readable loss/draw colours, v22 experimental prediction/replay and v23 eleven-player correction in both languages.
- Each simulated team contains one goalkeeper and ten outfield players. Replay is illustrative, not real footage, player-level forecasting or a confirmed result.
- Publish pre-match v2 code, stored-input features, metrics and independent review; keep model_adopted false. Attack/defence/pressing/recent-five features use strictly earlier records, with prior-season/league smoothing for sparse history. No actual passing accuracy, odds or market values are silently added.
- 2025/26 accuracy 50.92% versus 45.79% league-frequency baseline; current LaLiga accuracy remains below baseline. Prior rank proxy ablation did not improve 2025/26 results; official rank and time-correct market value remain candidates.
- 한국어·영어 README/SPEC와 파일 해시를 갱신합니다. 각 팀 11명 수정·실험 확률·가상 재생을 포함하며 정식 모델 채택은 보류합니다. 실제 브라우저 재생·참가자 확인은 아직입니다.
- Automated evidence is stored alongside the relevant engine/model/viewer/server checks. Mocked-provider tests are not live Google verification. No external hosting or GitHub CI success is claimed.

'''
text=text.replace('## 0.8.0',entry+'## 0.8.0',1)
path.write_text(text,encoding='utf8')
for name in ('README.md','README.ko.md'):
    path=p.parents[1]/name
    text=path.read_text(encoding='utf8').replace('· 0.8.0','· 0.9.0').replace('docs/SPEC-0.8.0.md','docs/SPEC-0.9.0.md')
    text=text.replace('Experimental prediction adoption remains false.','Experimental v2 probabilities and an illustrated 8-bit replay with eleven players per team are available; formal model adoption remains false.')
    text=text.replace('예측 모델 채택은 보류이며','실험 v2 승부 확률·각 팀 11명 가상 8비트 재생을 제공하며 정식 모델 채택은 보류입니다.')
    path.write_text(text,encoding='utf8')
print('Prepared 0.9.0 version, bilingual READMEs, changelog and preserved 0.8.0 manifest.')
