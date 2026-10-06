"""Check remote availability using HEAD only; do not download logo images."""
import concurrent.futures
import json
import urllib.request
from pathlib import Path
from datetime import datetime,timezone

out = Path(__file__).resolve().parent
manifest = json.loads((out/'logo-manifest-v02.json').read_text(encoding='utf-8'))
def check(item):
    tid,record=item
    try:
        req=urllib.request.Request(record['url'],headers={'User-Agent':'MatchDeskResearch/1.0'},method='HEAD')
        with urllib.request.urlopen(req,timeout=15) as response:
            mime=response.headers.get('Content-Type','')
            return dict(team_key=tid,url=record['url'],status=response.status,content_type=mime,image_header_ok=response.status==200 and mime.startswith('image/'))
    except Exception as exc:
        return dict(team_key=tid,url=record['url'],image_header_ok=False,error=type(exc).__name__)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    checks=list(executor.map(check,manifest['logos'].items()))
result=dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),method='HEAD only, no image downloaded; not rendered or visually verified',checked=len(checks),ok=sum(r['image_header_ok'] for r in checks),checks=checks)
with (out/'logo-header-check.json').open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False))
