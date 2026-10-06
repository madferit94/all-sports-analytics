import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
checks=[]
for folder in sorted((ROOT/'skills').iterdir()):
    text=(folder/'SKILL.md').read_text(encoding='utf-8')
    front=text.split('---',2)[1]
    name=re.search(r'^name: (.+)$',front,re.M).group(1)
    desc=re.search(r'^description: (.+)$',front,re.M).group(1)
    assert name==folder.name and len(name)<=64 and re.fullmatch(r'[a-z0-9-]+',name)
    assert desc and 'TODO' not in text
    assert (ROOT/f'roles/{name.removeprefix("matchdesk-")}.md').exists()
    checks.append(dict(skill=name,scalar_frontmatter_checked=True,role_reference_exists=True))
result=dict(agent_count=5,skill_checks=checks,
    protocol_tests=dict(tests=6,failures=0,errors=0,command='python -m unittest discover -s agent-team-integrated-2026-10-06-v01/tests -v'),
    official_quick_validate=dict(status='UNAVAILABLE',reason='ModuleNotFoundError: No module named yaml',attempted_skill='matchdesk-director'),
    fallback_scope='Simple name/description and references check; not the full bundled YAML validator.',
    actual_five_agent_runtime_executed=False,actual_claude_runtime_executed=False,
    previous_run_relabelled=False,participant_confirmed=False)
with (ROOT/'package-check.json').open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps(dict(agent_count=5,skills_checked=len(checks),protocol_tests=6,quick_validate='UNAVAILABLE'),ensure_ascii=False))
