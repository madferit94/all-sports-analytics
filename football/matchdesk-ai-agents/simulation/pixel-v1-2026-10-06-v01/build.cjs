'use strict';
const fs=require('node:fs'),path=require('node:path');const P=path.resolve(__dirname,'../..'),target=path.join(P,'visualization-design-2026-10-06-v22');
if(fs.existsSync(target))throw new Error('v22 exists; do not overwrite.');
const prediction=JSON.parse(fs.readFileSync(path.join(P,'modeling/prematch-v2-2026-10-06-v01/future-predictions.json'),'utf8'));
const payload=JSON.stringify({...prediction,predictions:prediction.predictions.map(({evidence,...p})=>p)}).replace(/</g,'\\u003c');
const js=fs.readFileSync(path.join(__dirname,'pixel-simulation.js'),'utf8'),css=fs.readFileSync(path.join(__dirname,'pixel-simulation.css'),'utf8'),integration=fs.readFileSync(path.join(__dirname,'integration.js'),'utf8');
fs.mkdirSync(target);
for(const file of ['index.html','index.en.html']){
  let html=fs.readFileSync(path.join(P,file),'utf8');if(html.includes('prematch-predictions-v22'))throw new Error('Integration already present.');
  html=html.replace('</head>','<style id="pixel-simulation-v22">'+css+'</style></head>');
  html=html.replace('</body>','<script id="prematch-predictions-v22" type="application/json">'+payload+'</script><script>'+js+'</script><script>'+integration+'</script></body>');
  fs.writeFileSync(path.join(target,file),html);fs.writeFileSync(path.join(P,file),html);
}
console.log(JSON.stringify({snapshot:'v22',predictions:prediction.predictions.length,inline:true,browserVerified:false}));
