from pathlib import Path
import json
p=Path(__file__).resolve().parents[1];d=p/'visualization-design-2026-10-06-v19';assert not d.exists();d.mkdir()
texts={
 'ko':dict(mode='분석 방식',local='저장 기록 분석',gemini='AI 분석관',openServer='AI 분석관은 로컬 서버 주소에서 사용합니다. 실행 안내를 확인해 주세요.',running='AI 분석관이 분석 조건을 해석하고 있습니다.',configured='AI 분석관 설정됨 · 실제 연결은 분석 실행 후 확인됩니다.',failed='서버 또는 Gemini 요청이 실패했습니다. 서버 실행과 키 설정을 확인해 주세요.',errors=dict(key_missing='.env의 GEMINI_API_KEY가 비어 있습니다. 로컬 파일에 키를 설정하고 서버를 재시작해 주세요.',provider_auth='AI 분석관 인증이 실패했습니다. 키와 접근 권한을 확인해 주세요.',provider_quota='AI 분석관 사용 한도에 도달했습니다. 잠시 후 또는 한도 확인 후 다시 시도해 주세요.',provider_response='Gemini가 지원하는 분석 조건을 반환하지 못했습니다. 요청을 구체적으로 다시 입력해 주세요.',invalid_plan='지원 범위를 벗어난 분석 조건입니다. 팀·시즌·지표를 다시 지정해 주세요.',league_mismatch='선택된 팀과 리그가 다릅니다.',busy='요청이 진행 중입니다. 잠시 후 다시 시도해 주세요.'),execution='Gemini가 선택한 조건을 검증하고 서버 JavaScript로 저장된 자료를 계산했습니다. SQL·Python·예측 모델 실행은 미연결입니다.'),
 'en':dict(mode='Analysis mode',local='Stored-record analysis',gemini='AI analyst',openServer='AI analyst requires the local server URL. See the setup guide.',running='The AI analyst is interpreting analysis conditions.',configured='AI analyst configured · A live connection is verified after running analysis.',failed='The server or Gemini request failed. Check server startup and key configuration.',errors=dict(key_missing='GEMINI_API_KEY in .env is empty. Set it locally and restart the server.',provider_auth='AI analyst authentication failed. Check key access.',provider_quota='AI analyst quota was reached. Try later or check usage limits.',provider_response='Gemini did not return a supported tool call. Make the request more specific.',invalid_plan='Unsupported analysis conditions. Specify clubs, season and metric again.',league_mismatch='The club and league do not match.',busy='A request is running. Please try again shortly.'),execution='Gemini selected validated parameters; server JavaScript calculated stored records. SQL, Python and prediction-model execution are not connected.')
}
for lang,name in [('ko','index.html'),('en','index.en.html')]:
 s=(p/'visualization-design-2026-10-06-v18'/name).read_text(encoding='utf8');t=texts[lang]
 start=s.index('<section class="panel analyst-workbench"');a=s[:start];b=s[start:]
 b=b.replace('<p class="muted">','<p id="analystconnection" class="muted">',1)
 b=b.replace('<form id="analystform">','<label>'+t['mode']+' <select id="analystmode"><option value="local">'+t['local']+'</option><option value="gemini">'+t['gemini']+'</option></select></label><form id="analystform">',1)
 b=b.replace('<button type="submit">','<button id="analystsubmit" type="submit">',1);s=a+b
 s=s.replace("${esc(analystText.execution)}","${esc(result.planner?geminiText.execution+' ('+result.model+')':analystText.execution)}")
 extra='\nconst geminiText='+json.dumps(t,ensure_ascii=False)+';\n'+(p/'server/browser-bridge.js').read_text(encoding='utf8');a,b=s.rsplit('</script>',1);s=a+extra+'\n</script>'+b
 (d/name).write_text(s,encoding='utf8');(p/name).write_text(s,encoding='utf8')
for name in ['check.cjs','check-en.cjs']:(d/name).write_bytes((p/'visualization-design-2026-10-06-v18'/name).read_bytes())
print('Built v19: local/Gemini modes, same-origin bridge and truthful configuration state.')
