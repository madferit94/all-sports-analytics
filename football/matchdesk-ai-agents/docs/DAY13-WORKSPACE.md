# Day13 작업 위치 / Workspace location

사용자 요청에 따라 2026-10-06에 MatchDesk 관련 전체 로컬 프로젝트를 day12에서 day13으로 이동했습니다. 코드·문서의 기존 0.8.0 공개 변경을 먼저 GitHub main에 머지했습니다.

- 이전: `day12/projects/ai-agent-planning-2026-10-06-v01/`
- 현재: `day13/projects/ai-agent-planning-2026-10-06-v01/`
- Git 저장소: 현재 프로젝트 안의 `github-workspace-2026-10-06-v01/`
- 사이트·서버: 저장소 안의 `football/matchdesk-ai-agents/`
- 사이트 실행 주소: `http://127.0.0.1:8765`

GitHub 저장소 내부의 `football/matchdesk-ai-agents` 경로는 유지합니다. day13은 로컬 수업 작업 폴더 분류입니다. 기존 날짜·버전 폴더명은 결과물 생성 이력을 보존하기 위해 유지합니다.

## 보존과 검증

이동 전후 2,417개 파일 수가 같고 .env 내용이 유지된 것을 해시 비교로 확인했습니다. 해시와 키는 기록하지 않습니다. 과거 화면·수집 자료·검증 기록·Git 이력·로컬 관리자 자료·키 파일을 같은 프로젝트 안에서 보존했습니다. 원본 수집 캐시와 .env는 Git 제외 정책을 유지하며 공개하지 않습니다.

이동 후 저장 경기 엔진 15개·서버 12개 재검사와 공개 파일 감사가 통과했습니다. 새 위치의 서버가 키 설정 상태로 실행됩니다. 추가 라이브 제공자 호출은 하지 않았습니다. 실제 AI 응답 성공·사용자 브라우저 확인과 API 결제/모델 접근 조건 확인은 별도입니다.

현재 실행 코드에는 day12 절대 경로 참조가 없습니다. 이전 모델 실행 JSON 안의 과거 경로는 당시 실행 근거이므로 바꾸지 않습니다. 루트 작업일지는 워크샵 최상위 작업일지.md 하나를 계속 사용합니다.

English: the complete local project moved to day13 after the existing publication merged to main. Internal GitHub paths are unchanged. File count and local configuration contents were preserved. Server/calculation checks and release audit passed at the new location; private caches and .env remain local.
