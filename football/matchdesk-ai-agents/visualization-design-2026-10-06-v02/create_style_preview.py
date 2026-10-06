"""Preserve v01 and produce an explicitly static visual design preview."""
from pathlib import Path

out = Path(__file__).resolve().parent
source = out.parent / 'visualization-design-2026-10-06-v01/index.html'
page = source.read_text(encoding='utf-8')
style = '''<style>
:root{--ink:#18283b;--muted:#526174;--bg:#f3f5f7;--line:#dce2e9;--brand:#111f32;--lime:#d5f36b}
body{font-variant-numeric:tabular-nums}header{background:var(--brand);color:white;padding:26px max(24px,calc((100% - 1132px)/2));border:0}header strong{letter-spacing:-.7px;font-size:26px}header strong:before{content:'M';display:inline-grid;place-items:center;width:36px;height:36px;border-radius:8px;margin-right:12px;background:var(--lime);color:var(--brand);font-size:24px}header .caption{color:#b9c5d5;margin-top:8px}nav{margin-top:20px;gap:12px}nav a{color:#e0e7f0;text-decoration:none;padding:8px 14px;border-radius:7px}nav a:hover{background:#2c3d54}nav a:focus-visible{outline-color:var(--lime)}main{padding-top:42px}h1{font-size:40px;letter-spacing:-1.4px;max-width:760px}h1+p{max-width:720px;color:var(--muted)}h2{letter-spacing:-.6px}.notice{background:#eaf0f5;border-left:4px solid var(--brand);border-radius:0 8px 8px;margin-top:24px;color:var(--ink)}.frame{padding:30px;border-radius:16px;box-shadow:0 3px 12px #111f3205}.frame>.tag{margin-bottom:10px;background:var(--brand);color:var(--lime);letter-spacing:.3px}.panel{border-radius:12px;background:#fff}.soft{background:#f3f6fb}.filters span{background:#f6f8fa;border-color:#d2dbe6;border-radius:7px;font-size:14px;font-weight:600}.teams{padding:24px 12px;border-radius:10px;background:#f4f7fb;margin:16px 0;letter-spacing:-.4px}.teams span:first-child{color:var(--blue)}.teams span:last-child{color:var(--orange)}.metric{padding:13px 0;font-size:15px}.metric span:last-child{color:var(--muted)}.skeleton{border-style:solid;background:repeating-linear-gradient(0deg,#f8fafc,#f8fafc 43px,#e9eef4 44px);color:#526174;font-size:15px}.explain{background:#f7f9fc;padding:20px;border-radius:0 10px 10px}.palette{display:flex;flex-wrap:wrap;gap:12px;margin:24px 0 32px}.swatch{display:flex;gap:9px;align-items:center;border:1px solid var(--line);padding:9px 12px;border-radius:7px;background:white;font-size:14px}.swatch i{width:18px;height:18px;border-radius:4px;display:inline-block;border:1px solid #18283b26}.pitch{background:#eef4ef}.pitch p{background:#eef4ef}@media(max-width:700px){h1{font-size:28px;letter-spacing:-.6px}header{padding:20px}header strong{font-size:20px}nav{gap:4px}nav a{padding:8px 10px}.frame{padding:18px}main{padding-top:28px}.teams{font-size:20px}}
</style>'''
page = page.replace('</style>', '</style>' + style, 1)
page = page.replace('시각화 설계 v01', '사이트 디자인 v02')
page = page.replace('href="DESIGN.ko.md"', 'href="DESIGN-SYSTEM.ko.md"')
page = page.replace('상세 설계 문서', '사이트 디자인 기준')
page = page.replace('숫자를 넣기 전 정보 배치 미리보기입니다.', '사이트 색상과 구성 요소를 적용한 정적 디자인 미리보기입니다.')
palette = '<div class="palette" aria-label="사이트 색상"><span class="swatch"><i style="background:#111f32"></i>브랜드 남색</span><span class="swatch"><i style="background:#d5f36b"></i>라임 강조</span><span class="swatch"><i style="background:#2454c6"></i>홈팀 파랑</span><span class="swatch"><i style="background:#a54d13"></i>원정팀 주황</span></div>'
page = page.replace('<section id="matches"', palette + '<section id="matches"', 1)
page = page.replace('href="coordinate-audit.json"', 'href="../visualization-design-2026-10-06-v01/coordinate-audit.json"')
with (out / 'index.html').open('x', encoding='utf-8') as file:
    file.write(page)
assert page.count('id="matches"') == 1
assert all('id="' + name + '"' in page for name in ('match', 'team', 'league'))
assert '사이트 디자인 v02' in page and '정적 설계안' in page
print('Created v02/index.html; preserved v01; four section links and static-design label checked.')
