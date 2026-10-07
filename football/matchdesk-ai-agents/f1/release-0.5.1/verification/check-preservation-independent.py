from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parents[1];old=P.parent/'matchlab-f1-2026-10-07-v06';files=['data/season-2026.json','modeling/historical-predictions.json','modeling/predictions.json','map-data/maps.json','replay/replay.js','replay/comparison.js'];checks=[]
for f in files:
 a=hashlib.sha256((old/f).read_bytes()).hexdigest();b=hashlib.sha256((P/f).read_bytes()).hexdigest();checks.append(dict(name=f,expected=a,actual=b,status='PASS' if a==b else 'FAIL'))
r=dict(producer_id='/root/f1_verifier',scope='v07 unchanged source/model/maps',status='PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL',checks=checks,remaining=['New map GPS data verification pending','Map UI pending','No repeated whole-model endorsement']);(P/'verification/preservation-independent-v01.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(dict(status=r['status'],checks=len(checks),failures=[x['name'] for x in checks if x['status']=='FAIL']),ensure_ascii=False));raise SystemExit(r['status']=='FAIL')
