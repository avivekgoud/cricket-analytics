import py_compile
from fastapi.testclient import TestClient
from backend.main import app
from backend.services.data_loader import data_loader
from backend.services.predictor import predictor
from backend.services.analytics_engine import analytics_engine

print("=== 1. VERIFYING STREAMLIT APP SYNTAX ===")
py_compile.compile("app.py", doraise=True)
print("[OK] app.py compiles cleanly with zero syntax errors!")

print("\n=== 2. VERIFYING FASTAPI TEST CLIENT ENDPOINTS ===")
client = TestClient(app)

# Root SPA & Static files
r_root = client.get("/")
assert r_root.status_code == 200, f"Root failed {r_root.status_code}"
assert "CricIntel" in r_root.text or "cricket" in r_root.text.lower(), "Root missing brand text"
print("[OK] GET / (SPA index.html) returned 200 OK")

r_css = client.get("/static/styles.css")
assert r_css.status_code == 200, f"CSS failed {r_css.status_code}"
print("[OK] GET /static/styles.css returned 200 OK")

r_js = client.get("/static/app.js")
assert r_js.status_code == 200, f"JS failed {r_js.status_code}"
print("[OK] GET /static/app.js returned 200 OK")

# JSON Endpoints
endpoints = [
    ("/api/players/search?q=Kohli", "Search Kohli"),
    ("/api/players/search?q=Dhoni", "Search Dhoni"),
    ("/api/players/v_kohli", "Profile Kohli"),
    ("/api/players/ms_dhoni", "Profile MS Dhoni"),
    ("/api/players/v_kohli/matchup?bowler=JJ%20Bumrah", "Matchup Kohli vs Bumrah"),
    ("/api/players/v_kohli/zones", "Scoring Zones Kohli"),
    ("/api/players/compare?ids=v_kohli,rg_sharma", "Compare Kohli & Rohit"),
    ("/api/teams", "All Teams List"),
    ("/api/teams/csk", "CSK Team Profile"),
    ("/api/teams/compare?team1=csk&team2=mi", "Compare CSK vs MI"),
    ("/api/venues", "All Venues List"),
    ("/api/matches/upcoming", "Upcoming Matches"),
    ("/api/matches/live", "Live Match Simulation"),
    ("/api/matches/historical?season=2024&limit=5", "Historical Matches 2024"),
    ("/api/records", "All-Time Records"),
    ("/api/news", "News Feed"),
    ("/api/availability", "Player Availability"),
    ("/api/admin/status", "Admin Status")
]

for ep, label in endpoints:
    r = client.get(ep)
    assert r.status_code == 200, f"Endpoint {ep} failed: {r.status_code}"
    print(f" [OK] GET {ep} -> {label} (200 OK)")

print("\n=== 3. VERIFYING PREDICTION ENDPOINT WITH VARIED CONDITIONS ===")
test_payloads = [
    {"team1": "Chennai Super Kings", "team2": "Mumbai Indians", "venue": "Wankhede Stadium, Mumbai", "pitch_type": "Pace friendly", "toss_winner": "Mumbai Indians", "toss_decision": "field"},
    {"team1": "Royal Challengers Bengaluru", "team2": "Kolkata Knight Riders", "venue": "M Chinnaswamy Stadium, Bengaluru", "pitch_type": "Batting paradise", "toss_winner": "Royal Challengers Bengaluru", "toss_decision": "bat"},
    {"team1": "Sunrisers Hyderabad", "team2": "Rajasthan Royals", "venue": "Rajiv Gandhi International Stadium, Uppal, Hyderabad", "pitch_type": "Balanced", "toss_winner": None, "toss_decision": "field"}
]

for idx, payload in enumerate(test_payloads, 1):
    r_pred = client.post("/api/predict", json=payload)
    assert r_pred.status_code == 200, f"Predict failed: {r_pred.status_code}"
    res = r_pred.json()
    assert "favored_team" in res and "confidence_score" in res and len(res["factors"]) >= 5
    t1_name = payload["team1"]
    t2_name = payload["team2"]
    fav = res["favored_team"]
    prob = res["favored_probability"]
    conf = res["confidence_score"]
    print(f" [OK] Scenario {idx}: {t1_name} vs {t2_name} -> Favored: {fav} ({prob}%, Conf: {conf}%)")

print("\n=== 4. VERIFYING ALL-TIME IPL STATISTICAL ACCURACY ===")
kohli = data_loader.get_player_profile("v_kohli")
assert kohli["ipl_stats"]["runs"] == 8671, f"Expected 8671, got {kohli['ipl_stats']['runs']}"
assert kohli["ipl_stats"]["matches"] == 260
print(f" [OK] Virat Kohli: {kohli['ipl_stats']['runs']} runs in {kohli['ipl_stats']['matches']} matches.")

bumrah = data_loader.get_player_profile("jj_bumrah")
assert bumrah["ipl_stats"]["wickets"] == 186, f"Expected 186, got {bumrah['ipl_stats']['wickets']}"
print(f" [OK] Jasprit Bumrah: {bumrah['ipl_stats']['wickets']} wickets, Economy: {bumrah['ipl_stats']['economy']}.")

chahal = data_loader.get_player_profile("ys_chahal")
assert chahal["ipl_stats"]["wickets"] >= 200
print(f" [OK] Yuzvendra Chahal: {chahal['ipl_stats']['wickets']} wickets (All-time IPL leader).")

print("\n" + "="*55)
print(" ALL AUDIT CATEGORIES PASSED WITH 100% SUCCESS!")
print("="*55)