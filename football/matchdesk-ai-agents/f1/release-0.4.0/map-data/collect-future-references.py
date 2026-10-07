"""Earlier same-circuit reference geometry, not upcoming-race observations."""
from pathlib import Path
import ast,json,time,gzip,hashlib
from datetime import datetime,timedelta,timezone
from urllib.request import Request,urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
ROOT=Path(__file__).resolve().parent
tree=ast.parse((ROOT/'collect-maps.py').read_text(encoding='utf8'));nodes=[]
for node in tree.body:
    if isinstance(node,(ast.Import,ast.ImportFrom,ast.FunctionDef)):nodes.append(node)
    elif isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'ROOT','RAW','manifest','outputs'} for t in node.targets):nodes.append(node)
ns={'__file__':str(ROOT/'collect-maps.py')};exec(compile(ast.Module(body=nodes,type_ignores=[]),'map-functions','exec'),ns)
fetch=ns['fetch'];instant=ns['instant'];epoch=ns['epoch'];save=ns['save'];manifest=ns['manifest']
maps=json.loads((ROOT/'maps.json').read_text(encoding='utf8'));prior_manifest=json.loads((ROOT/'source-manifest.json').read_text(encoding='utf8'))
season=json.loads((ROOT.parent/'data/season-2026.json').read_text(encoding='utf8'))
history=json.loads((ROOT/'historical-2025-reference-metadata.json').read_text(encoding='utf8'))['races']
def fetchlaps(key,num):
    f=ROOT/'raw'/f'{key}-{num}-laps.json.gz';url='https://api.openf1.org/v1/laps?'+urlencode({'session_key':key,'driver_number':num})
    if f.exists():blob=gzip.decompress(f.read_bytes());status='cached'
    else:
        for attempt in range(2):
            time.sleep(2.1)
            try:
                with urlopen(Request(url,headers={'User-Agent':'MatchLab historical circuit reference'}),timeout=60) as response:blob=response.read()
                f.write_bytes(gzip.compress(blob,mtime=0));status='ok';break
            except HTTPError as exc:
                if exc.code==429 and attempt==0:time.sleep(9);continue
                raise
    rows=json.loads(blob);manifest.append({'url':url,'file':str(f.relative_to(ROOT)).replace('\\','/'),'sha256_uncompressed':hashlib.sha256(blob).hexdigest(),'rows':len(rows),'status':status,'recorded_at':datetime.now(timezone.utc).isoformat()});return rows
for race in [r for r in season['races'] if r['state']=='scheduled']:
    target=race['session'];key=target['session_key'];matches=[r for r in history if r['session']['circuit_key']==target['circuit_key']]
    record={'session_key':key,'circuit_key':target['circuit_key'],'circuit_name':target['circuit_short_name'],'meeting_name':race['meeting']['meeting_name'],'points':[],'drivers':{},'status':'MISSING_HISTORICAL_REFERENCE',
      'scope':'Upcoming GP: 2025 same-circuit reference only; not current-year verified layout, actual race observations or lap forecasts.'}
    try:
        if not matches:raise ValueError('No 2025 race with same circuit_key')
        old=max(matches,key=lambda r:r['session']['date_start']);oldkey=old['session']['session_key'];ds=old['records']['drivers'];num=next((d['driver_number'] for d in ds if d['driver_number']==63),ds[0]['driver_number'])
        laps=fetchlaps(oldkey,num)
        valid=[l for l in laps if l.get('date_start') and l.get('lap_duration') and not l.get('is_pit_out_lap') and l.get('lap_number',0)>2]
        valid.sort(key=lambda l:(abs(l['lap_number']-10),l['lap_number']))
        if not valid:raise ValueError('No valid historical lap')
        lap=valid[0];t0=instant(lap['date_start']);t1=t0+timedelta(seconds=lap['lap_duration']);rows,source=fetch(oldkey,num,t0-timedelta(seconds=2.4),t1+timedelta(seconds=2.4))
        points=[r for r in rows if r.get('session_key')==oldkey and r.get('driver_number')==num and r.get('date') and t0<=instant(r['date'])<=t1 and isinstance(r.get('x'),(int,float)) and isinstance(r.get('y'),(int,float))]
        points.sort(key=lambda r:r['date'])
        if len(points)<100:raise ValueError('Fewer than 100 reference samples')
        record.update({'status':'HISTORICAL_REFERENCE','reference_session_key':oldkey,'reference_year':2025,'points':[[r['x'],r['y']] for r in points],
          'reference':{'session_key':oldkey,'year':2025,'driver_number':num,'lap_number':lap['lap_number'],'point_count':len(points),'start_ms':int(t0.timestamp()*1000),'end_ms':int(t1.timestamp()*1000),'source_url':source['url'],'closed_artificially':False},'source':source})
    except Exception as exc:record['error']=str(exc)
    maps['races'][str(key)]=record;save('maps.json',maps);save('source-manifest.json',prior_manifest+manifest)
    print('FUTURE_REFERENCE',key,record['status'],len(record['points']),flush=True)
print('FUTURE_COMPLETE',flush=True)
