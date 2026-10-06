from pathlib import Path
import json
import re
from html import escape

out = Path(__file__).parent
prior = out.parent / 'visualization-design-2026-10-06-v10'
page = (prior / 'index.html').read_text(encoding='utf-8')
pattern = r'(<script id="data" type="application/json">)(.*?)(</script>)'
match = re.search(pattern, page, re.S)
data = json.loads(match[2])
admin_rows = []
for key, snap in data['snapshots'].items():
    team, season = key.split('|')
    admin_rows.append((data['teams'][team]['name'], season, snap.pop('observed', ''), snap.pop('source', '')))
page = page[:match.start(2)] + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + page[match.end(2):]
block = '<details><summary>출처·수집 시점</summary><div id="snapshotprovenance" class="note"></div></details>'
assert block in page
page = page.replace(block, '')
page = page.replace(',#snapshotprovenance', '')
page = page.replace("$('snapshotprovenance').textContent='';", '')
page, count = re.subn(r"\$\('snapshotprovenance'\)\.innerHTML=`.*?`;?", '', page)
assert count == 1
assert 'snapshotprovenance' not in page
(out / 'index.html').write_text(page, encoding='utf-8')
# Separate local file outside the repository; never linked from the visitor page.
base = out.parents[3]
admin_dir = base / 'local-admin-sources-2026-10-06-v01'
admin_dir.mkdir(exist_ok=True)
admin_path = admin_dir / 'sources-v11.html'
if admin_path.exists():
    raise FileExistsError('Preserve previous admin output; choose a new filename.')
rows = ''.join('<tr>' + ''.join('<td>' + escape(v) + '</td>' for v in (name, season, observed)) + '<td><a href="' + escape(url, quote=True) + '" target="_blank" rel="noopener">원본</a></td></tr>' for name, season, observed, url in sorted(admin_rows))
admin_path.write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>관리자 자료 확인</title><style>body{font:16px/1.6 system-ui;margin:24px;color:#24364a}table{border-collapse:collapse;width:100%}th,td{padding:12px;border-bottom:1px solid #dce4ed;text-align:left}.tablewrap{overflow:auto}</style><h1>자료 출처·수집 시점</h1><p>로컬 관리자 확인용 파일입니다. 로그인이나 접근 권한 검사가 연결된 웹 관리 화면은 아닙니다. 공개 페이지에서 연결하지 않습니다.</p><div class="tablewrap"><table><thead><tr><th>팀</th><th>시즌</th><th>수집 시점 (UTC)</th><th>출처</th></tr></thead><tbody>' + rows + '</tbody></table></div></html>', encoding='utf-8')
check = (prior / 'check.cjs').read_text(encoding='utf-8')
check = check.replace("assert(html.includes('출처·수집 시점'));", "assert(!html.includes('출처·수집 시점'));")
extra = '''
test('visitor page contains neither source panel nor snapshot provenance payload',()=>{assert(!html.includes('snapshotprovenance'));Object.values(data.snapshots).forEach(s=>{assert(!('source' in s));assert(!('observed' in s));assert(Object.keys(s.values).length>0)});assert(!html.includes('sources-v11.html'));assert(html.includes('metricpopover'))});
'''
check = check.replace("fs.writeFileSync(__dirname+'/logic-check.json'", extra + "\nfs.writeFileSync(__dirname+'/logic-check.json'")
(out / 'check.cjs').write_text(check, encoding='utf-8')
print(f'Built v11; {len(admin_rows)} source records moved to local admin file: {admin_path}')
