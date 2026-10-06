from pathlib import Path
import json,re
p=Path(__file__).resolve().parents[1];d=p/'visualization-design-2026-10-06-v17'
assert not d.exists();d.mkdir()
definitions={
 'npxg_for':[
  ['페널티 제외 기대 득점','페널티킥을 제외한 슈팅에서 기대되는 득점의 합계입니다. 실제 득점 수와는 다릅니다.','선택한 경기의 합계입니다. 경기 수가 같은 기간끼리 비교하고 실제 득점도 함께 보세요.'],
  ['Non-penalty expected goals','Sum of expected goals from shots excluding penalties; not actual goals scored.','Total across selected matches. Compare equal match counts and review actual goals alongside it.']],
 'npxg_against':[
  ['페널티 제외 기대 실점','상대가 페널티킥을 제외한 슈팅으로 만든 기대 득점의 합계입니다. 실제 실점 수와는 다릅니다.','상대에게 허용한 기회의 정도를 봅니다. 낮다고 다음 경기 무실점이 보장되지는 않습니다.'],
  ['Non-penalty expected goals against','Sum of opponents’ expected goals from shots excluding penalties; not actual goals conceded.','Measures chances allowed. A lower value does not guarantee a clean sheet in the next match.']],
 'expected_points':[
  ['기대 승점','경기에서 만든 기대 득점을 바탕으로 제공자가 계산한 승점 기대값입니다. 실제 승점이나 다음 경기 승리 확률이 아닙니다.','선택 경기의 기대값을 합산합니다. 실제 승점과 비교하되 미래 결과를 확정하는 값으로 읽지 마세요.'],
  ['Expected points','Provider estimate of points based on match expected goals. It is neither actual points nor the next match’s win probability.','Sum across selected matches. Compare with actual points without treating it as a guaranteed future result.']],
 'deep':[
  ['위험 지역 패스 성공 (Deep)','상대 골문 가까운 위험 지역에서 성공한 패스를 세는 제공자 지표입니다. 슈팅이나 득점 수가 아닙니다.','선택 경기 합계입니다. 지역 경계와 제외 조건의 공식 세부 정의는 추가 확인이 필요하며, 단독으로 공격력을 판단하지 마세요.'],
  ['Deep completions','Provider count of completed passes in dangerous areas near the opposition goal; not shots or goals.','Total across selected matches. Exact area boundaries and exclusions still need provider confirmation; avoid judging attack from this alone.']],
 'deep_allowed':[
  ['위험 지역 패스 허용 (Deep)','상대에게 허용한 골문 가까운 위험 지역 패스 성공 횟수입니다. 실점 수가 아닙니다.','선택 경기 합계입니다. 상대 전력과 경기 수를 함께 보세요. 지역 경계와 제외 조건의 공식 세부 정의는 추가 확인이 필요합니다.'],
  ['Deep completions allowed','Opposition completed passes in dangerous areas near your goal; not goals conceded.','Total across selected matches. Consider opponent quality and match counts. Exact area boundaries and exclusions still need provider confirmation.']],
 'ppda':[
  ['수비 행동당 허용 패스 (PPDA)','제공자의 상대 패스 수(att)를 수비 행동 수(def)로 나눈 비율입니다. 선택 경기의 분자·분모를 각각 합친 뒤 나눕니다.','일반적으로 낮을수록 상대 패스 사이에 수비 행동을 더 자주 한 것으로 읽습니다. 수비력 점수는 아니며 수비 행동이 0이면 계산하지 않습니다.'],
  ['Passes per defensive action (PPDA)','Ratio of provider opponent passes (att) to defensive actions (def). Selected-match components are summed before division.','Lower values generally mean defensive actions occur more frequently between opposition passes. This is not a defensive quality score; zero defensive actions produce no ratio.']]
}
for lang,name in [('ko','index.html'),('en','index.en.html')]:
 s=(p/'visualization-design-2026-10-06-v16'/name).read_text(encoding='utf8')
 meta={('detail:'+key):dict(zip(['label','description','reading'],vals[lang=='en'])) for key,vals in definitions.items()}
 s=s.replace('const metricReadingTips={','const detailMetricMeta='+json.dumps(meta,ensure_ascii=False)+';\nconst metricReadingTips={')
 s=s.replace('const meta=D.metric_meta[code];if(!meta)return;','const meta=detailMetricMeta[code]||D.metric_meta[code];if(!meta)return;')
 s=s.replace("$('metrichelpreading').textContent=metricReadingTips[code]||", "$('metrichelpreading').textContent=meta.reading||metricReadingTips[code]||")
 label='경기 보기 ↗' if lang=='ko' else 'Match ↗'
 title='Understat 경기 페이지 · 새 탭' if lang=='ko' else 'Understat match page · new tab'
 helper="function matchLink(m){return /^https:\\/\\/understat\\.com\\/match\\/\\d+$/.test(m.source||'')?`<a class=\"match-link\" href=\"${esc(m.source)}\" target=\"_blank\" rel=\"noopener noreferrer\" aria-label=\"${esc(T[m.home].name)} vs ${esc(T[m.away].name)}, ${m.date}: "+title+"\">"+label+"</a>`:''}\n"
 s=s.replace('function rows(id,ms){',helper+'function rows(id,ms){')
 s=s.replace('${esc(T[h?m.away:m.home].name)}<br>', '${teamName(h?m.away:m.home)}<br>')
 # All three completed-match lists receive a distinct match link below the date.
 s=s.replace('${m.date}</small></td>', '${m.date}</small>${matchLink(m)}</td>')
 s=s.replace("${h?'홈':'원정'}</small></td>","${h?'홈':'원정'}</small>${matchLink(m)}</td>")
 s=s.replace("${h?'Home':'Away'}</small></td>","${h?'Home':'Away'}</small>${matchLink(m)}</td>")
 start=s.index('function detailedMatchStats(');end=s.index('\n',start)
 total='선택 경기 합계' if lang=='ko' else 'Selected-match total'
 ppdaNote='PPDA · 합산 비율' if lang=='ko' else 'PPDA · aggregate ratio'
 heading='선택 경기 상세 지표' if lang=='ko' else 'Selected match statistics'
 function='''function detailMetricButton(key){const code='detail:'+key;return `<button type="button" class="metric-trigger" data-metric="${code}" aria-haspopup="dialog" aria-expanded="false" aria-controls="metricpopover">${esc(detailMetricMeta[code].label)}<span aria-hidden="true">ⓘ</span></button>`}
function detailedMatchStats(id,ms){const cards=['npxg_for','npxg_against','expected_points','deep','deep_allowed'].map(key=>{const v=sumDetail(id,ms,key);return `<div class="metriccard">${detailMetricButton(key)}<strong>${v===null?'—':v.toFixed(key.includes('deep')?0:2)}</strong><small class="metric-note">TOTAL</small></div>`});const att=sumDetail(id,ms,'ppda_att'),def=sumDetail(id,ms,'ppda_def'),ratio=att!==null&&def>0?att/def:null;cards.push(`<div class="metriccard">${detailMetricButton('ppda')}<strong>${ratio===null?'—':ratio.toFixed(2)}</strong><small class="metric-note">RATIO</small></div>`);return `<div class="scope"><h3>HEADING</h3></div><div class="metricgrid">${cards.join('')}</div>`}'''.replace('TOTAL',total).replace('RATIO',ppdaNote).replace('HEADING',heading)
 s=s[:start]+function+s[end:]
 s=s.replace('</style></head>','.match-link{display:block;width:fit-content;font-size:12px;line-height:1.4;padding:12px 4px;min-height:44px;box-sizing:border-box;color:inherit;opacity:.8}.match-link:focus-visible{outline:3px solid #a47700;outline-offset:2px}.metric-trigger{overflow-wrap:anywhere} </style></head>')
 (d/name).write_text(s,encoding='utf8');(p/name).write_text(s,encoding='utf8')
for name in ['check.cjs','check-en.cjs']:
 s=(p/'visualization-design-2026-10-06-v16'/name).read_text(encoding='utf8')
 s=s.replace("assert(!table.includes('target=\"_blank\"'));assert(!table.includes('href=\"https://understat.com'));", "assert(table.includes('class=\"match-link\"'));assert(table.includes('rel=\"noopener noreferrer\"'));assert(table.includes('data-team='));")
 (d/name).write_text(s,encoding='utf8')
print('Built v17 bilingual navigation and six detailed metric explanations.')
