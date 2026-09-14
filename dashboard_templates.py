def get_dashboard_html() -> str:
    """Returns the comprehensive Squad Portal & Fortnite Control Plane single page application."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dadmom Squad Portal • Fortnite Telemetry & Shop</title>
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
      transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
    }
    .shop-item-card:hover { transform: translateY(-3px); }
    .shop-img {
      width: 110px;
      height: 110px;
      object-fit: contain;
      margin-bottom: 8px;
    }
    .shop-name { font-size: 0.85rem; font-weight: 700; margin-bottom: 6px; line-height: 1.3; }
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
      margin-top: auto;
    }

    /* Shop Filter Pills */
    .filter-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 12px;
    }
    .filter-pill {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }
    .filter-pill:hover {
      background: rgba(255, 255, 255, 0.08);
      color: var(--text);
    }
    .filter-pill.active {
      background: rgba(0, 168, 255, 0.2);
      border-color: var(--accent);
      color: var(--accent);
      font-weight: 700;
    }

    /* Rarity Glows */
    .rarity-legendary { border-color: rgba(245, 158, 11, 0.7) !important; box-shadow: 0 0 16px rgba(245, 158, 11, 0.18); }
    .rarity-epic { border-color: rgba(168, 85, 247, 0.7) !important; box-shadow: 0 0 16px rgba(168, 85, 247, 0.18); }
    .rarity-rare { border-color: rgba(59, 130, 246, 0.7) !important; box-shadow: 0 0 16px rgba(59, 130, 246, 0.18); }
    .rarity-uncommon { border-color: rgba(34, 197, 94, 0.7) !important; box-shadow: 0 0 16px rgba(34, 197, 94, 0.18); }
    .rarity-common { border-color: rgba(148, 163, 184, 0.4) !important; }
    .rarity-iconseries { border-color: rgba(6, 182, 212, 0.8) !important; box-shadow: 0 0 18px rgba(6, 182, 212, 0.25); }
    .rarity-gaminglegends { border-color: rgba(147, 51, 234, 0.8) !important; box-shadow: 0 0 18px rgba(147, 51, 234, 0.25); }
    .rarity-marvelseries { border-color: rgba(239, 68, 68, 0.8) !important; box-shadow: 0 0 18px rgba(239, 68, 68, 0.25); }
    .rarity-dc { border-color: rgba(37, 99, 235, 0.8) !important; box-shadow: 0 0 18px rgba(37, 99, 235, 0.25); }
    .rarity-starwars { border-color: rgba(234, 179, 8, 0.8) !important; box-shadow: 0 0 18px rgba(234, 179, 8, 0.25); }

    .item-type-badge {
      position: absolute;
      top: 8px;
      left: 8px;
      font-size: 0.65rem;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 6px;
      background: rgba(0, 0, 0, 0.65);
      color: var(--text-muted);
      backdrop-filter: blur(4px);
    }

    /* Map & Drop Roulette */
    .roulette-box {
      background: linear-gradient(135deg, rgba(0, 168, 255, 0.1), rgba(147, 51, 234, 0.1));
      border: 1px solid rgba(0, 168, 255, 0.3);
      border-radius: 14px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 16px;
      text-align: center;
      width: 100%;
    }
    .drop-target-display {
      font-size: 1.6rem;
      font-weight: 900;
      color: var(--accent);
      text-shadow: 0 0 20px var(--accent-glow);
      letter-spacing: 0.5px;
      padding: 12px 24px;
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid rgba(0, 168, 255, 0.4);
      border-radius: 12px;
      min-width: 280px;
    }
    .custom-poi-chip {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(147, 51, 234, 0.15);
      border: 1px solid rgba(147, 51, 234, 0.4);
      padding: 8px 14px;
      border-radius: 10px;
      font-size: 0.85rem;
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
        <h1>Dadmom</h1>
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
          <div style="flex: 2; min-width: 220px;">
            <input type="text" id="trackPlayerInput" placeholder="Enter username (e.g. Going__Ghost, KING_CONDOR_)" onkeydown="if(event.key==='Enter') trackPlayer()">
          </div>
          <div style="min-width: 150px;">
            <select id="trackPlatform" style="padding: 12px; background: var(--input-bg); border: 1px solid var(--card-border); border-radius: 10px; color: var(--text);">
              <option value="auto">🌐 Auto-Detect</option>
              <option value="psn">🎮 PlayStation (PSN)</option>
              <option value="epic">⚡ Epic Games</option>
              <option value="xbl">💚 Xbox (XBL)</option>
            </select>
          </div>
          <button class="btn btn-primary" id="trackBtn" onclick="trackPlayer()">➕ Track Player</button>
          <div style="flex: 1; min-width: 160px;">
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
          <span>🛒 Today's Fortnite Item Shop (Live & Organized)</span>
          <div style="display: flex; gap: 8px;">
            <button class="btn btn-secondary" onclick="loadLiveShop()">🔄 Refresh Shop</button>
            <button class="btn btn-primary" onclick="testShopBroadcast()">📢 Post to Discord</button>
          </div>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;" id="shopMetaDate">
          Live feed from Fortnite-API. Resets daily at 00:00 UTC.
        </p>

        <!-- Search, Sort & Category Controls -->
        <div style="background: rgba(0, 0, 0, 0.25); border: 1px solid var(--card-border); border-radius: 12px; padding: 16px; margin-bottom: 16px;">
          <div style="display: flex; flex-wrap: wrap; gap: 12px; align-items: center;">
            <div style="flex: 2; min-width: 220px;">
              <input type="text" id="shopSearchInput" placeholder="🔍 Search cosmetics, skins, jam tracks, cars..." oninput="filterShopItems()">
            </div>
            <div style="min-width: 170px;">
              <select id="shopSortSelect" onchange="filterShopItems()">
                <option value="default">↕️ Default Order</option>
                <option value="price-asc">🪙 Price: Low to High</option>
                <option value="price-desc">🪙 Price: High to Low</option>
                <option value="name-asc">🔤 Name: A to Z</option>
                <option value="rarity">✨ By Rarity</option>
              </select>
            </div>
            <div style="font-size: 0.8rem; color: var(--text-muted);" id="shopCountBadge">Loading items...</div>
          </div>

          <!-- Category Pills -->
          <div class="filter-pills" id="shopCategoryPills">
            <button class="filter-pill active" onclick="setShopCategory('all', this)">All Items</button>
            <button class="filter-pill" onclick="setShopCategory('outfit', this)">👕 Outfits / Skins</button>
            <button class="filter-pill" onclick="setShopCategory('pickaxe', this)">⛏️ Pickaxes</button>
            <button class="filter-pill" onclick="setShopCategory('emote', this)">💃 Emotes</button>
            <button class="filter-pill" onclick="setShopCategory('jam track', this)">🎵 Jam Tracks</button>
            <button class="filter-pill" onclick="setShopCategory('vehicle', this)">🏎️ Vehicles</button>
            <button class="filter-pill" onclick="setShopCategory('glider', this)">🪂 Gliders & Wraps</button>
            <button class="filter-pill" onclick="setShopCategory('other', this)">📦 Bundles & Other</button>
          </div>
        </div>

        <div id="shopContainer" class="shop-grid">
          <p style="color: var(--text-muted);">Fetching current shop items...</p>
        </div>
      </div>
    </section>

    <!-- TAB 3: ISLAND MAP & TACTICAL SQUAD DROPS -->
    <section id="tab-map" class="tab-content">
      <!-- Roulette & Broadcaster -->
      <div class="card" style="border-color: rgba(0, 168, 255, 0.35);">
        <div class="card-title">
          <span>🎲 Squad Drop Roulette & Tactical Landing</span>
        </div>
        <div class="roulette-box">
          <p style="font-size: 0.85rem; color: var(--text-muted);">
            Can't agree on where to drop? Spin the wheel to pick a random Island POI or your custom squad drop spots!
          </p>
          <div class="drop-target-display" id="rouletteDisplay">
            🎯 Ready to Drop — Click Spin!
          </div>
          <div style="display: flex; gap: 12px; flex-wrap: wrap; justify-content: center;">
            <button class="btn btn-primary" id="spinDropBtn" onclick="spinDropSpot()">🎲 Spin Drop Spot</button>
            <button class="btn btn-secondary" id="broadcastDropBtn" onclick="broadcastCurrentDrop()" disabled>📢 Broadcast Drop to Discord</button>
          </div>
        </div>
      </div>

      <!-- Island Map Card -->
      <div class="card">
        <div class="card-title">
          <span>🗺️ Chapter 5 Island Satellite & Named Locations</span>
          <div style="display: flex; gap: 8px;">
            <button class="btn btn-secondary" id="mapViewPoiBtn" style="background: rgba(0, 168, 255, 0.2); border: 1px solid var(--accent); color: var(--accent);" onclick="switchMapView('poi')">🏷️ Labeled POIs</button>
            <button class="btn btn-secondary" id="mapViewCleanBtn" onclick="switchMapView('clean')">🏝️ Clean Satellite</button>
            <button class="btn btn-secondary" onclick="loadMap()">🔄 Refresh</button>
          </div>
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; gap: 20px;">
          <img id="islandMapImg" src="https://fortnite-api.com/images/map_en.png" style="width: 100%; max-width: 820px; border-radius: 12px; border: 1px solid var(--card-border); box-shadow: 0 8px 30px rgba(0,0,0,0.5);" alt="Fortnite Map">
        </div>
      </div>

      <!-- Custom Squad Drop Spots Manager -->
      <div class="card">
        <div class="card-title">
          <span>📍 Custom Squad Drop Spots & Callouts</span>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">
          Add your squad's favorite unmarked spots, secret vaults, or callouts (saved permanently in MongoDB Atlas).
        </p>
        <div style="background: rgba(0, 0, 0, 0.25); border: 1px solid var(--card-border); border-radius: 12px; padding: 16px; margin-bottom: 20px; display: flex; flex-wrap: wrap; gap: 12px; align-items: center;">
          <input type="text" id="customPoiName" placeholder="Spot Name (e.g. Condor's Castle, Loot Bunker 3)" style="flex: 2; min-width: 200px;">
          <input type="text" id="customPoiNote" placeholder="Notes (e.g. 3 slurp barrels, high ground)" style="flex: 3; min-width: 220px;">
          <button class="btn btn-primary" onclick="submitCustomPoi()">➕ Save Drop Spot</button>
        </div>
        <div id="customPoisList" style="display: flex; flex-wrap: wrap; gap: 10px;">
          <p style="color: var(--text-muted); font-size: 0.85rem;">No custom drop spots saved yet.</p>
        </div>
      </div>

      <!-- Official POIs Directory -->
      <div class="card">
        <div class="card-title">
          <span>📍 Official Island Named Locations</span>
          <input type="text" id="filterPoisInput" placeholder="🔍 Search POIs..." style="max-width: 250px; padding: 8px 12px; font-size: 0.8rem;" oninput="filterMapPois()">
        </div>
        <div id="poisContainer" style="display: flex; flex-wrap: wrap; gap: 8px;"></div>
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
          <div class="hint">Where Dadmom announces when a squad member wins a match.</div>
        </div>

        <div style="display: flex; gap: 12px; margin-top: 18px;">
          <button class="btn btn-primary" onclick="saveRouting()">💾 Save Channel Settings</button>
          <button class="btn btn-secondary" onclick="testShopBroadcast()">📢 Test Post Shop</button>
        </div>
      </div>
    </section>

    <!-- TAB 6: BOT STATUS & PRESENCE -->
    <section id="tab-status" class="tab-content">
      <!-- GUIDE: HOW TO REMOVE KITE.ONL / CHANGE PROFILE -->
      <div class="card" style="border-color: rgba(0, 168, 255, 0.35);">
        <div class="card-title">
          <span>"🪁 Text Box for Instructions"</span>
        </div>
          </div>
        </div>
      </div>

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
      const platformSelect = document.getElementById('trackPlatform');
      const platform = platformSelect ? platformSelect.value : 'auto';
      if (!name) return;
      const btn = document.getElementById('trackBtn');
      const oldText = btn.innerText;
      btn.innerText = '⏳ Checking...';
      btn.disabled = true;

      try {
        const res = await fetch('/api/players/track', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ epic_name: name, account_type: platform })
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
          container.innerHTML = '<div style="grid-column: 1/-1; padding: 30px; background: rgba(255,255,255,0.02); border-radius: 12px; text-align: center;"><p style="font-size: 1.1rem; margin-bottom: 8px;">No squad members tracked yet!</p><p style="color: var(--text-muted);">Enter an Epic, PlayStation, or Xbox username above to start tracking stats.</p></div>';
          return;
        }

        // Sort by overall wins descending so squad leaderboard ranks top to bottom
        squad.sort((a, b) => ((b.overall?.wins || 0) - (a.overall?.wins || 0)));

        // Determine MVP (highest total wins)
        let maxWins = -1;
        let mvpPlayer = null;
        squad.forEach(p => {
          if (!p.error && p.overall && (p.overall.wins || 0) > maxWins) {
            maxWins = p.overall.wins;
            mvpPlayer = p.epic_name;
          }
        });

        container.innerHTML = squad.map((p, idx) => {
          let trackerUrl = `https://fortnitetracker.com/profile/all/${encodeURIComponent(p.epic_name)}`;
          if (p.account_type === 'psn') {
            trackerUrl = `https://fortnitetracker.com/profile/psn/${encodeURIComponent(p.epic_name)}`;
          } else if (p.account_type === 'xbl') {
            trackerUrl = `https://fortnitetracker.com/profile/xbl/${encodeURIComponent(p.epic_name)}`;
          }

          let platBadge = '<span style="background: rgba(255,255,255,0.06); border: 1px solid var(--card-border); color: var(--text-muted); padding: 2px 7px; border-radius: 10px; font-size: 0.65rem; font-weight: 700;">⚡ Epic</span>';
          if (p.account_type === 'psn') {
            platBadge = '<span style="background: rgba(0, 112, 209, 0.2); border: 1px solid rgba(0, 112, 209, 0.4); color: #38bdf8; padding: 2px 7px; border-radius: 10px; font-size: 0.65rem; font-weight: 700;">🎮 PSN</span>';
          } else if (p.account_type === 'xbl') {
            platBadge = '<span style="background: rgba(16, 124, 65, 0.2); border: 1px solid rgba(16, 124, 65, 0.4); color: #4ade80; padding: 2px 7px; border-radius: 10px; font-size: 0.65rem; font-weight: 700;">💚 Xbox</span>';
          }

          const isMvp = (p.epic_name === mvpPlayer && maxWins > 0);

          if (p.error) {
            return `
              <div class="player-card" style="border-color: rgba(245, 158, 11, 0.4); background: rgba(30, 41, 59, 0.7);">
                <div class="player-header">
                  <div class="player-name">
                    <span>${p.epic_name}</span>
                    ${platBadge}
                  </div>
                  <span style="background: rgba(245, 158, 11, 0.2); color: var(--warning); border: 1px solid rgba(245, 158, 11, 0.3); padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700;">
                    🔒 Stats Private
                  </span>
                </div>

                <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 10px; padding: 12px; font-size: 0.8rem; line-height: 1.5; color: #fde68a;">
                  <strong>To show stats here:</strong><br>
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
                  <span style="font-size: 0.8rem; color: var(--text-muted); font-weight: 800;">#${idx + 1}</span>
                  <span>🏆 ${p.epic_name}</span>
                  ${platBadge}
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

    let rawShopItems = [];
    let currentShopCategory = 'all';

    async function loadLiveShop() {
      const container = document.getElementById('shopContainer');
      container.innerHTML = '<p style="color: var(--text-muted);">Loading live item shop from Fortnite-API...</p>';
      try {
        const res = await fetch('/api/live-shop');
        const data = await res.json();
        rawShopItems = data.items || [];

        const dateStr = data.date ? data.date.slice(0, 10) : 'Today';
        const hashStr = data.hash ? data.hash.slice(0, 10) : 'Latest';
        document.getElementById('shopMetaDate').innerText = `Date: ${dateStr} • Hash: ${hashStr} • Total Items in Catalog: ${rawShopItems.length}`;

        filterShopItems();
      } catch (e) {
        container.innerHTML = `<p style="color: var(--error);">Error loading shop: ${e}</p>`;
      }
    }

    function setShopCategory(cat, btn) {
      currentShopCategory = cat.toLowerCase();
      document.querySelectorAll('#shopCategoryPills .filter-pill').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      filterShopItems();
    }

    function filterShopItems() {
      const q = (document.getElementById('shopSearchInput').value || '').toLowerCase().trim();
      const sortMode = document.getElementById('shopSortSelect').value;

      let filtered = rawShopItems.filter(item => {
        // Category check
        if (currentShopCategory !== 'all') {
          const it = (item.item_type || '').toLowerCase();
          const cat = (item.category || '').toLowerCase();
          if (currentShopCategory === 'outfit' && !it.includes('outfit') && !cat.includes('outfit')) return false;
          if (currentShopCategory === 'pickaxe' && !it.includes('pickaxe') && !it.includes('harvesting') && !cat.includes('pickaxe')) return false;
          if (currentShopCategory === 'emote' && !it.includes('emote') && !it.includes('dance') && !cat.includes('emote')) return false;
          if (currentShopCategory === 'jam track' && !it.includes('jam track') && !cat.includes('jam track') && !cat.includes('track')) return false;
          if (currentShopCategory === 'vehicle' && !it.includes('vehicle') && !it.includes('car') && !cat.includes('vehicle')) return false;
          if (currentShopCategory === 'glider' && !it.includes('glider') && !it.includes('wrap') && !cat.includes('glider') && !cat.includes('wrap')) return false;
          if (currentShopCategory === 'other') {
            const known = ['outfit', 'pickaxe', 'harvesting', 'emote', 'dance', 'jam track', 'vehicle', 'car', 'glider', 'wrap'];
            if (known.some(k => it.includes(k) || cat.includes(k))) return false;
          }
        }

        // Search check
        if (q) {
          const matchName = (item.name || '').toLowerCase().includes(q);
          const matchType = (item.item_type || '').toLowerCase().includes(q);
          const matchCat = (item.category || '').toLowerCase().includes(q);
          const matchRarity = (item.rarity || '').toLowerCase().includes(q);
          if (!matchName && !matchType && !matchCat && !matchRarity) return false;
        }

        return true;
      });

      // Sorting
      if (sortMode === 'price-asc') {
        filtered.sort((a, b) => (a.price || 0) - (b.price || 0));
      } else if (sortMode === 'price-desc') {
        filtered.sort((a, b) => (b.price || 0) - (a.price || 0));
      } else if (sortMode === 'name-asc') {
        filtered.sort((a, b) => (a.name || '').localeCompare(b.name || ''));
      } else if (sortMode === 'rarity') {
        const rarityScore = { legendary: 5, epic: 4, rare: 3, uncommon: 2, common: 1, iconseries: 6, gaminglegends: 6, marvelseries: 6, starwars: 6, dc: 6 };
        filtered.sort((a, b) => (rarityScore[b.rarity_clean] || 0) - (rarityScore[a.rarity_clean] || 0));
      }

      document.getElementById('shopCountBadge').innerText = `Showing ${filtered.length} of ${rawShopItems.length} items`;
      renderShopItems(filtered);
    }

    function renderShopItems(items) {
      const container = document.getElementById('shopContainer');
      if (items.length === 0) {
        container.innerHTML = '<div style="grid-column: 1/-1; padding: 40px; text-align: center; color: var(--text-muted);"><p style="font-size: 1.1rem;">No items match your filter!</p><p style="font-size: 0.85rem; margin-top: 6px;">Try clearing your search query or selecting "All Items".</p></div>';
        return;
      }

      container.innerHTML = items.map(item => {
        const rarityClass = 'rarity-' + (item.rarity_clean || 'common');
        return `
          <div class="shop-item-card ${rarityClass}">
            <span class="item-type-badge">${item.item_type || 'Cosmetic'}</span>
            ${item.icon ? `<img class="shop-img" src="${item.icon}" loading="lazy" alt="${item.name}">` : '<div style="height: 110px; display:flex; align-items:center; justify-content:center; font-size:2rem;">🎁</div>'}
            <div class="shop-name" title="${item.name}">${item.name}</div>
            <div class="shop-price">🪙 ${(item.price || 0).toLocaleString()}</div>
          </div>
        `;
      }).join('');
    }

    let mapImages = {};
    let islandPois = [];
    let customPois = [];
    let selectedDropTarget = null;

    async function loadMap() {
      try {
        const res = await fetch('/api/live-map');
        const data = await res.json();
        mapImages = data.images || {};
        islandPois = (data.pois || []).filter(p => p.name);
        customPois = data.custom_pois || [];

        if (mapImages.pois) {
          document.getElementById('islandMapImg').src = mapImages.pois;
        }

        renderCustomPois();
        renderOfficialPois(islandPois);
      } catch (e) {
        console.error('Map error:', e);
      }
    }

    function switchMapView(mode) {
      const img = document.getElementById('islandMapImg');
      const poiBtn = document.getElementById('mapViewPoiBtn');
      const cleanBtn = document.getElementById('mapViewCleanBtn');

      if (mode === 'clean' && mapImages.blank) {
        img.src = mapImages.blank;
        cleanBtn.style.background = 'rgba(0, 168, 255, 0.2)';
        cleanBtn.style.borderColor = 'var(--accent)';
        cleanBtn.style.color = 'var(--accent)';
        poiBtn.style.background = '';
        poiBtn.style.borderColor = '';
        poiBtn.style.color = '';
      } else {
        img.src = mapImages.pois || 'https://fortnite-api.com/images/map_en.png';
        poiBtn.style.background = 'rgba(0, 168, 255, 0.2)';
        poiBtn.style.borderColor = 'var(--accent)';
        poiBtn.style.color = 'var(--accent)';
        cleanBtn.style.background = '';
        cleanBtn.style.borderColor = '';
        cleanBtn.style.color = '';
      }
    }

    function renderCustomPois() {
      const listDiv = document.getElementById('customPoisList');
      if (!customPois || customPois.length === 0) {
        listDiv.innerHTML = '<p style="color: var(--text-muted); font-size: 0.85rem;">No custom drop spots saved yet. Add your squad secret spots above!</p>';
        return;
      }
      listDiv.innerHTML = customPois.map(p => {
        const safeName = encodeURIComponent(p.name);
        return `
          <div class="custom-poi-chip">
            <span style="cursor: pointer;" data-name="${safeName}" onclick="selectDropSpot(decodeURIComponent(this.dataset.name))" title="Select as drop target">
              📍 <strong>${p.name}</strong> ${p.note ? `<span style="color: var(--text-muted); font-size: 0.75rem;">(${p.note})</span>` : ''}
            </span>
            <button style="background: transparent; border: none; color: var(--error); cursor: pointer; font-size: 0.85rem; padding: 0 4px;" data-name="${safeName}" onclick="deleteCustomPoi(decodeURIComponent(this.dataset.name))" title="Delete custom spot">✕</button>
          </div>
        `;
      }).join('');
    }

    function renderOfficialPois(list) {
      const poisDiv = document.getElementById('poisContainer');
      poisDiv.innerHTML = list.map(p => `
        <button class="filter-pill" data-name="${encodeURIComponent(p.name)}" onclick="selectDropSpot(decodeURIComponent(this.dataset.name))" style="cursor: pointer;">
          📍 ${p.name}
        </button>
      `).join('');
    }

    function filterMapPois() {
      const q = (document.getElementById('filterPoisInput').value || '').toLowerCase().trim();
      const filtered = islandPois.filter(p => p.name.toLowerCase().includes(q));
      renderOfficialPois(filtered);
    }

    function selectDropSpot(name) {
      selectedDropTarget = name;
      const display = document.getElementById('rouletteDisplay');
      display.innerText = `🎯 Target Drop: ${name}`;
      display.style.borderColor = 'var(--gold)';
      display.style.color = 'var(--gold)';
      const broadcastBtn = document.getElementById('broadcastDropBtn');
      broadcastBtn.disabled = false;
      broadcastBtn.innerText = `📢 Broadcast "${name}" to Discord`;
      showToast(`Selected drop spot: ${name}`);
    }

    let isSpinning = false;
    function spinDropSpot() {
      if (isSpinning) return;
      const allCandidates = [
        ...islandPois.map(p => p.name),
        ...customPois.map(p => p.name)
      ];
      if (allCandidates.length === 0) {
        showToast('No POIs available to spin!');
        return;
      }

      isSpinning = true;
      const display = document.getElementById('rouletteDisplay');
      const spinBtn = document.getElementById('spinDropBtn');
      const broadcastBtn = document.getElementById('broadcastDropBtn');
      broadcastBtn.disabled = true;
      spinBtn.disabled = true;

      let counter = 0;
      const maxSpins = 20;
      const interval = setInterval(() => {
        const randomChoice = allCandidates[Math.floor(Math.random() * allCandidates.length)];
        display.innerText = `🎲 ${randomChoice}`;
        display.style.borderColor = 'var(--accent)';
        display.style.color = 'var(--text)';
        counter++;

        if (counter >= maxSpins) {
          clearInterval(interval);
          const finalSpot = allCandidates[Math.floor(Math.random() * allCandidates.length)];
          selectedDropTarget = finalSpot;
          display.innerText = `🏆 SQUAD DROP: ${finalSpot}!`;
          display.style.borderColor = 'var(--gold)';
          display.style.color = 'var(--gold)';
          broadcastBtn.disabled = false;
          broadcastBtn.innerText = `📢 Broadcast "${finalSpot}" to Discord`;
          spinBtn.disabled = false;
          isSpinning = false;
          showToast(`Drop location locked: ${finalSpot}! 🎯`);
        }
      }, 70);
    }

    async function broadcastCurrentDrop() {
      if (!selectedDropTarget) return;
      const btn = document.getElementById('broadcastDropBtn');
      const oldText = btn.innerText;
      btn.innerText = '⏳ Broadcasting...';
      btn.disabled = true;

      try {
        const res = await fetch('/api/drop/broadcast', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-Admin-Pin': getPin() },
          body: JSON.stringify({ poi_name: selectedDropTarget })
        });
        const data = await res.json();
        if (res.ok) {
          showToast(`🎯 Broadcasted ${selectedDropTarget} to ${data.posted_to || 1} Discord channel(s)!`);
        } else {
          showToast('Error: ' + data.message);
        }
      } catch (e) {
        showToast('Error: ' + e);
      } finally {
        btn.innerText = oldText;
        btn.disabled = false;
      }
    }

    async function submitCustomPoi() {
      const nameInput = document.getElementById('customPoiName');
      const noteInput = document.getElementById('customPoiNote');
      const name = nameInput.value.trim();
      const note = noteInput.value.trim();
      if (!name) {
        showToast('Please enter a spot name!');
        return;
      }

      try {
        const res = await fetch('/api/pois/custom', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-Admin-Pin': getPin() },
          body: JSON.stringify({ name, note })
        });
        const data = await res.json();
        if (res.ok) {
          showToast(`Added custom drop spot: ${name} 📍`);
          nameInput.value = '';
          noteInput.value = '';
          await loadMap();
        } else {
          showToast('Error: ' + data.message);
        }
      } catch (e) {
        showToast('Error: ' + e);
      }
    }

    async function deleteCustomPoi(name) {
      if (!confirm(`Delete custom spot "${name}"?`)) return;
      try {
        const res = await fetch('/api/pois/custom/delete', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-Admin-Pin': getPin() },
          body: JSON.stringify({ name })
        });
        const data = await res.json();
        if (res.ok) {
          showToast(`Removed ${name}`);
          await loadMap();
        } else {
          showToast('Error: ' + data.message);
        }
      } catch (e) {
        showToast('Error: ' + e);
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
