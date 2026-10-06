from pathlib import Path
import re

out=Path(__file__).parent
p=out.parent
prior=p/'visualization-design-2026-10-06-v14'
page=(prior/'index.html').read_text(encoding='utf8')
badge='''function badge(id,big=false){const t=T[id],initials=esc(t.name.split(' ').map(x=>x[0]).join('').slice(0,3));return `<a class="logolink ${big?'big':''}" href="#team=${encodeURIComponent(id)}" data-team="${id}" aria-label="${esc(t.name)} 종합 정보 보기" style="--accent:${colour(id)}">${t.logo?`<canvas class="logoimg pixel-logo" data-logo="${esc(t.logo)}" width="24" height="24" aria-hidden="true" hidden></canvas>`:''}<span class="logofallback">${initials}</span></a>`}
'''
page,count=re.subn(r'^function badge\(.*?\n',lambda m:badge,page,count=1,flags=re.M)
assert count==1
js='''
const pixelLogoAssets=new Map();
function loadPixelLogo(url){
 if(!pixelLogoAssets.has(url))pixelLogoAssets.set(url,new Promise((resolve,reject)=>{
  const image=new Image();image.referrerPolicy='no-referrer';
  image.onload=()=>resolve(image);image.onerror=()=>reject(new Error('Logo unavailable'));
  image.src=url;
 }));
 return pixelLogoAssets.get(url);
}
function renderPixelLogos(){
 const jobs=[];
 document.querySelectorAll('canvas[data-logo]').forEach(canvas=>{
  const url=canvas.dataset.logo;if(!url||canvas.dataset.pixelState)return;
  canvas.dataset.pixelState='loading';
  jobs.push(loadPixelLogo(url).then(image=>{
   if(canvas.isConnected===false)return;
   const ctx=canvas.getContext('2d');if(!ctx)throw new Error('Canvas unavailable');
   const size=24,scale=Math.min(size/image.naturalWidth,size/image.naturalHeight);
   const w=Math.max(1,Math.round(image.naturalWidth*scale)),h=Math.max(1,Math.round(image.naturalHeight*scale));
   ctx.clearRect(0,0,size,size);ctx.imageSmoothingEnabled=true;
   ctx.drawImage(image,Math.floor((size-w)/2),Math.floor((size-h)/2),w,h);
   canvas.hidden=false;canvas.nextElementSibling.hidden=true;canvas.dataset.pixelState='ready';
  }).catch(()=>{canvas.hidden=true;canvas.nextElementSibling.hidden=false;canvas.dataset.pixelState='failed'}));
 });
 return Promise.all(jobs);
}
renderPixelLogos();
if(typeof MutationObserver!=='undefined'){
 const observer=new MutationObserver(()=>renderPixelLogos());
 observer.observe(document.querySelector('main'),{childList:true,subtree:true});
}
'''
page=page.replace('</script></body></html>',js+'</script></body></html>')
css='''<style id="pixel-logos-v15">
.logoimg.pixel-logo{image-rendering:pixelated;image-rendering:crisp-edges;object-fit:contain;padding:2px;aspect-ratio:1}
.logoimg.pixel-logo[hidden]{display:none}
.big .logoimg.pixel-logo{width:64px;height:64px}
.fixture .pair .logoimg.pixel-logo{width:44px;height:44px}
.logofallback{font-family:Galmuri11,'Courier New',sans-serif;color:#203447;min-width:30px;text-align:center}
@media(max-width:750px){.big .logoimg.pixel-logo{width:48px;height:48px}}
</style>'''
page=page.replace('</head>',css+'</head>',1)
(out/'index.html').write_text(page,encoding='utf8')
(p/'index.html').write_text(page,encoding='utf8')
check=(prior/'check.cjs').read_text(encoding='utf8')
check=check.replace("assert(b.includes('<img'));assert(b.includes('nextElementSibling.hidden=false'));assert(b.includes('loading=\"lazy\"'))", "assert(b.includes('<canvas'));assert(b.includes('width=\"24\" height=\"24\"'));assert(b.includes('logofallback'));assert(!b.includes('<img'))")
check='async function main(){\n'+check
extra='''
const imageCalls=[];
class MockImage{constructor(){this.naturalWidth=120;this.naturalHeight=160}set src(url){imageCalls.push(url);if(url==='broken')this.onerror();else this.onload()}}
context.Image=MockImage;
const canvases=[];
context.document.querySelectorAll=selector=>selector==='canvas[data-logo]'?canvases:nav;
function makeCanvas(url){const n=new Node();n.dataset.logo=url;n.hidden=true;n.nextElementSibling={hidden:false};n.draws=[];n.getContext=()=>({clearRect(){},drawImage(...args){n.draws.push(args)}});return n}
Object.values(data.teams).forEach(t=>canvases.push(makeCanvas(t.logo)));
await run('renderPixelLogos()');
test('all 56 logos render on 24px canvases with contained proportions and initial fallback',()=>{assert.strictEqual(canvases.length,56);canvases.forEach(n=>{assert.strictEqual(n.dataset.pixelState,'ready');assert(!n.hidden);assert(n.nextElementSibling.hidden);assert.strictEqual(n.draws.length,1);const [image,x,y,w,h]=n.draws[0];assert(x>=0&&y>=0&&x+w<=24&&y+h<=24);assert.strictEqual(w,18);assert.strictEqual(h,24)});assert.strictEqual(imageCalls.length,56)});
const duplicate=makeCanvas(data.teams['understat:83'].logo);canvases.push(duplicate);await run('renderPixelLogos()');
test('newly rendered team areas reuse cached logos rather than fetching them again',()=>{assert.strictEqual(imageCalls.length,56);assert.strictEqual(duplicate.dataset.pixelState,'ready');assert.strictEqual(duplicate.draws.length,1)});
const broken=makeCanvas('broken'),noContext=makeCanvas('no-context');noContext.getContext=()=>null;canvases.push(broken,noContext);await run('renderPixelLogos()');
test('network and canvas failures retain readable initials without breaking navigation',()=>{[broken,noContext].forEach(n=>{assert.strictEqual(n.dataset.pixelState,'failed');assert(n.hidden);assert(!n.nextElementSibling.hidden)});assert(run('badge("understat:83")').includes('data-team="understat:83"'))});
test('default entry is the adopted pixel version, preserving all original football data',()=>{assert.strictEqual(fs.readFileSync(__dirname+'/../index.html','utf8'),html);assert(html.includes('id="pixel-logos-v15"'));assert(!html.includes('snapshotprovenance'));assert.strictEqual(data.completed.length,2399)});
'''
check=check.replace("fs.writeFileSync(__dirname+'/logic-check.json'",extra+"\nfs.writeFileSync(__dirname+'/logic-check.json'")
check+='\n}\nmain().catch(error=>{console.error(error);process.exitCode=1});\n'
(out/'check.cjs').write_text(check,encoding='utf8')
print('Built adopted pixel UI v15 and the canonical index.html; 56 original logos rendered on 24x24 grids.')
