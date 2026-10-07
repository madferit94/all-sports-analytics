from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent.parent
old=P.with_name(P.name.replace('-v09','-v08'))
current=(P/'replay/map-comparison.js').read_text(encoding='utf8')
prior=(old/'replay/map-comparison.js').read_text(encoding='utf8')
checks=[]
for start,end in [('driverHistory','historyChart'),('actualMarkers','raceLapCount'),('playbackDuration','fit')]:
    def body(s):
        text=s[s.index('function '+start+'('):s.index('function '+end+'(')]
        return text.split('\nconst ')[0].rstrip() if start=='driverHistory' else text
    checks.append(dict(name=start+' unchanged from v08',expected=hashlib.sha256(body(prior).encode()).hexdigest(),actual=hashlib.sha256(body(current).encode()).hexdigest()))
checks.append(dict(name='recorded replay unchanged',expected=hashlib.sha256((old/'replay/replay.js').read_bytes()).hexdigest(),actual=hashlib.sha256((P/'replay/replay.js').read_bytes()).hexdigest()))
for c in checks:c['status']='PASS' if c['expected']==c['actual'] else 'FAIL'
out=dict(producer_id='/root/f1_verifier',status='PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL',method='Function-source preservation of cursor cutoffs and real-time clock; existing v08 behavior tests remain prior-version evidence, not newly rerun',checks=checks)
(P/'verification/time-scope-independent-v09-v02.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out))
