from pathlib import Path
from datetime import datetime
import json,gzip,hashlib,math
ROOT=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text(encoding='utf8'))
maps=load(ROOT/'maps.json');manifest=load(ROOT/'source-manifest.json');season=load(ROOT.parent/'data/season-2026.json')
tests=[]
def check(name,condition):
    assert condition,name
    tests.append({'name':name,'passed':True})
epoch=lambda s:round(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1000)
source_rows={}
for entry in manifest:
    if not entry['file']:continue
    blob=gzip.decompress((ROOT/entry['file']).read_bytes())
    check('Original gzip hash '+entry['file'],hashlib.sha256(blob).hexdigest()==entry['sha256_uncompressed'])
    rows=json.loads(blob);check('Original row count '+entry['file'],len(rows)==entry['rows']);source_rows[entry['url']]=rows
expected={str(r['session']['session_key']) for r in season['races'] if r['state'] in ('completed','scheduled')}
check('All completed and scheduled GP maps present',set(maps['races'])==expected)
coverage=[]
for key,r in maps['races'].items():
    target=next(x for x in season['races'] if str(x['session']['session_key'])==key)
    check('Actual target circuit identity '+key,r['circuit_key']==target['session']['circuit_key'])
    reference=r.get('reference')
    if reference:
        raw=source_rows[reference['source_url']]
        xy={(row['x'],row['y']) for row in raw if reference['start_ms']<=epoch(row['date'])<=reference['end_ms']}
        check('Reference actual raw coordinates '+key,len(r['points'])>=100 and all(tuple(point) in xy for point in r['points']))
        check('No artificial reference closure '+key,not reference['closed_artificially'])
        if target['state']=='completed':
            pit_laps={v.get('lap_number') for v in target['records'].get('pit',[]) if v['driver_number']==reference['driver_number']}
            lap=next(v for v in target['records']['laps'] if v['driver_number']==reference['driver_number'] and v['lap_number']==reference['lap_number'])
            check('Reference excludes pit-in/out '+key,reference['lap_number'] not in pit_laps and not lap.get('is_pit_out_lap'))
    for num,d in r['drivers'].items():
        raw=source_rows[d['source']['url']];s=d['samples'];lookup={(epoch(row['date']),row['x'],row['y']) for row in raw}
        check('Sparse samples are original telemetry '+key+' '+num,all(tuple(point) in lookup for point in s))
        check('Sparse samples strictly time-sorted '+key+' '+num,all(s[i][0]>s[i-1][0] for i in range(1,len(s))))
        check('Session and driver original joins '+key+' '+num,all(row['session_key']==r['session_key'] and row['driver_number']==int(num) for row in raw))
        check('Sample time bounds '+key+' '+num,all(r['race_start_ms']-2400<t<r['race_end_ms']+2400 for t,x,y in s))
        original=sorted({epoch(row['date']) for row in raw if r['race_start_ms']-2400<epoch(row['date'])<r['race_end_ms']+2400})
        kept={point[0] for point in s}
        check('Original gap edges preserved '+key+' '+num,all(original[i-1] in kept and original[i] in kept for i in range(1,len(original)) if original[i]-original[i-1]>2000))
        check('Original first and last preserved '+key+' '+num,not original or original[0] in kept and original[-1] in kept)
    if target['state']=='scheduled':
        check('No upcoming observed drivers '+key,not r['drivers'])
        if reference:check('Earlier-year reference explicitly labelled '+key,r['reference_year']==2025 and r['reference_session_key']!=r['session_key'])
    coverage.append({'session_key':r['session_key'],'state':target['state'],'status':r['status'],'reference_points':len(r['points']),'observed_drivers':len(r['drivers']),'sparse_samples':sum(len(d['samples']) for d in r['drivers'].values())})
report={'producer_id':'root/f1_model','independent_review':False,'passed':len(tests),'failed':0,'coverage':coverage,'tests':tests}
(ROOT/'producer-check.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('MAP_CHECK_PASS',len(tests),json.dumps(coverage))
