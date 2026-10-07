from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent.parent
old=P.with_name(P.name.replace('-v09','-v08'))
files=['data/season-2026.json','map-data/maps.json','modeling/historical-predictions.json','modeling/predictions.json']
checks=[]
for name in files:
    prior=hashlib.sha256((old/name).read_bytes()).hexdigest()
    current=hashlib.sha256((P/name).read_bytes()).hexdigest()
    checks.append(dict(name=name,expected=prior,actual=current,status='PASS' if prior==current else 'FAIL'))
out=dict(producer_id='/root/f1_verifier',method='Independent SHA-256 byte comparison against preserved v08',status='PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL',checks=checks)
(P/'verification/preservation-independent-v09-v01.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out))
