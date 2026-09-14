def get_dashboard_html() -> str:
    """Returns the comprehensive Squad Portal & Fortnite Control Plane single page application."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ghost Squad Portal • Fortnite Telemetry & Shop</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #070b14;
      --card-bg: rgba(15, 23, 42, 0.75);
      --card-border: rgba(255, 255, 255, 0.08);
      --accent: #00a8ff;
      --accent-glow: rgba(0, 168, 255, 0.35);
      --accent-purple: #9333ea;
      --gold: #ffd700;
      --success: #10b981;
      --warning: #f59e0b;
      --error: #ef4444;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --input-bg: #0f172a;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', sans-serif;
      background: radial-gradient(circle at 10% 10%, #1e1b4b 0%, var(--bg) 60%);
      color: var(--text);
      min-height: 100vh;
      display: flex;
    }
    aside {
      width: 270px;
      background: rgba(10, 15, 29, 0.96);
      border-right: 1px solid var(--card-border);
      display: flex;
      flex-direction: column;
      padding: 24px 16px;
      gap: 24px;
      backdrop-filter: blur(12px);
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 0 8px;
    }
    .brand-icon {
      width: 44px;
      height: 44px;
      border-radius: 12px;
      background: linear-gradient(135deg, var(--accent), var(--accent-purple));
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.3rem;
      box-shadow: 0 0 20px var(--accent-glow);
    }
    .brand-text h1 { font-size: 1.2rem; font-weight: 900; letter-spacing: -0.5px; }
    .brand-text p { font-size: 0.75rem; color: var(--accent); font-weight: 700; text-transform: uppercase; }

    nav { display: flex; flex-direction: column; gap: 6px; }
    .nav-btn {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 14px;
      border-radius: 10px;
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-muted);
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      text-align: left;
    }
    .nav-btn:hover { background: rgba(255, 255, 255, 0.04); color: var(--text); }
    .nav-btn.active {
      background: rgba(0, 168, 255, 0.12);
      border-color: rgba(0, 168, 255, 0.3);
      color: var(--accent);
    }

    main {
      flex: 1;
      padding: 36px 40px;
      overflow-y: auto;
      max-width: 1300px;
    }
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 28px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--card-border);
    }
    .header-title h2 { font-size: 1.8rem; font-weight: 900; }
    .header-title p { color: var(--text-muted); font-size: 0.85rem; margin-top: 4px; }
    .auth-badge {
      display: flex;
      align-items: center;
      gap: 10px;
      background: var(--card-bg);
      padding: 8px 16px;
      border-radius: 30px;
      border: 1px solid var(--card-border);
      font-size: 0.85rem;
    }
    .status-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--success);
      box-shadow: 0 0 10px var(--success);
    }

    /* Cards */
    .card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 24px;
      backdrop-filter: blur(10px);
    }
    .card-title {
      font-size: 1.25rem;
      font-weight: 800;
      margin-bottom: 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    /* Squad Stats Grid */
    .squad-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 20px;
    }
    .player-card {
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      transition: transform 0.2s, border-color 0.2s;
    }
    .player-card:hover {
      transform: translateY(-3px);
      border-color: rgba(0, 168, 255, 0.4);
      box-shadow: 0 10px 25px rgba(0, 168, 255, 0.1);
    }
    .player-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .player-name {
      font-size: 1.3rem;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .player-bp {
      background: rgba(255, 215, 0, 0.15);
      border: 1px solid rgba(255, 215, 0, 0.3);
      color: var(--gold);
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 700;
    }
    .stats-matrix {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      text-align: center;
    }
    .stat-box {
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 10px;
      padding: 10px;
    }
    .stat-label { font-size: 0.7rem; color: var(--text-muted); font-weight: 700; text-transform: uppercase; }
    .stat-val { font-size: 1.25rem; font-weight: 800; color: #fff; margin-top: 4px; font-family: 'JetBrains Mono', monospace; }

    /* Modes pills */
    .mode-row {
      display: flex;
      justify-content: space-between;
      padding: 8px 12px;
      background: rgba(0, 0, 0, 0.2);
      border-radius: 8px;
      font-size: 0.8rem;
    }

    /* Live Shop Grid */
    .shop-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
      gap: 16px;
      margin-top: 16px;
    }
    .shop-item-card {
      background: rgba(30, 41, 59, 0.5);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      position: relative;
      overflow: hidden;
      transition: transform 0.2s;
    }
    .shop-item-card:hover { transform: scale(1.03); }
    .shop-img {
      width: 110px;
      height: 110px;
      object-fit: contain;
      margin-bottom: 8px;
    }
    .shop-name { font-size: 0.85rem; font-weight: 700; margin-bottom: 6px; }
    .shop-price {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: rgba(0, 168, 255, 0.15);
      color: var(--accent);
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
    }

    /* News Cards */
    .news-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 20px;
    }
    .news-card {
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      overflow: hidden;
    }
    .news-card img { width: 100%; height: 170px; object-fit: cover; }
    .news-body { padding: 18px; }
    .news-title { font-size: 1.05rem; font-weight: 800; margin-bottom: 8px; }
    .news-text { font-size: 0.8rem; color: var(--text-muted); line-height: 1.4; }

    /* Forms */
    .form-group { margin-bottom: 20px; }
    label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 8px; }
    .hint { font-size: 0.75rem; color: var(--text-muted); margin-top: 4px; }
    select, input[type="text"], input[type="password"] {
      width: 100%;
      background: var(--input-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 12px 14px;
      color: var(--text);
      font-size: 0.9rem;
      outline: none;
    }
    select:focus, input:focus { border-color: var(--accent); }

    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 12px 22px;
      border-radius: 10px;
      border: none;
      font-size: 0.9rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .btn-primary { background: linear-gradient(135deg, var(--accent), #0077ff); color: #fff; }
    .btn-primary:hover { opacity: 0.9; }
    .btn-secondary { background: rgba(255, 255, 255, 0.08); color: var(--text); }
    .btn-secondary:hover { background: rgba(255, 255, 255, 0.14); }

    .channel-box {
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 18px;
      margin-bottom: 16px;
    }

    #toast {
      position: fixed;
      bottom: 24px;
      right: 24px;
      padding: 14px 20px;
      background: var(--card-bg);
      border: 1px solid var(--accent);
      border-radius: 12px;
      color: var(--text);
      font-size: 0.9rem;
      font-weight: 600;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
      opacity: 0;
      transform: translateY(10px);
      transition: all 0.3s ease;
      pointer-events: none;
      z-index: 999;
    }
    #toast.show { opacity: 1; transform: translateY(0); }
    .tab-content { display: none; }
    .tab-content.active { display: block; }

    @media (max-width: 768px) {
      body { flex-direction: column; }
      aside { width: 100%; }
      main { padding: 20px; }
    }
  </style>
</head>
<body>

  <!-- Navigation Sidebar -->
  <aside>
    <div class="brand">
      <div class="brand-icon">⚡</div>
      <div class="brand-text">
        <h1>GHOST</h1>
        <p>Squad Portal</p>
      </div>
    </div>

    <nav>
      <button class="nav-btn active" onclick="switchTab('squad')">👥 Squad Stats</button>
      <button class="nav-btn" onclick="switchTab('shop')">🛒 Live Item Shop</button>
      <button class="nav-btn" onclick="switchTab('map')">🗺️ Island Map</button>
      <button class="nav-btn" onclick="switchTab('news')">📰 News & Season</button>
      <button class="nav-btn" onclick="switchTab('channels')">🎯 Channel Routing</button>
      <button class="nav-btn" onclick="switchTab('status')">🎮 Presence & Status</button>
    </nav>

    <div style="margin-top: auto; padding: 12px; background: rgba(255,255,255,0.03); border-radius: 12px; border: 1px solid var(--card-border);">
      <p style="font-size: 0.75rem; color: var(--text-muted);">Admin Session PIN</p>
      <input type="password" id="adminPin" placeholder="ghost123" style="margin-top: 6px; padding: 8px 10px; font-size: 0.8rem;" oninput="savePin()">
    </div>
  </aside>

  <!-- Main View -->
  <main>
    <header>
      <div class="header-title">
        <h2 id="pageTitle">Squad Telemetry & Detailed Stats</h2>
        <p>Live Fortnite game data tailored for your squad</p>
      </div>
      <div class="auth-badge">
        <div class="status-dot"></div>
        <span id="gatewayStatus">Connected (Render 24/7)</span>
      </div>
    </header>

    <!-- TAB 1: SQUAD DETAILED STATS -->
    <section id="tab-squad" class="tab-content active">
      <div class="card">
        <div class="card-title">
          <span>👥 Squad Telemetry & Live Tracker (5-10 Members)</span>
          <button class="btn btn-secondary" onclick="loadSquadStats()">🔄 Refresh Stats</button>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 20px;">
          Track your squad members directly from this dashboard. Stats update live from Epic Games.
        </p>

        <!-- Track Player & Filter Bar -->
        <div style="background: rgba(0, 0, 0, 0.25); border: 1px solid var(--card-border); border-radius: 12px; padding: 16px; margin-bottom: 20px; display: flex; flex-wrap: wrap; gap: 12px; align-items: center;">
          <div style="flex: 2; min-width: 240px;">
            <input type="text" id="trackPlayerInput" placeholder="Enter Epic Games username (e.g. KING_CONDOR_, p_lmpNastie)" onkeydown="if(event.key==='Enter') trackPlayer()">
          </div>
          <button class="btn btn-primary" id="trackBtn" onclick="trackPlayer()">➕ Track Player</button>
          <div style="flex: 1; min-width: 180px;">
            <input type="text" id="filterSquadInput" placeholder="🔍 Filter squad cards..." oninput="filterSquadCards()">
          </div>
        </div>

        <div id="squadContainer" class="squad-grid">
          <p style="color: var(--text-muted);">Loading squad telemetry from Fortnite API...</p>
        </div>
      </div>
    </section>

    <!-- TAB 2: LIVE ITEM SHOP -->
    <section id="tab-shop" class="tab-content">
      <div class="card">
        <div class="card-title">
          <span>🛒 Today's Fortnite Item Shop (Live Grid)</span>
          <button class="btn btn-secondary" onclick="loadLiveShop()">🔄 Refresh Shop</button>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted);" id="shopMetaDate">
          Live feed from Fortnite-API. Resets daily at 00:00 UTC.
        </p>
        <div id="shopContainer" class="shop-grid">
          <p style="color: var(--text-muted);">Fetching current shop items...</p>
        </div>
      </div>
    </section>

    <!-- TAB 3: ISLAND MAP -->
    <section id="tab-map" class="tab-content">
      <div class="card">
        <div class="card-title">
          <span>🗺️ Current Island Map & POIs</span>
          <button class="btn btn-secondary" onclick="loadMap()">🔄 Refresh Map</button>
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; gap: 20px;">
          <img id="islandMapImg" src="https://fortnite-api.com/images/map_en.png" style="width: 100%; max-width: 780px; border-radius: 12px; border: 1px solid var(--card-border);" alt="Fortnite Map">
          <div id="poisContainer" style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;"></div>
        </div>
      </div>
    </section>

    <!-- TAB 4: NEWS & SEASON COUNTDOWN -->
    <section id="tab-news" class="tab-content">
      <div class="card" style="margin-bottom: 24px;">
        <div class="card-title">
          <span>⏳ Season Timeline & Status</span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
          <div style="background: rgba(0,0,0,0.3); padding: 16px; border-radius: 10px;">
            <p style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;">CURRENT CHAPTER</p>
            <h3 style="font-size: 1.4rem; color: var(--accent); margin-top: 4px;">Chapter 5</h3>
          </div>
          <div style="background: rgba(0,0,0,0.3); padding: 16px; border-radius: 10px;">
            <p style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;">ACTIVE SEASON</p>
            <h3 style="font-size: 1.4rem; color: var(--gold); margin-top: 4px;">Battle Royale</h3>
          </div>
          <div style="background: rgba(0,0,0,0.3); padding: 16px; border-radius: 10px;">
            <p style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;">DAILY RESET TIMER</p>
            <h3 style="font-size: 1.4rem; font-family: 'JetBrains Mono', monospace; margin-top: 4px;" id="shopResetCountdown">00:00 UTC</h3>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-title">
          <span>📰 Active In-Game News & Announcements</span>
          <button class="btn btn-secondary" onclick="loadNews()">🔄 Refresh News</button>
        </div>
        <div id="newsContainer" class="news-grid">
          <p style="color: var(--text-muted);">Fetching in-game news...</p>
        </div>
      </div>
    </section>

    <!-- TAB 5: CHANNEL ROUTING -->
    <section id="tab-channels" class="tab-content">
      <div class="card">
        <div class="card-title">
          <span>🎯 Server Channel Post Routing</span>
          <button class="btn btn-secondary" onclick="loadChannels()">🔄 Reload Channels</button>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 20px;">
          Route specific post types to distinct Discord channels without role pings.
        </p>

        <div class="form-group">
          <label>Target Discord Server</label>
          <select id="guildSelector" onchange="onGuildChange()">
            <option value="">Loading servers...</option>
          </select>
        </div>

        <div class="channel-box">
          <h4 style="margin-bottom: 8px;">🛒 Daily Item Shop Drops</h4>
          <select id="routeShop">
            <option value="">-- Disabled --</option>
          </select>
          <div class="hint">Target channel for daily 00:00 UTC item shop showcases.</div>
        </div>

        <div class="channel-box">
          <h4 style="margin-bottom: 8px;">👑 Victory Royale Celebration Channel</h4>
          <select id="routeNews">
            <option value="">-- Same as Shop / #fortnite --</option>
          </select>
          <div class="hint">Where Ghost announces when a squad member wins a match.</div>
        </div>

        <div style="display: flex; gap: 12px; margin-top: 18px;">
          <button class="btn btn-primary" onclick="saveRouting()">💾 Save Channel Settings</button>
          <button class="btn btn-secondary" onclick="testShopBroadcast()">📢 Test Post Shop</button>
        </div>
      </div>
    </section>

    <!-- TAB 6: BOT STATUS & PRESENCE -->
    <section id="tab-status" class="tab-content">
      <div class="card">
        <div class="card-title">
          <span>🎮 Bot Activity & Status Text</span>
        </div>
        <div class="form-group">
          <label>Status Message</label>
          <input type="text" id="statusText" placeholder="Fortnite with the squad">
        </div>
        <div class="form-group">
          <label>Activity Type</label>
          <select id="activityType">
            <option value="watching">Watching</option>
            <option value="playing">Playing</option>
            <option value="listening">Listening to</option>
            <option value="competing">Competing in</option>
          </select>
        </div>
        <button class="btn btn-primary" onclick="savePresence()">💾 Update Status Live</button>
      </div>

      <div class="card">
        <div class="card-title">
          <span>💾 Database Persistence & Backup</span>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">
          Your tracked squad members and configurations are permanently saved in MongoDB Atlas 24/7. Click below to download a standalone JSON backup file anytime.
        </p>
        <div style="display: flex; gap: 12px; align-items: center;">
          <button class="btn btn-secondary" onclick="window.open('/api/backup/export', '_blank')">📥 Download DB Backup (.json)</button>
          <span style="font-size: 0.8rem; color: var(--success); font-weight: 600;">✓ Cloud Sync Active</span>
        </div>
      </div>
    </section>

  </main>

  <div id="toast">Settings updated successfully!</div>

  <script>
    let cachedGuilds = [];

    function switchTab(tabId) {
      document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
      const activeBtn = Array.from(document.querySelectorAll('.nav-btn')).find(b => b.getAttribute('onclick').includes(tabId));
      if (activeBtn) activeBtn.classList.add('active');
      const target = document.getElementById('tab-' + tabId);
      if (target) target.classList.add('active');

      if (tabId === 'squad') loadSquadStats();
      if (tabId === 'shop') loadLiveShop();
      if (tabId === 'map') loadMap();
      if (tabId === 'news') loadNews();
      if (tabId === 'channels') loadChannels();
    }

    function showToast(msg) {
      const t = document.getElementById('toast');
      t.innerText = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 3000);
    }

    function getPin() {
      return localStorage.getItem('ghost_pin') || document.getElementById('adminPin').value || 'ghost123';
    }

    function savePin() {
      localStorage.setItem('ghost_pin', document.getElementById('adminPin').value);
    }

    async function trackPlayer() {
      const input = document.getElementById('trackPlayerInput');
      const name = input.value.trim();
      if (!name) return;
      const btn = document.getElementById('trackBtn');
      const oldText = btn.innerText;
      btn.innerText = '⏳ Checking...';
      btn.disabled = true;

      try {
        const res = await fetch('/api/players/track', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ epic_name: name })
        });
        const data = await res.json();
        if (res.ok) {
          showToast(data.message || 'Player tracked successfully! 🎯');
          input.value = '';
          await loadSquadStats();
        } else {
          showToast('⚠️ ' + (data.message || 'Could not track player'));
        }
      } catch (err) {
        showToast('Error: ' + err);
      } finally {
        btn.innerText = oldText;
        btn.disabled = false;
      }
    }

    async function untrackPlayer(name) {
      if (!confirm(`Stop tracking squad member '${name}'?`)) return;
      try {
        const res = await fetch('/api/players/untrack', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ epic_name: name })
        });
        const data = await res.json();
        if (res.ok) {
          showToast(`Untracked ${name}`);
          await loadSquadStats();
        } else {
          showToast('Error: ' + data.message);
        }
      } catch (err) {
        showToast('Error: ' + err);
      }
    }

    function filterSquadCards() {
      const q = (document.getElementById('filterSquadInput').value || '').toLowerCase();
      document.querySelectorAll('.player-card').forEach(card => {
        const text = card.innerText.toLowerCase();
        card.style.display = text.includes(q) ? 'flex' : 'none';
      });
    }

    async function loadSquadStats() {
      const container = document.getElementById('squadContainer');
      container.innerHTML = '<p style="color: var(--text-muted);">Fetching detailed squad telemetry...</p>';
      try {
        const res = await fetch('/api/squad-stats');
        const squad = await res.json();
        if (!Array.isArray(squad) || squad.length === 0) {
          container.innerHTML = '<div style="grid-column: 1/-1; padding: 30px; background: rgba(255,255,255,0.02); border-radius: 12px; text-align: center;"><p style="font-size: 1.1rem; margin-bottom: 8px;">No squad members tracked yet!</p><p style="color: var(--text-muted);">Enter an Epic Games username above to start tracking stats.</p></div>';
          return;
        }

        // Determine MVP (highest total wins)
        let maxWins = -1;
        let mvpPlayer = null;
        squad.forEach(p => {
          if (!p.error && p.overall && (p.overall.wins || 0) > maxWins) {
            maxWins = p.overall.wins;
            mvpPlayer = p.epic_name;
          }
        });

        container.innerHTML = squad.map(p => {
          const trackerUrl = `https://fortnitetracker.com/profile/all/${encodeURIComponent(p.epic_name)}`;
          const isMvp = (p.epic_name === mvpPlayer && maxWins > 0);

          if (p.error) {
            return `
              <div class="player-card" style="border-color: rgba(245, 158, 11, 0.4); background: rgba(30, 41, 59, 0.7);">
                <div class="player-header">
                  <div class="player-name">
                    <span>🎮 ${p.epic_name}</span>
                  </div>
                  <span style="background: rgba(245, 158, 11, 0.2); color: var(--warning); border: 1px solid rgba(245, 158, 11, 0.3); padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700;">
                    🔒 Stats Private
                  </span>
                </div>

                <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 10px; padding: 12px; font-size: 0.8rem; line-height: 1.5; color: #fde68a;">
                  <strong>To make your stats visible:</strong><br>
                  1. Launch Fortnite on your console / PC.<br>
                  2. Open <strong>Settings ➔ Account and Privacy</strong>.<br>
                  3. Under <strong>Gameplay Privacy</strong>, toggle <strong>"Show on Career Leaderboard"</strong> to <strong>ON</strong>.<br>
                  4. Click <em>Re-Check</em> below.
                </div>

                <div style="display: flex; gap: 8px; margin-top: auto; justify-content: space-between; align-items: center; padding-top: 10px;">
                  <a href="${trackerUrl}" target="_blank" style="color: var(--accent); font-size: 0.8rem; font-weight: 700; text-decoration: none;">
                    📊 FortniteTracker ↗
                  </a>
                  <div style="display: flex; gap: 6px;">
                    <button class="btn btn-secondary" style="padding: 6px 12px; font-size: 0.75rem;" onclick="loadSquadStats()">🔄 Re-Check</button>
                    <button class="btn btn-secondary" style="padding: 6px 10px; font-size: 0.75rem; color: var(--error);" onclick="untrackPlayer('${p.epic_name}')" title="Untrack Player">🗑️</button>
                  </div>
                </div>
              </div>
            `;
          }

          const o = p.overall || {};
          return `
            <div class="player-card" style="${isMvp ? 'border-color: rgba(255, 215, 0, 0.5); box-shadow: 0 4px 20px rgba(255, 215, 0, 0.15);' : ''}">
              <div class="player-header">
                <div class="player-name">
                  <span>🏆 ${p.epic_name}</span>
                  ${p.has_controller ? '<span title="Controller Player" style="font-size: 0.9rem;">🎮</span>' : ''}
                  ${p.has_kbm ? '<span title="Keyboard & Mouse Player" style="font-size: 0.9rem;">⌨️</span>' : ''}
                  ${isMvp ? '<span title="Highest Wins in Squad" style="background: rgba(255, 215, 0, 0.2); color: var(--gold); border: 1px solid rgba(255, 215, 0, 0.4); padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: 800;">👑 MVP</span>' : ''}
                </div>
                <span class="player-bp">BP Lvl ${p.bp_level}</span>
              </div>

              <div class="stats-matrix">
                <div class="stat-box">
                  <div class="stat-label">Wins</div>
                  <div class="stat-val" style="color: var(--gold);">${(o.wins || 0).toLocaleString()}</div>
                </div>
                <div class="stat-box">
                  <div class="stat-label">K/D Ratio</div>
                  <div class="stat-val">${(o.kd || 0).toFixed(2)}</div>
                </div>
                <div class="stat-box">
                  <div class="stat-label">Win Rate</div>
                  <div class="stat-val" style="color: var(--success);">${(o.winRate || 0).toFixed(1)}%</div>
                </div>
                <div class="stat-box">
                  <div class="stat-label">Total Kills</div>
                  <div class="stat-val">${(o.kills || 0).toLocaleString()}</div>
                </div>
                <div class="stat-box">
                  <div class="stat-label">Matches</div>
                  <div class="stat-val">${(o.matches || 0).toLocaleString()}</div>
                </div>
                <div class="stat-box">
                  <div class="stat-label">Top 3</div>
                  <div class="stat-val">${(o.top3 || 0).toLocaleString()}</div>
                </div>
              </div>

              <div style="display: flex; flex-direction: column; gap: 6px;">
                <div class="mode-row">
                  <span>👤 <strong>Solo</strong></span>
                  <span>${p.solo?.wins || 0} Wins • ${(p.solo?.kd || 0).toFixed(2)} K/D</span>
                </div>
                <div class="mode-row">
                  <span>👥 <strong>Duo</strong></span>
                  <span>${p.duo?.wins || 0} Wins • ${(p.duo?.kd || 0).toFixed(2)} K/D</span>
                </div>
                <div class="mode-row">
                  <span>🛡️ <strong>Squad</strong></span>
                  <span>${p.squad?.wins || 0} Wins • ${(p.squad?.kd || 0).toFixed(2)} K/D</span>
                </div>
              </div>

              <div style="display: flex; gap: 8px; margin-top: auto; justify-content: space-between; align-items: center; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.06);">
                <a href="${trackerUrl}" target="_blank" style="color: var(--accent); font-size: 0.8rem; font-weight: 700; text-decoration: none;">
                  📊 FortniteTracker ↗
                </a>
                <button class="btn btn-secondary" style="padding: 6px 12px; font-size: 0.75rem; color: var(--error);" onclick="untrackPlayer('${p.epic_name}')" title="Untrack Player">
                  🗑️ Untrack
                </button>
              </div>
            </div>
          `;
        }).join('');
      } catch (e) {
        container.innerHTML = `<p style="color: var(--error);">Error loading squad stats: ${e}</p>`;
      }
    }

    async function loadLiveShop() {
      const container = document.getElementById('shopContainer');
      container.innerHTML = '<p style="color: var(--text-muted);">Loading shop items from Fortnite API...</p>';
      try {
        const res = await fetch('/api/live-shop');
        const data = await res.json();
        document.getElementById('shopMetaDate').innerText = `Date: ${data.date.slice(0, 10)} • Hash: ${data.hash.slice(0, 12)} • Total: ${data.items.length} items`;

        container.innerHTML = data.items.map(item => `
          <div class="shop-item-card">
            ${item.icon ? `<img class="shop-img" src="${item.icon}" loading="lazy">` : '<div style="height: 110px;"></div>'}
            <div class="shop-name">${item.name}</div>
            <div class="shop-price">🪙 ${item.price.toLocaleString()}</div>
          </div>
        `).join('');
      } catch (e) {
        container.innerHTML = `<p style="color: var(--error);">Error loading shop: ${e}</p>`;
      }
    }

    async function loadMap() {
      try {
        const res = await fetch('/api/live-map');
        const data = await res.json();
        if (data.images && data.images.pois) {
          document.getElementById('islandMapImg').src = data.images.pois;
        }
        const poisDiv = document.getElementById('poisContainer');
        const named = (data.pois || []).filter(p => p.name);
        poisDiv.innerHTML = named.map(p => `
          <span style="background: rgba(255,255,255,0.05); border: 1px solid var(--card-border); padding: 4px 10px; border-radius: 20px; font-size: 0.75rem;">
            📍 ${p.name}
          </span>
        `).join('');
      } catch (e) {
        console.error('Map error:', e);
      }
    }

    async function loadNews() {
      const container = document.getElementById('newsContainer');
      container.innerHTML = '<p style="color: var(--text-muted);">Fetching news...</p>';
      try {
        const res = await fetch('/api/live-news');
        const data = await res.json();
        const motds = data.motds || [];
        container.innerHTML = motds.map(n => `
          <div class="news-card">
            ${n.image ? `<img src="${n.image}" loading="lazy">` : ''}
            <div class="news-body">
              <div class="news-title">${n.title || n.tabTitle || 'News'}</div>
              <div class="news-text">${n.body || ''}</div>
            </div>
          </div>
        `).join('');
      } catch (e) {
        container.innerHTML = `<p style="color: var(--error);">Error loading news: ${e}</p>`;
      }
    }

    async function loadChannels() {
      try {
        const res = await fetch('/api/guilds-channels');
        cachedGuilds = await res.json();
        const selector = document.getElementById('guildSelector');
        if (cachedGuilds.length === 0) {
          selector.innerHTML = '<option value="">No servers connected</option>';
          return;
        }
        selector.innerHTML = cachedGuilds.map(g => `<option value="${g.id}">${g.name}</option>`).join('');
        onGuildChange();
      } catch (e) {
        console.error('Error loading channels:', e);
      }
    }

    function onGuildChange() {
      const gid = document.getElementById('guildSelector').value;
      const g = cachedGuilds.find(x => x.id === gid);
      if (!g) return;

      const channels = g.channels || [];
      const s = g.settings || {};

      const shopSelect = document.getElementById('routeShop');
      shopSelect.innerHTML = '<option value="">-- Disabled --</option>' +
        channels.map(c => `<option value="${c.id}" ${s.shop_channel_id === c.id ? 'selected' : ''}>#${c.name}</option>`).join('');

      const newsSelect = document.getElementById('routeNews');
      newsSelect.innerHTML = '<option value="">-- Disabled --</option>' +
        channels.map(c => `<option value="${c.id}" ${s.news_channel_id === c.id ? 'selected' : ''}>#${c.name}</option>`).join('');
    }

    async function saveRouting() {
      const gid = document.getElementById('guildSelector').value;
      if (!gid) return;
      const payload = {
        guild_id: gid,
        shop_channel_id: document.getElementById('routeShop').value,
        news_channel_id: document.getElementById('routeNews').value
      };
      await fetch('/api/guild-settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Admin-Pin': getPin() },
        body: JSON.stringify(payload)
      });
      showToast('Channel settings saved live! 🎯');
      loadChannels();
    }

    async function testShopBroadcast() {
      await fetch('/api/shop/broadcast', {
        method: 'POST',
        headers: { 'X-Admin-Pin': getPin() }
      });
      showToast('Item Shop broadcasted to Discord! 🛒');
    }

    async function savePresence() {
      const text = document.getElementById('statusText').value;
      const act = document.getElementById('activityType').value;
      await fetch('/api/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Admin-Pin': getPin() },
        body: JSON.stringify({ status_text: text, activity_type: act })
      });
      showToast('Status updated on Discord! 🎮');
    }

    window.onload = () => {
      document.getElementById('adminPin').value = localStorage.getItem('ghost_pin') || 'ghost123';
      loadSquadStats();
    };
  </script>
</body>
</html>
"""
