def get_dashboard_html() -> str:
    """Returns the full HTML, CSS, and JS Single Page Application for the bot dashboard."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ghost Control Plane • Channel Routing & Customization</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0b0f19;
      --card-bg: rgba(18, 24, 39, 0.8);
      --card-border: rgba(255, 255, 255, 0.08);
      --accent: #00a8ff;
      --accent-glow: rgba(0, 168, 255, 0.35);
      --accent-purple: #9333ea;
      --success: #10b981;
      --warning: #f59e0b;
      --error: #ef4444;
      --text: #f3f4f6;
      --text-muted: #9ca3af;
      --input-bg: #151d30;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', sans-serif;
      background: radial-gradient(circle at 15% 15%, #18223d 0%, var(--bg) 65%);
      color: var(--text);
      min-height: 100vh;
      display: flex;
    }
    aside {
      width: 270px;
      background: rgba(11, 15, 25, 0.95);
      border-right: 1px solid var(--card-border);
      display: flex;
      flex-direction: column;
      padding: 24px 16px;
      gap: 28px;
      backdrop-filter: blur(12px);
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 0 8px;
    }
    .brand-icon {
      width: 42px;
      height: 42px;
      border-radius: 12px;
      background: linear-gradient(135deg, var(--accent), var(--accent-purple));
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.2rem;
      box-shadow: 0 0 20px var(--accent-glow);
    }
    .brand-text h1 { font-size: 1.15rem; font-weight: 800; }
    .brand-text p { font-size: 0.75rem; color: var(--accent); font-weight: 600; text-transform: uppercase; }

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
      max-width: 1200px;
    }
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 28px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--card-border);
    }
    .header-title h2 { font-size: 1.7rem; font-weight: 800; }
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

    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 18px;
      margin-bottom: 28px;
    }
    .kpi-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 20px;
      backdrop-filter: blur(10px);
    }
    .kpi-label { font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700; }
    .kpi-value { font-size: 1.6rem; font-weight: 800; margin-top: 8px; font-family: 'JetBrains Mono', monospace; }
    .kpi-desc { font-size: 0.8rem; color: var(--accent); margin-top: 4px; }

    .card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 24px;
      backdrop-filter: blur(10px);
    }
    .card-title {
      font-size: 1.2rem;
      font-weight: 700;
      margin-bottom: 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .form-group { margin-bottom: 20px; }
    label {
      display: block;
      font-size: 0.85rem;
      font-weight: 600;
      margin-bottom: 8px;
      color: var(--text);
    }
    .hint { font-size: 0.75rem; color: var(--text-muted); margin-top: 5px; }

    input[type="text"], input[type="password"], select, textarea {
      width: 100%;
      background: var(--input-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 12px 14px;
      color: var(--text);
      font-size: 0.9rem;
      outline: none;
      transition: border-color 0.2s;
    }
    input[type="text"]:focus, select:focus, textarea:focus {
      border-color: var(--accent);
      box-shadow: 0 0 10px var(--accent-glow);
    }

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
    .btn-primary {
      background: linear-gradient(135deg, var(--accent), #0077ff);
      color: #fff;
      box-shadow: 0 4px 14px var(--accent-glow);
    }
    .btn-primary:hover { opacity: 0.9; transform: scale(1.02); }
    .btn-secondary {
      background: rgba(255, 255, 255, 0.08);
      color: var(--text);
    }
    .btn-secondary:hover { background: rgba(255, 255, 255, 0.14); }

    .color-swatches { display: flex; gap: 10px; margin-top: 8px; flex-wrap: wrap; }
    .swatch {
      width: 36px;
      height: 36px;
      border-radius: 10px;
      cursor: pointer;
      border: 2px solid transparent;
      transition: transform 0.2s;
    }
    .swatch:hover { transform: scale(1.1); }
    .swatch.active { border-color: #fff; box-shadow: 0 0 12px #fff; }

    table { width: 100%; border-collapse: collapse; margin-top: 12px; }
    th, td { padding: 12px 16px; text-align: left; font-size: 0.85rem; border-bottom: 1px solid var(--card-border); }
    th { color: var(--text-muted); text-transform: uppercase; font-size: 0.75rem; font-weight: 700; }
    tr:hover td { background: rgba(255, 255, 255, 0.02); }

    .channel-box {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 18px;
      margin-bottom: 16px;
    }
    .channel-box-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }
    .badge {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 0.7rem;
      font-weight: 700;
      text-transform: uppercase;
    }
    .badge-blue { background: rgba(0, 168, 255, 0.2); color: var(--accent); }
    .badge-purple { background: rgba(147, 51, 234, 0.2); color: #c084fc; }

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
      aside { width: 100%; border-right: none; border-bottom: 1px solid var(--card-border); }
      main { padding: 20px; }
    }
  </style>
</head>
<body>

  <!-- Sidebar Navigation -->
  <aside>
    <div class="brand">
      <div class="brand-icon">⚡</div>
      <div class="brand-text">
        <h1>GHOST</h1>
        <p>Control Plane</p>
      </div>
    </div>

    <nav>
      <button class="nav-btn active" onclick="switchTab('routing')">🎯 Channel Routing</button>
      <button class="nav-btn" onclick="switchTab('overview')">📊 Telemetry</button>
      <button class="nav-btn" onclick="switchTab('presence')">🎮 Presence & Status</button>
      <button class="nav-btn" onclick="switchTab('theme')">🎨 Colors & Theme</button>
      <button class="nav-btn" onclick="switchTab('players')">👥 Linked Players</button>
      <button class="nav-btn" onclick="switchTab('drops')">📍 Custom Drop POIs</button>
    </nav>

    <div style="margin-top: auto; padding: 12px; background: rgba(255,255,255,0.03); border-radius: 12px; border: 1px solid var(--card-border);">
      <p style="font-size: 0.75rem; color: var(--text-muted);">Admin Session PIN</p>
      <input type="password" id="adminPin" placeholder="ghost123" style="margin-top: 6px; padding: 8px 10px; font-size: 0.8rem;" oninput="savePin()">
    </div>
  </aside>

  <!-- Main Content Area -->
  <main>
    <header>
      <div class="header-title">
        <h2 id="pageTitle">Channel Post Routing</h2>
        <p>Specify exact channels for Item Shop drops, in-game news, and commands.</p>
      </div>
      <div class="auth-badge">
        <div class="status-dot"></div>
        <span id="gatewayStatus">Connecting...</span>
      </div>
    </header>

    <!-- TAB 1: CHANNEL ROUTING (PRIMARY USER FOCUS) -->
    <section id="tab-routing" class="tab-content active">
      <div class="card">
        <div class="card-title">
          <span>🎯 Server Channel Matrix</span>
          <button class="btn btn-secondary" onclick="loadGuildRouting()">🔄 Reload Channels</button>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 20px;">
          Select target text channels for each content type. Ghost routes messages directly without role pings.
        </p>

        <!-- Guild Selector -->
        <div class="form-group">
          <label>Target Discord Server</label>
          <select id="guildSelector" onchange="onGuildSelectChange()">
            <option value="">Loading connected servers...</option>
          </select>
          <div class="hint">Choose the server to configure.</div>
        </div>

        <div id="routingForms">
          <!-- Item Shop Channel Routing -->
          <div class="channel-box">
            <div class="channel-box-header">
              <div>
                <span class="badge badge-blue">Content Type</span>
                <strong style="margin-left: 8px; font-size: 1rem;">Daily Item Shop Drops</strong>
              </div>
              <button class="btn btn-secondary" style="padding: 6px 12px; font-size: 0.8rem;" onclick="testPostShop()">🚀 Test Post Shop Now</button>
            </div>
            <div class="form-group" style="margin-bottom: 12px;">
              <label>Select Channel for Item Shop</label>
              <select id="routeShopChannel">
                <option value="">-- Choose Channel --</option>
              </select>
              <div class="hint">Recommended: <code>#fortnite</code>, <code>#item-shop</code>, or <code>#general</code>.</div>
            </div>
            <div style="display: flex; gap: 20px; flex-wrap: wrap;">
              <label style="display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 0.85rem;">
                <input type="checkbox" id="routeAutoShop" checked> Auto-broadcast daily at 00:00 UTC
              </label>
            </div>
          </div>

          <!-- In-Game News Channel Routing -->
          <div class="channel-box">
            <div class="channel-box-header">
              <div>
                <span class="badge badge-purple">Content Type</span>
                <strong style="margin-left: 8px; font-size: 1rem;">Battle Royale In-Game News & Updates</strong>
              </div>
              <button class="btn btn-secondary" style="padding: 6px 12px; font-size: 0.8rem;" onclick="testPostNews()">📰 Test Post News Now</button>
            </div>
            <div class="form-group" style="margin-bottom: 12px;">
              <label>Select Channel for News</label>
              <select id="routeNewsChannel">
                <option value="">-- Disabled (Do not post news) --</option>
              </select>
              <div class="hint">Posts official Epic Games banners and update patch notices.</div>
            </div>
            <div style="display: flex; gap: 20px; flex-wrap: wrap;">
              <label style="display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 0.85rem;">
                <input type="checkbox" id="routeAutoNews"> Auto-post new in-game announcements
              </label>
            </div>
          </div>

          <!-- Bot Command Restrict Channel -->
          <div class="channel-box">
            <div class="channel-box-header">
              <div>
                <span class="badge" style="background: rgba(255,255,255,0.1);">Optional</span>
                <strong style="margin-left: 8px; font-size: 1rem;">Dedicated Bot Commands Channel</strong>
              </div>
            </div>
            <div class="form-group" style="margin-bottom: 0;">
              <label>Designated Commands Channel</label>
              <select id="routeCommandsChannel">
                <option value="">-- Allow commands in all channels --</option>
              </select>
              <div class="hint">Guides members to use <code>/stats</code> and <code>/leaderboard</code> in a specific room.</div>
            </div>
          </div>

          <!-- Save Button -->
          <button class="btn btn-primary" onclick="saveGuildRouting()" style="margin-top: 10px;">💾 Save Channel Routing</button>
        </div>
      </div>
    </section>

    <!-- TAB 2: TELEMETRY -->
    <section id="tab-overview" class="tab-content">
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-label">Gateway Latency</div>
          <div class="kpi-value" id="kpiPing">-- ms</div>
          <div class="kpi-desc">Discord WebSocket</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Connected Guilds</div>
          <div class="kpi-value" id="kpiGuilds">--</div>
          <div class="kpi-desc">Active Servers</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Storage Backend</div>
          <div class="kpi-value" id="kpiDb" style="color: var(--success); font-size: 1.3rem;">MongoDB Atlas</div>
          <div class="kpi-desc">Live Cluster</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Shop Hash</div>
          <div class="kpi-value" id="kpiShopHash" style="font-size: 1.1rem; overflow: hidden; text-overflow: ellipsis;">--</div>
          <div class="kpi-desc">Daily Rotation State</div>
        </div>
      </div>
    </section>

    <!-- TAB 3: PRESENCE & IDENTITY -->
    <section id="tab-presence" class="tab-content">
      <div class="card">
        <div class="card-title">
          <span>🎮 Bot Activity & Status</span>
        </div>
        <div class="form-group">
          <label>Status Text</label>
          <input type="text" id="statusText" placeholder="e.g. Fortnite Item Shop & /help">
          <div class="hint">Visible under Ghost's username in Discord.</div>
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
        <div class="form-group">
          <label>Presence Mode</label>
          <select id="presenceStatus">
            <option value="online">🟢 Online</option>
            <option value="idle">🟡 Idle / Away</option>
            <option value="dnd">🔴 Do Not Disturb</option>
          </select>
        </div>
        <button class="btn btn-primary" onclick="savePresence()">💾 Save Presence Changes</button>
      </div>
    </section>

    <!-- TAB 4: THEME & EMBEDS -->
    <section id="tab-theme" class="tab-content">
      <div class="card">
        <div class="card-title">
          <span>🎨 Embed Colors & Visual Styling</span>
        </div>
        <div class="form-group">
          <label>Primary Embed Accent Color</label>
          <input type="text" id="embedColor" value="#00A8FF" style="width: 160px; font-family: 'JetBrains Mono', monospace;">
          <div class="color-swatches">
            <div class="swatch" style="background: #00A8FF;" onclick="setColor('#00A8FF')"></div>
            <div class="swatch" style="background: #9333EA;" onclick="setColor('#9333EA')"></div>
            <div class="swatch" style="background: #10B981;" onclick="setColor('#10B981')"></div>
            <div class="swatch" style="background: #F59E0B;" onclick="setColor('#F59E0B')"></div>
            <div class="swatch" style="background: #EF4444;" onclick="setColor('#EF4444')"></div>
            <div class="swatch" style="background: #EC4899;" onclick="setColor('#EC4899')"></div>
          </div>
        </div>
        <div class="form-group">
          <label>Embed Footer Text</label>
          <input type="text" id="embedFooter" placeholder="Fortnite-API.com • Ghost Bot">
        </div>
        <button class="btn btn-primary" onclick="saveThemeSettings()">💾 Save Theme Changes</button>
      </div>
    </section>

    <!-- TAB 5: LINKED PLAYERS -->
    <section id="tab-players" class="tab-content">
      <div class="card">
        <div class="card-title">
          <span>👥 Linked Epic Games Accounts</span>
          <button class="btn btn-secondary" onclick="loadPlayers()">🔄 Refresh Table</button>
        </div>
        <table id="playersTable">
          <thead>
            <tr>
              <th>Discord User ID</th>
              <th>Epic Games Username</th>
              <th>Linked At</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody id="playersBody">
            <tr><td colspan="4" style="text-align: center; color: var(--text-muted);">Loading players...</td></tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- TAB 6: CUSTOM DROP POIS -->
    <section id="tab-drops" class="tab-content">
      <div class="card">
        <div class="card-title">
          <span>📍 Squad Drop Custom Locations</span>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">
          Add custom secret spots, troll locations, or squad nicknames to the <code>/drop</code> roulette.
        </p>
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
          <input type="text" id="newPoiInput" placeholder="e.g. Grandma's Secret Cabin" style="flex: 1;">
          <button class="btn btn-primary" onclick="addCustomPoi()">➕ Add Location</button>
        </div>
        <ul id="customPoiList" style="list-style: none; display: flex; flex-direction: column; gap: 8px;"></ul>
      </div>
    </section>

  </main>

  <div id="toast">Settings updated successfully!</div>

  <script>
    let globalConfig = {};
    let cachedGuilds = [];

    function switchTab(tabId) {
      document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
      const activeBtn = Array.from(document.querySelectorAll('.nav-btn')).find(b => b.getAttribute('onclick').includes(tabId));
      if (activeBtn) activeBtn.classList.add('active');
      const target = document.getElementById('tab-' + tabId);
      if (target) target.classList.add('active');
      if (tabId === 'players') loadPlayers();
      if (tabId === 'routing') loadGuildRouting();
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
      const pin = document.getElementById('adminPin').value;
      localStorage.setItem('ghost_pin', pin);
    }

    function setColor(hex) {
      document.getElementById('embedColor').value = hex;
    }

    async function fetchStatus() {
      try {
        const res = await fetch('/api/status');
        const data = await res.json();
        document.getElementById('kpiPing').innerText = data.ping + ' ms';
        document.getElementById('kpiGuilds').innerText = data.guild_count;
        document.getElementById('gatewayStatus').innerText = data.online ? 'Online (Gateway OK)' : 'Connecting...';
        document.getElementById('kpiShopHash').innerText = data.last_shop_hash || 'c7f7afc5...';
      } catch (err) {
        document.getElementById('gatewayStatus').innerText = 'Offline / Error';
      }
    }

    async function loadGuildRouting() {
      try {
        const res = await fetch('/api/guilds-channels');
        cachedGuilds = await res.json();
        const selector = document.getElementById('guildSelector');

        if (cachedGuilds.length === 0) {
          selector.innerHTML = '<option value="">No servers found. Invite bot to a server first!</option>';
          return;
        }

        selector.innerHTML = cachedGuilds.map((g, idx) => `
          <option value="${g.id}">${g.name} (${g.channels.length} text channels)</option>
        `).join('');

        onGuildSelectChange();
      } catch (e) {
        console.error('Failed to load guilds:', e);
      }
    }

    function onGuildSelectChange() {
      const selectedId = document.getElementById('guildSelector').value;
      const guild = cachedGuilds.find(g => g.id === selectedId);
      if (!guild) return;

      const channels = guild.channels || [];
      const settings = guild.settings || {};

      // Populate Shop dropdown
      const shopSelect = document.getElementById('routeShopChannel');
      shopSelect.innerHTML = '<option value="">-- Disabled (No shop posts) --</option>' +
        channels.map(c => `<option value="${c.id}" ${settings.shop_channel_id === c.id ? 'selected' : ''}>#${c.name}</option>`).join('');

      // Populate News dropdown
      const newsSelect = document.getElementById('routeNewsChannel');
      newsSelect.innerHTML = '<option value="">-- Disabled (No news posts) --</option>' +
        channels.map(c => `<option value="${c.id}" ${settings.news_channel_id === c.id ? 'selected' : ''}>#${c.name}</option>`).join('');

      // Populate Commands dropdown
      const cmdsSelect = document.getElementById('routeCommandsChannel');
      cmdsSelect.innerHTML = '<option value="">-- Allow in all channels --</option>' +
        channels.map(c => `<option value="${c.id}" ${settings.commands_channel_id === c.id ? 'selected' : ''}>#${c.name}</option>`).join('');

      document.getElementById('routeAutoShop').checked = settings.auto_shop !== false;
      document.getElementById('routeAutoNews').checked = Boolean(settings.auto_news);
    }

    async function saveGuildRouting() {
      const guildId = document.getElementById('guildSelector').value;
      if (!guildId) {
        alert('Please select a server first.');
        return;
      }

      const payload = {
        guild_id: guildId,
        shop_channel_id: document.getElementById('routeShopChannel').value,
        news_channel_id: document.getElementById('routeNewsChannel').value,
        commands_channel_id: document.getElementById('routeCommandsChannel').value,
        auto_shop: document.getElementById('routeAutoShop').checked,
        auto_news: document.getElementById('routeAutoNews').checked
      };

      try {
        const res = await fetch('/api/guild-settings', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-Admin-Pin': getPin() },
          body: JSON.stringify(payload)
        });
        const resp = await res.json();
        if (resp.status === 'success') {
          showToast('Channel routing saved & applied live! 🎯');
          loadGuildRouting();
        } else {
          alert('Error: ' + resp.message);
        }
      } catch (e) {
        alert('Network error: ' + e);
      }
    }

    async function testPostShop() {
      if (!confirm('Post the live Item Shop to the selected channel now?')) return;
      try {
        const res = await fetch('/api/shop/broadcast', {
          method: 'POST',
          headers: { 'X-Admin-Pin': getPin() }
        });
        const resp = await res.json();
        showToast(`Item shop posted to ${resp.posted_to} channel(s)! 🛒`);
      } catch (e) {
        alert('Error: ' + e);
      }
    }

    async function testPostNews() {
      if (!confirm('Post latest in-game news to the selected news channel now?')) return;
      try {
        const res = await fetch('/api/news/broadcast', {
          method: 'POST',
          headers: { 'X-Admin-Pin': getPin() }
        });
        const resp = await res.json();
        showToast(`News posted to ${resp.posted_to} channel(s)! 📰`);
      } catch (e) {
        alert('Error: ' + e);
      }
    }

    async function fetchConfig() {
      try {
        const res = await fetch('/api/config');
        globalConfig = await res.json();
        document.getElementById('statusText').value = globalConfig.status_text || '';
        document.getElementById('activityType').value = globalConfig.activity_type || 'watching';
        document.getElementById('presenceStatus').value = globalConfig.presence_status || 'online';
        document.getElementById('embedColor').value = globalConfig.embed_color || '#00A8FF';
        document.getElementById('embedFooter').value = globalConfig.embed_footer || '';
        renderPois(globalConfig.custom_pois || []);
      } catch (err) {
        console.error('Failed to load config:', err);
      }
    }

    async function saveConfigToServer(partial) {
      const payload = Object.assign({}, globalConfig, partial);
      try {
        const res = await fetch('/api/config', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-Admin-Pin': getPin() },
          body: JSON.stringify(payload)
        });
        const resp = await res.json();
        if (resp.status === 'success') {
          globalConfig = resp.config;
          showToast('Settings saved & applied live! 🚀');
        }
      } catch (err) {
        alert('Failed to connect: ' + err);
      }
    }

    function savePresence() {
      saveConfigToServer({
        status_text: document.getElementById('statusText').value,
        activity_type: document.getElementById('activityType').value,
        presence_status: document.getElementById('presenceStatus').value
      });
    }

    function saveThemeSettings() {
      saveConfigToServer({
        embed_color: document.getElementById('embedColor').value,
        embed_footer: document.getElementById('embedFooter').value
      });
    }

    async function loadPlayers() {
      const tbody = document.getElementById('playersBody');
      tbody.innerHTML = '<tr><td colspan="4" style="text-align: center;">Loading...</td></tr>';
      try {
        const res = await fetch('/api/players');
        const list = await res.json();
        if (list.length === 0) {
          tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--text-muted);">No players linked yet. Run /link in Discord!</td></tr>';
          return;
        }
        tbody.innerHTML = list.map(p => `
          <tr>
            <td><code>${p.discord_user_id}</code></td>
            <td><strong>${p.epic_username}</strong></td>
            <td style="color: var(--text-muted);">${p.linked_at.slice(0, 19)}</td>
            <td><button class="btn btn-secondary" style="padding: 4px 10px; font-size: 0.75rem;" onclick="removePlayer('${p.discord_user_id}')">Unlink</button></td>
          </tr>
        `).join('');
      } catch (e) {
        tbody.innerHTML = '<tr><td colspan="4" style="color: var(--error);">Error loading players</td></tr>';
      }
    }

    async function removePlayer(discordId) {
      if (!confirm(`Unlink player ${discordId}?`)) return;
      await fetch('/api/players/unlink', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Admin-Pin': getPin() },
        body: JSON.stringify({ discord_id: discordId })
      });
      loadPlayers();
    }

    function renderPois(pois) {
      const list = document.getElementById('customPoiList');
      if (!pois || pois.length === 0) {
        list.innerHTML = '<li style="color: var(--text-muted); font-size: 0.85rem;">No custom drop spots added yet.</li>';
        return;
      }
      list.innerHTML = pois.map((poi, idx) => `
        <li style="display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.03); padding: 10px 14px; border-radius: 8px;">
          <span>📍 <strong>${poi}</strong></span>
          <button class="btn btn-secondary" style="padding: 4px 8px; font-size: 0.75rem;" onclick="deletePoi(${idx})">Remove</button>
        </li>
      `).join('');
    }

    function addCustomPoi() {
      const input = document.getElementById('newPoiInput');
      const val = input.value.trim();
      if (!val) return;
      const pois = globalConfig.custom_pois || [];
      pois.push(val);
      saveConfigToServer({ custom_pois: pois });
      input.value = '';
    }

    function deletePoi(index) {
      const pois = globalConfig.custom_pois || [];
      pois.splice(index, 1);
      saveConfigToServer({ custom_pois: pois });
    }

    window.onload = () => {
      const savedPin = localStorage.getItem('ghost_pin') || 'ghost123';
      document.getElementById('adminPin').value = savedPin;
      fetchStatus();
      fetchConfig();
      loadGuildRouting();
      setInterval(fetchStatus, 15000);
    };
  </script>
</body>
</html>
"""
