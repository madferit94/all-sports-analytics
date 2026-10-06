from pathlib import Path

out=Path(__file__).parent
prior=out.parent/'visualization-design-2026-10-06-v12'
page=(prior/'index.html').read_text(encoding='utf8')
css='''<style id="soft-app-preview-v13">
/* Candidate 1: warm surfaces, gentle cards, restrained club accents. */
:root{--soft-ink:#28384a;--soft-muted:#59677a;--club-accent:#a93240;--club-wash:#f7eeef}
body{background:#f8f6f2;color:var(--soft-ink);line-height:1.65}
header{background:#fffefa;color:var(--soft-ink);border-bottom:1px solid #eee9e1;padding-top:20px;padding-bottom:20px}
header strong{font-size:25px;letter-spacing:-.8px}header small{color:var(--soft-muted)}
nav{background:#f1eee8;padding:5px;border-radius:999px;gap:3px}
nav button{color:#59677a;border-radius:999px;padding:10px 20px;transition:background .15s,color .15s}
nav button.active{background:white;color:#913644;box-shadow:0 2px 7px #40393212}
main{padding-top:38px;padding-bottom:42px}
h1{font-size:clamp(26px,3vw,34px);letter-spacing:-1px;line-height:1.3}h2{letter-spacing:-.6px}h3{letter-spacing:-.25px}
.toolbar{margin-bottom:28px;align-items:center}.muted{color:var(--soft-muted)}
select,.filterdeck input,.statfilters input,.catalogsearch input{border:1px solid #e5e1da;border-radius:14px;background:#fffefa;padding:11px 14px}
.cards{gap:22px}.fixture{border:1px solid #ece7df;border-radius:24px;padding:22px;background:#fffefa;box-shadow:0 4px 16px #4b413005}
.fixture:hover{box-shadow:0 8px 24px #4b413012;border-color:#d8c8c7}
.fixture.selected{outline:2px solid #b5656c;outline-offset:2px}
.openmatch{border-radius:999px;background:#f6eeeb;color:#85444c;padding:8px 17px;font-weight:600}
.fixture .pair{margin-top:22px}.fixture .pair>.mini{gap:12px}.fixture .logolink{width:58px;height:58px;border-radius:18px;border:0;background:#f6f3ed}.fixture .pair .logoimg{width:43px;height:43px}
.panel{border:1px solid #eee9e1;border-radius:26px;padding:28px;background:#fffefa;box-shadow:0 5px 24px #4b413005;margin-top:28px}
.overviewgrid,.grid,.splitstats{gap:22px}.overviewcard{border:0;background:#f7f5f0;border-radius:22px;padding:22px}
.status{background:#f0ede6;color:#59677a;border-radius:999px;padding:6px 12px;line-height:1.5}
.logolink{border:1px solid #e8e4dc;border-radius:14px;background:#fffefa}.logolink:hover{box-shadow:0 0 0 2px #e2d2d4}.logolink.big{border:0;background:#fffefa;box-shadow:0 4px 20px #493d3510;min-width:76px;min-height:80px;border-radius:22px}.big .logoimg{width:64px;height:68px}
.summary{gap:14px;margin-top:24px}.summary>div{background:#f7f5f0;border:0;border-radius:20px;padding:18px}.summary strong{font-size:clamp(24px,2.5vw,32px);letter-spacing:-.8px}.summary label{font-size:13px;color:var(--soft-muted)}
.splitstats>div{border:0;background:#f7f5f0;border-radius:20px;padding:20px}
.form span{border-radius:10px;min-width:34px;height:34px;background:#e8ede7;color:#3e5846}.track{background:#e8e5dd;border-radius:999px}.fill{border:0;border-radius:999px}
.catalog{gap:10px;margin-top:16px}.catalogitem{border:1px solid #e8e3da;border-radius:999px;padding:4px 14px 4px 5px;background:#fffefa}.catalogitem .logolink{border:0;background:transparent}.catalogitem.active{border:2px solid var(--club-accent);background:var(--club-wash);padding:3px 13px 3px 4px}.catalogitem .teamname{font-weight:500}
#team .historyname{background:var(--club-wash);padding:24px;border-radius:22px;gap:22px}
#team .teamheader h2{font-size:clamp(26px,3vw,38px);letter-spacing:-1px;line-height:1.3}
#team .historyname>.status{background:#fffefa}
#team .summary>div:first-child{border-top:3px solid var(--club-accent)}
#team .seasonbutton{color:var(--club-accent)}
.filterdeck{background:#f0ede6;border-radius:20px;padding:16px 18px;margin-top:18px;margin-bottom:18px;gap:14px}
.metricgrid{gap:14px;margin-top:22px}.metriccard,#snapshotstats .metriccard{background:#f7f5f0;border:0;border-radius:20px;padding:20px}
.metriccard strong{font-size:29px;letter-spacing:-.7px}.metriccard label,#snapshotstats .metric-trigger{color:#4c5b6b}
#snapshotstats .metric-trigger:hover,#snapshotstats .metric-trigger[aria-expanded="true"]{color:var(--club-accent)!important}
.metric-popover{border-color:#e5dcd4;border-radius:22px;box-shadow:0 15px 50px #493d3520;background:#fffefa}
.metric-reading{background:#f5f1e9;border-radius:14px}.metric-popover:before{background:#a9515b}
.recorddetails{border-top-color:#e7e2d9;padding-top:22px}.recorddetails>summary{font-size:17px}
th,td{border-bottom-color:#ece7df;padding-top:14px;padding-bottom:14px}th{font-size:13px}.selectedseason{background:#f6efed}
footer{border-top-color:#e8e3da;color:#687482}
@media(max-width:750px){header{gap:14px;padding:18px}header strong{font-size:23px}nav{width:100%;justify-content:space-between}nav button{flex:1;padding:9px 12px}main{padding:26px 14px}.panel{padding:18px;border-radius:22px}.fixture{padding:20px}.summary>div{padding:15px}.filterdeck{padding:14px}#team .historyname{padding:18px}.metriccard,#snapshotstats .metriccard{padding:16px}.overviewcard{padding:18px}}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
</style>'''
page=page.replace('</head>',css+'</head>',1)
old="function updateTeam(){let id=$('teamselect').value,season=$('season').value,ms=selectedGames(id)"
new="function updateTeam(){let id=$('teamselect').value; $('team').setAttribute('style','--club-accent:'+T[id].primary+';--club-wash:'+T[id].primary+'0d');let season=$('season').value,ms=selectedGames(id)"
assert old in page
page=page.replace(old,new)
assert not (out/'index.html').exists()
(out/'index.html').write_text(page,encoding='utf8')
check=(prior/'check.cjs').read_text(encoding='utf8')
extra='''
test('soft design retains layout containment and follows the selected club colour',()=>{assert(html.includes('id="soft-app-preview-v13"'));assert(html.includes('id="layout-containment-v07"'));run('openTeam("understat:83")');assert(get('team').attributes.style.includes(data.teams['understat:83'].primary));run('openTeam("understat:148")');assert(get('team').attributes.style.includes(data.teams['understat:148'].primary));assert(get('team').attributes.style.includes('--club-wash:'))});
'''
check=check.replace("fs.writeFileSync(__dirname+'/logic-check.json'",extra+"\nfs.writeFileSync(__dirname+'/logic-check.json'")
(out/'check.cjs').write_text(check,encoding='utf8')
print('Built functioning candidate-1 preview v13; v12 preserved.')
