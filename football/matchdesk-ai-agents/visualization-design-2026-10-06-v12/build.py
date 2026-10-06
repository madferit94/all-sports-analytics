from pathlib import Path

out=Path(__file__).parent
prior=out.parent/'visualization-design-2026-10-06-v11'
page=(prior/'index.html').read_text(encoding='utf8')
old='<a href="${m.source}" target="_blank" rel="noopener">${esc(T[h?m.away:m.home].name)}<br><small class="muted">${m.date}</small></a>'
assert page.count(old)==1
page=page.replace(old,'${esc(T[h?m.away:m.home].name)}<br><small class="muted">${m.date}</small>')
old='<a href="${m.source}" target="_blank" rel="noopener" aria-label="${m.date} 원본 경기 보기">${f>a?\'승\':f===a?\'무\':\'패\'} ${f} : ${a}</a>'
assert page.count(old)==1
page=page.replace(old,"${f>a?'승':f===a?'무':'패'} ${f} : ${a}")
assert '${m.source}' not in page
(out/'index.html').write_text(page,encoding='utf8')
check=(prior/'check.cjs').read_text(encoding='utf8')
extra='''
test('numeric and history tables retain scores and dates without external match links',()=>{const id='understat:83';const games=data.completed.filter(m=>m.season==='2026/27'&&(m.home===id||m.away===id));context.testGames=games;for(const fn of ['rows','historyRows']){const table=run(fn+'("understat:83",testGames)');assert(table.includes(games[0].date));assert(table.includes(' : '));assert(!table.includes('target="_blank"'));assert(!table.includes('href="https://understat.com'));assert(table.includes('xG'))}assert(run('historyRows("understat:83",testGames)').includes('data-team='))});
'''
check=check.replace("fs.writeFileSync(__dirname+'/logic-check.json'",extra+"\nfs.writeFileSync(__dirname+'/logic-check.json'")
(out/'check.cjs').write_text(check,encoding='utf8')
print('Built v12; external match links removed, original numerical data unchanged.')
