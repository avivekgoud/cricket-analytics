# CricIntel Pro: Cricket Analytics, Player Intelligence, and Explainable Match Prediction Platform

An enterprise-grade, data-driven cricket analytics and machine learning system engineered to deliver deep player intelligence, granular head-to-head matchup modeling, stadium pitch evaluations, and explainable match outcome predictions. Powered by authentic ball-by-ball records from 1,169 matches (278,205 deliveries) across 2008 to 2025.

---

## Developer Information

- **Developer:** A Vivek Goud
- **Department:** Department of Computer Science and Engineering
- **Institution:** Vardhaman College of Engineering
- **GitHub Profile:** [https://github.com/avivekgoud](https://github.com/avivekgoud)
- **Repository:** [https://github.com/avivekgoud/cricket-analytics](https://github.com/avivekgoud/cricket-analytics)

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Key Modules and Capabilities](#key-modules-and-capabilities)
3. [Architecture and Technology Stack](#architecture-and-technology-stack)
4. [Project Structure](#project-structure)
5. [Installation and Setup](#installation-and-setup)
6. [Running the Application](#running-the-application)
7. [API Reference](#api-reference)
8. [Automated Testing and Verification](#automated-testing-and-verification)
9. [License and Credits](#license-and-credits)

---

## Project Overview

Traditional cricket analytics dashboards frequently suffer from superficial aggregation, hardcoded statistics, or black-box predictions that lack explanatory context. CricIntel Pro was developed to address these limitations through an end-to-end data pipeline that transforms raw ball-by-ball tournament data into indexed in-memory analytical models.

The system features:
- Complete player profile evaluation across 11 analytical dimensions.
- Head-to-head batter versus bowler duel matrix with statistical sample size verification.
- Mathematical form scoring based on exponential decay recent performance and consistency variance.
- Multi-factor explainable match prediction with additive contribution waterfalls.
- Dual platform architecture: a high-performance FastAPI REST API paired with a modern responsive web SPA, alongside a standalone Streamlit analytics interface.

---

## Key Modules and Capabilities

### 1. Player Intelligence Hub (11 Dedicated Tabs)
- **Global Search:** Fast autocomplete search supporting player full names, short codes, team associations, and common aliases (e.g., King Kohli, Hitman, Thala, Boom Boom).
- **Career and Season Progression:** Season-by-season performance records from 2008 through 2025, tracking runs, batting averages, strike rates, bowling figures, and boundary counts.
- **Non-IPL Player Safeguard:** International cricketers who have never participated in the Indian Premier League (such as Babar Azam, Shaheen Afridi, and Mohammad Rizwan) are accurately flagged with an explicit zero-match IPL record, while seamlessly serving their verified T20I, ODI, Test, and domestic league statistics.
- **Match-by-Match History:** Comprehensive chronological match logs with filters, performance badges, and explicit status indicators for unbatted and unbowled innings.
- **Phase Distributions:** Batting and bowling splits categorized into Powerplay (overs 0-5), Middle Overs (overs 6-14), and Death Overs (overs 15-19).

### 2. Batter vs. Bowler Head-to-Head Duel Matrix
- Direct matchup modeling evaluating balls faced, runs scored, dismissals, strike rate, dot ball percentage, and boundary conversion percentage.
- Sample size safeguards: Automatically flags whether historical data meets reliability thresholds to prevent misleading small-sample conclusions.

### 3. Mathematical Form Scoring Engine
- Computes an objective form rating on a scale from 0 to 100:
  - **45% Weighted Recent Scoring:** Exponential decay weighting prioritizing the most recent matches.
  - **35% Strike Rate Benchmark:** Evaluated against format-specific par scoring rates.
  - **20% Consistency Metric:** Derived from score standard deviation and performance variance.

### 4. Explainable Match Outcome Prediction
- Evaluates fixture outcome probabilities dynamically based on:
  - Team baseline win percentages and historical head-to-head records.
  - Exponential recent team form (last 5 encounters).
  - Venue records, home advantage, and chasing vs. defending win ratios.
  - Dynamic Playing XI strength calculations and depth ratings.
  - Pitch characteristics (Batting paradise, Pace-friendly green track, Slow turner).
  - Toss winner and decision impact (batting first vs. bowling first).
- **Why This Prediction? Factor Decomposition:** Provides a transparent additive breakdown displaying the exact percentage contribution of each independent factor.
- **Confidence Rating:** High, Moderate, or Low confidence score reflecting data sample density.

### 5. Stadium and Pitch Analytics
- Detailed profiles for 57+ cricket venues.
- First and second innings average totals, boundary dimensions, and chasing win percentages.
- Objective friendliness meters for batting, pace bowling, and spin bowling.

### 6. Match Center
- **Upcoming Fixtures:** Pre-match analysis with probable Playing XIs, pitch reports, weather insights, and baseline predictions.
- **Live Match Center:** Real-time situation simulation displaying live scores, CRR, RRR, active partnerships, and ball-by-ball commentary.
- **Historical Match Explorer:** Searchable database of all 1,169 historical IPL scorecards with full batting and bowling summaries.

---

## Architecture and Technology Stack

- **Backend:** FastAPI, Uvicorn, Pydantic, Python 3.10+
- **Data Engineering and Machine Learning:** Pandas, NumPy, Scikit-learn, SciPy
- **Web SPA Frontend:** Semantic HTML5, Modern CSS3 (Variables, Grid, Flexbox), Vanilla ES6+ JavaScript, Chart.js
- **Alternative User Interface:** Streamlit 1.32+
- **Data Compression:** High-efficiency GZIP dataset compression (102.5 MB compressed to 6.3 MB)

---

## Project Structure

```text
cricintel-pro/
├── backend/
│   ├── main.py                     # FastAPI REST API application and static file server
│   └── services/
│       ├── data_loader.py          # Data ingestion, indexing, and player catalogs
│       ├── analytics_engine.py     # Form scoring and phase analytics
│       ├── predictor.py            # Multi-factor explainable prediction engine
│       ├── match_service.py        # Fixtures, live center, and scorecard service
│       ├── news_service.py         # News feed and player availability tracker
│       └── admin_service.py        # Data synchronization and audit logger
├── frontend/
│   ├── index.html                  # Single Page Application layout
│   ├── styles.css                  # Responsive dark and light theme stylesheet
│   └── app.js                      # Client-side routing, Chart.js, and UI logic
├── app.py                          # Streamlit application interface
├── run_server.py                   # One-click FastAPI server launcher
├── test_platform.py                # Automated test suite
├── verify_all.py                   # End-to-end audit verification script
├── requirements.txt                # Python dependencies
├── Players.csv                     # Player biographical metadata
├── IPL.csv.gz                      # Compressed ball-by-ball dataset (6.3 MB)
└── README.md                       # Project documentation
```

---

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/avivekgoud/cricket-analytics.git
cd cricket-analytics
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Application

### Option A: Modern Web SPA and FastAPI Server (Recommended)
```bash
python run_server.py
```
- Open **http://localhost:8000** in your web browser.
- Interactive OpenAPI documentation is accessible at **http://localhost:8000/docs**.

### Option B: Streamlit Platform
```bash
streamlit run app.py
```
- Open **http://localhost:8501** in your web browser.

---

## API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/players/search?q={query}` | Search players by name, role, team, or alias |
| `GET` | `/api/players/{player_id}` | Retrieve comprehensive 11-tab player profile |
| `GET` | `/api/players/{player_id}/matchup?bowler={name}` | Batter vs. bowler head-to-head metrics |
| `GET` | `/api/players/{player_id}/zones` | Wagon wheel and scoring zone distributions |
| `GET` | `/api/players/compare?ids={id1,id2}` | Multi-player side-by-side comparison |
| `GET` | `/api/teams` | List all franchise profiles, records, and squads |
| `GET` | `/api/venues` | Retrieve all venue records and pitch characteristics |
| `POST` | `/api/predict` | Generate explainable outcome prediction |
| `GET` | `/api/matches/upcoming` | Fetch upcoming fixtures with probable XIs |
| `GET` | `/api/matches/live` | Retrieve live match status and situation metrics |
| `GET` | `/api/matches/historical` | Query historical match database with scorecards |
| `GET` | `/api/records` | All-time league batting and bowling records |
| `GET` | `/api/news` | Tournament news and official squad updates |
| `GET` | `/api/availability` | Player fitness and availability tracker |

---

## Automated Testing and Verification

To execute the automated audit and test suite:

```bash
python verify_all.py
```

The test runner verifies:
1. Streamlit compilation and syntax integrity.
2. FastAPI REST endpoints and static file delivery.
3. Accurate indexing of 1,169 matches and 770+ players.
4. Non-IPL player empty-state enforcement (Babar Azam, Shaheen Afridi).
5. Head-to-head matchup accuracy and sample size flags.
6. Predictive engine consistency across varied pitch and toss scenarios.

---

## License and Credits

**Author:** A Vivek Goud  
**Department:** Computer Science and Engineering  
**Institution:** Vardhaman College of Engineering  

This project is licensed under the MIT License. See the LICENSE file for details.