'use strict';
const fs=require('node:fs'),path=require('node:path');const P=path.resolve(__dirname,'../..'),target=path.join(P,'visualization-design-2026-10-06-v23');
if(fs.existsSync(target))throw new Error('v23 exists; do not overwrite.');
const oldJs=fs.readFileSync(path.join(P,'simulation/pixel-v1-2026-10-06-v01/pixel-simulation.js'),'utf8'),newJs=fs.readFileSync(path.join(__dirname,'pixel-simulation.js'),'utf8');
const normalize=s=>s.replace(/\r\n/g,'\n');fs.mkdirSync(target);
for(const file of ['index.html','index.en.html']){
  let html=fs.readFileSync(path.join(P,file),'utf8'),oldPayload=html.match(/<script id="prematch-predictions-v22" type="application\/json">([\s\S]*?)<\/script>/)[1];
  const scripts=[...html.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/g)],moduleScript=scripts.find(m=>normalize(m[2])===normalize(oldJs));
  if(!moduleScript)throw new Error('Exactly matching previous module not found.');
  html=html.replace(moduleScript[0],'<script>'+newJs+'</script>');
  if(html.match(/<script id="prematch-predictions-v22" type="application\/json">([\s\S]*?)<\/script>/)[1]!==oldPayload)throw new Error('Forecast data changed.');
  fs.writeFileSync(path.join(target,file),html);fs.writeFileSync(path.join(P,file),html);
}
console.log(JSON.stringify({snapshot:'v23',playersPerTeam:11,forecastsChanged:false,browserVerified:false}));
