from pathlib import Path
import json
import re

out = Path(__file__).parent
prior = out.parent / 'visualization-design-2026-10-06-v08'
page = (prior / 'index.html').read_text(encoding='utf-8')
pattern = r'(<script id="data" type="application/json">)(.*?)(</script>)'
match = re.search(pattern, page, re.S)
data = json.loads(match[2])
labels = json.loads((out / 'metric-language.ko.json').read_text(encoding='utf-8'))
assert set(labels) == set(data['metric_meta'])
for code, (label, description) in labels.items():
    data['metric_meta'][code].update(label=label, description=description)
page = page[:match.start(2)] + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + page[match.end(2):]
old = '<small class="metric-note">${esc(code)} · ${meta.unit}</small>'
assert old in page
page = page.replace(old, '<small class="metric-note">${esc(meta.description)}</small>')
old = 'meta.label.toLowerCase().includes(q)'
assert old in page
page = page.replace(old, old + '||meta.description.toLowerCase().includes(q)')
page = page.replace('placeholder="슈팅, 패스, xA…"', 'placeholder="슈팅, 패스, 페널티킥…"')
css = '''<style id="metric-language-v09">
#snapshotstats .metriccard{min-width:0;padding:18px}
#snapshotstats .metriccard>label{display:block;font-size:14px;line-height:1.5;color:#33465b;overflow-wrap:anywhere;min-height:42px}
#snapshotstats .metriccard>strong{display:block;font-variant-numeric:tabular-nums;line-height:1.3;margin:6px 0}
#snapshotstats .metric-note{font-size:13px;line-height:1.65;color:#506278;overflow-wrap:anywhere;margin-top:10px}
</style>'''
page = page.replace('</head>', css + '</head>', 1)
(out / 'index.html').write_text(page, encoding='utf-8')
check = (prior / 'check.cjs').read_text(encoding='utf-8')
extra = '''
test('every snapshot metric has a Korean name and plain-language explanation',()=>{assert.strictEqual(Object.keys(data.metric_meta).length,47);Object.entries(data.metric_meta).forEach(([code,m])=>{assert(/[가-힣]/.test(m.label));assert.notStrictEqual(m.label,code);assert(m.description.length>5)});assert.strictEqual(data.metric_meta.A.label,'도움');assert.strictEqual(data.metric_meta['TKL-LM'].label,'최종 수비 태클');assert.strictEqual(data.metric_meta.PKC.label,'페널티킥 허용');assert(data.metric_meta.PKC.description.includes('실점 수가 아닙니다'))});
test('plain explanations render instead of code and original-total metadata',()=>{get('metricsearch').value='';get('metricgroup').value='all';run('renderSnapshot()');const cards=get('snapshotstats').innerHTML;assert(cards.includes('최종 수비 태클'));assert(cards.includes('페널티킥 허용'));assert(!cards.includes('TKL-LM'));assert(!cards.includes('PKC'));assert(!cards.includes('원본 합계'));assert(cards.includes(data.metric_meta.PKC.description))});
test('Korean names, explanation words and legacy codes remain searchable',()=>{for(const query of ['페널티킥 허용','PKC','실점 수가 아닙니다']){get('metricsearch').value=query;run('renderSnapshot()');assert(get('snapshotstats').innerHTML.includes('페널티킥 허용'));assert(get('snapcount').textContent.includes('1 / 47'))}get('metricsearch').value='TKL-LM';run('renderSnapshot()');assert(get('snapshotstats').innerHTML.includes('최종 수비 태클'))});
'''
check = check.replace("fs.writeFileSync(__dirname+'/logic-check.json'", extra + "\nfs.writeFileSync(__dirname+'/logic-check.json'")
(out / 'check.cjs').write_text(check, encoding='utf-8')
# Only presentation metadata changes: verify every original data value survives.
old_data = json.loads(re.search(pattern, (prior / 'index.html').read_text(encoding='utf-8'), re.S)[2])
assert {k:v for k,v in old_data.items() if k != 'metric_meta'} == {k:v for k,v in data.items() if k != 'metric_meta'}
print('Built v09; all source data unchanged; 47 Korean labels and explanations.')
