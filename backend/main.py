"""
Cricket Analytics Platform - FastAPI Main Server
REST API endpoints and Static Web Application Server
"""

import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional, List
from pydantic import BaseModel

from backend.services.data_loader import data_loader
from backend.services.analytics_engine import analytics_engine
from backend.services.predictor import predictor
from backend.services.match_service import match_service
from backend.services.news_service import news_service
from backend.services.admin_service import admin_service

app = FastAPI(
    title="Cricket Analytics & Prediction Platform",
    description="Professional cricket analytics, player intelligence, venue analysis, and explainable match prediction engine.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    team1: str
    team2: str
    venue: str
    toss_winner: Optional[str] = None
    toss_decision: Optional[str] = "field"
    team1_xi: Optional[List[str]] = None
    team2_xi: Optional[List[str]] = None
    pitch_type: Optional[str] = None

# Players Endpoints (Specific static routes FIRST, dynamic path params second)
@app.get("/api/players/search")
def search_players(q: str = Query("", description="Search term")):
    return data_loader.search_players(q)

@app.get("/api/players/compare")
def compare_players(ids: str = Query(..., description="Comma separated player IDs")):
    id_list = [i.strip() for i in ids.split(",") if i.strip()]
    profiles = []
    for pid in id_list:
        p = data_loader.get_player_profile(pid)
        if p:
            profiles.append(p)
    return profiles

@app.get("/api/players/{player_id}")
def get_player(player_id: str):
    p = data_loader.get_player_profile(player_id)
    if not p:
        raise HTTPException(status_code=404, detail="Player not found")
    return p

@app.get("/api/players/{player_id}/matchup")
def get_player_matchup(player_id: str, bowler: str = Query(...)):
    return data_loader.get_player_matchup(player_id, bowler)

@app.get("/api/players/{player_id}/zones")
def get_player_zones(player_id: str):
    p = data_loader.get_player_profile(player_id)
    if not p:
        raise HTTPException(status_code=404, detail="Player not found")
    return analytics_engine.get_scoring_zones(p['short_name'])

# Teams Endpoints (Specific static routes FIRST, dynamic path params second)
@app.get("/api/teams/compare")
def compare_teams(team1: str = Query(...), team2: str = Query(...)):
    t1 = data_loader.teams_catalog.get(team1.lower())
    t2 = data_loader.teams_catalog.get(team2.lower())
    if not t1 or not t2:
        raise HTTPException(status_code=404, detail="One or both teams not found")
    return {'team1': t1, 'team2': t2}

@app.get("/api/teams")
def get_teams():
    return list(data_loader.teams_catalog.values())

@app.get("/api/teams/{team_id}")
def get_team(team_id: str):
    t = data_loader.teams_catalog.get(team_id.lower())
    if not t:
        raise HTTPException(status_code=404, detail="Team not found")
    return t

# Venues Endpoints
@app.get("/api/venues")
def get_venues():
    return list(data_loader.venues_catalog.values())

@app.get("/api/venues/{venue_id}")
def get_venue(venue_id: str):
    v = data_loader.venues_catalog.get(venue_id.lower())
    if not v:
        raise HTTPException(status_code=404, detail="Venue not found")
    return v

# Matches Endpoints (Specific static routes FIRST, dynamic path params second)
@app.get("/api/matches/upcoming")
def get_upcoming_matches():
    return match_service.get_upcoming_matches()

@app.get("/api/matches/live")
def get_live_match():
    return match_service.get_live_match()

@app.get("/api/matches/historical")
def get_historical_matches(
    season: Optional[str] = "All",
    team: Optional[str] = "All",
    venue: Optional[str] = "All",
    search: Optional[str] = "",
    page: int = 1,
    limit: int = 20
):
    return match_service.get_historical_matches(season, team, venue, search, page, limit)

@app.get("/api/matches/{match_id}")
def get_match_scorecard(match_id: int):
    sc = match_service.get_match_scorecard(match_id)
    if not sc:
        raise HTTPException(status_code=404, detail="Match not found")
    return sc

# Prediction Endpoint
@app.post("/api/predict")
def predict_outcome(req: PredictRequest):
    return predictor.predict_match(
        team1_name=req.team1,
        team2_name=req.team2,
        venue_name=req.venue,
        toss_winner=req.toss_winner,
        toss_decision=req.toss_decision or "field",
        team1_xi=req.team1_xi,
        team2_xi=req.team2_xi,
        pitch_type=req.pitch_type
    )

# Records & News
@app.get("/api/records")
def get_records():
    return data_loader.records_catalog

@app.get("/api/news")
def get_news():
    return news_service.get_news()

@app.get("/api/availability")
def get_availability():
    return news_service.get_availability()

@app.get("/api/admin/status")
def get_admin_status():
    return admin_service.get_status()

# Mount Frontend static files
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    def serve_spa():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))