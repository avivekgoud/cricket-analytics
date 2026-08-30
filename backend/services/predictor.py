"""
Cricket Analytics Platform - Explainable Multi-Factor Prediction Engine
Predicts match outcome probabilities with dynamic Playing XI strength,
pitch conditions, toss impact, and additive factor decomposition.
"""

import os, math, numpy as np, pandas as pd
from typing import Dict, List, Any, Optional
from backend.services.data_loader import data_loader

class ExplainablePredictor:
    def __init__(self):
        pass

    def predict_match(
        self,
        team1_name: str,
        team2_name: str,
        venue_name: str,
        toss_winner: Optional[str] = None,
        toss_decision: str = 'field',
        team1_xi: Optional[List[str]] = None,
        team2_xi: Optional[List[str]] = None,
        pitch_type: Optional[str] = None
    ) -> Dict[str, Any]:
        t1 = data_loader.normalize_team(team1_name)
        t2 = data_loader.normalize_team(team2_name)
        
        t1_id = data_loader.teams_catalog.get(data_loader.normalize_team(t1), {}).get('id', '')
        t2_id = data_loader.teams_catalog.get(data_loader.normalize_team(t2), {}).get('id', '')
        
        t1_profile = data_loader.teams_catalog.get(t1_id, {})
        t2_profile = data_loader.teams_catalog.get(t2_id, {})
        
        # 1. Base team win percentages
        t1_win_pct = t1_profile.get('win_percentage', 50.0)
        t2_win_pct = t2_profile.get('win_percentage', 50.0)
        
        # 2. Recent form factor (last 5 matches)
        t1_form = t1_profile.get('recent_form', ['W', 'L', 'W', 'W', 'L'])
        t2_form = t2_profile.get('recent_form', ['L', 'W', 'L', 'W', 'L'])
        t1_form_score = (t1_form.count('W') / max(1, len(t1_form))) * 100.0
        t2_form_score = (t2_form.count('W') / max(1, len(t2_form))) * 100.0
        form_delta = (t1_form_score - t2_form_score) * 0.12 # weight factor
        
        # 3. Head-to-head factor
        h2h_data = t1_profile.get('head_to_head', {}).get(t2, {'matches': 0, 'wins': 0, 'losses': 0, 'win_pct': 50.0})
        h2h_delta = (h2h_data.get('win_pct', 50.0) - 50.0) * 0.15
        
        # 4. Venue record factor
        v_matches = [m for m in data_loader.historical_matches_list if venue_name.lower() in m['venue'].lower() or m['venue'].lower() in venue_name.lower()]
        t1_v_wins = sum(1 for m in v_matches if m['winner'] == t1)
        t1_v_total = sum(1 for m in v_matches if m['team1'] == t1 or m['team2'] == t1)
        t2_v_wins = sum(1 for m in v_matches if m['winner'] == t2)
        t2_v_total = sum(1 for m in v_matches if m['team1'] == t2 or m['team2'] == t2)
        
        t1_v_pct = (t1_v_wins / t1_v_total * 100.0) if t1_v_total > 0 else t1_win_pct
        t2_v_pct = (t2_v_wins / t2_v_total * 100.0) if t2_v_total > 0 else t2_win_pct
        venue_delta = (t1_v_pct - t2_v_pct) * 0.10
        
        # 5. Playing XI strength calculation
        squad1 = team1_xi if team1_xi and len(team1_xi) >= 5 else t1_profile.get('squad', [])[:11]
        squad2 = team2_xi if team2_xi and len(team2_xi) >= 5 else t2_profile.get('squad', [])[:11]
        
        def get_xi_power(squad_list):
            bat_score = 0.0
            bowl_score = 0.0
            for name in squad_list:
                p_prof = data_loader.get_player_profile(name)
                if p_prof and p_prof.get('ipl_stats'):
                    st = p_prof['ipl_stats']
                    bat_score += min(100.0, (st.get('runs', 0) / 2500.0) * 50.0 + (st.get('strike_rate', 120.0) / 160.0) * 50.0)
                    bowl_score += min(100.0, (st.get('wickets', 0) / 100.0) * 60.0 + (max(0, 10.0 - st.get('economy', 8.5)) / 4.0) * 40.0)
                else:
                    bat_score += 45.0
                    bowl_score += 45.0
            return (bat_score / max(1, len(squad_list)), bowl_score / max(1, len(squad_list)))
        
        t1_bat, t1_bowl = get_xi_power(squad1)
        t2_bat, t2_bowl = get_xi_power(squad2)
        xi_delta = ((t1_bat + t1_bowl) - (t2_bat + t2_bowl)) * 0.08
        
        # 6. Toss impact factor
        toss_delta = 0.0
        if toss_winner:
            toss_w = data_loader.normalize_team(toss_winner)
            is_t1_toss = (toss_w == t1)
            venue_chasing_bias = 52.0 # default
            for v_obj in data_loader.venues_catalog.values():
                if venue_name.lower() in v_obj['name'].lower():
                    venue_chasing_bias = v_obj['chasing_win_pct']
                    break
            
            if toss_decision == 'field':
                adv = (venue_chasing_bias - 50.0) * 0.15
            else:
                adv = ((100.0 - venue_chasing_bias) - 50.0) * 0.15
            toss_delta = adv if is_t1_toss else -adv

        # 7. Pitch & Matchup factor
        pitch_delta = 0.0
        if pitch_type:
            pt = pitch_type.lower()
            if 'pace' in pt or 'seam' in pt:
                pitch_delta = (t1_bowl - t2_bowl) * 0.04
            elif 'spin' in pt or 'slow' in pt:
                pitch_delta = (t1_bat - t2_bat) * 0.04
        
        # Base logit aggregation
        base_delta = (t1_win_pct - t2_win_pct) * 0.15
        total_delta = base_delta + form_delta + h2h_delta + venue_delta + xi_delta + toss_delta + pitch_delta
        
        # Softmax probability
        prob_t1 = round(1.0 / (1.0 + math.exp(-total_delta / 12.0)) * 100.0, 1)
        prob_t1 = max(18.0, min(82.0, prob_t1))
        prob_t2 = round(100.0 - prob_t1, 1)
        
        # Confidence score
        sample_strength = min(1.0, (h2h_data.get('matches', 0) + t1_v_total + t2_v_total) / 25.0)
        confidence_pct = round(60.0 + (sample_strength * 28.0) + (abs(prob_t1 - 50.0) * 0.25), 1)
        confidence_level = "High Confidence" if confidence_pct >= 75.0 else ("Moderate Confidence" if confidence_pct >= 65.0 else "Low Confidence")
        
        # Factor breakdown
        factors = [
            {'name': 'Team Baseline Strength', 'impact_pct': round(base_delta, 1), 'favors': t1 if base_delta >= 0 else t2, 'detail': f'{t1} ({t1_win_pct:.1f}%) vs {t2} ({t2_win_pct:.1f}%) all-time win rate'},
            {'name': 'Recent Form Advantage', 'impact_pct': round(abs(form_delta), 1), 'favors': t1 if form_delta >= 0 else t2, 'detail': f'{t1} ({"-".join(t1_form)}) vs {t2} ({"-".join(t2_form)}) in last 5'},
            {'name': 'Head-to-Head Record', 'impact_pct': round(abs(h2h_delta), 1), 'favors': t1 if h2h_delta >= 0 else t2, 'detail': f'{h2h_data.get("wins", 0)} wins in {h2h_data.get("matches", 0)} meetings'},
            {'name': 'Venue & Conditions Record', 'impact_pct': round(abs(venue_delta), 1), 'favors': t1 if venue_delta >= 0 else t2, 'detail': f'{t1} {t1_v_pct:.1f}% vs {t2} {t2_v_pct:.1f}% at {venue_name.split(",")[0]}'},
            {'name': 'Playing XI Lineup Strength', 'impact_pct': round(abs(xi_delta), 1), 'favors': t1 if xi_delta >= 0 else t2, 'detail': 'Calculated aggregate form & quality of selected 11 players'},
            {'name': 'Toss & Decision Impact', 'impact_pct': round(abs(toss_delta), 1), 'favors': t1 if toss_delta >= 0 else t2, 'detail': f'Toss winner chose to {toss_decision}' if toss_winner else 'Toss not yet conducted'}
        ]
        
        favored_team = t1 if prob_t1 >= prob_t2 else t2
        favored_pct = max(prob_t1, prob_t2)
        underdog_team = t2 if favored_team == t1 else t1
        underdog_pct = min(prob_t1, prob_t2)

        return {
            'team1': t1,
            'team2': t2,
            'team1_probability': prob_t1,
            'team2_probability': prob_t2,
            'favored_team': favored_team,
            'favored_probability': favored_pct,
            'underdog_team': underdog_team,
            'underdog_probability': underdog_pct,
            'confidence_score': confidence_pct,
            'confidence_level': confidence_level,
            'venue': venue_name,
            'factors': factors,
            'disclaimer': 'Prediction based on available historical and statistical data. Sports outcomes carry inherent variance.'
        }

predictor = ExplainablePredictor()
