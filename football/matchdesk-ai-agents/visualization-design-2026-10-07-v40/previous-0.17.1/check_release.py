"""Check release links, payload identity and manifest; optionally refresh hashes."""
from pathlib import Path
import hashlib,json,re,subprocess,sys

p=Path(__file__).resolve().parents[1]
repo=p.parents[1]
prefix=p.relative_to(repo).as_posix()+'/'
tracked=subprocess.check_output(['git','ls-files','-z','--',prefix],cwd=repo).decode().split('\0')
extra=subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z','--',prefix],cwd=repo).decode().split('\0')
files=sorted(set(x for x in tracked+extra if x and (repo/x).is_file()))
patterns=[re.compile(rb'gh[pousr]_[A-Za-z0-9]{30,}'),re.compile(rb'github_pat_[A-Za-z0-9_]{30,}'),re.compile(rb'AIza[A-Za-z0-9_-]{30,}'),re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')]
for f in files:
    path=Path(f)
    assert not any(part in {'private','raw','.env','__pycache__'} for part in path.parts), f'Excluded file: {f}'
    blob=(repo/f).read_bytes()
    assert not any(rx.search(blob) for rx in patterns), f'Credential-like content in {f}'
    assert (repo/f).stat().st_size<95*1024*1024, f'Oversize file: {f}'
link_docs=[repo/'README.md',repo/'README.ko.md',p/'README.md',p/'README.ko.md',p/'docs/SPEC-0.17.1.md']
links=0
for doc in link_docs:
    for target in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf8')):
        if '://' in target or target.startswith('#'): continue
        if doc.parent==repo and not target.startswith(prefix): continue
        assert (doc.parent/target.split('#')[0]).exists(), f'Missing link in {doc.name}: {target}'
        links+=1
def payload(version):
    html=(p/f'visualization-design-2026-10-06-{version}/index.html').read_text(encoding='utf8')
    return json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>',html,re.S)[1])
assert all(payload(f'v{n}')==payload('v12') for n in range(13,24)), 'Design preview changed source data'
assert (p/'index.html').read_bytes()==(p/'visualization-design-2026-10-07-v39/index.html').read_bytes(), 'Default entry differs from adopted v38'

en_html=(p/'index.en.html').read_text(encoding='utf8')
assert (p/'index.en.html').read_bytes()==(p/'visualization-design-2026-10-07-v39/index.en.html').read_bytes()
english=json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>',en_html,re.S)[1])
korean=payload('v23')
for key in korean:
    if key!='metric_meta': assert korean[key]==english[key], f'English data drift: {key}'
assert len(english['metric_meta'])==47
# The simulation contains a shared bilingual module. Verify its exact source
# identity before excluding that code from the static English-label check;
# dynamic English rendering is covered by the simulation integration checks.
english_labels=re.sub(r'<script id="data" type="application/json">.*?</script>','',en_html,flags=re.S)
for module in ('pixel-simulation.js','integration.js'):
    shared=(p/'simulation/pixel-v2-2026-10-06-v01'/module).read_text(encoding='utf8').strip()
    assert shared in english_labels, f'Shared module differs: {module}'
    english_labels=english_labels.replace(shared,'')
for module in ('team-chart-engine.cjs','team-chart-ui.js'):
    shared=(p/'visualization-design-2026-10-07-v31'/module).read_text(encoding='utf8')
    assert shared in english_labels, f'Chart module differs: {module}'
    english_labels=english_labels.replace(shared,'')
assert not re.search('[가-힣]',english_labels.replace('한국어',''))

old=json.loads((p/'docs/publication_manifest-0.9.0.json').read_text(encoding='utf8'))
labels={item['path']:item['snapshot'] for item in old['files']}
old_hashes={item['path']:item['sha256'] for item in old['files']}
text_ext={'.md','.json','.py','.cjs','.js','.css','.ps1','.example','.html','.txt','.yaml','.yml','.csv','.gitattributes','.gitignore'}
entries=[]
for f in files:
    relative=Path(f).relative_to(p.relative_to(repo)).as_posix()
    if relative=='publication_manifest.json': continue
    b=(repo/f).read_bytes()
    if Path(relative).suffix in text_ext or Path(relative).name in {'.gitignore','.gitattributes','VERSION'}:
        b=b.replace(b'\r\n',b'\n')
    digest=hashlib.sha256(b).hexdigest()
    snapshot=labels[relative] if old_hashes.get(relative)==digest else '0.17.1'
    entries.append(dict(path=relative,bytes=len(b),sha256=digest,snapshot=snapshot))
manifest=dict(version='0.17.1',public_export=True,files=entries,display_dataset=dict(completed=2399,scheduled=641,team_match_rows=4798,season_snapshots=160,metrics=47),csv_demo=dict(completed=20,scheduled=2),published_model_evidence=['prematch-v2 features, model weights, metrics and future probabilities','prior-rank ablation and independent review'],excluded=['full provider caches','complete source modeling CSV','ignored baseline generated runs','local administrator source report','credentials','workshop materials','root personal work journal'],text_hash_encoding='UTF-8 with LF line endings, matching published blob contents')
if '--write-manifest' in sys.argv:
    (p/'publication_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
else:
    actual=json.loads((p/'publication_manifest.json').read_text(encoding='utf8'))
    assert actual==manifest,'Manifest differs from current release files'
print(f'PASS release audit: {len(entries)} hashed files, {links} local documentation links; design payloads identical; no private/admin files or credential-pattern matches.')

