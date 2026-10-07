const {chromium}=require('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),assert=require('assert');const {pathToFileURL}=require('url');
let testBrowser;
(async()=>{
const browser=testBrowser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
const page=await browser.newPage();await page.route('https://**/*',r=>r.abort());const errors=[];page.on('pageerror',e=>errors.push(e.message));
const url=pathToFileURL(path.resolve(__dirname,'../index.html')).href,observations=[];let checks=0;
function check(value,label){checks++;assert(value,label)}
async function fit(scope){const r=await page.evaluate(scope=>({viewport:innerWidth,pageWidth:document.documentElement.scrollWidth,overflow:Array.from(document.querySelectorAll(scope)).filter(e=>e.getBoundingClientRect().width&&e.scrollWidth>e.clientWidth+2).map(e=>({text:e.textContent.slice(0,90),client:e.clientWidth,scroll:e.scrollWidth}))}),scope);check(r.pageWidth<=r.viewport+1,'page horizontal overflow '+JSON.stringify(r));check(!r.overflow.length,'text overflow '+JSON.stringify(r.overflow));return r;}
for(const width of [320,375,768,1280])for(const lang of ['ko','en']){
 await page.setViewportSize({width,height:900});await page.goto(url+'?lang='+lang+'#race=11234');
 await page.getByRole('button',{name:lang==='ko'?'드라이버 지표':'Driver metrics',exact:true}).click();
 check(await page.locator('.f1-metric-card').count()>=28,'full metric count');let result=await fit('.f1-metric-help,.f1-metric-value,.f1-metrics-controls select');observations.push({width,lang,view:'metrics',...result});
 await page.locator('[data-metric-driver]').selectOption('27');check(await page.locator('[data-metric-driver]').inputValue()==='27','driver filter');
 for(const category of ['result','pace','pit','prediction']){await page.locator('[data-metric-category]').selectOption(category);check(await page.locator('.f1-metric-card').count()>0,'category '+category);await fit('.f1-metric-help,.f1-metric-value');}
 await page.locator('[data-metric-category]').selectOption('all');
 const help=page.locator('[data-f1-help="recent5_nonfinish_rate"]');await help.click();check(await page.getByRole('dialog').isVisible(),'help opens');let b=await page.getByRole('dialog').boundingBox();check(b.x>=0&&b.x+b.width<=width+1&&b.y>=0&&b.y+b.height<=901,'help fits '+JSON.stringify(b));check((await page.getByRole('dialog').innerText()).length>80,'help explanation');
 if(width===1280&&lang==='ko')await page.screenshot({path:path.join(__dirname,'render-proof-desktop-help-v01.png')});
 if(width===375&&lang==='ko')await page.screenshot({path:path.join(__dirname,'render-proof-mobile-help-v01.png')});
 await page.keyboard.press('Escape');check(await page.getByRole('dialog').count()===0,'Escape closes');check(await help.evaluate(e=>e===document.activeElement),'focus restored');
 await help.focus();await page.keyboard.press('Enter');check(await page.getByRole('dialog').isVisible(),'keyboard opens');await page.locator('[data-f1-help-close]').click();check(await page.getByRole('dialog').count()===0,'button closes');
 await page.getByRole('button',{name:lang==='ko'?'타이어 · 피트':'Tyres & pits',exact:true}).click();observations.push({width,lang,view:'tyres',...await fit('.stint')});
 await page.getByRole('button',{name:lang==='ko'?'서킷 지도 비교':'Circuit map comparison',exact:true}).click();await fit('.f1-metric-help,.f1-driver-metric strong');await page.getByRole('slider').press('End');await fit('.f1-metric-help,.f1-driver-metric strong');await page.locator('[data-f1-help="current_rank"]').click();check(await page.getByRole('dialog').isVisible(),'live help');await page.keyboard.press('Escape');
}
const data=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../data/season-2026.json'),'utf8'));const future=data.races.find(r=>r.state==='scheduled');await page.goto(url+'#race='+future.session.session_key);check(await page.locator('.f1-metric-card').count()>0,'upcoming prediction cards');check(await page.locator('[data-f1-help="final_position"]').count()===0,'future no actual result card');await fit('.f1-metric-help,.f1-metric-value');
check(errors.length===0,'page errors '+JSON.stringify(errors));const report={method:'Actual HTML rendered in separate headless Edge; no user-tab control',checks,errors,observations,participant_confirmation:'pending'};fs.writeFileSync(path.join(__dirname,'render-proof-v01.json'),JSON.stringify(report,null,2));console.log('PASS render',checks,observations.length,'layout observations');await browser.close();
})().catch(async e=>{console.error(e);await testBrowser?.close();process.exitCode=1});


