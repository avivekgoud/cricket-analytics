<div align="center">

# 🏏 CricIntel Pro 2.0
### Advanced Cricket Analytics, Player Intelligence & Explainable Match Prediction Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B.svg)](https://streamlit.io)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458.svg)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

*An enterprise-grade, data-driven cricket analytics platform powered by authentic ball-by-ball records from 1,169 matches across 2008–2025.*

</div>

---

## 📌 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture & Tech Stack](#-architecture--tech-stack)
- [Repository Structure](#-repository-structure)
- [Quick Start](#-quick-start)
- [API Endpoints](#-api-endpoints)
- [Verification & Automated Tests](#-verification--automated-tests)
- [Contributing & License](#-contributing--license)

---

## 🌟 Overview

**CricIntel Pro** is a modern cricket intelligence system that unifies player scouting, granular head-to-head duel modeling, stadium pitch analytics, and explainable outcome predictions. It indexes over **278,000 deliveries** and **770+ cricketers** into high-speed in-memory models.

---

## 🚀 Key Features

### 1. 👤 11-Tab Player Intelligence Hub
- **Instant Global Search**: Fuzzy autocomplete matching by official names, short codes, and famous aliases (*King Kohli, Hitman, Thala, Boom Boom, Universe Boss*).
- **Authentic Career Records**: Season-by-season IPL stats (2008–2025), batting averages, strike rates, bowling economies, 50s/100s, 3w/4w/5w hauls.
- **Strict Non-IPL Player Handling**: For international stars who have not played in the IPL (*Babar Azam, Shaheen Afridi, Mohammad Rizwan*), displays explicit empty-state notices (0 IPL matches, 0 runs) alongside verified T20I, ODI, and Test records.
- **Granular Batter vs. Bowler Duel Matrix**: Head-to-head dot ball %, boundary conversion %, dismissals, strike rate, and sample size verification flags.
- **Mathematical Form Engine**: Evaluates exponential-decay scoring rate (45%), strike-rate benchmark (35%), and consistency deviation (20%) across last 5/10/15 encounters.

### 2. 🔮 Explainable Match Prediction Engine
- Real-time winning probability calculation considering:
  - Team baseline form & head-to-head history
  - Dynamic Playing XI ratings and depth
  - Venue records & chasing vs. defending win ratios
  - Pitch characteristics (*Batting Paradise, Green Seamer, Slow Turner*)
  - Toss winner & decision impact (*Batting vs Fielding*)
- **"Why This Prediction?" Factor Decomposition**: Waterfall visualizer showing exact additive percentage impacts.
- **Confidence Meter**: High / Moderate / Low confidence rating with statistical variance disclaimers.

### 3. 🏟️ 57+ Stadium & Pitch Analytics
- First & second innings average scores, highest/lowest totals.
- Chasing vs defending win percentages.
- Batting, Pace, and Spin friendliness meters (1 to 10 scale).

### 4. ⚡ Match Center
- **Upcoming Fixtures**: Probable & confirmed Playing XIs with pre-match predictions.
- **Interactive Live Center**: Real-time situation analysis with CRR, RRR, active partnerships, and ball-by-ball ticker.
- **1,169 Historical Match Explorer**: Searchable scorecards across all IPL editions with full batting, bowling, and dismissal breakdown.

### 5. 🎨 Dual Platform Delivery
- **Modern Responsive Web SPA**: Dark & Light mode themes, Chart.js integrations, and glassmorphism styling.
- **Streamlit Platform (`app.py`)**: Data-driven multi-page interactive application.

---

## 🛠️ Architecture & Tech Stack

- **Backend**: FastAPI, Uvicorn, Pydantic, RESTful API
- **Analytics & ML**: NumPy, Pandas, Scikit-learn, SciPy
- **Frontend SPA**: Vanilla ES6+, Modern CSS3 Variables, Chart.js
- **Alternative UI**: Streamlit 1.32+
- **Data Layer**: 1,169 authentic IPL matches (2008–2025) compressed to high-speed GZIP format

---

## 📁 Repository Structure

```text
├── backend/
│   ├── main.py                     # FastAPI REST API application & static file mounter
│   └── services/
│       ├── data_loader.py          # Core data engine & indexed player catalogs
│       ├── analytics_engine.py     # Form scoring & phase analytics
│       ├── predictor.py            # Multi-factor explainable prediction engine
│       ├── match_service.py        # Upcoming fixtures, live center & historical scorecards
│       ├── news_service.py         # Official news & player availability tracker
│       └── admin_service.py        # Data synchronization & audit log manager
├── frontend/
│   ├── index.html                  # Single Page Application layout
│   ├── styles.css                  # Responsive dark/light theme stylesheet
│   └── app.js                      # Client-side routing, Chart.js & reactive UI logic
├── app.py                          # Modern Streamlit platform interface
├── run_server.py                   # One-click FastAPI web server launcher
├── test_platform.py                # Automated test suite for data & predictions
├── verify_all.py                   # End-to-end audit script
├── requirements.txt                # Python package dependencies
├── Players.csv                     # Player biographical metadata
├── IPL.csv.gz                      # Compressed ball-by-ball historical dataset (6.3 MB)
└── README.md                       # Documentation
```

---

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/cricintel-pro.git
cd cricintel-pro
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Platform

#### Option A: FastAPI Web App & REST API (Recommended)
```bash
python run_server.py
```
- Open **`http://localhost:8000`** in your browser.
- Interactive OpenAPI documentation is available at **`http://localhost:8000/docs`**.

#### Option B: Streamlit Dashboard
```bash
streamlit run app.py
```
- Open **`http://localhost:8501`** in your browser.

---

## 🧪 Verification & Automated Tests

Run the automated test suite to verify data indexing, authentic statistics, and API endpoints:

```bash
python verify_all.py
```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.