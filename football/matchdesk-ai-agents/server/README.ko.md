# Gemini 연결과 로컬 실행

1. 프로젝트 최상위 `.env`의 `GEMINI_API_KEY=` 뒤에 Google AI Studio에서 발급한 키를 로컬로 입력합니다. 키를 채팅이나 GitHub에 보내지 않습니다. `.env`는 Git 제외 확인 완료이며 `.env.example`은 비어 있는 공개 양식입니다.
2. 프로젝트 폴더에서 `node --env-file=.env server/gemini.cjs`를 실행합니다. Windows에서는 `server/start.ps1`도 같은 명령을 실행합니다. Node 24에서 검사했으며 추가 패키지는 필요하지 않습니다.
3. `http://127.0.0.1:8765`를 엽니다. 한영 전환도 같은 서버를 사용합니다. `.env`를 바꾸면 서버를 재시작해야 합니다.

브라우저는 API 키를 읽거나 전달하지 않습니다. 질문·선택 조건·직전 조건을 같은 서버의 `/api/analyze`로 보내고, 서버가 Gemini에 질문과 공개 팀 목록만 전달합니다. 원본 경기 전체는 Google에 보내지 않습니다. Gemini의 `analyze_records` 도구 선택 조건을 엄격히 검사한 다음 서버 JavaScript가 실제 기록을 계산합니다. 모델이 직접 만든 수치는 표시하지 않습니다.

분석 방식에서 저장 기록 분석을 선택하면 이전 로컬 기능을 사용할 수 있습니다. file URL에서 Gemini를 선택하면 서버 주소로 열어야 한다고 안내합니다. 서버 화면의 설정됨은 키의 존재만 뜻하며 실제 인증/모델 권한 성공은 분석 호출 이후 확인됩니다.

기본 모델: `gemini-3.8-flash`, `.env`의 `GEMINI_MODEL`로 변경 가능. 2026-10-06 [공식 모델 목록](https://ai.google.dev/gemini-api/docs/models) 및 [도구 호출 REST 안내](https://ai.google.dev/gemini-api/docs/function-calling)를 확인했습니다. 계정별 실제 모델 접근·사용 한도는 라이브 호출로 확인해야 합니다.

로컬 서버는 127.0.0.1에만 연결합니다. 외부 배포용 인증·사용자별 한도·운영 설정은 이번 범위에 없습니다. SQL·Python 실행과 예측 모델은 여전히 미연결입니다. API 인증값은 [Google 공식 키 안내](https://ai.google.dev/gemini-api/docs/api-key)를 따릅니다.

검사: `node server/check.cjs`는 실제 로컬 HTTP와 가짜 Gemini 응답으로 12개 경로를 검증합니다. 실제 Gemini 호출 성공을 검증한 것으로 해석하지 않습니다.
