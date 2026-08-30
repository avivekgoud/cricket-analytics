"""
Cricket Analytics Platform - Match Center Service
Upcoming Fixtures, Interactive Live Match Center, and 1,169+ Historical Scorecards.
"""

import time
from typing import Dict, List, Any, Optional
from backend.services.data_loader import data_loader
from backend.services.predictor import predictor

class MatchService:
    def __init__(self):
        self.upcoming_matches = [
            {
                'id': 'up_2026_01',
                'team1': 'Chennai Super Kings',
                'team2': 'Mumbai Indians',
                'date': '2026-09-05',
                'time': '19:30 IST',
                'venue': 'Wankhede Stadium, Mumbai',
                'status': 'Upcoming',
                'toss_status': 'Toss at 19:00 IST',
                'pitch_report': 'True bounce, high scoring surface with slight early swing and evening dew factor.',
                'weather': '29°C, 65% Humidity, Clear Sky',
                'team1_xi': ['Ruturaj Gaikwad', 'Rachin Ravindra', 'Shivam Dube', 'Daryl Mitchell', 'Ravindra Jadeja', 'MS Dhoni', 'Moeen Ali', 'Deepak Chahar', 'Tushar Deshpande', 'Matheesha Pathirana', 'Mustafizur Rahman'],
                'team2_xi': ['Rohit Sharma', 'Ishan Kishan', 'Suryakumar Yadav', 'Tilak Varma', 'Hardik Pandya', 'Tim David', 'Mohammad Nabi', 'Gerald Coetzee', 'Piyush Chawla', 'Jasprit Bumrah', 'Nuwan Thushara'],
                'xi_status': 'Probable Playing XI'
            },
            {
                'id': 'up_2026_02',
                'team1': 'Royal Challengers Bengaluru',
                'team2': 'Kolkata Knight Riders',
                'date': '2026-09-06',
                'time': '19:30 IST',
                'venue': 'M Chinnaswamy Stadium, Bengaluru',
                'status': 'Upcoming',
                'toss_status': 'Toss at 19:00 IST',
                'pitch_report': 'Short boundaries, lightning outfield, 200+ par score with high sixes potential.',
                'weather': '26°C, 70% Humidity, Partly Cloudy',
                'team1_xi': ['Virat Kohli', 'Faf du Plessis', 'Will Jacks', 'Rajat Patidar', 'Glenn Maxwell', 'Cameron Green', 'Dinesh Karthik', 'Mahipal Lomror', 'Karn Sharma', 'Mohammed Siraj', 'Yash Dayal'],
                'team2_xi': ['Philip Salt', 'Sunil Narine', 'Venkatesh Iyer', 'Shreyas Iyer', 'Rinku Singh', 'Andre Russell', 'Ramandeep Singh', 'Mitchell Starc', 'Varun Chakaravarthy', 'Harshit Rana', 'Vaibhav Arora'],
                'xi_status': 'Probable Playing XI'
            },
            {
                'id': 'up_2026_03',
                'team1': 'Sunrisers Hyderabad',
                'team2': 'Rajasthan Royals',
                'date': '2026-09-08',
                'time': '19:30 IST',
                'venue': 'Rajiv Gandhi International Stadium, Uppal, Hyderabad',
                'status': 'Upcoming',
                'toss_status': 'Toss at 19:00 IST',
                'pitch_report': 'Flat, high-tempo track favoring boundary hitters in powerplay.',
                'weather': '31°C, 55% Humidity, Clear Sky',
                'team1_xi': ['Travis Head', 'Abhishek Sharma', 'Rahul Tripathi', 'Heinrich Klaasen', 'Nitish Kumar Reddy', 'Abdul Samad', 'Shahbaz Ahmed', 'Pat Cummins', 'Bhuvneshwar Kumar', 'Jaydev Unadkat', 'T Natarajan'],
                'team2_xi': ['Yashasvi Jaiswal', 'Jos Buttler', 'Sanju Samson', 'Riyan Parag', 'Shimron Hetmyer', 'Dhruv Jurel', 'Ravichandran Ashwin', 'Trent Boult', 'Avesh Khan', 'Sandeep Sharma', 'Yuzvendra Chahal'],
                'xi_status': 'Probable Playing XI'
            }
        ]

    def get_upcoming_matches(self) -> List[Dict[str, Any]]:
        results = []
        for m in self.upcoming_matches:
            pred = predictor.predict_match(
                team1_name=m['team1'],
                team2_name=m['team2'],
                venue_name=m['venue'],
                team1_xi=m['team1_xi'],
                team2_xi=m['team2_xi']
            )
            item = dict(m)
            item['prediction'] = pred
            results.append(item)
        return results

    def get_live_match(self) -> Dict[str, Any]:
        return {
            'match_id': 'live_2026_ipl_final',
            'tournament': 'IPL 2026 Super Clash',
            'team1': 'Royal Challengers Bengaluru',
            'team2': 'Chennai Super Kings',
            'venue': 'M Chinnaswamy Stadium, Bengaluru',
            'status': 'Live - 2nd Innings',
            'toss_summary': 'CSK won the toss and elected to field',
            'innings1': {
                'team': 'Royal Challengers Bengaluru',
                'runs': 218,
                'wickets': 5,
                'overs': '20.0',
                'run_rate': 10.9,
                'top_performers': ['Virat Kohli 82 (48)', 'Rajat Patidar 54 (28)', 'Mustafizur 2/38']
            },
            'innings2': {
                'team': 'Chennai Super Kings',
                'runs': 164,
                'wickets': 3,
                'overs': '15.2',
                'crr': 10.69,
                'rrr': 11.78,
                'target': 219,
                'runs_needed': 55,
                'balls_remaining': 28,
                'striker': {'name': 'Ruturaj Gaikwad', 'runs': 76, 'balls': 44, 'fours': 8, 'sixes': 3, 'sr': 172.7},
                'non_striker': {'name': 'Ravindra Jadeja', 'runs': 24, 'balls': 12, 'fours': 2, 'sixes': 1, 'sr': 200.0},
                'current_bowler': {'name': 'Mohammed Siraj', 'overs': '3.2', 'runs': 34, 'wickets': 1, 'econ': 10.2},
                'partnership': {'runs': 48, 'balls': 24, 'rr': 12.0}
            },
            'recent_balls': ['1', '4', '6', '1', '2', '4', '1', 'W', '6', '2'],
            'win_probability': {
                'team1_pct': 58.4,
                'team2_pct': 41.6,
                'favored': 'Royal Challengers Bengaluru'
            },
            'situation_analysis': 'CSK requires 55 runs from 28 balls at 11.78 RRR. Ruturaj Gaikwad is well-set on 76*. RCB defending tightly with Siraj bowling death overs.'
        }

    def get_historical_matches(
        self,
        season: Optional[str] = None,
        team: Optional[str] = None,
        venue: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        limit: int = 20
    ) -> Dict[str, Any]:
        filtered = data_loader.historical_matches_list
        
        if season and season != 'All':
            filtered = [m for m in filtered if m['season'] == season]
        
        if team and team != 'All':
            t_norm = data_loader.normalize_team(team)
            filtered = [m for m in filtered if m['team1'] == t_norm or m['team2'] == t_norm]
            
        if venue and venue != 'All':
            filtered = [m for m in filtered if venue.lower() in m['venue'].lower()]
            
        if search and search.strip():
            q = search.lower().strip()
            filtered = [
                m for m in filtered if (
                    q in m['team1'].lower() or
                    q in m['team2'].lower() or
                    q in m['venue'].lower() or
                    q in m['winner'].lower() or
                    q in m['player_of_match'].lower() or
                    q in str(m['date']).lower()
                )
            ]

        total = len(filtered)
        start = (page - 1) * limit
        end = start + limit
        paged_items = filtered[start:end]

        return {
            'total_matches': total,
            'page': page,
            'limit': limit,
            'total_pages': max(1, (total + limit - 1) // limit),
            'matches': paged_items
        }

    def get_match_scorecard(self, match_id: int) -> Optional[Dict[str, Any]]:
        df_m = data_loader.df_balls[data_loader.df_balls['match_id'] == match_id]
        if len(df_m) == 0:
            return None

        match_meta = next((m for m in data_loader.historical_matches_list if m['match_id'] == match_id), None)
        
        inns1_df = df_m[df_m['innings'] == 1]
        inns2_df = df_m[df_m['innings'] == 2]

        def parse_innings_card(df_inns):
            if len(df_inns) == 0:
                return {'batting': [], 'bowling': [], 'total_runs': 0, 'wickets': 0, 'overs': '0.0'}
            
            # Batting card
            batters_list = []
            for b in df_inns['batter'].unique():
                df_b = df_inns[df_inns['batter'] == b]
                b_runs = int(df_b['runs_batter'].sum())
                b_balls = len(df_b)
                b_4s = int((df_b['runs_batter'] == 4).sum())
                b_6s = int((df_b['runs_batter'] == 6).sum())
                b_sr = round(b_runs / b_balls * 100, 1) if b_balls > 0 else 0.0
                
                # Dismissal info
                out_rows = df_inns[df_inns['player_out'] == b]
                if len(out_rows) > 0:
                    kind = out_rows['wicket_kind'].iloc[0]
                    bowler = out_rows['bowler'].iloc[0]
                    dismissal = f"{kind} b {bowler}"
                else:
                    dismissal = "not out"

                batters_list.append({
                    'batter': b,
                    'dismissal': dismissal,
                    'runs': b_runs,
                    'balls': b_balls,
                    'fours': b_4s,
                    'sixes': b_6s,
                    'strike_rate': b_sr
                })

            # Bowling card
            bowlers_list = []
            for w in df_inns['bowler'].unique():
                df_w = df_inns[df_inns['bowler'] == w]
                w_balls = len(df_w)
                w_overs = f"{w_balls // 6}.{w_balls % 6}"
                w_runs = int(df_w['runs_bowler'].sum()) if 'runs_bowler' in df_w.columns else int(df_w['runs_total'].sum())
                w_wkts = int((df_w['bowler_wicket'] == True).sum()) if 'bowler_wicket' in df_w.columns else len(df_w['player_out'].dropna())
                w_econ = round(w_runs / (w_balls / 6.0), 2) if w_balls > 0 else 0.0

                bowlers_list.append({
                    'bowler': w,
                    'overs': w_overs,
                    'runs_conceded': w_runs,
                    'wickets': w_wkts,
                    'economy': w_econ
                })

            total_runs = int(df_inns['runs_total'].sum())
            total_wkts = int(df_inns['player_out'].dropna().count())
            balls_cnt = len(df_inns)
            overs_str = f"{balls_cnt // 6}.{balls_cnt % 6}"

            return {
                'team': df_inns['batting_team_clean'].iloc[0],
                'batting': batters_list,
                'bowling': bowlers_list,
                'total_runs': total_runs,
                'wickets': total_wkts,
                'overs': overs_str
            }

        inns1_card = parse_innings_card(inns1_df)
        inns2_card = parse_innings_card(inns2_df)

        return {
            'match_id': match_id,
            'match_info': match_meta,
            'innings1': inns1_card,
            'innings2': inns2_card
        }

match_service = MatchService()
