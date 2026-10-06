# MatchDesk 0.8.0 · .env 기반 Gemini 연결

사용자 요청: .env 파일로 Gemini를 관리하고 연결 방법을 실행합니다.

- 로컬 `.env`를 빈 키로 생성하고 기존 `.gitignore` 제외를 확인합니다. 공개 `.env.example`은 빈 양식만 포함합니다. 기존 키 파일이 있으면 덮어쓰지 않습니다.
- Node 로컬 서버가 시작 시 `.env`를 읽고 Gemini Interactions REST에 한 번의 도구 선택을 요청합니다. 키는 요청 헤더에만 사용하며 HTML·응답·로그에 포함하지 않습니다.
- 한영 v19에서 저장 기록/Gemini 방식을 선택합니다. 서버 URL에서는 health 상태를 읽어 Gemini 모드를 선택합니다. 설정 상태와 실제 호출 성공을 구분합니다.
- 질문·팀/시즌 기본 조건·직전 조건·공개 팀 식별 목록을 전송합니다. 경기 원본 전체를 모델에 보내지 않습니다. 반환된 조건의 도구·팀·리그·시즌·최근 수·지표·자료형을 검증합니다. 코드 실행·임의 SQL을 허용하지 않습니다.
- 실제 수치는 기존 서버 JavaScript 도구로 계산합니다. 모델 자연어 숫자나 여러 도구 호출을 그대로 채택하지 않습니다. 예측은 미연결로 반환합니다.
- 빈 키·인증/한도·잘못된 응답·연결 실패를 분리하여 안내합니다. 외부 요청/Host를 제한하고 서버는 127.0.0.1만 바인딩합니다. 공개 정적 경로는 기본 한영 HTML만이며 .env/서버 소스는 제공하지 않습니다.
- 30초 제공자 시간 제한, 500자 질문/12KB 요청 제한, 동시에 한 요청·1초 최소 간격을 적용합니다. 서버는 로컬 사용용이며 인터넷 배포는 하지 않습니다.
- 통계 데이터는 기존과 동일합니다. SQL·Python·예측·모델 성능 개선은 포함하지 않습니다. Node 24 기본 기능만 사용합니다.

## 검증과 남은 확인

기존 분석 15개·한국어 48개·영어 23개와 서버 12개 = 98개 코드 검사 통과. 서버 검사는 실제 로컬 HTTP와 가짜 Gemini 제공자 응답입니다. 실제 API 키가 제공되지 않아 Google 인증·모델 호출 성공은 확인하지 못했습니다. 사용자 키 설정과 라이브 요청 확인이 남아 있습니다. 실제 브라우저 배치와 참가자 확인도 아직입니다.

## English

Local Node server loads ignored .env and calls Gemini to select one validated analysis tool. Server JavaScript calculates recorded statistics. API keys stay server-side; static routes cannot serve .env. Bilingual v19 adds async same-origin Gemini mode with explicit configuration/error states. 98 code checks passed, including mocked-provider HTTP tests; live Gemini verification awaits a user-supplied key. Local serving is not external hosting.

[설정 안내](../server/README.ko.md) · [공식 도구 호출](https://ai.google.dev/gemini-api/docs/function-calling) · [공식 모델 목록](https://ai.google.dev/gemini-api/docs/models)

## 명칭과 제공자 오류 처리

방문자 표시 명칭은 AI 분석관/AI analyst입니다. 제공자 HTTP402(결제 관련)·404(모델 사용 불가)를 앱에서 따로 안내합니다. 계정별 인증·모델 접근·결제 상태는 사용자 환경에서 확인하며 실제 성공과 가짜 응답 검증을 구분합니다.
