from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent.with_name(P.parent.name.replace('-v09','-v08'))/'verification/check-ui-independent.cjs').read_text(encoding='utf8')
s=s.replace('let mounted=[],destroyed=0;','let mounted=[],destroyed=0,metricsMounted=[],closedHelp=0;')
s=s.replace('window:{MatchLabF1MapComparison:',"window:{MatchLabF1Metrics:{buttonHtml:(k,l)=>'<button data-f1-help='+k+'>'+k+'</button>',mount:(e,r,p)=>{metricsMounted.push(r.session.session_key);return {destroy:()=>destroyed++}},closeHelp:()=>closedHelp++},MatchLabF1MapComparison:")
s=s.replace('const out={producer_id:', '''for(const locale of ['ko','en']){vm.runInContext('lang='+JSON.stringify(locale)+';tab="metrics";detail(11234)',ctx);ck(locale+' metrics tab mount',11234,metricsMounted.at(-1));ck(locale+' metrics tab present',true,el('detail').innerHTML.includes('data-tab="metrics"'));}const beforeClose=closedHelp;vm.runInContext('stopReplay()',ctx);ck('all route changes close explanation bubble',true,closedHelp>beforeClose);ck('metrics latest embedded',true,html.includes(fs.readFileSync(path.join(P,'replay/metrics.js'),'utf8')));const out={producer_id:''')
s=s.replace('ui-independent-v08-v01.json','ui-independent-v09-v01.json')
(P/'check-ui-independent.cjs').write_text(s,encoding='utf8')
