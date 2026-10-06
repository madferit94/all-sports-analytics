from pathlib import Path
import re

out = Path(__file__).parent
prior = out.parent / 'visualization-design-2026-10-06-v07'
html = (prior / 'index.html').read_text(encoding='utf-8')
# Limit metadata styling to metric cards; keep provenance and filter scope visible.
for note in ['${esc(code)} · ${meta.unit}', '선택 ${ms.length}경기 합계', '원본 att 합 / def 합']:
    old = '<small>' + note + '</small>'
    assert old in html, note
    html = html.replace(old, '<small class="metric-note">' + note + '</small>')
anchor = '<div class="statfilters">'
assert html.count(anchor) == 1
html = html.replace(anchor, anchor + '<label class="metric-details-toggle"><input id="metricdetails" type="checkbox" aria-controls="snapshotstats teamcontent">지표 설명 보기</label>', 1)
css = '''<style id="metric-details-v08">
#team .metric-note{display:none}
#team.show-metric-details .metric-note{display:block}
.statfilters .metric-details-toggle{display:flex;align-items:center;gap:8px;font-size:13px;cursor:pointer}
.statfilters .metric-details-toggle input{width:18px;height:18px;min-width:18px;margin:0;accent-color:var(--navy,#182b40)}
.metric-details-toggle:focus-within{outline:2px solid #476f9f;outline-offset:4px;border-radius:4px}
</style>'''
html = html.replace('</head>', css + '</head>', 1)
js = "\nfunction syncMetricDetails(){ $('team').classList.toggle('show-metric-details',Boolean($('metricdetails').checked)); }\n$('metricdetails').onchange=syncMetricDetails;\nsyncMetricDetails();\n"
assert html.endswith('</script></body></html>\n') or html.endswith('</script></body></html>')
html = html.replace('</script></body></html>', js + '</script></body></html>')
(out / 'index.html').write_text(html, encoding='utf-8')
check = (prior / 'check.cjs').read_text(encoding='utf-8')
check = check.replace("this.classList={toggle(){}}", "this.checked=false;const classes=new Set();this.classList={toggle(name,on){if(on)classes.add(name);else classes.delete(name)},contains(name){return classes.has(name)}}")
extra = '''
test('metric explanations are off by default with scoped metadata styles',()=>{assert.strictEqual(get('metricdetails').checked,false);assert(!get('team').classList.contains('show-metric-details'));assert(html.includes('#team .metric-note{display:none}'));assert(get('snapshotstats').innerHTML.includes('class="metric-note"'));assert(html.includes('기간/장소/결과 필터 미적용'))});
test('explanation toggle changes visibility without altering metrics',()=>{const before=get('snapshotstats').innerHTML;get('metricdetails').checked=true;get('metricdetails').onchange();assert(get('team').classList.contains('show-metric-details'));assert.strictEqual(get('snapshotstats').innerHTML,before);get('metricdetails').checked=false;get('metricdetails').onchange();assert(!get('team').classList.contains('show-metric-details'))});
test('explanation preference survives metric filtering and retains percentage units',()=>{get('metricdetails').checked=true;get('metricdetails').onchange();get('metricsearch').value='PASS%';get('metricsearch').oninput();assert(get('team').classList.contains('show-metric-details'));assert(get('metricdetails').checked);assert(get('snapshotstats').innerHTML.match(/<strong>[^<]+%<\\/strong>/));get('metricdetails').checked=false;get('metricdetails').onchange()});
'''
check = check.replace("fs.writeFileSync(__dirname+'/logic-check.json'", extra + "\nfs.writeFileSync(__dirname+'/logic-check.json'")
(out / 'check.cjs').write_text(check, encoding='utf-8')
print('Built v08; v07 preserved.')
