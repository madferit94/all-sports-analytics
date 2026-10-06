# 8비트 선수 11명 수정 v2

통합 팀 `matchdesk-builder` 스킬을 적용한 builder 담당의 수정입니다. 기존 v1은 각 팀 7명만 그려졌습니다. v2는 각 팀 골키퍼 1명과 필드 선수 10명을 그립니다. 골키퍼는 별도 유니폼 색과 흰 장갑으로 구분합니다. 두 팀 유니폼과 같은 색이 되면 다른 골키퍼 색을 선택합니다.

배치는 가상 경기 연출을 위한 고정 간격입니다. 실제 팀 포메이션, 실제 선발 명단, 실제 선수 움직임을 재현했다고 주장하지 않습니다. 선수들이 서로 겹치거나 경기장 밖으로 나가지 않도록 움직임 범위를 제한했습니다. 기존 확률 641경기와 원래 기록 데이터는 그대로 유지했습니다.

새 파일은 `simulation/pixel-v2-2026-10-06-v01/`, 새 화면 보존본은 `visualization-design-2026-10-06-v23/`에 있습니다. v1과 v22는 보존했습니다. `build.cjs`는 한 번만 실행하는 생성 도구이며 v23이 이미 있으면 중단합니다.

검사 명령:

```text
node simulation/pixel-v2-2026-10-06-v01/check.cjs
node simulation/pixel-v2-2026-10-06-v01/check-integration.cjs
node simulation/pixel-v2-2026-10-06-v01/check-roster.cjs
```

순수 확률 검사 13개, 기존 통합 검사 10개, 선수·이동 검사 10개를 통과했습니다. 애니메이션 1,081개 위치를 확인했고, 실제 mount 그리기 함수를 DOM 대역으로 호출해 시작·중간·끝에 22명이 그려지는지 검사했습니다. 실제 브라우저 렌더링과 참가자 확인은 아직 하지 않았습니다.

공개 계약: `MatchDeskSimulation.rosterPositions(progress, colors)`로 `{team,index,role,x,y,shirt}` 배열을 얻고, `drawRoster(ctx, players)`로 동일한 선수들을 그립니다. mount 내부도 이 함수를 그대로 사용합니다.
