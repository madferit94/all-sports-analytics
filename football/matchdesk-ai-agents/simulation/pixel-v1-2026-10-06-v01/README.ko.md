# 8비트 시뮬레이션 v1

담당: 통합 팀 builder 역할. 실제 실행 주체: Codex 하위 에이전트 `/root/pixel_simulation`. `matchdesk-builder` 스킬과 통합 팀 규칙을 읽고 적용했습니다.

`pixel-simulation.js`는 외부 의존성이 없는 Canvas 애니메이션입니다. 화면에 표시하는 승무패 확률은 예측 담당이 제출한 숫자만 사용합니다. 제공된 확률의 합계가 1인지 검증합니다. 확률에서 한 가지 결과를 추출해 18초 길이의 가상 경기 움직임으로 표현합니다. 실제 경기 영상·예상 선발·실제 슛 좌표 재현은 아닙니다.

현재 모델은 점수 분포를 제공하지 않으므로 화면 점수는 홈 승 1:0, 무승부 1:1, 원정 승 0:1의 연출용 점수입니다. 이 점수는 모델이 예측한 정확한 점수가 아닙니다. 표시는 그 사실을 항상 설명합니다. 결과별 확률은 가상 경기에서 뽑힌 결과와 별도로 모두 표시됩니다.

재생, 일시정지, 새 시뮬레이션 버튼을 제공합니다. 운영체제의 움직임 줄이기 설정이 켜지면 애니메이션 없이 가상 결과를 표시합니다. 동영상 파일 내보내기(WebM/MP4)는 구현하지 않았습니다.

## 연결

```js
const instance = MatchDeskSimulation.mount(container, {
  model: modelResult.model_id,
  status: modelResult.status,
  home: modelResult.home_team,
  away: modelResult.away_team,
  probabilities: [
    modelResult.probabilities.home,
    modelResult.probabilities.draw,
    modelResult.probabilities.away
  ]
}, { locale: 'ko', homeColor: '#cf3340', awayColor: '#4779d5' });
// 다른 경기나 페이지로 이동할 때 실행합니다.
instance.destroy();
```

향후 `scoreDistribution: [{home,away,probability}]`를 추가할 수 있습니다. 각 승무패 영역의 합계가 입력 확률과 일치해야 합니다. 점수 범위는 0–12골입니다. 테스트의 고정 확률은 테스트 전용이며 사용자 화면 데이터에 사용하지 않습니다.

`integration.js`는 현재 경기 선택 정보를 실제 예측 행의 경기 키, 홈·원정 팀 키, 리그, 날짜와 대조합니다. 불일치나 미준비 시 확률을 만들어 넣지 않고 안내를 표시합니다. `renderMatches`와 `render` 후에 선택 경기에 맞게 갱신하고 페이지를 떠나면 애니메이션을 정리합니다.

`build.cjs`는 기존 v21을 보존하고 새 v22 스냅샷을 만든 뒤 한국어·영어 기본 화면에 JS/CSS/미래 경기 641개의 예측을 넣습니다. 이미 v22가 있으면 중단하므로 반복 실행하지 않습니다. 배포 서버는 HTML만 제공하므로 브라우저에서 별도 원시 데이터 파일을 읽지 않습니다. 모델 원시 학습 데이터·키는 포함하지 않습니다.

## 검증

`node simulation/pixel-v1-2026-10-06-v01/check.cjs`: 순수 함수 검사 13개.

`node simulation/pixel-v1-2026-10-06-v01/check-integration.cjs`: 한영 예측 641행 식별/확률 대조, 스크립트 문법, 스냅샷 동일성, DOM 대역으로 재생·정지·정리·움직임 줄이기 검사. 실제 브라우저 렌더링 검증과 구분합니다.

실제 브라우저 화면과 참가자 확인은 아직 하지 않았습니다. 확률 모델의 정확성·채택 여부는 analyst/reviewer 담당의 별도 판단입니다.
