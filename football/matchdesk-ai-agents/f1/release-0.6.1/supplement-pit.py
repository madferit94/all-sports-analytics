from pathlib import Path
import json,csv,io,urllib.request,hashlib,unicodedata,datetime
p=Path(__file__).resolve().parent
src=p.parent/'matchlab-f1-2026-10-07-v09/data/season-2026.json'
d=json.loads(src.read_text(encoding='utf8'))
files={11234:'1aus.csv',11245:'2chi.csv',11253:'3jap.csv',11280:'4mia.csv',11291:'5can.csv',11299:'6mon.csv',11307:'7cat.csv',11315:'8austr.csv',11326:'9gb.csv',11334:'10bel.csv',11342:'11hun.csv',11353:'12pb.csv',11361:'13ita.csv'}
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKD',s).lower() if c.isascii() and c.isalnum())
report={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':'DHL-derived Jordan-Soria/PitStops; third-party transcription, not direct DHL verification','files':[],'filled':[],'unmatched':[],'conflicts':[]}
for race in d['races']:
 key=race['session']['session_key']
 if key not in files:continue
 fn=files[key];url='https://raw.githubusercontent.com/Jordan-Soria/PitStops/main/2026/'+fn;f=p/'supplement'/fn
 if not f.exists():f.write_bytes(urllib.request.urlopen(url,timeout=25).read())
 raw=f.read_bytes();rows=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig')),delimiter='\t'));rows=[{k.strip():v.strip() for k,v in x.items()} for x in rows]
 report['files'].append({'session_key':key,'circuit':race['session']['circuit_short_name'],'url':url,'sha256':hashlib.sha256(raw).hexdigest(),'rows':len(rows)})
 for row in rows:
  name=norm(row['Driver']);drivers=[x for x in race['records']['drivers'] if norm(x.get('last_name',''))==name or norm(x.get('full_name','')).endswith(name)]
  lap=int(row['Lap']);value=float(row['Time (sec)'])
  hits=[x for x in race['records']['pit'] if len(drivers)==1 and x['driver_number']==drivers[0]['driver_number'] and x['lap_number']==lap]
  evidence={'session_key':key,'driver':row['Driver'],'lap':lap,'stop_duration':value}
  if len(hits)!=1 or not value>0:report['unmatched'].append(evidence);continue
  hit=hits[0];old=hit.get('stop_duration')
  if isinstance(old,(int,float)) and old>0:
   if abs(old-value)>0.15:report['conflicts'].append({**evidence,'openf1':old})
   continue
  assert value<=hit.get('lane_duration',hit.get('pit_duration',float('inf')))+0.15
  hit['stop_duration']=value;hit['stop_duration_source']={'provider':'DHL-derived f1pits archive','url':url,'match':'session+unique surname+lap','original_openf1':old}
  report['filled'].append(evidence)
(p/'data/season-2026.json').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')),encoding='utf8')
(p/'verification/pit-supplement-v01.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('files',len(report['files']),'filled',len(report['filled']),'unmatched',len(report['unmatched']),'conflicts preserved',len(report['conflicts']))

