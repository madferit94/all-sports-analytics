# MatchLab 0.12.2

요청: 사이트 이름 MatchLab 채택 및 지속되는 AI 분석관 호출 오류 해결.
관찰: 8765 서버 configured=true, gemini-3.8-flash. 분석 요청 provider_unavailable. 현재 .env를 읽는 별도 진단 서버에서 upstream HTTP200/function_call, 로컬 HTTP200. 결제/인증 실패로 확인되지 않음.
수정: 한영 제목·헤더 MatchLab. 원본 v33/previous-0.12.1 보존. 제공자 HTTP5xx에만 최대1회 재시도, 각25초 제한·750ms 대기. 인증/결제/한도/모델 오류 무재시도, 실패를 성공으로 표시하지 않음. 지원 분석 조건 검증·기록 계산 유지. 기존 환경설정 재시작으로 반영.
검증: 서버 실제 로컬HTTP+제공자 모의응답 검사, 재시도 성공/실패상한/한도 미재시도/비밀 미반환, 원본 데이터 및 예측값 동일성, 실제 사이트 및 현재 키 분석 호출 확인. 사용자 화면 확인 전.

实际 실행 결과: 서버검사16PASS/0FAIL, 한영JS구문 및 기록/641예측 불변PASS. 재시작후 실제 한국어 질문 HTTP200/status=ok/planner=Gemini. 본 수정은 로컬 반영이며 GitHub전송은 이번 단계에서 실행하지 않음.
