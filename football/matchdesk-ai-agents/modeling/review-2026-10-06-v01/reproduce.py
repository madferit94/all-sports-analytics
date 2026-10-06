import csv,json,subprocess,sys,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;M=D.parent;R=M/'runs/2026-10-06-v01';REPO=M.parent;BASE=next(p for p in REPO.parents if p.name=='ai-agent-planning-2026-10-06-v01');OUT=D/'reproduction-2026-10-06-v01'
cmd=[sys.executable,'-B',str(M/'train_baseline.py'),'--dataset',str(BASE/'source-unified-2026-10-06-v01'),'--out',str(OUT),'--cutoff-date','2026-10-06'];p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
checks=[]
if p.returncode==0:
 for f in ['metrics.json','model.json','historical_features.json','future_inputs.json','predictions.csv']:
  checks.append({'file':f,'identical_bytes':(R/f).read_bytes()==(OUT/f).read_bytes(),'original_sha256':hashlib.sha256((R/f).read_bytes()).hexdigest(),'reproduced_sha256':hashlib.sha256((OUT/f).read_bytes()).hexdigest()})
with (D/'reproduction-check.json').open('x',encoding='utf-8') as f:json.dump({'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'checks':checks,'input_manifest_compared_except_observed_at':json.loads((R/'input_manifest.json').read_text(encoding='utf-8'))|{'observed_at':None} == (json.loads((OUT/'input_manifest.json').read_text(encoding='utf-8'))|{'observed_at':None}) if p.returncode==0 else False},f,ensure_ascii=False,indent=2)
print(json.dumps({'returncode':p.returncode,'checks':checks},ensure_ascii=True))
