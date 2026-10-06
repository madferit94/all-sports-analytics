import unittest,json,importlib.util,tempfile,hashlib,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def module(name):
    s=importlib.util.spec_from_file_location(name,ROOT/'tools'/(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
c=module('context_cli');g=module('approval_gate')
class TeamTests(unittest.TestCase):
    def record(self,kind='formation'):
        return dict(record_id='TEST_ONLY',kind=kind,team_key='understat:83',match_key='understat:31230',source_url='https://example.org/synthetic-test-only',observed_at='2026-10-06T00:00:00+00:00',fact_status='CONFIRMED',collection_status='COLLECTED',formation='4-3-3',formation_type='NOMINAL_START')
    def test_context_valid_and_wrong_team(self):
        r=self.record();self.assertTrue(c.validate_records([r])['passed']);r['team_key']='understat:88';self.assertFalse(c.validate_records([r])['passed'])
    def test_missing_does_not_mean_zero(self):
        r=self.record();r.update(collection_status='MISSING',fact_status='UNKNOWN',reason='Not fetched')
        for k in ['match_key','formation','formation_type']:r.pop(k)
        self.assertTrue(c.validate_records([r])['passed']);r['formation']=0;self.assertFalse(c.validate_records([r])['passed'])
    def test_lineup_predicted_is_not_confirmed(self):
        r=self.record('lineup');r.update(lineup_type='PREDICTED',players=[dict(name=f'TEST_PLAYER_{i}',starter=True) for i in range(11)])
        self.assertFalse(c.validate_records([r])['passed']);r['fact_status']='PREDICTED';self.assertTrue(c.validate_records([r])['passed'])
    def test_market_value_date_currency_required(self):
        r=self.record('market_value');r.update(valuation_date='2026-10-01',amount=100,currency='EUR',valuation_scope='SQUAD',fact_status='ESTIMATED')
        self.assertTrue(c.validate_records([r])['passed']);r['currency']='euros';self.assertFalse(c.validate_records([r])['passed'])
        r['currency']='EUR';r['amount']=float('nan');self.assertFalse(c.validate_records([r])['passed'])
    def test_missing_model_cannot_approve_prediction(self):
        result=g.decide(dict(mode='prediction',run_id='t',match_key='m',reports={},reviewer_id='approval'))
        self.assertEqual(result['decision'],'HOLD');self.assertFalse(result['display_probabilities'])
    def test_independent_gate_and_tampering(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as td:
            base=Path(td);(base/'evidence.txt').write_text('SYNTHETIC TEST EVIDENCE ONLY',encoding='utf-8')
            reports={role:dict(role=role,run_id='t',match_key='m',producer_id=role,status='DONE',summary='Synthetic test only',issues=[],evidence=[dict(path='evidence.txt')]) for role in ['data','analysis','validation','operations','prediction','model-evaluation']}
            reports['prediction']['probabilities']=dict(home=.4,draw=.3,away=.3);reports['model-evaluation']['model_accepted']=True
            bundle=dict(mode='prediction',run_id='t',match_key='m',reviewer_id='approval',reports=reports)
            self.assertEqual(g.decide(bundle,base)['decision'],'APPROVE')
            self.assertFalse(g.decide(bundle,base)['human_release_authorized'])
            reports['prediction']['probabilities']['home']=.9;self.assertEqual(g.decide(bundle,base)['decision'],'REJECT')
            reports['prediction']['probabilities']['home']=.4;reports['validation']['producer_id']='prediction';self.assertEqual(g.decide(bundle,base)['decision'],'REJECT')
            reports['validation']['producer_id']='validation';reports['data']['evidence'][0]['path']='../outside.txt';self.assertEqual(g.decide(bundle,base)['decision'],'REJECT')
    def test_dependency_graph_and_skill_exports(self):
        team=json.loads((ROOT/'team.json').read_text(encoding='utf-8'));remaining={r['id']:set(r['depends_on']) for r in team['roles']};done=set()
        while remaining:
            ready={r for r,deps in remaining.items() if deps<=done};self.assertTrue(ready,'cycle or missing dependency');done|=ready
            for r in ready:remaining.pop(r)
        self.assertEqual(len(done),10)
        for r in team['roles']:
            payload=(ROOT/'skills'/r['skill']/'SKILL.md').read_bytes()
            for folder in ['.agents/skills','.claude/skills']:self.assertEqual(payload,(ROOT/folder/r['skill']/'SKILL.md').read_bytes())
if __name__=='__main__':unittest.main()
