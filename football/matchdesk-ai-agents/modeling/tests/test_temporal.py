import copy,sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from train_baseline import build_features,fit,predict,softmax,FEATURES,goals

def fixture(key,day,home='a',away='b',gf='1',ga='0'):
    return dict(match_key=key,source_date=day,league='EPL',season='2023/24',home_team_key=home,away_team_key=away,home_team_name=home,away_team_name=away,home_goals=gf,away_goals=ga,home_xg='1.1',away_xg='0.5')

class TemporalTests(unittest.TestCase):
    def test_csv_integral_decimal_goals_and_invalid_fraction(self):
        self.assertEqual(goals('0.0'),0);self.assertEqual(goals('3.0'),3)
        for bad in ['0.5','nan','-1']:
            with self.assertRaises(ValueError):goals(bad)
    def test_current_and_same_day_results_cannot_leak(self):
        original=[fixture('p','2023-08-01'),fixture('q','2023-08-02'),fixture('r','2023-08-02')]
        before,_=build_features(original,[],'2023-08-10')
        changed=copy.deepcopy(original);changed[1]['home_goals']='9';changed[1]['home_xg']='8.5'
        after,_=build_features(changed,[],'2023-08-10')
        self.assertEqual(before[1]['features'],after[1]['features']);self.assertEqual(before[2]['features'],after[2]['features'])
        self.assertEqual(before[2]['history_keys']['home'],['p'])
    def test_future_target_labels_ignored_and_prior_result_used(self):
        past=[fixture('p','2023-08-01')];target=fixture('f','2023-08-05')
        _,first=build_features(past,[target],'2023-08-03');target['home_goals']='99'
        _,second=build_features(past,[target],'2023-08-03');self.assertEqual(first,second);self.assertNotIn('label',first[0])
        past[0]['home_goals']='5';_,third=build_features(past,[target],'2023-08-03');self.assertNotEqual(first[0]['features'],third[0]['features'])
    def test_boundary_results_excluded(self):
        past=[fixture('p','2023-08-01'),fixture('cutoff','2023-08-03')]
        rows,future=build_features(past,[fixture('f','2023-08-04')],'2023-08-03')
        self.assertEqual(len(rows),1);self.assertEqual(future[0]['history_keys']['home'],['p'])
    def test_stable_probabilities_and_model_serialization(self):
        rows=[]
        for i in range(18):
            rows.append(dict(features=[float(i%4)]*len(FEATURES),label=i%3))
        model=fit(rows,0.1);p=predict(model,rows)
        self.assertTrue(np.all(np.isfinite(p)));self.assertTrue(np.allclose(p.sum(axis=1),1))
        import json
        loaded=json.loads(json.dumps(model));self.assertTrue(np.array_equal(p,predict(loaded,rows)))
        self.assertTrue(np.allclose(softmax(np.asarray([[10000.,-10000.,0.]])),[[1.,0.,0.]]))

if __name__=='__main__':unittest.main(verbosity=2)
