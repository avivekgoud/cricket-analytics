"""
CricIntel Pro - Streamlit Analytics & Prediction Interface
Complete data-driven intelligence powered by authentic 1,169 IPL matches.

Developed by A VIVEK GOUD
Computer Science and Engineering | Vardhaman College of Engineering
"""

import streamlit as st
import pandas as pd
import numpy as np
from backend.services.data_loader import data_loader
from backend.services.predictor import predictor
from backend.services.analytics_engine import analytics_engine
from backend.services.match_service import match_service
from backend.services.news_service import news_service

st.set_page_config(
    page_title="CricIntel Pro - Cricket Analytics Platform",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("🏏 CRICINTEL PRO 2.0")
st.sidebar.caption("Data-Driven Cricket Intelligence Engine")

nav = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "👤 Player Intelligence", "🛡️ Team Analytics", "🏟️ Venues & Pitches", "🔮 Match Predictor", "⚡ Match Center", "📰 News & Squads"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("👨‍💻 **Developer Info**")
st.sidebar.markdown("**A VIVEK GOUD**")
st.sidebar.caption("Computer Science & Engineering\nVardhaman College of Engineering")

# 1. DASHBOARD
if nav == "📊 Dashboard":
    st.title("🏏 Cricket Analytics & Intelligence Platform")
    st.markdown("Authentic data-driven insights across **1,169 matches**, **770+ cricketers**, and multi-tournament intelligence.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Matches Indexed", "1,169", "2008-2025")
    with col2:
        st.metric("Total Deliveries", "278,205", "Ball-by-Ball")
    with col3:
        st.metric("Player Profiles", "771", "IPL & Global")
    with col4:
        st.metric("Stadiums Analyzed", "57", "Pitch Metrics")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🏆 All-Time Top Run Scorers")
        runs_df = pd.DataFrame(data_loader.records_catalog['all_time_runs'])
        st.dataframe(runs_df.head(8), use_container_width=True)
    with c2:
        st.subheader("🎯 All-Time Top Wicket Takers")
        wkts_df = pd.DataFrame(data_loader.records_catalog['all_time_wickets'])
        st.dataframe(wkts_df.head(8), use_container_width=True)

# 2. PLAYER INTELLIGENCE
elif nav == "👤 Player Intelligence":
    st.title("👤 Player Intelligence Hub")
    
    query = st.text_input("🔍 Search any cricketer (e.g. Virat Kohli, Rohit Sharma, Bumrah, Babar Azam, Klaasen)...", "Virat Kohli")
    search_results = data_loader.search_players(query)
    
    if search_results:
        options = {f"{p['display_name']} ({p['role']} - {p['country']})": p['id'] for p in search_results}
        selected_label = st.selectbox("Select Player Profile", list(options.keys()))
        selected_id = options[selected_label]
        
        p = data_loader.get_player_profile(selected_id)
        if p:
            st.markdown(f"## {p['display_name']} {'🟢 (IPL Player)' if p['ipl_played'] else '🟠 (International Player)'}")
            st.caption(f"**Country:** {p['country']} | **Role:** {p['role']} | **Batting:** {p['batting_style']} | **Bowling:** {p['bowling_style']} | **Current Team:** {p['current_team']} | **Status:** {p['status']}")
            
            tabs = st.tabs(["Overview", "Batting", "Bowling", "IPL Career & Seasons", "Last 5 & Matches", "Teams", "Venues", "Opposition", "Form Engine", "Records", "Matchup Matrix"])
            
            # Tab 1: Overview
            with tabs[0]:
                st.subheader("📊 Key Career Metrics")
                st_data = p.get('ipl_stats', {})
                if p['ipl_played']:
                    mc1, mc2, mc3, mc4, mc5 = st.columns(5)
                    mc1.metric("IPL Matches", st_data.get('matches', 0))
                    mc2.metric("IPL Runs", f"{st_data.get('runs', 0):,}")
                    mc3.metric("Batting Avg", st_data.get('average', 0.0))
                    mc4.metric("Strike Rate", st_data.get('strike_rate', 0.0))
                    mc5.metric("IPL Wickets", st_data.get('wickets', 0))
                else:
                    t20i = p.get('international_stats', {}).get('T20I', {})
                    mc1, mc2, mc3, mc4 = st.columns(4)
                    mc1.metric("T20I Matches", t20i.get('matches', 0))
                    mc2.metric("T20I Runs", f"{t20i.get('runs', 0):,}")
                    mc3.metric("T20I Average", t20i.get('average', 0.0))
                    mc4.metric("T20I Strike Rate", t20i.get('strike_rate', 0.0))

            # Tab 4: IPL Career & Seasons
            with tabs[3]:
                if not p['ipl_played']:
                    st.warning("⚠️ **IPL Career: This player has not played an IPL match.**")
                    st.info("""IPL Matches: 0 | IPL Runs: 0 | IPL Wickets: 0 | IPL Seasons: 0

No IPL match data available for this player. International statistics are available under other tabs.""")
                else:
                    st.subheader("📅 Season-by-Season IPL Record")
                    seasons_df = pd.DataFrame(list(p['ipl_seasons'].values()))
                    st.dataframe(seasons_df, use_container_width=True)

            # Tab 5: Last 5 & Matches
            with tabs[4]:
                st.subheader("⏱️ Last 5 Matches")
                if p['last_5_matches']:
                    st.dataframe(pd.DataFrame(p['last_5_matches']), use_container_width=True)
                else:
                    st.write("No recent IPL matches on record.")

            # Tab 8: Opposition
            with tabs[7]:
                st.subheader("⚔️ Performance vs Oppositions")
                if p['opposition_stats']:
                    st.dataframe(pd.DataFrame(list(p['opposition_stats'].values())), use_container_width=True)

            # Tab 9: Form Engine
            with tabs[8]:
                st.subheader("🔥 Mathematical Form Engine")
                f_data = p.get('form_analysis', {})
                st.metric("Calculated Form Rating", f"{f_data.get('form_score', 75.0)} / 100", f"Consistency: {f_data.get('consistency', 80.0)}%")
                st.caption(f_data.get('explanation', ''))
                if f_data.get('last_5_runs'):
                    st.line_chart(f_data['last_5_runs'])

            # Tab 11: Matchup Matrix
            with tabs[10]:
                st.subheader("⚔️ Batter vs Bowler Head-to-Head Matrix")
                bowler_q = st.text_input("Enter Bowler Name to analyze matchup:", "Jasprit Bumrah")
                if bowler_q:
                    mu = data_loader.get_player_matchup(p['short_name'], bowler_q)
                    st.json(mu)

# 5. MATCH PREDICTOR
elif nav == "🔮 Match Predictor":
    st.title("🔮 Explainable Match Prediction Engine")
    
    colA, colB, colC = st.columns(3)
    teams_list = list(data_loader.teams_catalog.keys())
    venues_list = [v['name'] for v in data_loader.venues_catalog.values()]
    
    with colA:
        t1 = st.selectbox("Select Team 1", [data_loader.teams_catalog[k]['name'] for k in teams_list], index=0)
    with colB:
        t2 = st.selectbox("Select Team 2", [data_loader.teams_catalog[k]['name'] for k in teams_list], index=1)
    with colC:
        v = st.selectbox("Select Venue", venues_list, index=0)
        
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        toss_winner = st.selectbox("Toss Winner (Optional)", ["None", t1, t2])
    with p_col2:
        toss_dec = st.selectbox("Toss Decision", ["field", "bat"])
        
    if st.button("🚀 Calculate Match Prediction", type="primary"):
        pred = predictor.predict_match(
            team1_name=t1,
            team2_name=t2,
            venue_name=v,
            toss_winner=None if toss_winner == "None" else toss_winner,
            toss_decision=toss_dec
        )
        
        st.markdown(f"### Predicted Winner: **{pred['favored_team']}** ({pred['favored_probability']}%)")
        st.progress(int(pred['team1_probability']))
        st.caption(f"**{pred['team1']}:** {pred['team1_probability']}% | **{pred['team2']}:** {pred['team2_probability']}% | **Confidence:** {pred['confidence_level']} ({pred['confidence_score']}%)")
        
        st.markdown("#### 🔍 Why this prediction? (Additive Factor Decomposition)")
        st.dataframe(pd.DataFrame(pred['factors']), use_container_width=True)
        st.info(f"ℹ️ {pred['disclaimer']}")

# 6. MATCH CENTER
elif nav == "⚡ Match Center":
    st.title("⚡ Match Center")
    m_tabs = st.tabs(["Upcoming Fixtures", "Live Match Simulation", "Historical Matches"])
    with m_tabs[0]:
        st.subheader("📅 Upcoming IPL Clashes")
        up = match_service.get_upcoming_matches()
        for match in up:
            st.markdown(f"**{match['team1']} vs {match['team2']}** - {match['date']} at {match['venue']}")
            st.caption(f"Pre-Match Favorite: {match['prediction']['favored_team']} ({match['prediction']['favored_probability']}%)")
            st.markdown("---")
    with m_tabs[1]:
        st.subheader("🔴 Live Match Center")
        live = match_service.get_live_match()
        st.write(f"**{live['innings1']['team']}** {live['innings1']['runs']}/{live['innings1']['wickets']} vs **{live['innings2']['team']}** {live['innings2']['runs']}/{live['innings2']['wickets']} (Overs: {live['innings2']['overs']})")
        st.info(live['situation_analysis'])
    with m_tabs[2]:
        st.subheader("📜 1,169+ Historical Scorecards")
        h_data = match_service.get_historical_matches(limit=30)
        st.dataframe(pd.DataFrame(h_data['matches']), use_container_width=True)

# 7. NEWS
elif nav == "📰 News & Squads":
    st.title("📰 News & Player Availability")
    n_list = news_service.get_news()
    for item in n_list:
        st.markdown(f"### {item['title']}")
        st.caption(f"{item['category']} • {item['date']} • Source: {item['source']}")
        st.write(item['summary'])
        st.markdown("---")