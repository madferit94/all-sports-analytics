import copy,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from integrated_gate import decide

class IntegratedTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.base=Path(self.temp.name)
        (self.base/'evidence.txt').write_text('Synthetic test evidence, not actual team run.',encoding='utf-8')
        self.bundle=dict(run_id='synthetic',match_key='test:1',mode='analysis',agents=[])
        tasks={'director':['operations'],'research':['data'],'analyst':['analysis','prediction'],'builder':['visualization'],'reviewer':['validation','model-evaluation']}
        for ident,parts in tasks.items():
            reports=[]
            for role in parts:
                reports.append(dict(run_id='synthetic',match_key='test:1',role=role,producer_id=ident,status='NOT_IMPLEMENTED' if role in ['prediction','model-evaluation'] else 'DONE',summary='Synthetic test',evidence=[dict(path='evidence.txt',description='Synthetic')],issues=[]))
            self.bundle['agents'].append(dict(agent_id=ident,producer_id=ident,run_id='synthetic',match_key='test:1',reports=reports))
    def tearDown(self):self.temp.cleanup()
    def result(self):return decide(self.bundle,self.base)
    def test_analysis_allowed_without_model_but_prediction_held(self):
        self.assertEqual(self.result()['decision'],'APPROVE')
        self.bundle['mode']='prediction';r=self.result();self.assertEqual(r['decision'],'HOLD');self.assertFalse(r['display_probabilities'])
    def test_reviewer_cannot_be_author(self):
        reviewer=self.bundle['agents'][-1];reviewer['producer_id']='analyst'
        for r in reviewer['reports']:r['producer_id']='analyst'
        self.assertEqual(self.result()['decision'],'REJECT')
    def test_final_director_cannot_be_author(self):
        director=self.bundle['agents'][0];director['producer_id']='analyst'
        for r in director['reports']:r['producer_id']='analyst'
        self.assertEqual(self.result()['decision'],'REJECT')
    def test_capability_cannot_move_to_wrong_owner(self):
        r=self.bundle['agents'][2]['reports'].pop(0)
        r['producer_id']='director';self.bundle['agents'][0]['reports'].append(r)
        self.assertIn('WRONG_AGENT_FOR_analysis',self.result()['reasons'])
    def test_tampered_producer_and_duplicate_rejected(self):
        self.bundle['agents'][1]['reports'][0]['producer_id']='other'
        self.assertEqual(self.result()['decision'],'REJECT')
        self.bundle['agents'][1]['reports'][0]['producer_id']='research'
        self.bundle['agents'][1]['reports'].append(copy.deepcopy(self.bundle['agents'][1]['reports'][0]))
        self.assertIn('DUPLICATE_CAPABILITY_data',self.result()['reasons'])
    def test_skills_exports_and_phase_graph(self):
        team=json.loads((ROOT/'team.json').read_text(encoding='utf-8'));self.assertEqual(len(team['roles']),5)
        seen=set()
        for phase in team['phases']:
            self.assertTrue(set(phase['depends_on'])<=seen);seen.add(phase['id'])
        for member in team['roles']:
            paths=[ROOT/folder/member['skill']/'SKILL.md' for folder in ['skills','.agents/skills','.claude/skills']]
            self.assertEqual(len({p.read_bytes() for p in paths}),1)
        self.assertEqual(len(list((ROOT/'.claude/agents').glob('*.md'))),5)

if __name__=='__main__':unittest.main(verbosity=2)
