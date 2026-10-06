from pathlib import Path

out=Path(__file__).parent
prior=out.parent/'visualization-design-2026-10-06-v13'
page=(prior/'index.html').read_text(encoding='utf8')
svg='''<svg viewBox="0 0 240 120" class="pixel-pitch" aria-hidden="true" focusable="false" shape-rendering="crispEdges">
<rect width="240" height="120" fill="#182b3b"/><rect x="8" y="8" width="224" height="24" fill="#334b61"/>
<path d="M12 14h212M12 22h212" stroke="#ffd56b" stroke-width="4" stroke-dasharray="4 8"/>
<rect x="8" y="40" width="224" height="72" fill="#507e54"/><path d="M8 56h224M8 88h224" stroke="#609362" stroke-width="16"/>
<path d="M18 48h204v56H18zM120 48v56M18 60h26v32H18M222 60h-26v32h26" stroke="#d9edaf" stroke-width="2" fill="none"/>
<path d="M110 68h20v16h-20z" stroke="#d9edaf" stroke-width="2" fill="none"/>
<rect x="73" y="63" width="8" height="8" fill="#ffceac"/><rect x="69" y="71" width="16" height="12" fill="#f66d7a"/><rect x="69" y="83" width="6" height="9" fill="#f9efd8"/><rect x="79" y="83" width="6" height="9" fill="#f9efd8"/>
<rect x="157" y="59" width="8" height="8" fill="#ffceac"/><rect x="153" y="67" width="16" height="12" fill="#77c8ee"/><rect x="153" y="79" width="6" height="9" fill="#f9efd8"/><rect x="163" y="79" width="6" height="9" fill="#f9efd8"/>
<rect x="110" y="89" width="8" height="8" fill="#fff9e7"/><rect x="113" y="92" width="3" height="3" fill="#182b3b"/></svg>'''
hero='<section class="arcade-hero"><div><span class="arcade-kicker">MATCHDESK / 8-BIT CLUBHOUSE</span><h2>오늘의 축구 분석실</h2><p>팀을 고르고, 기록을 탐험해 보세요.</p></div>'+svg+'</section>'
assert '<main><div class="toolbar">' in page
page=page.replace('<main><div class="toolbar">','<main>'+hero+'<div class="toolbar">',1)
page=page.replace('<strong>MatchDesk</strong>','<strong>MatchDesk <span class="pixel-tag">8-BIT</span></strong>',1)
font='<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/galmuri@2.40.3/dist/galmuri.css">'
css='''<style id="pixel-clubhouse-v14">
:root{--pixel-ink:#203447;--pixel-paper:#fff7df;--pixel-green:#b9dfb3;--pixel-yellow:#ffd56b}
body{background-color:#e2ecd9;background-image:radial-gradient(#91a99038 1px,transparent 1px);background-size:8px 8px;color:var(--pixel-ink)}
header{background:#203447;color:#fff7df;border-bottom:4px solid #132334;box-shadow:0 4px 0 #a3bb9e}
header strong,nav button,h1,h2,h3,.arcade-kicker,.pixel-tag,.summary strong,.metriccard strong,.openmatch,.form span{font-family:Galmuri11,'Courier New',system-ui,sans-serif}
header small{color:#c8dec9}.pixel-tag{font-size:12px;vertical-align:middle;background:#ffd56b;color:#203447;padding:5px 8px;letter-spacing:0}
nav{background:#142536;border-radius:0;padding:4px;gap:8px}nav button{border:2px solid #627789;border-radius:0;color:#f2ecd7;background:#334a5e;box-shadow:2px 2px 0 #101e2a}
nav button.active{background:#ffd56b;color:#203447;border-color:#ffd56b;box-shadow:2px 2px 0 #956b35}
main{padding-top:30px}.arcade-hero{display:grid;grid-template-columns:minmax(0,1fr) 280px;align-items:center;gap:30px;background:#203447;color:#fff7df;border:4px solid #132334;box-shadow:6px 6px 0 #91a58e;margin-bottom:32px;padding:26px}
.arcade-kicker{display:block;color:#c9eaa5;font-size:12px;letter-spacing:1px}.arcade-hero h2{font-size:30px;margin:12px 0 8px;line-height:1.5}.arcade-hero p{font-size:14px;color:#d4e3d0;margin:0}.pixel-pitch{width:100%;height:auto;border:4px solid #132334;image-rendering:pixelated}
.panel,.fixture{border:3px solid #314b50;border-radius:0;background:#fff9e9;box-shadow:5px 5px 0 #a6b99a;padding:24px}
.fixture.selected{outline:3px solid #b86756;outline-offset:3px}.fixture:hover{border-color:#557e55;box-shadow:5px 5px 0 #789a78}
.openmatch{background:#b9dfb3;border:2px solid #314b50;color:#203447;border-radius:0;box-shadow:3px 3px 0 #829b7b;padding:8px 15px;min-height:44px}
.openmatch:active,nav button:active{transform:translate(2px,2px);box-shadow:none}
.logolink,.logolink.big,.fixture .logolink{border:2px solid #ced5b9;border-radius:0;background:#fffefa;box-shadow:none}.logoimg{image-rendering:auto}
select,.filterdeck input,.statfilters input,.catalogsearch input{border:2px solid #527067;border-radius:0;background:#fffefa;box-shadow:2px 2px 0 #c1ccb0;color:#203447}
.filterdeck{border:2px solid #7b9a7b;background:#d3e4c6;border-radius:0}
.catalogitem,.catalogitem.active{border-radius:0;border:2px solid #799471;background:#f5f8e8;box-shadow:2px 2px 0 #bdd0af}.catalogitem.active{border-color:var(--club-accent);background:#fff3d9}
#team .historyname{background:#eef3d8;border:2px solid #879d75;border-left:6px solid var(--club-accent);border-radius:0}
.summary>div,.splitstats>div,.overviewcard,.metriccard,#snapshotstats .metriccard{background:#f2efd7;border:2px solid #bbc6a1;border-radius:0;box-shadow:3px 3px 0 #dce1c9}
.summary strong,.metriccard strong{font-size:29px;letter-spacing:0}.summary>div:first-child{border-top:2px solid #bbc6a1!important}
.status{border-radius:0;background:#d8e4c7;border:1px solid #a9bd94;color:#314b40}.form span{border:1px solid #789474;border-radius:0;background:#d4e7c6;color:#29452e}
.track,.fill{border-radius:0}.track{background:#d8dfc5}.fill{border:1px solid #20344733}
.metric-popover{border:3px solid #314b50;border-radius:0;background:#fff9e9;box-shadow:5px 5px 0 #58725b44}.metric-reading{border-radius:0;background:#edf0d7;border-left:3px solid #90ae7b}.metric-popover:before{background:#6d985f}
#metrichelpclose{border-radius:0;background:#d8e4c7;border:1px solid #a9bd94}
.seasoncolumn .stick{border-radius:0}th,td{border-bottom-color:#d8ddc6}.selectedseason{background:#ebf1d9}
button:focus-visible,select:focus-visible,a:focus-visible,input:focus-visible{outline:3px solid #b84b41;outline-offset:3px}
@media(max-width:750px){.arcade-hero{grid-template-columns:minmax(0,1fr);gap:20px;padding:20px}.pixel-pitch{max-width:320px;justify-self:center}.arcade-hero h2{font-size:24px}header strong{font-size:22px}.panel,.fixture{padding:18px;box-shadow:3px 3px 0 #a6b99a}.pixel-tag{font-size:10px}.summary strong,.metriccard strong{font-size:25px}}
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
</style>'''
page=page.replace('</head>',font+css+'</head>',1)
(out/'index.html').write_text(page,encoding='utf8')
check=(prior/'check.cjs').read_text(encoding='utf8')
extra='''
test('pixel preview keeps real data and adds a decorative stadium without fake coordinates',()=>{assert(html.includes('id="pixel-clubhouse-v14"'));assert(html.includes('class="pixel-pitch" aria-hidden="true"'));assert(html.includes('galmuri@2.40.3'));assert.strictEqual(data.completed.length,2399);assert.strictEqual(data.scheduled.length,641);assert(!html.includes('animation:blink'));assert(!html.includes('snapshotprovenance'))});
'''
check=check.replace("fs.writeFileSync(__dirname+'/logic-check.json'",extra+"\nfs.writeFileSync(__dirname+'/logic-check.json'")
(out/'check.cjs').write_text(check,encoding='utf8')
print('Built v14 pixel preview with unchanged football data.')
