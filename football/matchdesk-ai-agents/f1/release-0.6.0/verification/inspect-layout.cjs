const {chromium}=require('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path');
const {pathToFileURL}=require('url');
(async()=>{
 const source=process.argv[2], label=process.argv[3]||'baseline';
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const page=await browser.newPage(); await page.route('https://**/*',r=>r.abort());
 const results=[];
 for(const width of [320,375,768,1280]){
  await page.setViewportSize({width,height:900});
  await page.goto(pathToFileURL(path.resolve(source)).href+'#race=11234');
  for(const name of ['서킷 지도 비교','경기 결과','랩타임 비교','타이어 · 피트','경기 운영 공지']){
   await page.getByRole('button',{name,exact:true}).click();
   results.push({width,tab:name,...await page.evaluate(()=>({pageWidth:document.documentElement.scrollWidth,viewport:innerWidth,overflow:Array.from(document.querySelectorAll('button,select,.stint,.f1-driver-metric strong')).filter(e=>e.getBoundingClientRect().width&&e.scrollWidth>e.clientWidth+2).map(e=>({tag:e.tagName,text:e.textContent.slice(0,100),client:e.clientWidth,scroll:e.scrollWidth}))}))});
  }
 }
 fs.writeFileSync(path.join(__dirname,'render-'+label+'-v01.json'),JSON.stringify({method:'Separate headless Edge, no user tab interaction',results},null,2));
 console.log(JSON.stringify(results.filter(x=>x.pageWidth>x.viewport+1||x.overflow.length),null,2));
 await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1});
