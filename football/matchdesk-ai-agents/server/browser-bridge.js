// Same-origin Gemini bridge. Keys never enter the page or request body.
let geminiRequestVersion=0;
const submitLocalAnalysis=submitAnalysis;
submitAnalysis=function(question){
 if($('analystmode').value!=='gemini')return submitLocalAnalysis(question);
 return submitGeminiAnalysis(question);
};
async function submitGeminiAnalysis(question){
 const version=++geminiRequestVersion;
 if(!['http:','https:'].includes(window.location.protocol)){$('analyststatus').textContent=geminiText.openServer;return {status:'unavailable',reason:'server_required'}}
 $('analyststatus').textContent=geminiText.running;$('analystsubmit').disabled=true;
 try{
  const response=await fetch('/api/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question,defaults:analystDefaults(),previous:analystPrevious}),signal:AbortSignal.timeout(35000)});
  const result=await response.json();
  if(version!==geminiRequestVersion)return result;
  if(!response.ok){$('analystresult').innerHTML='';$('analyststatus').textContent=geminiText.errors[result.error]||geminiText.failed;return {status:'unavailable',reason:result.error}}
  if(result.status==='ok')analystPrevious=result.plan;
  renderAnalysis(result);return result;
 }catch{
  if(version===geminiRequestVersion){$('analystresult').innerHTML='';$('analyststatus').textContent=geminiText.failed}
  return {status:'unavailable',reason:'server_unreachable'};
 }finally{if(version===geminiRequestVersion)$('analystsubmit').disabled=false}
}
$('analystmode').onchange=()=>{geminiRequestVersion++;$('analystsubmit').disabled=false;$('analystresult').innerHTML='';$('analyststatus').textContent=$('analystmode').value==='gemini'?geminiText.openServer:geminiText.local};
async function checkGeminiConnection(){
 if(typeof fetch!=='function'||!['http:','https:'].includes(window.location.protocol))return;
 try{const response=await fetch('/api/health');if(!response.ok)return;const status=await response.json();$('analystmode').value='gemini';$('analystconnection').textContent=status.configured?geminiText.configured.replace('{model}',status.model):geminiText.errors.key_missing}catch{/* Local mode remains available; no false connection claim. */}
}
checkGeminiConnection();
