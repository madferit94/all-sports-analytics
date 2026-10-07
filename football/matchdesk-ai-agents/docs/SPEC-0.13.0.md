# MatchLab 0.13.0

축구/F1동일서버전환: 한영축구헤더→f1/index.html, F1→각언어축구. 허용된F1 index만서버제공,다른F1파일접근불가. 기존기록·확률·서버키보안불변.

개최지: GP브랜드/meeting_key/session_key/circuit_key/실제country분리. 25개meeting/session필드대조. 바레인1308/11731/12는공식F1확인으로Malaysia/Sepang표시,원본country=Bahrain은보존. 이전취소바레인1282/11261/63은Sakhir유지. 나머지개최지는OpenF1연결검사이며독립공식확인은미수행.

이전축구0.12.2 v34백업, F1v01보존·v02추가. 데이터수집이나모델재학습없음. 참가자확인전.

검증결과: 개최지분리/원본보존/취소Sakhir별도유지PASS. F1가상DOM34PASS,서버17PASS,한영구문·기록·641확률불변PASS. 동일서버두경로HTTP200. 실제브라우저배치·참가자확인전. 본수정GitHub미전송.
