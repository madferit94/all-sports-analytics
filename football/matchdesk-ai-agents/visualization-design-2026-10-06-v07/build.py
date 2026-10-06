"""Preserve v06 and constrain card/team content without hiding overflowing text."""
from pathlib import Path

out=Path(__file__).resolve().parent
source=out.parent/'visualization-design-2026-10-06-v06/index.html'
page=source.read_text(encoding='utf-8')
css='''<style id="layout-containment-v07">
/* Zero minimum track sizes let long team labels wrap inside their own cell. */
.fixture,.panel,.overviewcard,.metriccard,.catalogitem{min-width:0;max-width:100%}
.grid,.overviewgrid,.splitstats{grid-template-columns:repeat(2,minmax(0,1fr))}
.grid>*,.overviewgrid>*,.splitstats>*{min-width:0}
.fixture .pair{display:grid;grid-template-columns:minmax(0,1fr) 24px minmax(0,1fr);gap:10px;align-items:start;margin-top:18px}
.fixture .pair>.mini{display:flex;flex-direction:column;align-items:center;gap:10px;min-width:0;width:100%;text-align:center}
.fixture .pair>.muted{padding-top:13px;text-align:center;white-space:nowrap}
.teamname{min-width:0;max-width:100%;white-space:normal;overflow-wrap:anywhere;word-break:normal}
.fixture .pair .teamname{width:100%;min-height:44px;justify-content:center;align-items:flex-start;line-height:1.4}
.fixture .logolink{width:48px;height:48px;flex-shrink:0}
.fixture .pair .logoimg{width:34px;height:34px}
.matchhead{grid-template-columns:minmax(0,1fr) auto minmax(0,1fr)}
.matchhead>.club{flex-direction:column;align-items:center;text-align:center;gap:12px;min-width:0}
.matchhead>.club.right{flex-direction:column-reverse;justify-content:flex-start;text-align:center}
.matchhead .teamname{justify-content:center;line-height:1.4}
.teamheader>div{min-width:0}.teamheader h2{white-space:normal;overflow-wrap:anywhere}
.mini{min-width:0;max-width:100%}.mini>.teamname{flex:1 1 auto;line-height:1.4}
.legend{flex-wrap:wrap}.legend>span{min-width:0;overflow-wrap:anywhere}
.summary{grid-template-columns:repeat(4,minmax(0,1fr))}.summary>div{min-width:0}
.summary strong,.metriccard strong{overflow-wrap:anywhere;line-height:1.4}
.tablewrap{min-width:0;max-width:100%;overflow-x:auto;overscroll-behavior-x:contain}
.tablewrap td:first-child{white-space:normal}.tablewrap .mini{max-width:230px}
.teamchooser label,.filterdeck label,.statfilters label,.toolbar>label{min-width:0;max-width:100%}
.teamchooser select,.filterdeck input,.filterdeck select,.statfilters select{min-width:0;max-width:100%}
.note,.overviewcaption,#snapshotprovenance{overflow-wrap:anywhere}
@media(max-width:1100px){.cards{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:750px){.cards,.grid,.overviewgrid,.splitstats{grid-template-columns:minmax(0,1fr)}.summary{grid-template-columns:repeat(2,minmax(0,1fr))}.fixture .pair{gap:12px}.matchhead>.club{font-size:16px}.teamheader{flex-wrap:wrap}.statfilters>input{width:100%}}
</style>'''
assert 'layout-containment-v07' not in page
page=page.replace('</head>',css+'</head>')
with (out/'index.html').open('x',encoding='utf-8') as f:f.write(page)
# Existing data/navigation checks also run against the new output.
test=(out.parent/'visualization-design-2026-10-06-v06/check.cjs').read_text(encoding='utf-8')
with (out/'check.cjs').open('x',encoding='utf-8') as f:f.write(test)
print('Created v07: logo-over-label cards, fixed VS cell, shrinking grid tracks, contained tables. Preserved v06.')
