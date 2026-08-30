// CricIntel Pro - Frontend Application Core Logic
let currentView = 'dashboard';
let currentPlayerId = 'v_kohli';
let currentPlayerTab = 'overview';
let activeCharts = {};

document.addEventListener('DOMContentLoaded', () => {
  initSearch();
  initDashboard();
  loadTeamsView();
  loadVenuesView();
  loadPredictorView();
  loadMatchCenterView();
  loadNewsView();
  loadAdminView();
});

function toggleTheme() {
  const isLight = document.body.classList.toggle('light-theme');
  document.getElementById('theme-toggle-btn').innerText = isLight ? '☀️' : '🌙';
}

function navigate(viewName, param = null) {
  document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
  
  const target = document.getElementById(`view-${viewName}`);
  if (target) target.classList.add('active');
  const navBtn = document.getElementById(`nav-${viewName}`);
  if (navBtn) navBtn.classList.add('active');
  
  currentView = viewName;
  window.scrollTo({ top: 0, behavior: 'smooth' });
  
  if (viewName === 'player' && param) {
    loadPlayerProfile(param);
  } else if (viewName === 'player' && !param) {
    loadPlayerProfile(currentPlayerId);
  }
}

// Global Search
function initSearch() {
  const input = document.getElementById('global-search-input');
  const dropdown = document.getElementById('search-dropdown');
  let debounceTimeout = null;

  input.addEventListener('input', (e) => {
    clearTimeout(debounceTimeout);
    const q = e.target.value.trim();
    if (!q) {
      dropdown.classList.remove('active');
      return;
    }
    debounceTimeout = setTimeout(async () => {
      try {
        const res = await fetch(`/api/players/search?q=${encodeURIComponent(q)}`);
        const players = await res.json();
        renderSearchDropdown(players);
      } catch (err) {
        console.error('Search error:', err);
      }
    }, 200);
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-wrapper')) {
      dropdown.classList.remove('active');
    }
  });
}

function renderSearchDropdown(players) {
  const dropdown = document.getElementById('search-dropdown');
  if (!players || players.length === 0) {
    dropdown.innerHTML = '<div class="empty-state" style="padding: 1rem;">No player found. Try another name.</div>';
    dropdown.classList.add('active');
    return;
  }

  dropdown.innerHTML = players.map(p => `
    <div class="search-item" onclick="selectPlayerSearch('${p.id}')">
      <div style="display: flex; align-items: center; gap: 0.75rem;">
        <div style="width: 36px; height: 36px; border-radius: 50%; background: #334155; display: flex; align-items: center; justify-content: center; font-weight: 700; color: #10b981;">
          ${p.display_name.split(' ').map(n => n[0]).join('')}
        </div>
        <div>
          <div style="font-weight: 700; font-size: 0.95rem;">${p.display_name}</div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${p.role} • ${p.country} • ${p.current_team}</div>
        </div>
      </div>
      <div>
        <span class="badge badge-blue">IPL Record</span>
      </div>
    </div>
  `).join('');
  dropdown.classList.add('active');
}

function selectPlayerSearch(playerId) {
  document.getElementById('search-dropdown').classList.remove('active');
  document.getElementById('global-search-input').value = '';
  navigate('player', playerId);
}

// Dashboard Init
async function initDashboard() {
  try {
    const recRes = await fetch('/api/records');
    const records = await recRes.json();
    
    // Top runs
    document.getElementById('dashboard-top-runs').innerHTML = records.all_time_runs.slice(0, 5).map((r, i) => `
      <div style="display: flex; justify-content: space-between; padding: 0.4rem 0; border-bottom: 1px solid var(--border-color); font-size: 0.85rem;">
        <span><strong>${i+1}.</strong> ${r.player}</span>
        <span style="font-weight: 700; color: var(--accent-green);">${r.runs.toLocaleString()} runs</span>
      </div>
    `).join('');

    // Top wickets
    document.getElementById('dashboard-top-wickets').innerHTML = records.all_time_wickets.slice(0, 5).map((r, i) => `
      <div style="display: flex; justify-content: space-between; padding: 0.4rem 0; border-bottom: 1px solid var(--border-color); font-size: 0.85rem;">
        <span><strong>${i+1}.</strong> ${r.player}</span>
        <span style="font-weight: 700; color: var(--accent-blue);">${r.wickets} wkts</span>
      </div>
    `).join('');

    // Form leaders
    const formStars = [
      { name: 'Virat Kohli', team: 'RCB', score: 88.4, type: 'Batter' },
      { name: 'Jasprit Bumrah', team: 'MI', score: 94.2, type: 'Bowler' },
      { name: 'Heinrich Klaasen', team: 'SRH', score: 91.0, type: 'WK-Batter' },
      { name: 'Travis Head', team: 'SRH', score: 89.5, type: 'Batter' }
    ];
    document.getElementById('dashboard-form-leaders').innerHTML = formStars.map(s => `
      <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid var(--border-color);">
        <div>
          <div style="font-weight: 700; font-size: 0.9rem;">${s.name}</div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${s.team} • ${s.type}</div>
        </div>
        <div style="font-size: 1.1rem; font-weight: 800; color: var(--accent-green);">${s.score} <span style="font-size: 0.7rem; color: var(--text-muted);">/100</span></div>
      </div>
    `).join('');

    // Populate quick predictor dropdowns
    const teamsRes = await fetch('/api/teams');
    const teams = await teamsRes.json();
    const venuesRes = await fetch('/api/venues');
    const venues = await venuesRes.json();

    const t1Sel = document.getElementById('dash-pred-t1');
    const t2Sel = document.getElementById('dash-pred-t2');
    const vSel = document.getElementById('dash-pred-venue');

    t1Sel.innerHTML = teams.map(t => `<option value="${t.name}">${t.name}</option>`).join('');
    t2Sel.innerHTML = teams.map((t, idx) => `<option value="${t.name}" ${idx===1?'selected':''}>${t.name}</option>`).join('');
    vSel.innerHTML = venues.map(v => `<option value="${v.name}">${v.name}</option>`).join('');
  } catch (err) {
    console.error('Dashboard init error:', err);
  }
}

async function runDashboardPrediction() {
  const t1 = document.getElementById('dash-pred-t1').value;
  const t2 = document.getElementById('dash-pred-t2').value;
  const venue = document.getElementById('dash-pred-venue').value;
  const resDiv = document.getElementById('dash-pred-result');

  try {
    const res = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ team1: t1, team2: t2, venue: venue })
    });
    const data = await res.json();
    resDiv.style.display = 'block';
    resDiv.innerHTML = `
      <div style="background: var(--bg-card-hover); padding: 0.75rem; border-radius: 8px; border: 1px solid var(--border-color);">
        <div style="font-weight: 800; font-size: 1rem; color: var(--accent-green); margin-bottom: 0.25rem;">
          ${data.favored_team} favored (${data.favored_probability}%)
        </div>
        <div class="prob-bar-container" style="height: 12px; margin: 0.5rem 0;">
          <div class="prob-bar-team1" style="width: ${data.team1_probability}%;"></div>
          <div class="prob-bar-team2" style="width: ${data.team2_probability}%;"></div>
        </div>
        <div style="font-size: 0.75rem; color: var(--text-secondary);">
          ${data.confidence_level} (${data.confidence_score}%) • ${data.factors[1].name}: +${data.factors[1].impact_pct}%
        </div>
      </div>
    `;
  } catch (err) {
    console.error('Prediction error:', err);
  }
}

// Player Profile Loader
async function loadPlayerProfile(playerId) {
  currentPlayerId = playerId;
  try {
    const res = await fetch(`/api/players/${playerId}`);
    if (!res.ok) throw new Error('Player not found');
    const p = await res.json();
    renderPlayerHeader(p);
    renderPlayerTab(currentPlayerTab, p);
  } catch (err) {
    document.getElementById('player-profile-header').innerHTML = `<div class="empty-state"><h3>Player not found</h3></div>`;
  }
}

function renderPlayerHeader(p) {
  const stats = p.ipl_stats || {};
  
  document.getElementById('player-profile-header').innerHTML = `
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
      <div style="display: flex; gap: 1.25rem; align-items: center;">
        <div style="width: 64px; height: 64px; border-radius: 8px; background: var(--accent-primary); display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 800; color: white;">
          ${p.display_name.split(' ').map(n => n[0]).join('')}
        </div>
        <div>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <h1 style="font-size: 1.6rem; font-weight: 800;">${p.display_name}</h1>
            <span class="badge badge-blue">IPL Record</span>
            <span class="badge badge-green">${p.status}</span>
          </div>
          <div style="font-size: 0.9rem; color: var(--text-secondary); margin-top: 0.25rem;">
            ${p.role} • ${p.batting_style} ${p.bowling_style !== 'N/A' ? '• ' + p.bowling_style : ''} • Franchise: <strong>${p.current_team}</strong>
          </div>
          <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem;">
            Career: ${p.career_span} ${p.jersey_number ? '| Jersey #' + p.jersey_number : ''}
          </div>
        </div>
      </div>

      <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
        <div style="background: var(--bg-card-hover); padding: 0.6rem 0.85rem; border-radius: 6px; text-align: center; border: 1px solid var(--border-color);">
          <div style="font-size: 0.75rem; color: var(--text-muted);">IPL Runs</div>
          <div style="font-size: 1.2rem; font-weight: 800; color: var(--accent-primary);">
            ${(stats.runs || 0).toLocaleString()}
          </div>
        </div>
        <div style="background: var(--bg-card-hover); padding: 0.6rem 0.85rem; border-radius: 6px; text-align: center; border: 1px solid var(--border-color);">
          <div style="font-size: 0.75rem; color: var(--text-muted);">IPL Wickets</div>
          <div style="font-size: 1.2rem; font-weight: 800; color: var(--accent-green);">
            ${stats.wickets || 0}
          </div>
        </div>
        <div style="background: var(--bg-card-hover); padding: 0.6rem 0.85rem; border-radius: 6px; text-align: center; border: 1px solid var(--border-color);">
          <div style="font-size: 0.75rem; color: var(--text-muted);">Form Rating</div>
          <div style="font-size: 1.2rem; font-weight: 800; color: var(--accent-orange);">
            ${p.form_analysis?.form_score || 75.0}
          </div>
        </div>
      </div>
    </div>
  `;
}

function switchPlayerTab(tabName) {
  currentPlayerTab = tabName;
  document.querySelectorAll('.tabs-header .tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.innerText.toLowerCase().includes(tabName));
  });
  loadPlayerProfile(currentPlayerId);
}

function renderPlayerTab(tabName, p) {
  const container = document.getElementById('player-tab-content');
  const isIpl = p.ipl_played;
  const st = p.ipl_stats || {};

  if (!isIpl && tabName === 'ipl') {
    container.innerHTML = `
      <div class="card empty-state">
        <div class="empty-state-icon">🏏</div>
        <h3 style="font-size: 1.25rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.5rem;">IPL Career</h3>
        <p style="font-size: 1rem; color: var(--text-secondary); margin-bottom: 1rem;">This player has not played an IPL match.</p>
        <div style="display: inline-grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 1rem 0; background: var(--bg-card-hover); padding: 1rem 2rem; border-radius: 12px;">
          <div><div style="color: var(--text-muted); font-size: 0.8rem;">IPL Matches</div><div style="font-weight: 800; font-size: 1.2rem;">0</div></div>
          <div><div style="color: var(--text-muted); font-size: 0.8rem;">IPL Runs</div><div style="font-weight: 800; font-size: 1.2rem;">0</div></div>
          <div><div style="color: var(--text-muted); font-size: 0.8rem;">IPL Wickets</div><div style="font-weight: 800; font-size: 1.2rem;">0</div></div>
          <div><div style="color: var(--text-muted); font-size: 0.8rem;">IPL Seasons</div><div style="font-weight: 800; font-size: 1.2rem;">0</div></div>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted);">No IPL match data available for this player. International & Other League statistics are available under other tabs.</p>
      </div>
    `;
    return;
  }

  if (tabName === 'overview') {
    container.innerHTML = `
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
        <div class="card">
          <div class="card-title" style="margin-bottom: 1rem;">📊 Career Summary</div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem;">
            <div style="background: var(--bg-card-hover); padding: 0.75rem; border-radius: 8px;"><span style="color: var(--text-muted); font-size: 0.8rem;">Matches:</span> <strong>${st.matches || 0}</strong></div>
            <div style="background: var(--bg-card-hover); padding: 0.75rem; border-radius: 8px;"><span style="color: var(--text-muted); font-size: 0.8rem;">Innings:</span> <strong>${st.innings || 0}</strong></div>
            <div style="background: var(--bg-card-hover); padding: 0.75rem; border-radius: 8px;"><span style="color: var(--text-muted); font-size: 0.8rem;">Total Runs:</span> <strong>${st.runs || 0}</strong></div>
            <div style="background: var(--bg-card-hover); padding: 0.75rem; border-radius: 8px;"><span style="color: var(--text-muted); font-size: 0.8rem;">Batting Avg:</span> <strong>${st.average || 0}</strong></div>
            <div style="background: var(--bg-card-hover); padding: 0.75rem; border-radius: 8px;"><span style="color: var(--text-muted); font-size: 0.8rem;">Strike Rate:</span> <strong>${st.strike_rate || 0}</strong></div>
            <div style="background: var(--bg-card-hover); padding: 0.75rem; border-radius: 8px;"><span style="color: var(--text-muted); font-size: 0.8rem;">Highest Score:</span> <strong>${st.highest_score || 0}</strong></div>
            <div style="background: var(--bg-card-hover); padding: 0.75rem; border-radius: 8px;"><span style="color: var(--text-muted); font-size: 0.8rem;">Wickets:</span> <strong>${st.wickets || 0}</strong></div>
            <div style="background: var(--bg-card-hover); padding: 0.75rem; border-radius: 8px;"><span style="color: var(--text-muted); font-size: 0.8rem;">Economy:</span> <strong>${st.economy || 0}</strong></div>
          </div>
        </div>

        <div class="card">
          <div class="card-title" style="margin-bottom: 1rem;">🔥 Form & Phase Distribution</div>
          <div style="margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 0.25rem;">
              <span>Powerplay Strike Rate</span><strong>${p.phase_stats?.batting?.powerplay?.sr || 135.0}</strong>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 0.25rem;">
              <span>Middle Overs Strike Rate</span><strong>${p.phase_stats?.batting?.middle?.sr || 140.0}</strong>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem;">
              <span>Death Overs Strike Rate</span><strong>${p.phase_stats?.batting?.death?.sr || 185.0}</strong>
            </div>
          </div>
          <div style="background: var(--bg-card-hover); padding: 1rem; border-radius: 8px; font-size: 0.85rem; color: var(--text-secondary);">
            ${p.form_analysis?.explanation || 'Form score computed from recent exponential weighted performances.'}
          </div>
        </div>
      </div>
    `;
  } else if (tabName === 'ipl') {
    const seasons = Object.values(p.ipl_seasons || {}).reverse();
    container.innerHTML = `
      <div class="card" style="margin-bottom: 1.5rem;">
        <div class="card-header">
          <div class="card-title">📅 Season-by-Season Breakdown (${st.seasons_played} Seasons)</div>
          <span class="badge badge-green">IPL Debut: ${st.debut}</span>
        </div>
        <div class="table-responsive">
          <table>
            <thead>
              <tr><th>Season</th><th>Team</th><th>Mat</th><th>Inn</th><th>Runs</th><th>Avg</th><th>SR</th><th>HS</th><th>50s</th><th>100s</th><th>4s</th><th>6s</th><th>Wkts</th><th>Econ</th></tr>
            </thead>
            <tbody>
              ${seasons.map(s => `
                <tr>
                  <td><strong>${s.season}</strong></td><td>${s.team}</td><td>${s.matches}</td><td>${s.innings}</td>
                  <td style="color: var(--accent-green); font-weight: 700;">${s.runs}</td>
                  <td>${s.average}</td><td>${s.strike_rate}</td><td>${s.highest_score}</td>
                  <td>${s.fifties}</td><td>${s.hundreds}</td><td>${s.fours}</td><td>${s.sixes}</td>
                  <td style="color: var(--accent-blue); font-weight: 700;">${s.wickets}</td><td>${s.economy}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  } else if (tabName === 'matches') {
    const last5 = p.last_5_matches || [];
    const allMatches = p.matches_history || [];
    container.innerHTML = `
      <div class="card" style="margin-bottom: 1.5rem;">
        <div class="card-header"><div class="card-title">⏱️ Last 5 Matches Performance</div></div>
        <div class="grid-cards" style="margin-bottom: 1rem;">
          ${last5.map(m => `
            <div style="background: var(--bg-card-hover); padding: 1rem; border-radius: 10px; border: 1px solid var(--border-color);">
              <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.25rem;">
                <span>${m.date}</span><span class="badge ${m.result==='Won'?'badge-green':'badge-red'}">${m.result}</span>
              </div>
              <div style="font-weight: 700; margin-bottom: 0.5rem;">vs ${m.opposition}</div>
              <div style="font-size: 0.9rem; color: var(--accent-green); font-weight: 700;">
                ${m.did_bat ? m.runs + ' runs (' + m.balls + 'b)' : '<span style="color: var(--text-muted);">Did not bat</span>'}
              </div>
              <div style="font-size: 0.85rem; color: var(--accent-blue); margin-top: 0.25rem;">
                ${m.did_bowl ? m.wickets + ' wkts (' + m.overs + ' ov)' : '<span style="color: var(--text-muted);">Did not bowl</span>'}
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  } else if (tabName === 'comparison') {
    container.innerHTML = `
      <div class="card" style="margin-bottom: 1.5rem;">
        <div class="card-header"><div class="card-title">⚔️ Batter vs Bowler Head-to-Head Matchup Matrix</div></div>
        <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
          <input type="text" id="matchup-bowler-input" class="search-input" placeholder="Enter bowler name (e.g. Jasprit Bumrah)..." value="Jasprit Bumrah">
          <button class="tab-btn active" onclick="calculateMatchup()">Query Matchup</button>
        </div>
        <div id="matchup-result-container"></div>
      </div>
    `;
    calculateMatchup();
  } else {
    container.innerHTML = `<div class="card"><div class="card-title">Player Data</div><pre style="background: var(--bg-card-hover); padding: 1rem; border-radius: 8px; font-size: 0.85rem; overflow-x: auto;">${JSON.stringify(p.ipl_stats || p.international_stats, null, 2)}</pre></div>`;
  }
}

async function calculateMatchup() {
  const bowler = document.getElementById('matchup-bowler-input')?.value || 'Jasprit Bumrah';
  const container = document.getElementById('matchup-result-container');
  if (!container) return;

  try {
    const res = await fetch(`/api/players/${currentPlayerId}/matchup?bowler=${encodeURIComponent(bowler)}`);
    const data = await res.json();
    container.innerHTML = `
      <div style="background: var(--bg-card-hover); padding: 1.25rem; border-radius: 12px; border: 1px solid var(--border-color);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
          <div style="font-weight: 800; font-size: 1.1rem;">${data.batter} vs ${data.bowler}</div>
          <span class="badge ${data.sufficient_data ? 'badge-green' : 'badge-orange'}">${data.sample_status}</span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 0.75rem; text-align: center;">
          <div style="background: var(--bg-input); padding: 0.75rem; border-radius: 8px;"><div style="font-size: 0.75rem; color: var(--text-muted);">Balls</div><div style="font-weight: 800; font-size: 1.1rem;">${data.balls_faced}</div></div>
          <div style="background: var(--bg-input); padding: 0.75rem; border-radius: 8px;"><div style="font-size: 0.75rem; color: var(--text-muted);">Runs</div><div style="font-weight: 800; font-size: 1.1rem; color: var(--accent-green);">${data.runs_scored}</div></div>
          <div style="background: var(--bg-input); padding: 0.75rem; border-radius: 8px;"><div style="font-size: 0.75rem; color: var(--text-muted);">Outs</div><div style="font-weight: 800; font-size: 1.1rem; color: var(--accent-red);">${data.dismissals}</div></div>
          <div style="background: var(--bg-input); padding: 0.75rem; border-radius: 8px;"><div style="font-size: 0.75rem; color: var(--text-muted);">SR</div><div style="font-weight: 800; font-size: 1.1rem;">${data.strike_rate}</div></div>
          <div style="background: var(--bg-input); padding: 0.75rem; border-radius: 8px;"><div style="font-size: 0.75rem; color: var(--text-muted);">Dot %</div><div style="font-weight: 800; font-size: 1.1rem;">${data.dot_ball_percentage}%</div></div>
          <div style="background: var(--bg-input); padding: 0.75rem; border-radius: 8px;"><div style="font-size: 0.75rem; color: var(--text-muted);">Average</div><div style="font-weight: 800; font-size: 1.1rem;">${data.batting_average}</div></div>
        </div>
      </div>
    `;
  } catch (err) {
    console.error('Matchup query error:', err);
  }
}

// Teams View
async function loadTeamsView() {
  const container = document.getElementById('teams-grid');
  if (!container) return;
  try {
    const res = await fetch('/api/teams');
    const teams = await res.json();
    container.innerHTML = teams.map(t => `
      <div class="card" style="border-top: 4px solid ${t.primary_color}; cursor: pointer;" onclick="showTeamDetail('${t.id}')">
        <div class="card-header">
          <div style="font-weight: 800; font-size: 1.1rem;">${t.name}</div>
          <span class="badge badge-green">${t.titles} Titles</span>
        </div>
        <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.5rem;">
          Captain: <strong>${t.captain}</strong> | Coach: ${t.coach}
        </div>
        <div style="font-size: 0.85rem; color: var(--text-muted);">
          Matches: ${t.total_matches} | Win Rate: <strong>${t.win_percentage}%</strong>
        </div>
      </div>
    `).join('');
  } catch (err) {
    console.error('Load teams error:', err);
  }
}

async function showTeamDetail(teamId) {
  const container = document.getElementById('team-detail-container');
  try {
    const res = await fetch(`/api/teams/${teamId}`);
    const t = await res.json();
    container.innerHTML = `
      <div class="card" style="margin-top: 1.5rem;">
        <div class="card-header">
          <div class="card-title">🛡️ ${t.name} Profile & Squad Analytics</div>
          <span class="badge badge-blue">Home: ${t.home_venue.split(',')[0]}</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
          <div>
            <h4 style="margin-bottom: 0.5rem;">Home vs Away Records</h4>
            <div style="display: flex; gap: 1rem;">
              <div style="background: var(--bg-card-hover); padding: 0.75rem 1rem; border-radius: 8px; flex: 1;">
                <div style="color: var(--text-muted); font-size: 0.75rem;">Home Wins</div>
                <div style="font-weight: 800; font-size: 1.1rem;">${t.home_record.wins} (${t.home_record.win_pct}%)</div>
              </div>
              <div style="background: var(--bg-card-hover); padding: 0.75rem 1rem; border-radius: 8px; flex: 1;">
                <div style="color: var(--text-muted); font-size: 0.75rem;">Away Wins</div>
                <div style="font-weight: 800; font-size: 1.1rem;">${t.away_record.wins} (${t.away_record.win_pct}%)</div>
              </div>
            </div>
          </div>
          <div>
            <h4 style="margin-bottom: 0.5rem;">Key Squad Lineup</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 0.4rem;">
              ${t.squad.map(p => `<span class="badge" style="background: var(--bg-card-hover); color: var(--text-primary);">${p}</span>`).join('')}
            </div>
          </div>
        </div>
      </div>
    `;
  } catch (err) {
    console.error('Team detail error:', err);
  }
}

// Venues View
async function loadVenuesView() {
  const container = document.getElementById('venues-grid');
  if (!container) return;
  try {
    const res = await fetch('/api/venues');
    const venues = await res.json();
    container.innerHTML = venues.slice(0, 12).map(v => `
      <div class="card">
        <div class="card-header">
          <div style="font-weight: 800; font-size: 1rem;">${v.name.split(',')[0]}</div>
          <span class="badge badge-blue">${v.matches_played} Matches</span>
        </div>
        <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.5rem;">
          Avg 1st Inns: <strong>${v.avg_first_innings_score}</strong> | 2nd Inns: <strong>${v.avg_second_innings_score}</strong>
        </div>
        <div style="display: flex; gap: 0.5rem; margin-top: 0.5rem;">
          <span class="badge badge-green">Bat: ${v.batting_friendly_meter}/10</span>
          <span class="badge badge-orange">Pace: ${v.pace_friendly_meter}/10</span>
          <span class="badge badge-blue">Spin: ${v.spin_friendly_meter}/10</span>
        </div>
      </div>
    `).join('');
  } catch (err) {
    console.error('Load venues error:', err);
  }
}

// Predictor Workbench
async function loadPredictorView() {
  const container = document.getElementById('predictor-workbench');
  if (!container) return;
  const teamsRes = await fetch('/api/teams');
  const teams = await teamsRes.json();
  const venuesRes = await fetch('/api/venues');
  const venues = await venuesRes.json();

  container.innerHTML = `
    <div style="display: grid; grid-template-columns: 1fr 1.5fr; gap: 1.5rem;">
      <div class="card">
        <div class="card-title" style="margin-bottom: 1rem;">⚙️ Match Configuration</div>
        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
          <div><label style="font-size: 0.8rem; color: var(--text-muted);">Team 1</label>
            <select id="pred-team1" class="search-input">${teams.map(t => `<option value="${t.name}">${t.name}</option>`).join('')}</select>
          </div>
          <div><label style="font-size: 0.8rem; color: var(--text-muted);">Team 2</label>
            <select id="pred-team2" class="search-input">${teams.map((t, i) => `<option value="${t.name}" ${i===1?'selected':''}>${t.name}</option>`).join('')}</select>
          </div>
          <div><label style="font-size: 0.8rem; color: var(--text-muted);">Venue</label>
            <select id="pred-venue" class="search-input">${venues.map(v => `<option value="${v.name}">${v.name}</option>`).join('')}</select>
          </div>
          <div><label style="font-size: 0.8rem; color: var(--text-muted);">Pitch Type</label>
            <select id="pred-pitch" class="search-input">
              <option value="Balanced">Balanced Sporting Pitch</option>
              <option value="Batting paradise">Flat Batting Track (200+)</option>
              <option value="Pace friendly">Green Seamer / Pace Assist</option>
              <option value="Spin friendly">Slow Turner / Spin Assist</option>
            </select>
          </div>
          <div><label style="font-size: 0.8rem; color: var(--text-muted);">Toss Winner</label>
            <select id="pred-toss-winner" class="search-input">
              <option value="">Toss not conducted yet</option>
              ${teams.map(t => `<option value="${t.name}">${t.name}</option>`).join('')}
            </select>
          </div>
          <div><label style="font-size: 0.8rem; color: var(--text-muted);">Toss Decision</label>
            <select id="pred-toss-decision" class="search-input">
              <option value="field">Bowl First (Fielding)</option>
              <option value="bat">Bat First</option>
            </select>
          </div>
          <button class="tab-btn active" onclick="executeFullPrediction()" style="margin-top: 0.5rem;">🚀 Generate Explainable Prediction</button>
        </div>
      </div>
      <div id="prediction-output-card" class="card"><div class="empty-state">Generating prediction...</div></div>
    </div>
  `;
  executeFullPrediction();
}

async function executeFullPrediction() {
  const t1 = document.getElementById('pred-team1')?.value || 'Chennai Super Kings';
  const t2 = document.getElementById('pred-team2')?.value || 'Mumbai Indians';
  const venue = document.getElementById('pred-venue')?.value || 'Wankhede Stadium, Mumbai';
  const pitch = document.getElementById('pred-pitch')?.value || 'Balanced';
  const tossW = document.getElementById('pred-toss-winner')?.value || null;
  const tossDec = document.getElementById('pred-toss-decision')?.value || 'field';
  const output = document.getElementById('prediction-output-card');

  try {
    const res = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        team1: t1, team2: t2, venue: venue, pitch_type: pitch,
        toss_winner: tossW, toss_decision: tossDec
      })
    });
    const p = await res.json();
    output.innerHTML = `
      <div class="card-header">
        <div class="card-title">📊 Prediction Outcome & Factor Explainability</div>
        <span class="badge badge-green">${p.confidence_level} (${p.confidence_score}%)</span>
      </div>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
        <div style="font-weight: 800; font-size: 1.25rem;">${p.team1} <span style="color: var(--accent-green);">${p.team1_probability}%</span></div>
        <div style="font-weight: 800; font-size: 1.25rem;"><span style="color: var(--accent-blue);">${p.team2_probability}%</span> ${p.team2}</div>
      </div>
      <div class="prob-bar-container">
        <div class="prob-bar-team1" style="width: ${p.team1_probability}%;"></div>
        <div class="prob-bar-team2" style="width: ${p.team2_probability}%;"></div>
      </div>
      <div style="margin: 1.25rem 0;">
        <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 0.75rem;">🔍 Why This Prediction? (Factor Decomposition)</h4>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          ${p.factors.map(f => `
            <div style="background: var(--bg-card-hover); padding: 0.6rem 0.85rem; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
              <div>
                <div style="font-weight: 700; font-size: 0.85rem;">${f.name}</div>
                <div style="font-size: 0.75rem; color: var(--text-muted);">${f.detail}</div>
              </div>
              <div style="text-align: right;">
                <span class="badge ${f.favors===p.team1?'badge-green':'badge-blue'}">+${f.impact_pct}% (${f.favors})</span>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
      <div style="font-size: 0.75rem; color: var(--text-muted); border-top: 1px solid var(--border-color); padding-top: 0.75rem;">
        ℹ️ ${p.disclaimer}
      </div>
    `;
  } catch (err) {
    console.error('Prediction execution error:', err);
  }
}

// Match Center
async function loadMatchCenterView() {
  switchMatchCenterTab('upcoming');
}

async function switchMatchCenterTab(subtab) {
  const container = document.getElementById('match-center-content');
  if (!container) return;
  document.querySelectorAll('#view-matches .tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.innerText.toLowerCase().includes(subtab));
  });

  if (subtab === 'upcoming') {
    const res = await fetch('/api/matches/upcoming');
    const upcoming = await res.json();
    container.innerHTML = `
      <div class="grid-cards">
        ${upcoming.map(m => `
          <div class="card" style="border-left: 4px solid var(--accent-green);">
            <div class="card-header">
              <span class="badge badge-green">${m.status}</span>
              <span style="font-size: 0.8rem; color: var(--text-muted);">${m.date} • ${m.time}</span>
            </div>
            <div style="font-weight: 800; font-size: 1.25rem; margin-bottom: 0.25rem;">${m.team1} vs ${m.team2}</div>
            <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.5rem;">🏟️ ${m.venue}</div>
            <div style="background: var(--bg-card-hover); padding: 0.75rem; border-radius: 8px; margin-bottom: 0.75rem;">
              <div style="font-size: 0.8rem; color: var(--text-muted);">Pre-Match Win Probability</div>
              <div style="font-weight: 700; font-size: 0.95rem; color: var(--accent-green);">
                ${m.prediction.favored_team} (${m.prediction.favored_probability}%)
              </div>
            </div>
            <button class="tab-btn active" style="width: 100%;" onclick="openUpcomingMatchModal('${m.id}')">View Playing XI & Pitch</button>
          </div>
        `).join('')}
      </div>
    `;
  } else if (subtab === 'live') {
    const res = await fetch('/api/matches/live');
    const live = await res.json();
    container.innerHTML = `
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">🔴 ${live.tournament}</div>
            <div style="font-size: 0.8rem; color: var(--text-muted);">${live.venue} • ${live.toss_summary}</div>
          </div>
          <span class="badge badge-red">LIVE</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem;">
          <div style="background: var(--bg-card-hover); padding: 1rem; border-radius: 12px;">
            <div style="font-size: 0.9rem; color: var(--text-muted);">1st Innings</div>
            <div style="font-size: 1.5rem; font-weight: 800;">${live.innings1.team}</div>
            <div style="font-size: 1.25rem; font-weight: 700; color: var(--accent-green);">${live.innings1.runs}/${live.innings1.wickets} (${live.innings1.overs} ov)</div>
          </div>
          <div style="background: var(--bg-card-hover); padding: 1rem; border-radius: 12px; border: 1px solid var(--accent-green);">
            <div style="font-size: 0.9rem; color: var(--text-muted);">2nd Innings (Chasing ${live.innings2.target})</div>
            <div style="font-size: 1.5rem; font-weight: 800;">${live.innings2.team}</div>
            <div style="font-size: 1.25rem; font-weight: 700; color: var(--accent-green);">${live.innings2.runs}/${live.innings2.wickets} (${live.innings2.overs} ov)</div>
            <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem;">Need ${live.innings2.runs_needed} runs in ${live.innings2.balls_remaining} balls (RRR: ${live.innings2.rrr})</div>
          </div>
        </div>
        <div style="background: var(--bg-card-hover); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
          <div style="font-weight: 700; margin-bottom: 0.5rem;">At the Crease</div>
          <div style="display: flex; justify-content: space-between; font-size: 0.85rem;">
            <span>Striker: <strong>${live.innings2.striker.name}</strong> ${live.innings2.striker.runs}* (${live.innings2.striker.balls}b)</span>
            <span>Non-Striker: <strong>${live.innings2.non_striker.name}</strong> ${live.innings2.non_striker.runs}* (${live.innings2.non_striker.balls}b)</span>
            <span>Bowler: <strong>${live.innings2.current_bowler.name}</strong> (${live.innings2.current_bowler.overs} ov, ${live.innings2.current_bowler.wickets}/${live.innings2.current_bowler.runs})</span>
          </div>
        </div>
        <div style="font-size: 0.85rem; color: var(--text-secondary);">
          <strong>Situation:</strong> ${live.situation_analysis}
        </div>
      </div>
    `;
  } else if (subtab === 'historical') {
    const res = await fetch('/api/matches/historical?limit=25');
    const hist = await res.json();
    container.innerHTML = `
      <div class="card">
        <div class="card-header">
          <div class="card-title">📜 1,169 Authentic IPL Scorecards (2008–2025)</div>
          <span class="badge badge-green">${hist.total_matches} Total Matches</span>
        </div>
        <div class="table-responsive" style="max-height: 500px;">
          <table>
            <thead><tr><th>Date</th><th>Season</th><th>Match</th><th>Winner</th><th>Player of Match</th><th>Venue</th><th>Action</th></tr></thead>
            <tbody>
              ${hist.matches.map(m => `
                <tr>
                  <td>${m.date}</td>
                  <td><strong>${m.season}</strong></td>
                  <td>${m.team1} vs ${m.team2}</td>
                  <td><span class="badge badge-green">${m.winner}</span></td>
                  <td>${m.player_of_match}</td>
                  <td>${m.venue.split(',')[0]}</td>
                  <td><button class="tab-btn active" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" onclick="openScorecardModal(${m.match_id})">Scorecard</button></td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  }
}

async function openScorecardModal(matchId) {
  try {
    const res = await fetch(`/api/matches/${matchId}`);
    const sc = await res.json();
    const info = sc.match_info || {};
    alert(`Scorecard for Match #${matchId}\n\nDate: ${info.date}\nWinner: ${info.winner}\nPlayer of Match: ${info.player_of_match}\n\n1st Innings: ${sc.innings1.team} - ${sc.innings1.total_runs}/${sc.innings1.wickets} (${sc.innings1.overs} ov)\n2nd Innings: ${sc.innings2.team} - ${sc.innings2.total_runs}/${sc.innings2.wickets} (${sc.innings2.overs} ov)`);
  } catch (err) {
    console.error('Error loading scorecard:', err);
  }
}

function openUpcomingMatchModal(id) {
  alert('Upcoming match details loaded into Predictor.');
  navigate('predictor');
}

// News View
async function loadNewsView() {
  try {
    const newsRes = await fetch('/api/news');
    const news = await newsRes.json();
    const availRes = await fetch('/api/availability');
    const avail = await availRes.json();

    document.getElementById('news-list-container').innerHTML = news.map(n => `
      <div style="padding: 1rem 0; border-bottom: 1px solid var(--border-color);">
        <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.25rem;">
          <span>${n.category} • ${n.source}</span><span>${n.date}</span>
        </div>
        <div style="font-weight: 700; font-size: 1rem; margin-bottom: 0.35rem;">${n.title}</div>
        <div style="font-size: 0.85rem; color: var(--text-secondary);">${n.summary}</div>
      </div>
    `).join('');

    document.getElementById('availability-list-container').innerHTML = avail.map(a => `
      <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.6rem 0; border-bottom: 1px solid var(--border-color); font-size: 0.85rem;">
        <div>
          <div style="font-weight: 700;">${a.player}</div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${a.team}</div>
        </div>
        <span class="badge ${a.status==='Available'?'badge-green':'badge-orange'}">${a.status}</span>
      </div>
    `).join('');
  } catch (err) {
    console.error('News view error:', err);
  }
}

// Admin View
async function loadAdminView() {
  try {
    const res = await fetch('/api/admin/status');
    const data = await res.json();
    document.getElementById('admin-container').innerHTML = `
      <div class="card" style="margin-bottom: 1.5rem;">
        <div class="card-header">
          <div class="card-title">🔄 Data Ingestion & Live Connectors</div>
          <span class="badge badge-green">${data.sync_health}</span>
        </div>
        <div class="table-responsive" style="margin-bottom: 1rem;">
          <table>
            <thead><tr><th>Data Source</th><th>Integration Type</th><th>Status</th><th>Last Synchronized</th></tr></thead>
            <tbody>
              ${data.data_sources.map(s => `
                <tr>
                  <td><strong>${s.name}</strong></td>
                  <td>${s.type}</td>
                  <td><span class="badge badge-green">${s.status}</span></td>
                  <td>${s.last_sync}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  } catch (err) {
    console.error('Admin view error:', err);
  }
}

function exportPlatformSummary() {
  window.print();
}
