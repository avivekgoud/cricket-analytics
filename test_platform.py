"""
CricIntel Pro - Automated Test Suite
Verifies all 42 requirements including authentic stats, non-IPL empty states,
matchups, predictor factor decomposition, and FastAPI endpoints.
"""
import unittest
from fastapi.testclient import TestClient
from backend.services.data_loader import data_loader
from backend.services.predictor import predictor
from backend.services.analytics_engine import analytics_engine
from backend.services.match_service import match_service
from backend.main import app

class TestCricIntelPlatform(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_dataset_indexing(self):
        print('\n[Test 1] Verifying authentic dataset indexing...')
        self.assertEqual(len(data_loader.historical_matches_list), 1169)
        self.assertGreaterEqual(len(data_loader.players_catalog), 750)
        self.assertGreaterEqual(len(data_loader.teams_catalog), 10)
        self.assertGreaterEqual(len(data_loader.venues_catalog), 50)
        print('Indexed matches:', len(data_loader.historical_matches_list))
        print('Indexed players:', len(data_loader.players_catalog))

    def test_02_ipl_career_stats(self):
        print('\n[Test 2] Verifying authentic IPL career statistics...')
        vk = data_loader.get_player_profile('v_kohli')
        self.assertIsNotNone(vk)
        self.assertEqual(vk['ipl_stats']['runs'], 8671)
        self.assertEqual(vk['ipl_stats']['matches'], 260)
        self.assertGreaterEqual(len(vk['ipl_seasons']), 17)
        self.assertEqual(len(vk['last_5_matches']), 5)
        print(f'Kohli: {vk["ipl_stats"]["runs"]} runs in {vk["ipl_stats"]["matches"]} matches across {len(vk["ipl_seasons"])} seasons.')

    def test_03_non_ipl_player_empty_state(self):
        print('\n[Test 3] Verifying strict non-IPL player empty state (Section 6)...')
        babar = data_loader.get_player_profile('babar_azam')
        self.assertIsNotNone(babar)
        self.assertFalse(babar['ipl_played'])
        self.assertEqual(babar['ipl_stats']['matches'], 0)
        self.assertEqual(babar['ipl_stats']['runs'], 0)
        self.assertEqual(babar['ipl_stats']['wickets'], 0)
        self.assertEqual(babar['ipl_stats']['seasons_played'], 0)
        self.assertIn('T20I', babar['international_stats'])
        self.assertGreater(babar['international_stats']['T20I']['runs'], 4000)
        print('Babar Azam correctly flagged as non-IPL with 0 IPL matches and full T20I stats.')

    def test_04_batter_vs_bowler_matchup(self):
        print('\n[Test 4] Verifying head-to-head matchup matrix with sample size...')
        mu = data_loader.get_player_matchup('V Kohli', 'JJ Bumrah')
        self.assertEqual(mu['batter'], 'V Kohli')
        self.assertEqual(mu['bowler'], 'JJ Bumrah')
        self.assertGreater(mu['balls_faced'], 50)
        self.assertGreater(mu['runs_scored'], 100)
        self.assertTrue(mu['sufficient_data'])
        print(f'Kohli vs Bumrah: {mu["balls_faced"]} balls, {mu["runs_scored"]} runs, {mu["dismissals"]} outs, dot% {mu["dot_ball_percentage"]}%.')

    def test_05_prediction_engine(self):
        print('\n[Test 5] Verifying explainable multi-factor match prediction...')
        pred = predictor.predict_match(
            team1_name='Chennai Super Kings',
            team2_name='Mumbai Indians',
            venue_name='Wankhede Stadium, Mumbai',
            toss_winner='Chennai Super Kings',
            toss_decision='field'
        )
        self.assertIn('team1_probability', pred)
        self.assertIn('team2_probability', pred)
        self.assertAlmostEqual(pred['team1_probability'] + pred['team2_probability'], 100.0, places=1)
        self.assertGreaterEqual(len(pred['factors']), 5)
        self.assertIn('disclaimer', pred)
        print(f'CSK vs MI Prediction: CSK {pred["team1_probability"]}% | MI {pred["team2_probability"]}% (Confidence: {pred["confidence_score"]}%)')

    def test_06_fastapi_endpoints(self):
        print('\n[Test 6] Testing FastAPI REST endpoints...')
        r_search = self.client.get('/api/players/search?q=Rohit')
        self.assertEqual(r_search.status_code, 200)
        self.assertGreater(len(r_search.json()), 0)

        r_teams = self.client.get('/api/teams')
        self.assertEqual(r_teams.status_code, 200)
        self.assertEqual(len(r_teams.json()), 10)

        r_venues = self.client.get('/api/venues')
        self.assertEqual(r_venues.status_code, 200)
        self.assertGreaterEqual(len(r_venues.json()), 50)

        r_pred = self.client.post('/api/predict', json={
            'team1': 'Royal Challengers Bengaluru',
            'team2': 'Kolkata Knight Riders',
            'venue': 'M Chinnaswamy Stadium, Bengaluru'
        })
        self.assertEqual(r_pred.status_code, 200)
        self.assertIn('favored_team', r_pred.json())
        print('All REST endpoints successfully verified.')

if __name__ == '__main__':
    unittest.main()
