# v06 독립 검증 실행 전 기대값
검사주체 /root/f1_verifier. verification-evidence 및 reviewer기존지침적용,production수정금지.
범위: 선택드라이버중심정보와전체차량표시정책,시각별실제지표/차트.
- v05원본경기·지도·회고및예정예측바이트불변.
- 기본모든22차량표시·동일가독성; 선택드라이버정보별도. pausedsingle허용,재생클릭시전체자동복귀. 선택드라이버변경시정보업데이트.
- completedlap.date_start+duration<=cursor,position.date<=cursor,pit.date<=cursor 및레이스전pit제외. 마지막완료랩만시각별실제값. 미래/최종정답을진행차트로사용금지.
- 실제pit_duration과lane_duration/stop_duration별도뜻,결측0변환금지. 예측미래GP는실제지표미제공또는해당없음정직표시.
- 0/중간/끝·pit경계·랩완료경계·futureinjection 격리검사,한영/cleanup/unknownmap.
- 실제브라우저root근거별도,참가자확인전. 이전v05검사를전체새기능인증으로확대하지않음.

상위추가확정: pit진입date<=cursor는입장횟수만. lane총시간값은date+lane_duration<=cursor이후완료값으로표시. 진입중에는총28초같은사후소요값누출금지. 진입/완료구분및lane vs정차stop뜻구분필수.
