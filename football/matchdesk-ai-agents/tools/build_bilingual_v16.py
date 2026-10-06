"""Build preserved Korean/English viewers from v15 without altering statistics."""
from pathlib import Path
import json,re
p=Path(__file__).resolve().parents[1]
d=p/'visualization-design-2026-10-06-v16'
assert not d.exists() or not any(d.iterdir()), 'Preserve existing version'
d.mkdir(exist_ok=True)
s=(p/'visualization-design-2026-10-06-v15/index.html').read_text(encoding='utf8')
switch='<div class="language-switch" aria-label="Language"><a id="language-ko" href="index.html" lang="ko" hreflang="ko">한국어</a><a id="language-en" href="index.en.html" lang="en" hreflang="en">English</a></div>'
s=s.replace('</nav></header>','</nav>'+switch+'</header>')
s=s.replace('</style></head>',' .language-switch{display:flex;gap:8px;flex-wrap:wrap}.language-switch a{color:#fff9e7;padding:8px;border:2px solid #fff9e7;text-decoration:none;font-size:14px}.language-switch a[aria-current]{background:#ffe08a;color:#182b3b}.language-switch a:focus-visible{outline:3px solid #ffe08a;outline-offset:3px}header{flex-wrap:wrap} </style></head>')
extra="""
function syncLanguageLinks(){
 ['ko','en'].forEach(lang=>{
  const link=$('language-'+lang);
  link.setAttribute('href',(lang==='en'?'index.en.html':'index.html')+window.location.hash);
 });
}
syncLanguageLinks();window.addEventListener('hashchange',syncLanguageLinks);
"""
# Keep the existing hash handler: register language sync within it rather than a second stub handler.
s=s.replace("window.addEventListener('hashchange',readTeamHash)","window.addEventListener('hashchange',()=>{readTeamHash();syncLanguageLinks()})")
extra=extra.replace(";window.addEventListener('hashchange',syncLanguageLinks)",'')
s=s.replace('</script>\n</body>',extra+'</script>\n</body>') if '</script>\n</body>' in s else s.rsplit('</script>',1)[0]+extra+'</script>'+s.rsplit('</script>',1)[1]
s=s.replace('id="language-ko" href=', 'id="language-ko" aria-current="page" href=')
rx=r'(<script id="data" type="application/json">)(.*?)(</script>)'
match=re.search(rx,s,re.S);data=json.loads(match[2])
assert {k:sum(t['league']==k for t in data['teams'].values()) for k in ['EPL','La_liga']}=={'EPL':27,'La_liga':29}
translations={
 'AI 경기 분석실':'AI Football Analysis Room','경기 분석실':'Football Analysis Room',
 '오늘의 축구 분석실':'Your Football Clubhouse','팀을 고르고, 기록을 탐험해 보세요.':'Pick a club. Explore its story.',
 '주 메뉴':'Main navigation','다가오는 경기':'Upcoming matches','자료 기준':'Data through',
 '프리미어리그':'Premier League','라리가':'LaLiga','최근 전력 비교':'Recent form comparison','최근 리그 5경기':'Last 5 league matches',
 '기대 득점 흐름':'Expected goals trend','팀 이름 검색':'Search club names','팀 이름':'Club name','팀 검색':'Search clubs','팀 목록':'Club list',
 '시즌 전체':'Full season','최근 5경기':'Last 5 matches','최근 10경기':'Last 10 matches','날짜 선택':'Custom dates','경기 범위':'Match range',
 '시즌 상세 통계':'Season statistics','기간/장소/결과 필터 미적용':'Date, venue and result filters do not apply','전체 지표':'All metrics',
 '패스·점유':'Passing & possession','수비·골키핑':'Defence & goalkeeping','반칙·징계':'Fouls & discipline','슈팅, 패스, 페널티킥…':'Shots, passes, penalties…','지표 검색':'Search metrics',
 '승점순 통계':'Table by points','저장 자료 기반 미리보기 · 경기 날짜는 원본 표기 · 구단 로고: StatMuse · 시즌 기록은 수집 리그 범위':'Stored dataset · Dates as listed by providers · Club logos: StatMuse · Records cover the selected leagues',
 '지표 설명 닫기':'Close metric explanation','읽는 법':'How to read it',
 '수가 많다고 곧바로 공격력이 나쁘다는 뜻은 아닙니다. 공을 다룬 횟수와 패스 시도, 경기 수도 함께 보세요.':'A high count alone does not mean poor attacking play. Compare touches, pass attempts and matches played.',
 '득점·실점이 아니라 상대에게 준 기회의 횟수입니다. 실제 페널티킥 실점과 구분해서 보세요.':'Counts penalties awarded to opponents, not goals conceded. Keep it separate from penalty goals conceded.',
 '위기 상황의 수비 기록입니다. 많다는 이유만으로 전체 수비가 좋다고 판단하지 마세요.':'Records tackles in dangerous situations. A high count alone does not establish overall defensive quality.',
 '패스가 얼마나 잘 연결됐는지 보여줍니다. 패스 거리와 공격 지역 패스도 함께 보세요.':'Shows how often passes reach teammates. Also consider passing distance and passes in the attacking third.',
 '공을 오래 소유한 정도입니다. 점유율만으로 승리나 좋은 득점 기회를 판단할 수는 없습니다.':'Measures possession share. Possession alone does not establish wins or the quality of scoring chances.',
 '실제 도움과 비교할 수 있는 참고값입니다. 이 숫자만으로 다음 경기 도움 수를 확정할 수는 없습니다.':'Compare with actual assists. This value does not guarantee assists in the next match.',
 '공격·수비 방향의 원본 정의가 확인되기 전에는 수비력 평가에 사용하지 마세요.':'Do not use this for defensive evaluation until the provider confirms whether it refers to attacking or defensive actions.',
 '같은 리그와 기간의 비율을 비교해 보세요. 이 지표 하나만으로 팀의 전체 경기력을 판단하지 마세요.':'Compare rates within the same league and period. Avoid judging overall performance from one metric.',
 '경기당 평균입니다. 시즌 누적 횟수와 구분해 비교해 보세요.':'This is a per-match average. Keep it separate from season totals.',
 '시즌 전체 누적값입니다. 경기 수가 다르면 같은 기간이나 경기당 값으로 비교해 보세요.':'This is a season total. When match counts differ, compare equivalent periods or per-match values.',
 '종합 정보 보기':'view club profile','최근 경기 결과':'Recent results','예정 경기 없음':'No scheduled matches',
 '양 팀 최근 리그 경기 기대 득점, 상세 수치는 표에 표시':'Recent league xG for both clubs; exact values in the table',
 '같은 경기 순서로 비교 · xG: 기회의 득점 기대치':'Compared by match order · xG: expected goals from chances','이전 경기':'Earlier','수치 보기':'View numbers',
 '날짜 / 상대':'Date / opponent','상대 xG':'Opponent xG','선택 조건 · 최근':'Filtered · Last',
 '선택 시즌의 기록 없음':'No records for this season','저장된 예정 경기 없음':'No stored upcoming matches','리그 일정 · 원본 날짜':'league schedule · provider dates',
 '선택 경기 공격·수비':'Attack & defence in selected matches','최근 성적':'Recent record','다음 경기':'Next matches','승률':'Win rate',
 '경기당 평균':'Per-match average','최근 기대 득점':'Recent expected goals','최근 경기 기대 득점, 실제 값은 최근 경기 표에 표시':'Recent xG; exact values in the recent matches table',
 '검색 결과 없음':'No clubs found','시작 날짜는 종료 날짜보다 앞서야 합니다.':'Start date must be on or before end date.',
 '선택 기간':'Selected dates','전체 장소':'All venues','전체 결과':'All results',
 '페널티 제외 기대 득점':'Non-penalty expected goals','페널티 제외 기대 실점':'Non-penalty expected goals against',
 'Deep 허용 (원본 지표)':'Deep allowed (provider metric)','Deep (원본 지표)':'Deep (provider metric)','기대 승점':'Expected points',
 '선택 경기 상세 지표':'Selected match statistics','PPDA · 합산 비율':'PPDA · aggregate ratio','원본 att 합 / def 합':'Sum of provider att / sum of def',
 '해당 팀·시즌의 상세 자료 없음':'No detailed data for this club and season','자료 없음':'No data','선택 조건의 지표 없음':'No metrics match these filters',
 '팀 종합 정보':'Club profile','선택 조건의 리그 자료가 없습니다.':'No league data match these filters.',
 '시즌별 기록 · 전체 경기':'Season history · all matches','시즌별 경기당 승점, 상세 수치는 아래 표에 표시':'Points per match by season; exact values below',
 '시즌별 기록':'Season history','경기 기록 보기':'view match records','경기 기록':'Match history','2026/27은 진행 중 · 자료 없는 시즌은 — 표시':'2026/27 is in progress · Missing seasons shown as —',
 '선택 조건의 경기가 없습니다.':'No matches meet these filters.','경기 결과 집계 · 징계에 따른 승점 조정 미반영':'Calculated from results · Disciplinary points adjustments are not included',
 '리그 현황':'League table','경기당 기대 득점':'xG per match','경기당 득점':'Goals per match','경기당 실점':'Goals conceded per match','경기당 승점':'Points per match','경기당 xG':'xG per match',
 '기대 득점':'Expected goals','기대 실점':'Expected goals against','득점 / 실점':'Goals for / against','승 / 무 / 패':'W / D / L','승·무·패':'W · D · L','득실점':'GF:GA','득실':'GD',
 '최근 경기':'Recent matches','원본 합계':'Season total','경기당':'Per match',
 '승점':'Points','득점':'Goals for','실점':'Goals against','무승부':'Draw','승리':'Win','패배':'Loss','분석':'Analyse','상대':'Opponent','장소':'Venue','결과':'Result','시즌':'Season','시작':'Start','종료':'End','지표':'Metrics','공격':'Attack','경합':'Duels','전체':'All','선택':'Selected','합계':'total','리그':'League','경기':' matches','팀':'Clubs','홈':'Home','원정':'Away','승':'W','무':'D','패':'L','최근':'Last'
}
def translate(text):
 for ko,en in sorted(translations.items(),key=lambda item:-len(item[0])):text=text.replace(ko,en)
 return text
metrics={
 'A':('Assists','Final passes directly leading to goals.'),
 'xA':('Expected assists','Estimated likelihood that a pass becomes an assist.'),
 'POSS%':('Possession','Share of possession, expressed as a percentage.'),
 'PK':('Penalty goals','Goals scored from penalties.'),
 'FK':('Free-kick goals','Goals scored directly from free kicks.'),
 'SH':('Shots','Total shot attempts.'),'SOT':('Shots on target','Shots directed on target.'),
 'TCH':('Touches','Recorded touches of the ball.'),'TCH-BOX':('Touches in opponent box','Touches inside the opposition penalty area.'),
 'OFF':('Offsides','Recorded offside offences.'),'PASS':('Accurate passes','Passes successfully completed to teammates.'),
 'PASS/M':('Accurate passes per match','Accurate passes divided by matches played.'),'PASS%':('Pass accuracy','Accurate passes as a percentage of pass attempts.'),
 'PASS-ATT':('Pass attempts','Total attempted passes, including incomplete passes.'),
 'BCC':('Big chances created','Passes creating chances classified as big chances by the provider.'),
 'PASS-KEY':('Key passes','Final passes before shots that do not result in goals.'),
 'PASS-LNG':('Long passes','Passes longer than 35 yards. This count alone does not establish completion.'),
 'PASS-F3RD':('Passes in attacking third','Passes made in the attacking third; not necessarily entries into that area.'),
 'THRU-BALL':('Through balls','Successful passes splitting the defensive line for a teammate.'),
 'CRS':('Crosses','Crosses delivered from wide positions.'),'CNR':('Corners','Corner kicks taken.'),
 'TKL':('Tackle attempts','Attempted tackles, including unsuccessful attempts.'),'TKL-W':('Tackles won','Successful tackles winning the ball.'),
 'TKL-LM':('Last-man tackles','Tackles by the last defender to prevent an opponent breaking through.'),
 'SH-BLK':('Shots blocked','Provider blocked-shot count. Its attacking or defensive direction remains unconfirmed.'),
 'BLK-CRS':('Crosses blocked','Opposition crosses blocked.'),'INT':('Interceptions','Opposition passes intercepted.'),
 'CLR':('Clearances','Actions clearing the ball from danger.'),'REC':('Loose-ball recoveries','Recoveries of loose balls.'),
 'ERR-SH':('Errors leading to shots','Errors directly leading to opposition shots.'),'ERR-G':('Errors leading to goals','Errors directly leading to opposition goals.'),
 'PKC':('Penalties conceded','Penalties awarded to opponents. This is not the number of goals conceded.'),
 'OG':('Own goals','Goals scored into the club’s own net.'),'SV':('Saves','Goalkeeper saves.'),'SV-PK':('Penalties saved','Penalty kicks saved by the goalkeeper.'),
 'CS':('Clean sheets','Matches without conceding a goal.'),'YC':('Yellow cards','Yellow cards received.'),'RC':('Red cards','Red cards received.'),
 'FOUL':('Fouls committed','Fouls committed against opponents.'),'FOULED':('Fouls won','Fouls suffered from opponents.'),
 'PK-W':('Penalties won','Penalties awarded to the club.'),'CNR-W':('Corners won','Corner kicks won by the club.'),
 'AER-W':('Aerial duels won','Contests for aerial balls won.'),'AER-L':('Aerial duels lost','Contests for aerial balls lost.'),
 'DUEL-W':('Duels won','Contested-ball duels won.'),'DUEL-L':('Duels lost','Contested-ball duels lost.'),
 'POSS-L':('Possessions lost','Recorded losses of possession, including unsuccessful passes and other turnovers.')
}
assert set(metrics)==set(data['metric_meta'])
en_data=json.loads(json.dumps(data))
for code,meta in en_data['metric_meta'].items():
 meta['label'],meta['description']=metrics[code];meta['unit']=translate(meta['unit'])
body=s[:match.start(2)]+'__PAYLOAD__'+s[match.end(2):]
en=translate(body).replace('<html lang="ko">','<html lang="en">')
en=en.replace('id="language-ko" aria-current="page"','id="language-ko"').replace('id="language-en" href=','id="language-en" aria-current="page" href=')
# Keep native-language navigation intentionally visible on the English edition.
en=en.replace('>한국어</a>','>한국어</a>')
en=en.replace('> matches<','>Matches<').replace('>Clubs<','>Teams<').replace("+'Metrics'","+' metrics'")
en=en.replace('__PAYLOAD__',json.dumps(en_data,ensure_ascii=False,separators=(',',':')))
remaining=re.findall(r'[^\n]*[가-힣][^\n]*',re.sub(rx,'',en,flags=re.S).replace('한국어',''))
assert not remaining, json.dumps(remaining,ensure_ascii=True)
for name,content in [('index.html',s),('index.en.html',en)]:
 (d/name).write_text(content,encoding='utf8');(p/name).write_text(content,encoding='utf8')
(d/'ui-translations.en.json').write_text(json.dumps(translations,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(d/'metric-language.en.json').write_text(json.dumps(en_data['metric_meta'],ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(d/'check.cjs').write_bytes((p/'visualization-design-2026-10-06-v15/check.cjs').read_bytes())
print('Built v16: Korean + English, 27 EPL and 29 LaLiga clubs, 47 metric definitions.')
