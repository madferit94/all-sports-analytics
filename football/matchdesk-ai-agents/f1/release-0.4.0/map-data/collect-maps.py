"""Observed OpenF1 coordinates, separate from forecast inputs and symbolic order."""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError,URLError
from datetime import datetime,timezone,timedelta
import json,time,gzip,hashlib,math,statistics
ROOT=Path(__file__).resolve().parent;RAW=ROOT/'raw';RAW.mkdir(exist_ok=True)
season=json.loads((ROOT.parent/'data/season-2026.json').read_text(encoding='utf8'))
manifest=[];outputs={}
def instant(s):return datetime.fromisoformat(s.replace('Z','+00:00'))
def epoch(s):return int(round(instant(s).timestamp()*1000))
def save(name,d):
    f=ROOT/name;temp=f.with_suffix(f.suffix+'.tmp');temp.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'),allow_nan=False),encoding='utf8');temp.replace(f)
def fetch(key,num,start,end):
    # OpenF1 supports strict date comparisons; >= and <= returned 404, not absent telemetry.
    query=urlencode({'session_key':key,'driver_number':num,'date>':start.isoformat(),'date<':end.isoformat()})
    url='https://api.openf1.org/v1/location?'+query;f=RAW/f'{key}-{num}-location.json.gz'
    status='cached' if f.exists() else 'ok';error=None
    if f.exists():blob=gzip.decompress(f.read_bytes())
    else:
        for attempt in range(2):
            time.sleep(2.1)
            try:
                with urlopen(Request(url,headers={'User-Agent':'MatchLab recorded circuit coordinates'}),timeout=75) as response:blob=response.read()
                data=json.loads(blob);assert isinstance(data,list)
                f.write_bytes(gzip.compress(blob,mtime=0));break
            except HTTPError as exc:
                if exc.code==429 and attempt==0:time.sleep(9);continue
                status='HTTP_'+str(exc.code);error=str(exc);blob=b'[]';break
            except (URLError,TimeoutError) as exc:
                status=type(exc).__name__;error=str(exc);blob=b'[]';break
    rows=json.loads(blob)
    manifest.append({'url':url,'file':str(f.relative_to(ROOT)).replace('\\','/') if f.exists() else None,'sha256_uncompressed':hashlib.sha256(blob).hexdigest(),'rows':len(rows),'status':status,'error':error,'recorded_at':datetime.now(timezone.utc).isoformat()})
    return rows,manifest[-1]
for race in sorted([r for r in season['races'] if r['state']=='completed'],key=lambda r:r['session']['date_start']):
    s=race['session'];key=s['session_key'];laps=race['records']['laps'];available={d['driver_number']:d for d in race['records']['drivers']}
    valid=[l for l in laps if l.get('date_start') and l.get('lap_duration') and l['lap_duration']>0]
    begin=min(instant(l['date_start']) for l in valid);end=max(instant(l['date_start'])+timedelta(seconds=l['lap_duration']) for l in valid)
    nums=[num for num in [63,3] if num in available and any(l['driver_number']==num for l in valid)]
    nums+= [d['driver_number'] for d in race['records']['drivers'] if d['driver_number'] not in nums and any(l['driver_number']==d['driver_number'] for l in valid)]
    nums=nums[:2]
    record={'session_key':key,'circuit_key':s['circuit_key'],'circuit_name':s['circuit_short_name'],'meeting_name':race['meeting']['meeting_name'],
      'race_start_ms':int(begin.timestamp()*1000),'race_end_ms':int(end.timestamp()*1000),'points':[],'drivers':{},'status':'MISSING','reference':None,
      'coordinate_system':'OpenF1 recorded x/y; identical raw coordinate system for trace and circuit outline',
      'scope':'Two selected drivers have observed coordinates; remaining cars require labelled lap reconstruction; forecast lane never uses these target-race coordinates.'}
    for num in nums:
        raw,source=fetch(key,num,begin-timedelta(seconds=2.4),end+timedelta(seconds=2.4))
        bytime={}
        for item in raw:
            if item.get('session_key')!=key or item.get('driver_number')!=num:continue
            if item.get('date') and all(isinstance(item.get(a),(int,float)) and math.isfinite(item[a]) for a in ('x','y')):
                t=epoch(item['date'])
                if record['race_start_ms']-2400<t<record['race_end_ms']+2400:bytime[t]=[t,item['x'],item['y']]
        points=sorted(bytime.values())
        # Keep first/last; no interpolation and no deletion that bridges original large gaps.
        sparse=[]
        for j,point in enumerate(points):
            prior=points[j-1] if j else None
            following=points[j+1] if j+1<len(points) else None
            edge_gap=prior is not None and point[0]-prior[0]>2000 or following is not None and following[0]-point[0]>2000
            if not sparse or point[0]-sparse[-1][0]>=1000 or edge_gap or j==len(points)-1:sparse.append(point)
        gaps=[points[i][0]-points[i-1][0] for i in range(1,len(points))]
        record['drivers'][str(num)]={'driver_number':num,'name':available[num]['full_name'],'team':available[num]['team_name'],
          'samples':sparse,'source_rows':len(raw),'valid_original_samples':len(points),'max_original_gap_ms':max(gaps,default=None),
          'original_gaps_over_2s':sum(g>2000 for g in gaps),'median_original_interval_ms':statistics.median(gaps) if gaps else None,
          'status':'OBSERVED_LOCATION' if points else 'MISSING','source':source}
        if not record['points'] and points:
            pit_laps={p.get('lap_number') for p in race['records'].get('pit',[]) if p['driver_number']==num}
            choices=[l for l in valid if l['driver_number']==num and not l.get('is_pit_out_lap') and l.get('lap_number',0)>2 and l['lap_number'] not in pit_laps]
            choices.sort(key=lambda l:(abs(l['lap_number']-10),l['lap_number']))
            for lap in choices:
                t0=epoch(lap['date_start']);t1=t0+int(round(lap['lap_duration']*1000));lap_points=[p for p in points if t0<=p[0]<=t1]
                if len(lap_points)>=100:
                    record['points']=[[p[1],p[2]] for p in lap_points]
                    record['reference']={'driver_number':num,'lap_number':lap['lap_number'],'start_ms':t0,'end_ms':t1,'point_count':len(lap_points),'source_url':source['url'],'closed_artificially':False};break
        print('DRIVER',key,num,len(raw),len(sparse),source['status'],flush=True)
    record['status']='OBSERVED_LOCATION' if len(record['points'])>=100 else 'MISSING_TRACK_REFERENCE'
    outputs[str(key)]=record
    save('maps.json',{'version':'0.4.0','as_of':season['summary']['as_of'],'races':outputs})
    save('source-manifest.json',manifest)
    print('GP_COMPLETE',key,len(outputs),'trackpoints',len(record['points']),flush=True)
print('MAPS_COMPLETE',len(outputs),flush=True)
