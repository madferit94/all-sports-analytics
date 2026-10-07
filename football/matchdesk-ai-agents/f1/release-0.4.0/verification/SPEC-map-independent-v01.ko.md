# v05 지도 비교 독립 검증 기대값

reviewer /root/f1_verifier, 2026-10-07. v05 verification/만 수정. 저장 reviewer skill/protocol·verification-evidence 앞 단계에서 읽은 지침 적용.
1. v04 모델·예측·경기자료 보존, 지도/GPS는 경기후비교용이며예측입력으로사용하지않음.
2. 위치수집원본·manifest해시,원본xy/epochms→다운샘플자료참조검사.16GP2명GPS목표는실제수집성공범위만PASS.결측실패를숨기지않음.
3. GPS샘플시간범위/정렬/동일driver key,좌표유한,보간간격<=2초.더큰공백에서경로복원/결측임을명시.
4. 실제GPS2명·나머지랩기반경로재구성의범례및한영표시구분,22마커·시간이동·종료·취소해제·unknownmap안전처리.
5. 실제원본xy트랙과맵데이터사용. 최종HTMLpayload저장자료동일·최신JS·모바일overflow실브라우저root근거별도.
6. 준비전산출물은NOT_READY,전체기존모델을재인증하지않고v05증분범위만판정. 참가자확인전.
