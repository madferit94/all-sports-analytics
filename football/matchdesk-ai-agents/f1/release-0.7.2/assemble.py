from pathlib import Path
import json,re
p=Path(__file__).resolve().parent
def data(name,default):
 f=p/name
 return json.loads(f.read_text(encoding="utf8")) if f.exists() else default
t=(p/"template.html").read_text(encoding="utf8")
for token,path,default in [("__MAP_DATA__","map-data/maps.json",{"races":{}}),("__HISTORICAL__","modeling/historical-predictions.json",{"races":{}}),("__DATA__","data/season-2026.json",{}),("__FORECASTS__","modeling/predictions.json",{"races":{}}),("__TRACKS__","replay/track-shapes.json",{})]:
 t=t.replace(token,json.dumps(data(path,default),ensure_ascii=False).replace("</","<\\/"))
t=t.replace("__NATURAL_MODULE__",(p/"replay/natural-analysis.js").read_text(encoding="utf-8-sig"))
metrics=p/"replay/metrics.js"
t=t.replace("__METRICS_MODULE__",metrics.read_text(encoding="utf8") if metrics.exists() else "")
m=p/"replay/map-comparison.js"
t=t.replace("__MAP_COMPARISON_MODULE__",m.read_text(encoding="utf8") if m.exists() else "")
c=p/"replay/comparison.js"
t=t.replace("__COMPARISON_MODULE__",c.read_text(encoding="utf8") if c.exists() else "")
f=p/"replay/replay.js"
t=t.replace("__REPLAY_MODULE__",f.read_text(encoding="utf8") if f.exists() else "")
(p/"index.html").write_text(t,encoding="utf8")
(p/"ui-check-source.js").write_text(re.findall(r"<script>(.*?)</script>",t,re.S)[-1],encoding="utf8")
print("Assembled MatchLab F1 0.7.2")


