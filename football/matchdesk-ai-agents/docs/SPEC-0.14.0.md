# MatchLab 0.14.0 · F1 기록 시뮬레이션·미래 예측

요청: 중단작업복구,종료GP시뮬레이션·예정GP지표예측.
복구:0.13.0메뉴/세팡표시파일은존재,서버2개꺼짐·마지막문서/manifest갱신중단. 기존W작업일지에보강.
저장5인팀skill/protocol:root조정및UI통합,f1_replay builder,f1_model analyst/research,f1_verifier독립reviewer. 최종별도 f1_director 검토,자가검사를독립승인으로부르지않음.
종료16GP:22차량/유효랩시작·종료시각보간,DNF/DNS/결측/피트/타이어/공식최종순위. 재생/일시정지/속도/탐색/정리. OpenF1location16요청HTTP404로실제GPS없음;도식주행이라고표시하고실제추월·주행라인이라주장하지않음.
예정7GP:과거완료경기지표학습,최근드라이버명단예상22인. 미래실제명단미발표·예선/그리드미확보를숨기지않음. 과거2025추가·현재2026종료자료,시간순홀드아웃·기준선비교·최종모델refit분리. 훈련labelmissing 행은패자로추정하지않음. 시점누수검사필수.
예정GP공식예측성능보장없음. 취소2GP확률·시뮬레이션없음. GP명과실제서킷분리/세팡key12유지.
UI:종료처음재생탭/예정처음예측탭,한영·종목전환·같은8765서버. 이전8766주소는현재F1으로넘겨원래racefragment유지.
이전축구0.13.0v35백업/F1v01-v02보존,v03새파일. 원본2026기록/축구641예측불변. 참가자확인전. GitHub전송은이번요청에포함되지않음.

## Final evidence
- Independent reviewer: 618 assertions (data16/model156/timeline101/mount208/UI137), separate from producers.
- Actual browser: replay starts/clock progresses/22 rows; scheduled forecast22 rows; Korean/English and Football link verified. User verification pending.
- Win top1 2/6; log loss 3.1194645291 vs uniform3.0910424534/recent-win2.9699472885. Experimental, not improved accuracy claim.
- Final future predictions refit35 historical races after holding out6 for evaluation; feature source end strictly before target start. Actual historical entry-publication times not established.
- All16 coordinate API requests404; schematic replay does not reconstruct actual GPS or overtakes.
- GP1308 Bahrain branding/actual Sepang Malaysia venue preserved separately; other venues joined but not all independently officially verified.
- Local server8765 active, legacy8766 redirects with hash. No GitHub upload in this task.

## Browser regression resolved
Actual browser range End initially stopped before fractional duration. Changed step to any and finished-aware row caching; independent tests rerun. Actual browser now reaches max4885.787, shows 종료/FINISH and official final classification.
