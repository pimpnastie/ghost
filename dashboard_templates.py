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
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
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

    /* Expandable Squad Cards */
    .card-expand-btn {
      width: 100%;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 8px;
      color: var(--accent);
      padding: 8px 12px;
      font-size: 0.8rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .card-expand-btn:hover {
      background: rgba(0, 168, 255, 0.12);
      border-color: rgba(0, 168, 255, 0.3);
    }
    .card-expandable-section {
      display: none;
      flex-direction: column;
      gap: 12px;
      padding-top: 12px;
      border-top: 1px dashed rgba(255, 255, 255, 0.1);
    }
    .card-expandable-section.open {
      display: flex;
    }
    .expand-sub-title {
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      font-weight: 800;
      color: var(--text-muted);
      margin-bottom: 2px;
    }
    .expanded-modes-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
    }
    @media (max-width: 768px) {
      .expanded-modes-grid { grid-template-columns: 1fr; }
    }
    .expanded-mode-card {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 8px;
      padding: 10px;
    }
    .expanded-mode-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.8rem;
      font-weight: 800;
      margin-bottom: 8px;
      color: #fff;
    }
    .expanded-mode-stats {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 6px;
    }
    .expanded-stat-item {
      display: flex;
      flex-direction: column;
    }
    .expanded-stat-item .lbl {
      color: var(--text-muted);
      font-size: 0.65rem;
      font-weight: 600;
    }
    .expanded-stat-item .val {
      font-weight: 700;
      font-size: 0.85rem;
      color: #f1f5f9;
      font-family: 'JetBrains Mono', monospace;
    }
    .expanded-telemetry-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
    }
    @media (max-width: 768px) {
      .expanded-telemetry-grid { grid-template-columns: repeat(2, 1fr); }
    }
    .device-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 0.75rem;
      font-weight: 700;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: var(--text-muted);
    }
    .device-pill.active {
      background: rgba(0, 168, 255, 0.15);
      border-color: rgba(0, 168, 255, 0.4);
      color: var(--accent);
    }

    /* Admin Gating */
    .admin-only {
      display: none !important;
    }
    body.is-admin .admin-only {
      display: flex !important;
    }
    body.is-admin button.admin-only,
    body.is-admin div.admin-only {
      display: flex !important;
    }
    body.is-admin tr.admin-only {
      display: table-row !important;
    }

    /* Tonight's Squad Session Banner */
    .session-banner {
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.12), rgba(59, 130, 246, 0.12));
      border: 1px solid rgba(245, 158, 11, 0.35);
      border-radius: 14px;
      padding: 16px 20px;
      margin-bottom: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    .session-left {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .session-title-row {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .session-badge {
      background: rgba(245, 158, 11, 0.25);
      border: 1px solid rgba(245, 158, 11, 0.5);
      color: var(--gold);
      padding: 3px 8px;
      border-radius: 12px;
      font-size: 0.7rem;
      font-weight: 800;
      letter-spacing: 0.5px;
    }
    .session-metrics {
      display: flex;
      gap: 18px;
      align-items: center;
      flex-wrap: wrap;
    }
    .session-metric {
      display: flex;
      flex-direction: column;
    }
    .session-metric .lbl {
      font-size: 0.65rem;
      color: var(--text-muted);
      font-weight: 700;
      text-transform: uppercase;
    }
    .session-metric .val {
      font-size: 1.2rem;
      font-weight: 900;
      font-family: 'JetBrains Mono', monospace;
    }
    .session-right {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 8px;
    }

    /* Accolade Badges */
    .accolades-shelf {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 4px;
    }
    .accolade-badge {
      font-size: 0.68rem;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 10px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    }
    .accolade-gold {
      background: rgba(255, 215, 0, 0.18);
      border: 1px solid rgba(255, 215, 0, 0.4);
      color: var(--gold);
    }
    .accolade-blue {
      background: rgba(56, 189, 248, 0.18);
      border: 1px solid rgba(56, 189, 248, 0.4);
      color: #38bdf8;
    }
    .accolade-purple {
      background: rgba(168, 85, 247, 0.18);
      border: 1px solid rgba(168, 85, 247, 0.4);
      color: #c084fc;
    }
    .accolade-green {
      background: rgba(34, 197, 94, 0.18);
      border: 1px solid rgba(34, 197, 94, 0.4);
      color: #4ade80;
    }
    .accolade-pink {
      background: rgba(244, 114, 182, 0.18);
      border: 1px solid rgba(244, 114, 182, 0.4);
      color: #f472b6;
    }

    /* Shop Item Card Wishlist Heart & Cursor */
    .shop-item-card {
      cursor: pointer;
    }
    .shop-item-card.is-wishlisted {
      border-color: rgba(244, 114, 182, 0.7) !important;
      box-shadow: 0 0 16px rgba(244, 114, 182, 0.3) !important;
    }
    .wishlist-tag {
      position: absolute;
      top: 8px;
      right: 8px;
      font-size: 0.9rem;
      filter: drop-shadow(0 2px 4px rgba(0,0,0,0.6));
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
    .item-sale-badge {
      position: absolute;
      top: 30px;
      left: 8px;
      background: linear-gradient(135deg, #10b981, #059669);
      color: #fff;
      font-size: 0.62rem;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 6px;
      z-index: 3;
      box-shadow: 0 2px 6px rgba(0,0,0,0.5);
      letter-spacing: 0.4px;
    }
    .vote-btn {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      color: var(--text);
      padding: 5px 10px;
      border-radius: 8px;
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: all 0.2s;
    }
    .vote-btn:hover {
      background: rgba(255, 255, 255, 0.12);
      transform: translateY(-1px);
    }
    .vote-btn.active {
      background: rgba(0, 168, 255, 0.25);
      border-color: var(--accent);
      box-shadow: 0 0 10px rgba(0, 168, 255, 0.3);
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

    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(8px);
      z-index: 1000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .modal-backdrop.open {
      display: flex;
    }
    .modal-box {
      background: #0f172a;
      border: 1px solid rgba(88, 101, 242, 0.4);
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 0 0 30px rgba(88, 101, 242, 0.2);
      border-radius: 16px;
      width: 100%;
      max-width: 480px;
      padding: 24px;
      position: relative;
    }
    .code-display {
      display: flex;
      justify-content: center;
      gap: 12px;
      margin: 18px 0;
    }
    .code-letter {
      width: 60px;
      height: 70px;
      background: rgba(88, 101, 242, 0.15);
      border: 2px solid #5865F2;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 2rem;
      font-weight: 900;
      font-family: 'JetBrains Mono', monospace;
      color: #fff;
      box-shadow: 0 0 15px rgba(88, 101, 242, 0.4);
      letter-spacing: 2px;
    }
    .cache-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.3);
      color: #38bdf8;
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 600;
    }
    .item-new-badge {
      position: absolute;
      top: 8px;
      left: 8px;
      background: linear-gradient(135deg, #f59e0b, #ec4899);
      color: #fff;
      font-size: 0.65rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 6px;
      z-index: 3;
      box-shadow: 0 2px 8px rgba(0,0,0,0.5);
      letter-spacing: 0.5px;
    }

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
      <button class="nav-btn admin-only" id="navChannels" onclick="switchTab('channels')">🎯 Channel Routing</button>
      <button class="nav-btn admin-only" id="navStatus" onclick="switchTab('status')">🎮 Presence & Status</button>
    </nav>

    <div style="margin-top: auto; padding-top: 14px;">
      <button id="adminLoginBtn" class="btn btn-secondary" style="width: 100%; font-size: 0.78rem; padding: 10px 8px; justify-content: center; gap: 6px; background: rgba(255,255,255,0.03); border: 1px solid var(--card-border);" onclick="handleAdminButtonClick()">
        <span id="adminBtnIcon">🔒</span> <span id="adminBtnText">Admin Unlock</span>
      </button>
    </div>
  </aside>

  <!-- Main View -->
  <main>
    <header>
      <div class="header-title">
        <h2 id="pageTitle">Squad Telemetry & Detailed Stats</h2>
        <p>Live Fortnite game data tailored for your squad</p>
      </div>
      <div style="display: flex; gap: 10px; align-items: center;">
        <div id="discordLinkStatusBox">
          <button class="btn btn-secondary" style="background: rgba(88, 101, 242, 0.2); border: 1px solid rgba(88, 101, 242, 0.4); color: #a5b4fc; font-size: 0.8rem; padding: 6px 12px; display: flex; align-items: center; gap: 6px;" onclick="openDiscordLinkModal()">
            <span>🔗</span> Link Discord
          </button>
        </div>
        <div class="auth-badge">
          <div class="status-dot"></div>
          <span id="gatewayStatus">Connected (Render 24/7)</span>
        </div>
      </div>
    </header>

    <!-- TAB 1: SQUAD DETAILED STATS -->
    <section id="tab-squad" class="tab-content active">
      <div class="card">
        <div class="card-title">
          <span>👥 Squad Telemetry & Live Tracker</span>
          <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
            <div class="cache-pill" title="Stats auto-sync at fixed squad gaming hours">
              <span>🕒 Auto-syncs at 7:00 PM & 10:00 PM EDT</span>
              <span id="squadCacheStatus" style="color: var(--text); font-weight: 700; margin-left: 4px;">• Cached</span>
            </div>
            <button class="btn btn-secondary" id="toggleAllCardsBtn" onclick="toggleAllCards()">📂 Expand All</button>
            <button class="btn btn-secondary" onclick="loadSquadStats(true)">🔄 Force Live Sync</button>
          </div>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 20px;">
          Track your squad members directly from this dashboard. Stats update live from Epic Games.
        </p>

        <!-- Tonight's Session Banner -->
        <div id="squadSessionBanner" class="session-banner" style="display: none;">
          <div class="session-left">
            <div class="session-title-row">
              <span class="session-badge">🔥 TONIGHT'S SESSION</span>
              <span id="sessionStartedAt" style="font-size: 0.75rem; color: var(--text-muted);">Active this evening</span>
            </div>
            <div class="session-metrics">
              <div class="session-metric">
                <span class="lbl">Squad Wins</span>
                <span id="sessionWins" class="val" style="color: var(--gold);">+0</span>
              </div>
              <div class="session-metric">
                <span class="lbl">Squad Kills</span>
                <span id="sessionKills" class="val" style="color: #38bdf8;">+0</span>
              </div>
              <div class="session-metric">
                <span class="lbl">Matches</span>
                <span id="sessionMatches" class="val">+0</span>
              </div>
              <div class="session-metric" id="sessionMvpBox" style="display: none;">
                <span class="lbl">Tonight's MVP</span>
                <span id="sessionMvp" class="val" style="color: #f472b6;">👑 None</span>
              </div>
            </div>
          </div>
          <div class="session-right">
            <div id="sessionLastWinText" style="font-size: 0.8rem; color: #fde68a;">
              🏆 Last Win: <strong>None yet tonight</strong>
            </div>
            <button class="btn btn-secondary admin-only" id="resetSessionBtn" style="font-size: 0.72rem; padding: 6px 12px;" onclick="resetSessionBaseline()">
              🔄 Reset Baseline
            </button>
          </div>
        </div>

        <!-- Squad Filter Bar (Public) -->
        <div style="background: rgba(0, 0, 0, 0.25); border: 1px solid var(--card-border); border-radius: 12px; padding: 14px 16px; margin-bottom: 16px;">
          <input type="text" id="filterSquadInput" placeholder="🔍 Fuzzy search players (e.g. condoe, ghost, nastie, coyote)..." oninput="filterSquadCards()">
        </div>

        <!-- Admin-Only Track Player Bar -->
        <div class="admin-only" id="trackPlayerBox" style="background: rgba(0, 0, 0, 0.35); border: 1px dashed rgba(255, 215, 0, 0.4); border-radius: 12px; padding: 14px 16px; margin-bottom: 20px; flex-wrap: wrap; gap: 12px; align-items: center;">
          <div style="width: 100%; font-size: 0.75rem; color: var(--gold); font-weight: 700; display: flex; align-items: center; gap: 6px;">
            <span>🔒 Admin Action:</span> Add New Squad Member
          </div>
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
            <button class="btn btn-primary admin-only" onclick="testShopBroadcast()">📢 Post to Discord</button>
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

          <!-- Category Pills & New Items Filter -->
          <div class="filter-pills" id="shopCategoryPills" style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px;">
            <button class="filter-pill" id="pillNewOnly" style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4); color: #fbbf24;" onclick="toggleNewItemsFilter(this)">✨ New Items Only (<span id="newItemsBadge">0</span>)</button>
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
            <button class="btn btn-secondary admin-only" id="broadcastDropBtn" onclick="broadcastCurrentDrop()" disabled>📢 Broadcast Drop to Discord</button>
          </div>
        </div>
      </div>

      <!-- Island Map Card with Fortnite.gg Interactive Embed & Satellite Switching -->
      <div class="card" id="mapCardContainer">
        <div class="card-title" style="flex-wrap: wrap; gap: 10px;">
          <div style="display: flex; align-items: center; gap: 8px;">
            <span>🗺️ Island Interactive & Satellite Map</span>
            <span class="accolade-badge accolade-gold" style="font-size: 0.68rem;">Live Spawns & Chests</span>
          </div>
          <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <button class="btn btn-secondary" id="mapViewInteractiveBtn" style="background: rgba(0, 168, 255, 0.2); border: 1px solid var(--accent); color: var(--accent);" onclick="switchMapView('interactive')">🗺️ Interactive (Fortnite.gg)</button>
            <button class="btn btn-secondary" id="mapViewPoiBtn" onclick="switchMapView('poi')">🏷️ Labeled POIs</button>
            <button class="btn btn-secondary" id="mapViewCleanBtn" onclick="switchMapView('clean')">🏝️ Satellite View</button>
            <button class="btn btn-secondary" id="mapFullscreenBtn" onclick="toggleMapFullscreen()" title="Toggle Fullscreen Map">⛶ Fullscreen</button>
            <a href="https://fortnite.gg/" target="_blank" class="btn btn-secondary" style="text-decoration: none;" title="Open Fortnite.gg in new tab">↗ Fortnite.gg</a>
          </div>
        </div>

        <!-- Interactive Fortnite.gg Embed -->
        <div id="interactiveMapWrapper" style="width: 100%; display: flex; flex-direction: column; gap: 8px;">
          <div style="position: relative; width: 100%; height: 750px; border-radius: 12px; overflow: hidden; border: 1px solid var(--card-border); box-shadow: 0 8px 30px rgba(0,0,0,0.5);">
            <iframe id="fortniteGgIframe" src="https://fortnite.gg/" style="width: 100%; height: 100%; border: none;" allowfullscreen loading="lazy"></iframe>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; color: var(--text-muted); padding: 4px 8px; flex-wrap: wrap; gap: 6px;">
            <span>⚡ Powered by <strong>Fortnite.gg</strong> — filter live chest spawns, reboot vans, NPCs, boss vaults, and vehicles.</span>
            <button onclick="reloadMapIframe()" style="background: transparent; border: none; color: #38bdf8; cursor: pointer; font-size: 0.75rem;">🔄 Reload Map</button>
          </div>
        </div>

        <!-- Static Image Fallback / Satellite View -->
        <div id="staticMapWrapper" style="display: none; flex-direction: column; align-items: center; gap: 16px; width: 100%;">
          <img id="islandMapImg" src="https://fortnite-api.com/images/map_en.png" style="width: 100%; max-width: 860px; border-radius: 12px; border: 1px solid var(--card-border); box-shadow: 0 8px 30px rgba(0,0,0,0.5);" alt="Fortnite Map">
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
        <div id="addCustomPoiBox" class="admin-only" style="background: rgba(0, 0, 0, 0.25); border: 1px dashed rgba(255, 215, 0, 0.4); border-radius: 12px; padding: 16px; margin-bottom: 20px; flex-wrap: wrap; gap: 12px; align-items: center;">
          <div style="width: 100%; font-size: 0.75rem; color: var(--gold); font-weight: 700; display: flex; align-items: center; gap: 6px;">
            <span>🔒 Admin Action:</span> Add Squad Callout
          </div>
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

  <!-- DISCORD LINK MODA CODE MODAL -->
  <div id="discordLinkModal" class="modal-backdrop">
    <div class="modal-box">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <h3 style="font-size: 1.15rem; font-weight: 800; display: flex; align-items: center; gap: 8px;">
          <span style="color: #5865F2;">🔗</span> Link Discord Profile
        </h3>
        <button onclick="closeDiscordLinkModal()" style="background: transparent; border: none; color: var(--text-muted); font-size: 1.2rem; cursor: pointer;">✕</button>
      </div>

      <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 18px; line-height: 1.5;">
        Generate a 3-character verification code made of letters <strong>M - O - D - A</strong>. Enter it in Discord to instantly link your Discord account to your squad stats on this website!
      </p>

      <div id="modalGenerateStep">
        <div class="form-group" style="margin-bottom: 12px;">
          <label>Fortnite / Epic Username</label>
          <input type="text" id="modalEpicInput" placeholder="e.g. p_lmpNastie, Going__Ghost, KING_CONDOR_">
        </div>
        <div class="form-group" style="margin-bottom: 16px;">
          <label>Platform</label>
          <select id="modalPlatformSelect">
            <option value="epic">⚡ Epic Games</option>
            <option value="psn">🎮 PlayStation (PSN)</option>
            <option value="xbl">💚 Xbox (XBL)</option>
          </select>
        </div>
        <button class="btn btn-primary" style="width: 100%; justify-content: center; padding: 12px;" onclick="requestLinkCode()">
          ⚡ Generate 3-Digit MODA Code
        </button>
      </div>

      <div id="modalCodeDisplayStep" style="display: none; text-align: center;">
        <div style="font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;">Your 3-Letter Verification Code:</div>
        
        <div class="code-display" id="modalCodeBoxes">
          <div class="code-letter" id="letter1">-</div>
          <div class="code-letter" id="letter2">-</div>
          <div class="code-letter" id="letter3">-</div>
        </div>

        <div style="background: rgba(88, 101, 242, 0.1); border: 1px solid rgba(88, 101, 242, 0.3); border-radius: 12px; padding: 14px; text-align: left; font-size: 0.85rem; line-height: 1.6; margin-bottom: 16px;">
          <div style="font-weight: 800; color: #a5b4fc; margin-bottom: 6px;">How to redeem in Discord:</div>
          <div>1. Open your Discord server with Ghost.</div>
          <div>2. Run slash command: <strong style="color: #fff; background: rgba(0,0,0,0.4); padding: 2px 6px; border-radius: 4px;">/verify code: <span id="instructionCode">MOD</span></strong></div>
          <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 4px;">Or simply type in any channel: <code style="color: #fff;">!verify <span id="instructionCode2">MOD</span></code> or <code style="color: #fff;">/link <span id="instructionCode3">MOD</span></code></div>
        </div>

        <div style="display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 0.8rem; color: #38bdf8; margin-bottom: 12px;">
          <div class="status-dot" style="background: #38bdf8;"></div>
          <span>Waiting for Discord verification... (auto-detecting)</span>
        </div>

        <button class="btn btn-secondary" style="font-size: 0.8rem; padding: 6px 14px;" onclick="cancelLinkPolling()">Cancel</button>
      </div>

      <div id="modalSuccessStep" style="display: none; text-align: center; padding: 10px 0;">
        <div style="font-size: 2.5rem; margin-bottom: 10px;">🎉</div>
        <h4 style="font-size: 1.1rem; color: var(--success); margin-bottom: 8px; font-weight: 800;">Account Linked Successfully!</h4>
        <p id="modalSuccessMsg" style="font-size: 0.85rem; color: var(--text); margin-bottom: 16px;"></p>
        <button class="btn btn-primary" style="width: 100%; justify-content: center;" onclick="closeDiscordLinkModal()">
          ✓ Done
        </button>
      </div>
    </div>
  </div>

  <!-- ADMIN AUTHENTICATION MODAL -->
  <div id="adminModal" class="modal-backdrop">
    <div class="modal-box" style="max-width: 420px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <h3 style="font-size: 1.15rem; font-weight: 800; display: flex; align-items: center; gap: 8px;">
          <span>🔒</span> Admin Authentication
        </h3>
        <button onclick="closeAdminModal()" style="background: transparent; border: none; color: var(--text-muted); font-size: 1.2rem; cursor: pointer;">✕</button>
      </div>

      <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px; line-height: 1.5;">
        Unlock admin management tools for squad tracking, channel routing, custom POIs, and Discord broadcasts.
      </p>

      <div class="form-group" style="margin-bottom: 16px;">
        <label for="adminModalPassword">Admin Password</label>
        <input type="password" id="adminModalPassword" placeholder="Enter password (e.g. ghost123)..." onkeydown="if(event.key==='Enter') submitAdminPassword()">
        <div id="adminModalError" style="display: none; color: var(--error); font-size: 0.8rem; margin-top: 6px; font-weight: 600;"></div>
      </div>

      <div style="display: flex; gap: 10px;">
        <button class="btn btn-secondary" style="flex: 1; justify-content: center;" onclick="closeAdminModal()">Cancel</button>
        <button class="btn btn-primary" id="adminModalSubmitBtn" style="flex: 1; justify-content: center;" onclick="submitAdminPassword()">Unlock 🔓</button>
      </div>
    </div>
  </div>

  <!-- COSMETIC INSPECT, MUSIC SHOWCASE & 3D .OBJ TRANSFORMER MODAL -->
  <div id="cosmeticInspectModal" class="modal-backdrop">
    <div class="modal-box" style="max-width: 640px; max-height: 92vh; overflow-y: auto;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px;">
        <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
          <span id="inspectModalRarityBadge" class="accolade-badge accolade-gold">✨ Rarity</span>
          <span id="inspectModalTypeBadge" class="accolade-badge accolade-blue">Outfit</span>
          <span id="inspectModalNewBadge" class="item-new-badge" style="position: static; display: none;">✨ NEW</span>
          <span id="inspectModalSavingsBadge" class="accolade-badge accolade-green" style="display: none;"></span>
        </div>
        <button onclick="closeCosmeticModal()" style="background: transparent; border: none; color: var(--text-muted); font-size: 1.3rem; cursor: pointer; line-height: 1;">✕</button>
      </div>

      <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 16px;">
        <div style="flex: 1; min-width: 170px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: rgba(0,0,0,0.3); border: 1px solid var(--card-border); border-radius: 12px; padding: 16px; position: relative;">
          <img id="inspectModalImg" src="" style="width: 150px; height: 150px; object-fit: contain; filter: drop-shadow(0 8px 16px rgba(0,0,0,0.6));" alt="Cosmetic">
          <div style="display: flex; align-items: center; gap: 6px; margin-top: 10px;">
            <div id="inspectModalPrice" class="shop-price">🪙 0</div>
            <span id="inspectModalRegularPrice" style="text-decoration: line-through; color: var(--text-muted); font-size: 0.85rem; font-family: 'JetBrains Mono', monospace; display: none;"></span>
          </div>
        </div>

        <div style="flex: 1.4; min-width: 220px; display: flex; flex-direction: column; gap: 10px;">
          <div>
            <h3 id="inspectModalName" style="font-size: 1.35rem; font-weight: 800; margin-bottom: 4px;">Item Name</h3>
            <p id="inspectModalDesc" style="font-size: 0.85rem; color: var(--text-muted); font-style: italic; line-height: 1.4;">"Item description..."</p>
          </div>

          <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.8rem;">
            <div id="inspectModalSetRow" style="display: none; color: #a5b4fc;">
              <strong>Set:</strong> <span id="inspectModalSet"></span>
              <button id="btnFilterSet" class="btn btn-secondary" style="padding: 2px 8px; font-size: 0.7rem; margin-left: 6px;" onclick="filterCurrentSetInShop()">🔍 Filter Set in Shop</button>
            </div>
            <div id="inspectModalIntroRow" style="display: none; color: var(--text-muted);">
              <strong>Introduced:</strong> <span id="inspectModalIntro"></span>
            </div>
            <div id="inspectModalGiftableRow" style="color: var(--text-muted);">
              <strong>Giftable:</strong> <span id="inspectModalGiftable">Yes</span>
            </div>
          </div>

          <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: auto; padding-top: 8px;">
            <button id="inspectWishlistBtn" class="btn btn-secondary" style="font-size: 0.8rem; padding: 8px 12px;" onclick="toggleModalWishlist()">
              🤍 Wishlist
            </button>
            <a id="inspectDownloadBtn" href="#" target="_blank" download class="btn btn-secondary" style="font-size: 0.8rem; padding: 8px 12px; text-decoration: none;">
              📥 Art (.PNG)
            </a>
          </div>
        </div>
      </div>

      <!-- Squad Hype Reaction Shelf (Fortnite.gg Inspired) -->
      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; background: rgba(0,0,0,0.25); border: 1px solid var(--card-border); border-radius: 10px; padding: 10px 14px; margin-bottom: 14px;">
        <span style="font-size: 0.78rem; font-weight: 700; color: var(--text-muted);">Squad Hype Rating:</span>
        <div style="display: flex; gap: 6px; flex-wrap: wrap;" id="voteButtonsGroup">
          <button class="vote-btn" id="vote_fire" onclick="submitCosmeticVote('fire')">🔥 Fire <span id="voteCount_fire" style="font-size: 0.72rem; color: var(--text-muted);">(0)</span></button>
          <button class="vote-btn" id="vote_love" onclick="submitCosmeticVote('love')">😍 Cop <span id="voteCount_love" style="font-size: 0.72rem; color: var(--text-muted);">(0)</span></button>
          <button class="vote-btn" id="vote_mid" onclick="submitCosmeticVote('mid')">😐 Mid <span id="voteCount_mid" style="font-size: 0.72rem; color: var(--text-muted);">(0)</span></button>
          <button class="vote-btn" id="vote_trash" onclick="submitCosmeticVote('trash')">💩 Drop <span id="voteCount_trash" style="font-size: 0.72rem; color: var(--text-muted);">(0)</span></button>
        </div>
      </div>

      <!-- 3D Viewport & .OBJ Transformer (For 3D Cosmetics ONLY) -->
      <div id="inspect3dSection" style="border-top: 1px solid var(--card-border); padding-top: 16px; margin-top: 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
          <h4 style="font-size: 0.95rem; font-weight: 800; color: var(--accent); display: flex; align-items: center; gap: 6px;">
            <span>🌐</span> 3D Viewport & .OBJ Transformer
          </h4>
          <div style="display: flex; gap: 6px; align-items: center;">
            <button class="btn btn-secondary" style="padding: 4px 10px; font-size: 0.75rem;" onclick="toggle3dWireframe()">📐 Wireframe</button>
            <button class="btn btn-secondary" id="btn3dRotateToggle" style="padding: 4px 10px; font-size: 0.75rem;" onclick="toggle3dRotation()">⏸️ Pause</button>
            <button class="btn btn-secondary" style="padding: 4px 10px; font-size: 0.75rem;" onclick="reset3dCamera()">🎯 Reset</button>
          </div>
        </div>

        <div id="threeJsCanvasContainer" style="width: 100%; height: 260px; background: radial-gradient(circle at center, #1e293b 0%, #090d16 80%); border: 1px solid var(--card-border); border-radius: 12px; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center;">
          <canvas id="cosmeticThreeCanvas" style="width: 100%; height: 100%; cursor: grab;"></canvas>
          <div style="position: absolute; bottom: 8px; left: 10px; font-size: 0.7rem; color: var(--text-muted); background: rgba(0,0,0,0.6); padding: 2px 8px; border-radius: 6px; pointer-events: none;">
            🖱️ Drag to rotate 360° • Scroll to zoom
          </div>
        </div>

        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px; align-items: center;">
          <button class="btn btn-primary" style="font-size: 0.82rem; padding: 9px 16px; background: linear-gradient(135deg, #9333ea, #00a8ff); gap: 6px;" onclick="exportCosmeticObj()">
            <span>📦</span> Export .OBJ Mesh
          </button>
          <button class="btn btn-secondary" style="font-size: 0.82rem; padding: 9px 14px; gap: 6px;" onclick="downloadCosmeticMtl()">
            <span>🎨</span> Download .MTL Material
          </button>
          <a id="inspect3dBtn" href="#" target="_blank" class="btn btn-secondary" style="font-size: 0.82rem; padding: 9px 14px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px;">
            <span>↗</span> Fortnite.gg 3D Viewer
          </a>
        </div>

        <p style="font-size: 0.72rem; color: var(--text-muted); margin-top: 8px; line-height: 1.4;">
          💡 <strong>.OBJ Transformer:</strong> Exports standard Wavefront 3D geometry (.obj) and material (.mtl) files textured for Blender, Unreal Engine, Maya, or 3D printing. For raw proprietary game skeleton rigs, use <a href="https://github.com/FortnitePorting/FortnitePorting" target="_blank" style="color: #38bdf8;">FortnitePorting</a>.
        </p>
      </div>

      <!-- Music Showcase Section (Shown ONLY for Jam Tracks / Music Packs) -->
      <div id="inspectMusicSection" style="display: none; border-top: 1px solid var(--card-border); padding-top: 16px; margin-top: 14px;">
        <div style="background: linear-gradient(135deg, rgba(147, 51, 234, 0.15), rgba(6, 182, 212, 0.15)); border: 1px solid rgba(147, 51, 234, 0.35); border-radius: 12px; padding: 16px; display: flex; flex-direction: column; gap: 10px;">
          <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="font-size: 1.4rem;">🎵</span>
              <div>
                <h4 style="font-size: 0.95rem; font-weight: 800; color: #c084fc;">Jam Track Audio Showcase</h4>
                <p style="font-size: 0.75rem; color: var(--text-muted);">Audio asset • 3D mesh not applicable</p>
              </div>
            </div>
            <span class="accolade-badge accolade-purple">Fortnite Festival</span>
          </div>

          <div style="font-size: 0.85rem; line-height: 1.5;">
            <div><strong>Track:</strong> <span id="musicTrackTitle"></span></div>
            <div><strong>Artist:</strong> <span id="musicTrackArtist" style="color: #38bdf8;"></span></div>
          </div>

          <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 4px;">
            <a id="musicSearchYoutube" href="#" target="_blank" class="btn btn-secondary" style="font-size: 0.8rem; padding: 8px 14px; text-decoration: none; color: #f87171; border-color: rgba(239, 68, 68, 0.4);">
              ▶ Search on YouTube
            </a>
            <a id="musicSearchSpotify" href="#" target="_blank" class="btn btn-secondary" style="font-size: 0.8rem; padding: 8px 14px; text-decoration: none; color: #4ade80; border-color: rgba(34, 197, 94, 0.4);">
              🎧 Search on Spotify
            </a>
          </div>
        </div>
      </div>

      <!-- Variants Shelf -->
      <div id="inspectVariantsBox" style="display: none; border-top: 1px solid var(--card-border); padding-top: 14px; margin-top: 10px;">
        <h4 style="font-size: 0.85rem; font-weight: 700; color: #fde68a; margin-bottom: 8px;">🎨 Available Styles & Variants</h4>
        <div id="inspectVariantsList" style="display: flex; flex-wrap: wrap; gap: 8px;"></div>
      </div>

      <!-- Bundle Items Shelf -->
      <div id="inspectBundleBox" style="display: none; border-top: 1px solid var(--card-border); padding-top: 14px; margin-top: 10px;">
        <h4 style="font-size: 0.85rem; font-weight: 700; color: #a5b4fc; margin-bottom: 8px;">📦 Bundle Included Items</h4>
        <div id="inspectBundleList" style="display: flex; flex-wrap: wrap; gap: 8px;"></div>
      </div>
    </div>
  </div>

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

    let isAdmin = false;

    function checkAdminState() {
      const token = sessionStorage.getItem('ghost_admin_token');
      const auth = sessionStorage.getItem('ghost_is_admin');
      if (token && auth === 'true') {
        setAdminState(true);
      } else {
        setAdminState(false);
      }
    }

    function setAdminState(adminActive) {
      isAdmin = !!adminActive;
      if (isAdmin) {
        document.body.classList.add('is-admin');
        const icon = document.getElementById('adminBtnIcon');
        const text = document.getElementById('adminBtnText');
        if (icon) icon.innerText = '🔓';
        if (text) text.innerText = 'Admin Mode (Lock)';
      } else {
        document.body.classList.remove('is-admin');
        const icon = document.getElementById('adminBtnIcon');
        const text = document.getElementById('adminBtnText');
        if (icon) icon.innerText = '🔒';
        if (text) text.innerText = 'Admin Unlock';
        const currentTab = document.querySelector('.nav-btn.active');
        if (currentTab && (currentTab.id === 'navChannels' || currentTab.id === 'navStatus')) {
          switchTab('squad');
        }
      }
      if (typeof renderCustomPois === 'function' && customPois) {
        renderCustomPois();
      }
    }

    function handleAdminButtonClick() {
      if (isAdmin) {
        sessionStorage.removeItem('ghost_admin_token');
        sessionStorage.removeItem('ghost_is_admin');
        setAdminState(false);
        showToast('Admin mode locked 🔒');
        if (lastSquadData && lastSquadData.length > 0) {
          renderSquadCards(lastSquadData);
        }
      } else {
        openAdminModal();
      }
    }

    function openAdminModal() {
      const modal = document.getElementById('adminModal');
      if (modal) {
        modal.classList.add('open');
        const err = document.getElementById('adminModalError');
        if (err) err.style.display = 'none';
        const pwdInput = document.getElementById('adminModalPassword');
        if (pwdInput) {
          pwdInput.value = '';
          setTimeout(() => pwdInput.focus(), 50);
        }
      }
    }

    function closeAdminModal() {
      const modal = document.getElementById('adminModal');
      if (modal) modal.classList.remove('open');
    }

    async function submitAdminPassword() {
      const pwdInput = document.getElementById('adminModalPassword');
      const pwd = (pwdInput ? pwdInput.value : '').trim();
      const errDiv = document.getElementById('adminModalError');
      const submitBtn = document.getElementById('adminModalSubmitBtn');

      if (!pwd) {
        if (errDiv) {
          errDiv.innerText = 'Please enter an admin password.';
          errDiv.style.display = 'block';
        }
        return;
      }

      if (submitBtn) {
        submitBtn.innerText = 'Verifying...';
        submitBtn.disabled = true;
      }

      try {
        const res = await fetch('/api/admin/verify', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ password: pwd })
        });
        const data = await res.json();
        if (res.ok && data.status === 'success') {
          sessionStorage.setItem('ghost_admin_token', pwd);
          sessionStorage.setItem('ghost_is_admin', 'true');
          setAdminState(true);
          closeAdminModal();
          showToast('Admin unlocked! 🔓');
          if (lastSquadData && lastSquadData.length > 0) {
            renderSquadCards(lastSquadData);
          }
        } else {
          if (errDiv) {
            errDiv.innerText = data.message || 'Incorrect password.';
            errDiv.style.display = 'block';
          }
        }
      } catch (e) {
        if (errDiv) {
          errDiv.innerText = 'Error verifying password: ' + e;
          errDiv.style.display = 'block';
        }
      } finally {
        if (submitBtn) {
          submitBtn.innerText = 'Unlock 🔓';
          submitBtn.disabled = false;
        }
      }
    }

    function getPin() {
      return sessionStorage.getItem('ghost_admin_token') || '';
    }

    async function resetSessionBaseline() {
      if (!confirm("Reset tonight's squad session stats? This sets the baseline to current totals.")) return;
      try {
        const res = await fetch('/api/squad-session/reset', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-Admin-Pin': getPin() }
        });
        const data = await res.json();
        if (res.ok) {
          showToast('Session baseline reset! 🔥');
          await loadSquadStats();
        } else {
          showToast('Error: ' + (data.message || 'Could not reset session'));
        }
      } catch (e) {
        showToast('Error: ' + e);
      }
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

    function levenshtein(a, b) {
      if (a.length === 0) return b.length;
      if (b.length === 0) return a.length;
      const matrix = [];
      for (let i = 0; i <= b.length; i++) matrix[i] = [i];
      for (let j = 0; j <= a.length; j++) matrix[0][j] = j;
      for (let i = 1; i <= b.length; i++) {
        for (let j = 1; j <= a.length; j++) {
          if (b.charAt(i - 1) === a.charAt(j - 1)) {
            matrix[i][j] = matrix[i - 1][j - 1];
          } else {
            matrix[i][j] = Math.min(
              matrix[i - 1][j - 1] + 1,
              matrix[i][j - 1] + 1,
              matrix[i - 1][j] + 1
            );
          }
        }
      }
      return matrix[b.length][a.length];
    }

    function fuzzyMatch(query, target) {
      const q = query.toLowerCase().trim();
      const t = target.toLowerCase().trim();
      if (!q) return true;
      if (t.includes(q)) return true;

      // Subsequence match (e.g. acronyms or typed letters in order)
      let qIdx = 0;
      for (let i = 0; i < t.length && qIdx < q.length; i++) {
        if (t[i] === q[qIdx]) qIdx++;
      }
      if (qIdx === q.length && q.length >= 3) return true;

      // Token-based fuzzy match with Levenshtein distance
      const qTokens = q.replace(/[^a-z0-9]/g, ' ').split(/\s+/).filter(Boolean);
      const tTokens = t.replace(/[^a-z0-9]/g, ' ').split(/\s+/).filter(Boolean);

      return qTokens.every(qTok => {
        return tTokens.some(tTok => {
          if (tTok.includes(qTok) || qTok.includes(tTok)) return true;
          const maxLen = Math.max(qTok.length, tTok.length);
          if (maxLen < 4) return false;
          const dist = levenshtein(qTok, tTok);
          const maxAllowed = maxLen <= 5 ? 1 : 2;
          return dist <= maxAllowed;
        });
      });
    }

    function filterSquadCards() {
      const q = (document.getElementById('filterSquadInput').value || '').trim();
      let matchCount = 0;
      const cards = document.querySelectorAll('.player-card');
      cards.forEach(card => {
        const nameElem = card.querySelector('.player-name') || card;
        const text = nameElem.innerText + ' ' + card.innerText;
        const isMatch = !q || fuzzyMatch(q, text);
        card.style.display = isMatch ? 'flex' : 'none';
        if (isMatch) matchCount++;
      });

      let noMatchElem = document.getElementById('noMatchNotice');
      if (!noMatchElem) {
        noMatchElem = document.createElement('div');
        noMatchElem.id = 'noMatchNotice';
        noMatchElem.style.gridColumn = '1/-1';
        noMatchElem.style.padding = '30px';
        noMatchElem.style.textAlign = 'center';
        noMatchElem.style.color = 'var(--text-muted)';
        const container = document.getElementById('squadContainer');
        if (container) container.appendChild(noMatchElem);
      }
      if (q && matchCount === 0) {
        noMatchElem.style.display = 'block';
        noMatchElem.innerHTML = `<p style="font-size: 1rem; color: #fde68a;">No squad members matched <strong>"${q}"</strong>.</p><p style="font-size: 0.8rem; margin-top: 6px;">Try searching with a partial username or nickname (e.g. <em>condor</em>, <em>ghost</em>, <em>nastie</em>, <em>coyote</em>).</p>`;
      } else if (noMatchElem) {
        noMatchElem.style.display = 'none';
      }
    }

    let lastSquadData = [];

    function computeSquadAccolades(squad) {
      const map = {};
      squad.forEach(p => { map[p.epic_name] = []; });
      const valid = squad.filter(p => !p.error && !p.is_private && p.overall);
      if (valid.length === 0) return map;

      // 👑 Victory King: highest career wins
      const sortedWins = [...valid].sort((a,b) => (b.overall.wins || 0) - (a.overall.wins || 0));
      if (sortedWins[0] && (sortedWins[0].overall.wins || 0) > 0) {
        map[sortedWins[0].epic_name].push({ icon: '👑', title: 'Victory King', class: 'accolade-gold', desc: 'Most Career Wins in Squad' });
      }

      // 🎯 Deadeye: highest overall K/D (min 5 matches, K/D > 1.0)
      const kdCandidates = valid.filter(p => (p.overall.matches || 0) >= 5);
      kdCandidates.sort((a,b) => (b.overall.kd || 0) - (a.overall.kd || 0));
      if (kdCandidates[0] && (kdCandidates[0].overall.kd || 0) > 1.0) {
        map[kdCandidates[0].epic_name].push({ icon: '🎯', title: 'Deadeye', class: 'accolade-blue', desc: 'Highest Career K/D Ratio' });
      }

      // 🛡️ Squad Anchor: highest squad mode win rate (min 5 squad matches, win rate > 0)
      const squadCandidates = valid.filter(p => (p.squad?.matches || 0) >= 5);
      squadCandidates.sort((a,b) => (b.squad?.winRate || 0) - (a.squad?.winRate || 0));
      if (squadCandidates[0] && (squadCandidates[0].squad?.winRate || 0) > 0) {
        map[squadCandidates[0].epic_name].push({ icon: '🛡️', title: 'Squad Anchor', class: 'accolade-purple', desc: 'Highest Squad Win Rate' });
      }

      // 👤 Lone Wolf: most solo wins (min 1)
      const soloCandidates = valid.filter(p => (p.solo?.wins || 0) > 0);
      soloCandidates.sort((a,b) => (b.solo?.wins || 0) - (a.solo?.wins || 0));
      if (soloCandidates[0]) {
        map[soloCandidates[0].epic_name].push({ icon: '👤', title: 'Lone Wolf', class: 'accolade-green', desc: 'Most Solo Wins' });
      }

      // ⚡ Grinder: most matches played (min 10)
      const matchCandidates = [...valid].sort((a,b) => (b.overall.matches || 0) - (a.overall.matches || 0));
      if (matchCandidates[0] && (matchCandidates[0].overall.matches || 0) >= 10) {
        map[matchCandidates[0].epic_name].push({ icon: '⚡', title: 'Grinder', class: 'accolade-gold', desc: 'Most Matches Played' });
      }

      // 🎮 Controller Demon & ⌨️ KBM Wizard
      valid.forEach(p => {
        const isController = Boolean((p.gamepad && p.gamepad.matches > 0) || p.has_controller || p.account_type === 'psn' || p.account_type === 'xbl');
        const isKbm = Boolean((p.kbm && p.kbm.matches > 0) || p.has_kbm);
        if (isController && ((p.overall.kd || 0) >= 2.0 || (p.overall.wins || 0) >= 20)) {
          map[p.epic_name].push({ icon: '🎮', title: 'Controller Demon', class: 'accolade-pink', desc: 'High Tier Gamepad Specialist' });
        }
        if (isKbm && ((p.overall.kd || 0) >= 2.0 || (p.overall.wins || 0) >= 20)) {
          map[p.epic_name].push({ icon: '⌨️', title: 'KBM Wizard', class: 'accolade-blue', desc: 'Precision Keyboard & Mouse Specialist' });
        }
      });

      return map;
    }

    function renderSquadCards(squad) {
      const container = document.getElementById('squadContainer');
      if (!Array.isArray(squad) || squad.length === 0) {
        container.innerHTML = '<div style="grid-column: 1/-1; padding: 30px; background: rgba(255,255,255,0.02); border-radius: 12px; text-align: center;"><p style="font-size: 1.1rem; margin-bottom: 8px;">No squad members tracked yet!</p><p style="color: var(--text-muted);">Admin can add squad members using the track bar above.</p></div>';
        return;
      }

      let linkedUser = null;
      try {
        linkedUser = JSON.parse(localStorage.getItem('ghost_linked_player') || 'null');
      } catch (e) {}

      // Sort by overall wins descending
      squad.sort((a, b) => ((b.overall?.wins || 0) - (a.overall?.wins || 0)));

      let maxWins = -1;
      let mvpPlayer = null;
      squad.forEach(p => {
        if (!p.error && p.overall && (p.overall.wins || 0) > maxWins) {
          maxWins = p.overall.wins;
          mvpPlayer = p.epic_name;
        }
      });

      const accoladesMap = computeSquadAccolades(squad);

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
        const isLinkedMe = Boolean(linkedUser && (
          (linkedUser.epic_name && linkedUser.epic_name.toLowerCase() === p.epic_name.toLowerCase()) ||
          (linkedUser.discord_id && String(linkedUser.discord_id) === String(p.discord_id))
        ));

        const meBadge = isLinkedMe ? '<span title="Your Linked Account" style="background: rgba(88, 101, 242, 0.25); color: #a5b4fc; border: 1px solid #5865F2; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: 800;">👤 YOU</span>' : '';
        const cardBorder = isLinkedMe ? 'border: 2px solid #5865F2; box-shadow: 0 0 20px rgba(88, 101, 242, 0.35);' : (isMvp ? 'border-color: rgba(255, 215, 0, 0.5); box-shadow: 0 4px 20px rgba(255, 215, 0, 0.15);' : '');

        const deleteBtn = isAdmin ? `<button class="btn btn-secondary" style="padding: 6px 10px; font-size: 0.75rem; color: var(--error);" onclick="untrackPlayer('${p.epic_name}')" title="Untrack Player">🗑️</button>` : '';

        // Accolades Shelf
        const playerAccolades = accoladesMap[p.epic_name] || [];
        let accoladesHtml = '';
        if (playerAccolades.length > 0) {
          accoladesHtml = `
            <div class="accolades-shelf">
              ${playerAccolades.map(a => `<span class="accolade-badge ${a.class}" title="${a.desc}">${a.icon} ${a.title}</span>`).join('')}
            </div>
          `;
        }

        if (p.is_private) {
          return `
            <div class="player-card" style="border-color: rgba(245, 158, 11, 0.4); background: rgba(30, 41, 59, 0.7); ${cardBorder}">
              <div class="player-header">
                <div class="player-name">
                  <span>${p.epic_name}</span>
                  ${platBadge}
                  ${meBadge}
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
                  <button class="btn btn-secondary" style="padding: 6px 12px; font-size: 0.75rem;" onclick="loadSquadStats(true)">🔄 Re-Check</button>
                  ${deleteBtn}
                </div>
              </div>
            </div>
          `;
        }

        if (p.error) {
          return `
            <div class="player-card" style="border-color: rgba(59, 130, 246, 0.4); background: rgba(30, 41, 59, 0.7); ${cardBorder}">
              <div class="player-header">
                <div class="player-name">
                  <span>${p.epic_name}</span>
                  ${platBadge}
                  ${meBadge}
                </div>
                <span style="background: rgba(59, 130, 246, 0.2); color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.3); padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700;">
                  ⏳ Connecting...
                </span>
              </div>

              <div style="background: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.25); border-radius: 10px; padding: 12px; font-size: 0.8rem; line-height: 1.5; color: #bfdbfe;">
                <strong>Fortnite API Notice:</strong><br>
                ${p.error}<br>
                <span style="font-size: 0.75rem; color: var(--text-muted);">Please wait a few seconds and click Re-Check.</span>
              </div>

              <div style="display: flex; gap: 8px; margin-top: auto; justify-content: space-between; align-items: center; padding-top: 10px;">
                <a href="${trackerUrl}" target="_blank" style="color: var(--accent); font-size: 0.8rem; font-weight: 700; text-decoration: none;">
                  📊 FortniteTracker ↗
                </a>
                <div style="display: flex; gap: 6px;">
                  <button class="btn btn-secondary" style="padding: 6px 12px; font-size: 0.75rem;" onclick="loadSquadStats(true)">🔄 Re-Check</button>
                  ${deleteBtn}
                </div>
              </div>
            </div>
          `;
        }

        const o = p.overall || {};
        const isController = Boolean((p.gamepad && p.gamepad.matches > 0) || p.has_controller);
        const isKbm = Boolean((p.kbm && p.kbm.matches > 0) || p.has_kbm);
        const killsPerMatch = (o.killsPerMatch || (o.matches ? (o.kills / o.matches) : 0)).toFixed(2);
        const careerScore = (o.score || 0).toLocaleString();
        const playHours = Math.round((o.minutesPlayed || 0) / 60).toLocaleString();
        const outlived = (o.playersOutlived || 0).toLocaleString();
        const gamepadMatches = (p.gamepad?.matches || (isController ? (p.account_type === 'epic' ? 'Detected' : o.matches || 0) : 0)).toLocaleString();
        const kbmMatches = (p.kbm?.matches || (isKbm ? 'Detected' : 0)).toLocaleString();

        return `
          <div class="player-card" id="playerCard_${idx}" style="${cardBorder}">
            <div class="player-header">
              <div class="player-name">
                <span style="font-size: 0.8rem; color: var(--text-muted); font-weight: 800;">#${idx + 1}</span>
                <span>🏆 ${p.epic_name}</span>
                ${platBadge}
                ${meBadge}
                ${isMvp ? '<span title="Highest Wins in Squad" style="background: rgba(255, 215, 0, 0.2); color: var(--gold); border: 1px solid rgba(255, 215, 0, 0.4); padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: 800;">👑 MVP</span>' : ''}
              </div>
              <span class="player-bp">BP Lvl ${p.bp_level}</span>
            </div>

            ${accoladesHtml}

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

            <!-- Expand / Collapse Toggle Button -->
            <button class="card-expand-btn" id="expandBtn_${idx}" onclick="toggleCardExpand('${idx}')">
              <span>🔽</span> View Detailed Telemetry
            </button>

            <!-- Expandable Detailed Telemetry -->
            <div class="card-expandable-section" id="expandSection_${idx}">
              <div class="expand-sub-title">🎯 Detailed Game Mode Telemetry</div>
              <div class="expanded-modes-grid">
                <!-- Solo -->
                <div class="expanded-mode-card">
                  <div class="expanded-mode-header">
                    <span>👤 Solo</span>
                    <span style="color: var(--gold);">${(p.solo?.wins || 0).toLocaleString()} Wins</span>
                  </div>
                  <div class="expanded-mode-stats">
                    <div class="expanded-stat-item"><span class="lbl">Matches</span><span class="val">${(p.solo?.matches || 0).toLocaleString()}</span></div>
                    <div class="expanded-stat-item"><span class="lbl">Win Rate</span><span class="val">${(p.solo?.winRate || 0).toFixed(1)}%</span></div>
                    <div class="expanded-stat-item"><span class="lbl">Kills</span><span class="val">${(p.solo?.kills || 0).toLocaleString()}</span></div>
                    <div class="expanded-stat-item"><span class="lbl">K/D</span><span class="val">${(p.solo?.kd || 0).toFixed(2)}</span></div>
                    <div class="expanded-stat-item"><span class="lbl">Kills/Match</span><span class="val">${(p.solo?.killsPerMatch || (p.solo?.matches ? (p.solo.kills / p.solo.matches) : 0)).toFixed(2)}</span></div>
                    <div class="expanded-stat-item"><span class="lbl">Top 10 / 25</span><span class="val">${p.solo?.top10 || 0} / ${p.solo?.top25 || 0}</span></div>
                  </div>
                </div>

                <!-- Duo -->
                <div class="expanded-mode-card">
                  <div class="expanded-mode-header">
                    <span>👥 Duo</span>
                    <span style="color: var(--gold);">${(p.duo?.wins || 0).toLocaleString()} Wins</span>
                  </div>
                  <div class="expanded-mode-stats">
                    <div class="expanded-stat-item"><span class="lbl">Matches</span><span class="val">${(p.duo?.matches || 0).toLocaleString()}</span></div>
                    <div class="expanded-stat-item"><span class="lbl">Win Rate</span><span class="val">${(p.duo?.winRate || 0).toFixed(1)}%</span></div>
                    <div class="expanded-stat-item"><span class="lbl">Kills</span><span class="val">${(p.duo?.kills || 0).toLocaleString()}</span></div>
                    <div class="expanded-stat-item"><span class="lbl">K/D</span><span class="val">${(p.duo?.kd || 0).toFixed(2)}</span></div>
                    <div class="expanded-stat-item"><span class="lbl">Kills/Match</span><span class="val">${(p.duo?.killsPerMatch || (p.duo?.matches ? (p.duo.kills / p.duo.matches) : 0)).toFixed(2)}</span></div>
                    <div class="expanded-stat-item"><span class="lbl">Top 5 / 12</span><span class="val">${p.duo?.top5 || 0} / ${p.duo?.top12 || 0}</span></div>
                  </div>
                </div>

                <!-- Squad -->
                <div class="expanded-mode-card">
                  <div class="expanded-mode-header">
                    <span>🛡️ Squad</span>
                    <span style="color: var(--gold);">${(p.squad?.wins || 0).toLocaleString()} Wins</span>
                  </div>
                  <div class="expanded-mode-stats">
                    <div class="expanded-stat-item"><span class="lbl">Matches</span><span class="val">${(p.squad?.matches || 0).toLocaleString()}</span></div>
                    <div class="expanded-stat-item"><span class="lbl">Win Rate</span><span class="val">${(p.squad?.winRate || 0).toFixed(1)}%</span></div>
                    <div class="expanded-stat-item"><span class="lbl">Kills</span><span class="val">${(p.squad?.kills || 0).toLocaleString()}</span></div>
                    <div class="expanded-stat-item"><span class="lbl">K/D</span><span class="val">${(p.squad?.kd || 0).toFixed(2)}</span></div>
                    <div class="expanded-stat-item"><span class="lbl">Kills/Match</span><span class="val">${(p.squad?.killsPerMatch || (p.squad?.matches ? (p.squad.kills / p.squad.matches) : 0)).toFixed(2)}</span></div>
                    <div class="expanded-stat-item"><span class="lbl">Top 3 / 6</span><span class="val">${p.squad?.top3 || 0} / ${p.squad?.top6 || 0}</span></div>
                  </div>
                </div>
              </div>

              <!-- Advanced Combat & Survival Metrics -->
              <div class="expand-sub-title">⚔️ Combat & Survival Telemetry</div>
              <div class="expanded-telemetry-grid">
                <div class="stat-box" style="padding: 8px;">
                  <div class="stat-label">Kills / Match</div>
                  <div class="stat-val" style="font-size: 1rem;">${killsPerMatch}</div>
                </div>
                <div class="stat-box" style="padding: 8px;">
                  <div class="stat-label">Outlived Players</div>
                  <div class="stat-val" style="font-size: 1rem; color: #38bdf8;">${outlived}</div>
                </div>
                <div class="stat-box" style="padding: 8px;">
                  <div class="stat-label">Career Playtime</div>
                  <div class="stat-val" style="font-size: 1rem;">${playHours} hrs</div>
                </div>
                <div class="stat-box" style="padding: 8px;">
                  <div class="stat-label">Total Score</div>
                  <div class="stat-val" style="font-size: 1rem; color: #a78bfa;">${careerScore}</div>
                </div>
              </div>

              <!-- Input Device Telemetry -->
              <div class="expand-sub-title">🎮 Input Device Telemetry</div>
              <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <div class="device-pill ${isController ? 'active' : ''}">
                  <span>🎮</span>
                  <span>Gamepad / Controller: <strong>${gamepadMatches}</strong> matches</span>
                </div>
                <div class="device-pill ${isKbm ? 'active' : ''}">
                  <span>⌨️</span>
                  <span>Keyboard & Mouse: <strong>${kbmMatches}</strong> matches</span>
                </div>
              </div>
            </div>

            <div style="display: flex; gap: 8px; margin-top: auto; justify-content: space-between; align-items: center; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.06);">
              <a href="${trackerUrl}" target="_blank" style="color: var(--accent); font-size: 0.8rem; font-weight: 700; text-decoration: none;">
                📊 FortniteTracker ↗
              </a>
              <div style="display: flex; gap: 6px;">
                <button class="btn btn-secondary" style="padding: 6px 12px; font-size: 0.75rem;" onclick="loadSquadStats(true)">🔄 Re-Check</button>
                ${deleteBtn}
              </div>
            </div>
          </div>
        `;
      }).join('');

      if (allCardsExpanded) {
        document.querySelectorAll('.card-expandable-section').forEach(s => s.classList.add('open'));
        document.querySelectorAll('.card-expand-btn').forEach(b => b.innerHTML = '<span>🔼</span> Hide Detailed Telemetry');
      }
      filterSquadCards();
    }

    async function loadSquadStats(force = false) {
      const container = document.getElementById('squadContainer');
      container.innerHTML = '<p style="color: var(--text-muted);">Fetching detailed squad telemetry...</p>';
      try {
        const url = force ? '/api/squad-stats?refresh=1' : '/api/squad-stats';
        const res = await fetch(url);
        const resData = await res.json();
        const squad = Array.isArray(resData) ? resData : (resData.squad || []);
        lastSquadData = squad;
        const lastUpdated = resData.last_updated || 'Cached';
        const statusElem = document.getElementById('squadCacheStatus');
        if (statusElem) statusElem.innerText = '• ' + lastUpdated;

        // Tonight's Squad Session Banner Data Binding
        const session = resData.session;
        const banner = document.getElementById('squadSessionBanner');
        if (session && banner) {
          banner.style.display = 'flex';
          const winsElem = document.getElementById('sessionWins');
          const killsElem = document.getElementById('sessionKills');
          const matchesElem = document.getElementById('sessionMatches');
          const mvpBox = document.getElementById('sessionMvpBox');
          const mvpElem = document.getElementById('sessionMvp');
          const lastWinElem = document.getElementById('sessionLastWinText');

          if (winsElem) winsElem.innerText = `+${session.wins || 0}`;
          if (killsElem) killsElem.innerText = `+${session.kills || 0}`;
          if (matchesElem) matchesElem.innerText = `+${session.matches || 0}`;

          if (session.mvp && session.mvp_wins > 0) {
            if (mvpBox) mvpBox.style.display = 'flex';
            if (mvpElem) mvpElem.innerText = `👑 ${session.mvp} (+${session.mvp_wins})`;
          } else if (mvpBox) {
            mvpBox.style.display = 'none';
          }

          if (lastWinElem) {
            if (session.last_win) {
              const lw = session.last_win;
              const timeStr = lw.time ? new Date(lw.time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';
              lastWinElem.innerHTML = `🏆 Latest Victory Royale: <strong style="color: var(--gold);">${lw.player}</strong> (${lw.mode || 'Battle Royale'}${timeStr ? ' at ' + timeStr : ''})`;
            } else {
              lastWinElem.innerHTML = `🏆 Last Win: <strong>None yet tonight</strong>`;
            }
          }
        }

        renderSquadCards(squad);
      } catch (e) {
        container.innerHTML = `<p style="color: var(--error);">Error loading squad stats: ${e}</p>`;
      }
    }

    function toggleCardExpand(idx) {
      const sec = document.getElementById(`expandSection_${idx}`);
      const btn = document.getElementById(`expandBtn_${idx}`);
      if (!sec || !btn) return;
      const isOpen = sec.classList.toggle('open');
      btn.innerHTML = isOpen ? '<span>🔼</span> Hide Detailed Telemetry' : '<span>🔽</span> View Detailed Telemetry';
    }

    let allCardsExpanded = false;
    function toggleAllCards() {
      allCardsExpanded = !allCardsExpanded;
      const sections = document.querySelectorAll('.card-expandable-section');
      const buttons = document.querySelectorAll('.card-expand-btn');
      sections.forEach(sec => {
        if (allCardsExpanded) sec.classList.add('open');
        else sec.classList.remove('open');
      });
      buttons.forEach(btn => {
        btn.innerHTML = allCardsExpanded ? '<span>🔼</span> Hide Detailed Telemetry' : '<span>🔽</span> View Detailed Telemetry';
      });
      const topBtn = document.getElementById('toggleAllCardsBtn');
      if (topBtn) topBtn.innerText = allCardsExpanded ? '📁 Collapse All' : '📂 Expand All';
    }

    let rawShopItems = [];
    let currentShopCategory = 'all';
    let filterNewOnly = false;

    async function loadLiveShop() {
      const container = document.getElementById('shopContainer');
      container.innerHTML = '<p style="color: var(--text-muted);">Loading live item shop from Fortnite-API...</p>';
      try {
        const res = await fetch('/api/live-shop');
        const data = await res.json();
        rawShopItems = data.items || [];

        const dateStr = data.date ? data.date.slice(0, 10) : 'Today';
        const hashStr = data.hash ? data.hash.slice(0, 10) : 'Latest';
        const newCount = data.new_total || rawShopItems.filter(i => i.is_new).length;
        document.getElementById('shopMetaDate').innerText = `Date: ${dateStr} • Hash: ${hashStr} • Total Items: ${rawShopItems.length} (${newCount} new today)`;
        const badgeElem = document.getElementById('newItemsBadge');
        if (badgeElem) badgeElem.innerText = newCount;

        filterShopItems();
      } catch (e) {
        container.innerHTML = `<p style="color: var(--error);">Error loading shop: ${e}</p>`;
      }
    }

    function toggleNewItemsFilter(btn) {
      filterNewOnly = !filterNewOnly;
      if (filterNewOnly) {
        btn.classList.add('active');
        btn.style.background = 'rgba(245, 158, 11, 0.4)';
      } else {
        btn.classList.remove('active');
        btn.style.background = 'rgba(245, 158, 11, 0.15)';
      }
      filterShopItems();
    }

    function setShopCategory(cat, btn) {
      currentShopCategory = cat.toLowerCase();
      document.querySelectorAll('#shopCategoryPills .filter-pill').forEach(b => {
        if (b.id !== 'pillNewOnly') b.classList.remove('active');
      });
      if (btn && btn.id !== 'pillNewOnly') btn.classList.add('active');
      filterShopItems();
    }

    function filterShopItems() {
      const q = (document.getElementById('shopSearchInput').value || '').toLowerCase().trim();
      const sortMode = document.getElementById('shopSortSelect').value;

      let filtered = rawShopItems.filter(item => {
        // New items only toggle
        if (filterNewOnly && !item.is_new) return false;

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

    function getWishlist() {
      try {
        return JSON.parse(localStorage.getItem('ghost_item_wishlist') || '[]');
      } catch (e) {
        return [];
      }
    }

    let activeModalItem = null;

    function renderShopItems(items) {
      const container = document.getElementById('shopContainer');
      if (items.length === 0) {
        container.innerHTML = '<div style="grid-column: 1/-1; padding: 40px; text-align: center; color: var(--text-muted);"><p style="font-size: 1.1rem;">No items match your filter!</p><p style="font-size: 0.85rem; margin-top: 6px;">Try clearing your search query or selecting "All Items".</p></div>';
        return;
      }

      const wishlist = getWishlist();
      container.innerHTML = items.map(item => {
        const rarityClass = 'rarity-' + (item.rarity_clean || 'common');
        const isWishlisted = wishlist.includes(item.id || item.name);
        const safeId = encodeURIComponent(item.id || item.name);
        const regPrice = item.regularPrice || item.regular_price || 0;
        const curPrice = item.price || 0;
        const hasSale = regPrice > curPrice && curPrice > 0;
        const saved = regPrice - curPrice;
        const saleBadge = hasSale ? `<span class="item-sale-badge">SALE -${saved.toLocaleString()} 🪙</span>` : '';
        return `
          <div class="shop-item-card ${rarityClass} ${isWishlisted ? 'is-wishlisted' : ''}" data-id="${safeId}" onclick="openCosmeticModal(decodeURIComponent(this.dataset.id))" title="Click to inspect 3D model & styles">
            ${isWishlisted ? '<span class="wishlist-tag" title="In Wishlist">❤️</span>' : ''}
            ${item.is_new ? '<span class="item-new-badge">✨ NEW</span>' : ''}
            ${saleBadge}
            <span class="item-type-badge">${item.item_type || 'Cosmetic'}</span>
            ${item.icon ? `<img class="shop-img" src="${item.icon}" loading="lazy" alt="${item.name}">` : '<div style="height: 110px; display:flex; align-items:center; justify-content:center; font-size:2rem;">🎁</div>'}
            <div class="shop-name" title="${item.name}">${item.name}</div>
            <div class="shop-price">🪙 ${(item.price || 0).toLocaleString()}</div>
          </div>
        `;
      }).join('');
    }

    // Squad Hype Reactions & Community Voting
    function getCosmeticVotes() {
      try {
        return JSON.parse(localStorage.getItem('ghost_cosmetic_votes') || '{}');
      } catch (e) {
        return {};
      }
    }

    function renderCosmeticVotes(itemId) {
      const allVotes = getCosmeticVotes();
      const itemVotes = allVotes[itemId] || { fire: 0, love: 0, mid: 0, trash: 0, myVote: null };

      ['fire', 'love', 'mid', 'trash'].forEach(t => {
        const countElem = document.getElementById('voteCount_' + t);
        const btnElem = document.getElementById('vote_' + t);
        if (countElem) countElem.innerText = `(${itemVotes[t] || 0})`;
        if (btnElem) {
          if (itemVotes.myVote === t) {
            btnElem.classList.add('voted');
          } else {
            btnElem.classList.remove('voted');
          }
        }
      });
    }

    function submitCosmeticVote(voteType) {
      if (!activeModalItem) return;
      const itemId = activeModalItem.id || activeModalItem.name;
      let allVotes = getCosmeticVotes();
      if (!allVotes[itemId]) {
        allVotes[itemId] = { fire: 0, love: 0, mid: 0, trash: 0, myVote: null };
      }
      const curr = allVotes[itemId];

      if (curr.myVote === voteType) {
        curr[voteType] = Math.max(0, (curr[voteType] || 1) - 1);
        curr.myVote = null;
        showToast(`Removed your vote for ${activeModalItem.name}`);
      } else {
        if (curr.myVote && curr[curr.myVote]) {
          curr[curr.myVote] = Math.max(0, curr[curr.myVote] - 1);
        }
        curr[voteType] = (curr[voteType] || 0) + 1;
        curr.myVote = voteType;
        const labels = { fire: '🔥 Fire', love: '😍 Cop', mid: '😐 Mid', trash: '💩 Drop' };
        showToast(`Voted ${labels[voteType] || voteType} on ${activeModalItem.name}!`);
      }

      localStorage.setItem('ghost_cosmetic_votes', JSON.stringify(allVotes));
      renderCosmeticVotes(itemId);
    }

    function filterCurrentSetInShop() {
      if (!activeModalItem || !activeModalItem.set) return;
      const targetSet = activeModalItem.set;
      closeCosmeticModal();
      const searchInput = document.getElementById('shopSearchInput');
      if (searchInput) searchInput.value = targetSet;
      currentShopCategory = 'all';
      document.querySelectorAll('#shopCategoryPills .filter-pill').forEach(b => {
        if (b.id !== 'pillNewOnly') b.classList.remove('active');
      });
      const allPill = Array.from(document.querySelectorAll('#shopCategoryPills .filter-pill')).find(b => b.innerText.includes('All'));
      if (allPill) allPill.classList.add('active');

      filterShopItems();
      showToast(`Filtered Item Shop for Set: "${targetSet}"`);
    }

    // Three.js Interactive 3D Viewport & .OBJ Mesh Transformer
    let threeScene = null;
    let threeCamera = null;
    let threeRenderer = null;
    let threeMesh = null;
    let threeAutoRotate = true;
    let isThreeInitialized = false;
    let isDragging3d = false;
    let previousPointerPos = { x: 0, y: 0 };

    function initThreeJsViewport() {
      const canvas = document.getElementById('cosmeticThreeCanvas');
      const container = document.getElementById('threeJsCanvasContainer');
      if (!canvas || !container || typeof THREE === 'undefined') return;

      if (isThreeInitialized && threeRenderer) {
        const width = container.clientWidth || 400;
        const height = container.clientHeight || 260;
        if (threeCamera) {
          threeCamera.aspect = width / height;
          threeCamera.updateProjectionMatrix();
        }
        threeRenderer.setSize(width, height);
        return;
      }

      const width = container.clientWidth || 400;
      const height = container.clientHeight || 260;

      threeScene = new THREE.Scene();
      threeCamera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
      threeCamera.position.set(0, 0, 4.2);

      threeRenderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
      threeRenderer.setSize(width, height);
      threeRenderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

      // Studio Lighting
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
      threeScene.add(ambientLight);

      const keyLight = new THREE.DirectionalLight(0xffffff, 1.2);
      keyLight.position.set(5, 8, 5);
      threeScene.add(keyLight);

      const fillLight = new THREE.DirectionalLight(0x38bdf8, 0.8);
      fillLight.position.set(-5, -4, -3);
      threeScene.add(fillLight);

      // Interactive Orbit Drag Controls
      const onPointerDown = (e) => {
        isDragging3d = true;
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        previousPointerPos = { x: clientX, y: clientY };
      };

      const onPointerMove = (e) => {
        if (!isDragging3d || !threeMesh) return;
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        const deltaX = clientX - previousPointerPos.x;
        const deltaY = clientY - previousPointerPos.y;

        threeMesh.rotation.y += deltaX * 0.01;
        threeMesh.rotation.x += deltaY * 0.01;

        previousPointerPos = { x: clientX, y: clientY };
      };

      const onPointerUp = () => {
        isDragging3d = false;
      };

      canvas.addEventListener('mousedown', onPointerDown);
      window.addEventListener('mousemove', onPointerMove);
      window.addEventListener('mouseup', onPointerUp);

      canvas.addEventListener('touchstart', onPointerDown, { passive: true });
      window.addEventListener('touchmove', onPointerMove, { passive: true });
      window.addEventListener('touchend', onPointerUp);

      canvas.addEventListener('wheel', (e) => {
        e.preventDefault();
        if (!threeCamera) return;
        threeCamera.position.z += e.deltaY * 0.005;
        threeCamera.position.z = Math.max(2.0, Math.min(8.0, threeCamera.position.z));
      }, { passive: false });

      isThreeInitialized = true;
      animateThree();
    }

    function animateThree() {
      requestAnimationFrame(animateThree);
      if (threeAutoRotate && !isDragging3d && threeMesh) {
        threeMesh.rotation.y += 0.012;
      }
      if (threeRenderer && threeScene && threeCamera) {
        threeRenderer.render(threeScene, threeCamera);
      }
    }

    function loadModelForCosmetic(item) {
      initThreeJsViewport();
      if (!threeScene) return;

      if (threeMesh) {
        threeScene.remove(threeMesh);
        if (threeMesh.geometry) threeMesh.geometry.dispose();
        if (Array.isArray(threeMesh.material)) {
          threeMesh.material.forEach(m => m.dispose());
        } else if (threeMesh.material) {
          threeMesh.material.dispose();
        }
        threeMesh = null;
      }

      const textureUrl = item.images?.featured || item.images?.icon || item.icon;
      const textureLoader = new THREE.TextureLoader();
      const geometry = new THREE.BoxGeometry(2.0, 2.0, 0.22, 4, 4, 2);

      let rimColor = 0x3b82f6;
      if (item.rarity_clean === 'legendary') rimColor = 0xf59e0b;
      else if (item.rarity_clean === 'epic') rimColor = 0xa855f7;
      else if (item.rarity_clean === 'rare') rimColor = 0x0ea5e9;
      else if (item.rarity_clean === 'uncommon') rimColor = 0x22c55e;

      const rimMaterial = new THREE.MeshStandardMaterial({
        color: rimColor,
        metalness: 0.85,
        roughness: 0.25
      });

      if (textureUrl) {
        textureLoader.load(
          textureUrl,
          (tex) => {
            tex.anisotropy = 4;
            const faceMaterial = new THREE.MeshStandardMaterial({
              map: tex,
              roughness: 0.35,
              metalness: 0.1,
              transparent: true
            });

            const materials = [
              rimMaterial,
              rimMaterial,
              rimMaterial,
              rimMaterial,
              faceMaterial,
              rimMaterial
            ];

            threeMesh = new THREE.Mesh(geometry, materials);
            threeMesh.rotation.set(0, 0, 0);
            threeScene.add(threeMesh);
          },
          undefined,
          (err) => {
            console.warn('Could not load 3D texture in Three.js viewport:', err);
            const fallbackMat = new THREE.MeshStandardMaterial({ color: rimColor, wireframe: true });
            threeMesh = new THREE.Mesh(geometry, fallbackMat);
            threeScene.add(threeMesh);
          }
        );
      } else {
        const fallbackMat = new THREE.MeshStandardMaterial({ color: rimColor, wireframe: true });
        threeMesh = new THREE.Mesh(geometry, fallbackMat);
        threeScene.add(threeMesh);
      }
    }

    function toggle3dWireframe() {
      if (!threeMesh) return;
      if (Array.isArray(threeMesh.material)) {
        threeMesh.material.forEach(m => { m.wireframe = !m.wireframe; });
      } else if (threeMesh.material) {
        threeMesh.material.wireframe = !threeMesh.material.wireframe;
      }
    }

    function toggle3dRotation() {
      threeAutoRotate = !threeAutoRotate;
      const btn = document.getElementById('btn3dRotateToggle');
      if (btn) {
        btn.innerText = threeAutoRotate ? '⏸️ Pause' : '▶️ Rotate';
      }
    }

    function reset3dCamera() {
      if (threeMesh) threeMesh.rotation.set(0, 0, 0);
      if (threeCamera) threeCamera.position.set(0, 0, 4.2);
    }

    function getSafeItemName(item) {
      return (item?.name || 'cosmetic').toLowerCase().replace(/[^a-z0-9]/g, '_');
    }

    function exportCosmeticObj() {
      if (!activeModalItem) {
        showToast('No active cosmetic selected!');
        return;
      }
      const safeName = getSafeItemName(activeModalItem);
      const mtlName = `${safeName}.mtl`;
      const w = 1.2, h = 1.2, d = 0.12;

      const objContent = [
        `# Wavefront .OBJ File`,
        `# Exported from Ghost Fortnite Assistant`,
        `# Model: ${activeModalItem.name} (${activeModalItem.item_type || 'Cosmetic'})`,
        `mtllib ${mtlName}`,
        `o ${safeName}`,
        ``,
        `# Vertices`,
        `v ${-w} ${-h} ${d}`,
        `v ${w} ${-h} ${d}`,
        `v ${w} ${h} ${d}`,
        `v ${-w} ${h} ${d}`,
        `v ${-w} ${-h} ${-d}`,
        `v ${w} ${-h} ${-d}`,
        `v ${w} ${h} ${-d}`,
        `v ${-w} ${h} ${-d}`,
        ``,
        `# Texture Coordinates`,
        `vt 0.0000 0.0000`,
        `vt 1.0000 0.0000`,
        `vt 1.0000 1.0000`,
        `vt 0.0000 1.0000`,
        ``,
        `# Normals`,
        `vn 0.0000 0.0000 1.0000`,
        `vn 0.0000 0.0000 -1.0000`,
        `vn 0.0000 1.0000 0.0000`,
        `vn 0.0000 -1.0000 0.0000`,
        `vn 1.0000 0.0000 0.0000`,
        `vn -1.0000 0.0000 0.0000`,
        ``,
        `# Front Face (Art Textured)`,
        `usemtl FrontMat_${safeName}`,
        `s 1`,
        `f 1/1/1 2/2/1 3/3/1`,
        `f 1/1/1 3/3/1 4/4/1`,
        ``,
        `# Back Face`,
        `usemtl RimMat_${safeName}`,
        `f 6/2/2 5/1/2 8/4/2`,
        `f 6/2/2 8/4/2 7/3/2`,
        ``,
        `# Top Face`,
        `f 4/4/3 3/3/3 7/2/3`,
        `f 4/4/3 7/2/3 8/1/3`,
        ``,
        `# Bottom Face`,
        `f 5/1/4 6/2/4 2/3/4`,
        `f 5/1/4 2/3/4 1/4/4`,
        ``,
        `# Right Face`,
        `f 2/1/5 6/2/5 7/3/5`,
        `f 2/1/5 7/3/5 3/4/5`,
        ``,
        `# Left Face`,
        `f 5/1/6 1/2/6 4/3/6`,
        `f 5/1/6 4/3/6 8/4/6`
      ].join('\n');

      const blob = new Blob([objContent], { type: 'text/plain;charset=utf-8' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `${safeName}.obj`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      showToast(`Exported ${activeModalItem.name} as Wavefront .OBJ!`);
    }

    function downloadCosmeticMtl() {
      if (!activeModalItem) {
        showToast('No active cosmetic selected!');
        return;
      }
      const safeName = getSafeItemName(activeModalItem);
      const textureUrl = activeModalItem.images?.featured || activeModalItem.images?.icon || activeModalItem.icon || 'texture.png';

      const mtlContent = [
        `# Wavefront .MTL File`,
        `# Exported from Ghost Fortnite Assistant`,
        `# Material for: ${activeModalItem.name}`,
        ``,
        `newmtl FrontMat_${safeName}`,
        `Ka 1.000 1.000 1.000`,
        `Kd 1.000 1.000 1.000`,
        `Ks 0.200 0.200 0.200`,
        `Ns 50.0`,
        `d 1.0`,
        `illum 2`,
        `map_Kd ${textureUrl}`,
        ``,
        `newmtl RimMat_${safeName}`,
        `Ka 0.150 0.150 0.200`,
        `Kd 0.300 0.350 0.450`,
        `Ks 0.800 0.800 0.900`,
        `Ns 120.0`,
        `d 1.0`,
        `illum 2`
      ].join('\n');

      const blob = new Blob([mtlContent], { type: 'text/plain;charset=utf-8' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `${safeName}.mtl`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      showToast(`Downloaded ${activeModalItem.name} .MTL Material!`);
    }

    function openCosmeticModal(itemId) {
      const item = rawShopItems.find(i => (i.id === itemId || i.name === itemId));
      if (!item) return;
      activeModalItem = item;

      const modal = document.getElementById('cosmeticInspectModal');
      if (!modal) return;

      const rarityBadge = document.getElementById('inspectModalRarityBadge');
      if (rarityBadge) {
        rarityBadge.innerText = item.rarity || 'Common';
        rarityBadge.className = 'accolade-badge accolade-' + (item.rarity_clean === 'legendary' ? 'gold' : (item.rarity_clean === 'epic' ? 'purple' : (item.rarity_clean === 'rare' ? 'blue' : 'gold')));
      }

      const typeBadge = document.getElementById('inspectModalTypeBadge');
      if (typeBadge) typeBadge.innerText = item.item_type || 'Cosmetic';

      const newBadge = document.getElementById('inspectModalNewBadge');
      if (newBadge) newBadge.style.display = item.is_new ? 'inline-block' : 'none';

      const img = document.getElementById('inspectModalImg');
      if (img) img.src = item.icon || (item.images?.featured || item.images?.icon || '');

      const price = document.getElementById('inspectModalPrice');
      if (price) price.innerText = `🪙 ${(item.price || 0).toLocaleString()}`;

      // Regular price & savings badge
      const regPrice = item.regularPrice || item.regular_price || 0;
      const curPrice = item.price || 0;
      const savingsBadge = document.getElementById('inspectModalSavingsBadge');
      const regPriceElem = document.getElementById('inspectModalRegularPrice');
      if (regPrice > curPrice && curPrice > 0) {
        const saved = regPrice - curPrice;
        const pct = Math.round((saved / regPrice) * 100);
        if (savingsBadge) {
          savingsBadge.style.display = 'inline-block';
          savingsBadge.innerText = `Save ${saved.toLocaleString()} 🪙 (${pct}% OFF)`;
        }
        if (regPriceElem) {
          regPriceElem.style.display = 'inline';
          regPriceElem.innerText = `🪙 ${regPrice.toLocaleString()}`;
        }
      } else {
        if (savingsBadge) savingsBadge.style.display = 'none';
        if (regPriceElem) regPriceElem.style.display = 'none';
      }

      const name = document.getElementById('inspectModalName');
      if (name) name.innerText = item.name;

      const desc = document.getElementById('inspectModalDesc');
      if (desc) desc.innerText = item.description ? `"${item.description}"` : 'No description available in game files.';

      const setRow = document.getElementById('inspectModalSetRow');
      const setElem = document.getElementById('inspectModalSet');
      if (setRow && setElem) {
        if (item.set) {
          setRow.style.display = 'block';
          setElem.innerText = item.set;
        } else {
          setRow.style.display = 'none';
        }
      }

      const introRow = document.getElementById('inspectModalIntroRow');
      const introElem = document.getElementById('inspectModalIntro');
      if (introRow && introElem) {
        if (item.introduction) {
          introRow.style.display = 'block';
          introElem.innerText = item.introduction;
        } else {
          introRow.style.display = 'none';
        }
      }

      const giftableElem = document.getElementById('inspectModalGiftable');
      if (giftableElem) giftableElem.innerText = item.giftable ? 'Yes' : 'No';

      updateModalWishlistBtn();

      const dlBtn = document.getElementById('inspectDownloadBtn');
      if (dlBtn) {
        dlBtn.href = item.images?.featured || item.images?.icon || item.icon || '#';
      }

      const threeDBtn = document.getElementById('inspect3dBtn');
      if (threeDBtn) {
        if (item.id) {
          threeDBtn.href = `https://fortnite.gg/cosmetics?id=${item.id}`;
        } else {
          threeDBtn.href = `https://fortnite.gg/cosmetics?q=${encodeURIComponent(item.name)}`;
        }
      }

      // Detect Jam Track / Music vs 3D Cosmetic
      const it = (item.item_type || '').toLowerCase();
      const cat = (item.category || '').toLowerCase();
      const isMusic = it.includes('jam track') || it.includes('music') || it.includes('track') || cat.includes('jam track') || cat.includes('music') || cat.includes('track');

      const sec3d = document.getElementById('inspect3dSection');
      const secMusic = document.getElementById('inspectMusicSection');

      if (isMusic) {
        if (sec3d) sec3d.style.display = 'none';
        if (secMusic) {
          secMusic.style.display = 'block';
          const trackTitle = document.getElementById('musicTrackTitle');
          if (trackTitle) trackTitle.innerText = item.name;
          const trackArtist = document.getElementById('musicTrackArtist');
          const artist = item.artist || (item.description ? item.description.replace(/^.*by\s+/i, '').replace(/\.$/, '') : 'Various Artists');
          if (trackArtist) trackArtist.innerText = artist;
          const ytLink = document.getElementById('musicSearchYoutube');
          if (ytLink) ytLink.href = `https://www.youtube.com/results?search_query=${encodeURIComponent(item.name + ' ' + artist + ' fortnite')}`;
          const spLink = document.getElementById('musicSearchSpotify');
          if (spLink) spLink.href = `https://open.spotify.com/search/${encodeURIComponent(item.name + ' ' + artist)}`;
        }
      } else {
        if (secMusic) secMusic.style.display = 'none';
        if (sec3d) {
          sec3d.style.display = 'block';
          loadModelForCosmetic(item);
        }
      }

      // Render Squad Hype Ratings / Community Votes
      renderCosmeticVotes(item.id || item.name);

      const variantsBox = document.getElementById('inspectVariantsBox');
      const variantsList = document.getElementById('inspectVariantsList');
      if (variantsBox && variantsList) {
        if (item.variants && item.variants.length > 0) {
          variantsBox.style.display = 'block';
          variantsList.innerHTML = item.variants.map(v => `
            <div style="display: flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.05); border: 1px solid var(--card-border); padding: 4px 8px; border-radius: 8px;">
              ${v.image ? `<img src="${v.image}" style="width: 28px; height: 28px; object-fit: contain;">` : ''}
              <span style="font-size: 0.75rem; font-weight: 600;">${v.name || 'Style'}</span>
            </div>
          `).join('');
        } else {
          variantsBox.style.display = 'none';
        }
      }

      const bundleBox = document.getElementById('inspectBundleBox');
      const bundleList = document.getElementById('inspectBundleList');
      if (bundleBox && bundleList) {
        if (item.bundle_items && item.bundle_items.length > 0) {
          bundleBox.style.display = 'block';
          bundleList.innerHTML = item.bundle_items.map(b => `
            <div style="display: flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.05); border: 1px solid var(--card-border); padding: 4px 8px; border-radius: 8px;">
              ${b.icon ? `<img src="${b.icon}" style="width: 28px; height: 28px; object-fit: contain;">` : ''}
              <span style="font-size: 0.75rem; font-weight: 600;">${b.name || 'Item'}</span>
            </div>
          `).join('');
        } else {
          bundleBox.style.display = 'none';
        }
      }

      modal.classList.add('open');
    }

    function closeCosmeticModal() {
      const modal = document.getElementById('cosmeticInspectModal');
      if (modal) modal.classList.remove('open');
      activeModalItem = null;
      isDragging3d = false;
    }

    function updateModalWishlistBtn() {
      const btn = document.getElementById('inspectWishlistBtn');
      if (!btn || !activeModalItem) return;
      const wishlist = getWishlist();
      const isWish = wishlist.includes(activeModalItem.id || activeModalItem.name);
      btn.innerHTML = isWish ? '❤️ Wishlisted' : '🤍 Add to Wishlist';
      btn.style.color = isWish ? '#f472b6' : 'var(--text)';
      btn.style.borderColor = isWish ? 'rgba(244, 114, 182, 0.6)' : 'var(--card-border)';
    }

    function toggleModalWishlist() {
      if (!activeModalItem) return;
      let wishlist = getWishlist();
      const itemId = activeModalItem.id || activeModalItem.name;
      const idx = wishlist.indexOf(itemId);
      if (idx >= 0) {
        wishlist.splice(idx, 1);
        showToast(`Removed "${activeModalItem.name}" from Wishlist`);
      } else {
        wishlist.push(itemId);
        showToast(`Added "${activeModalItem.name}" to Wishlist! ❤️`);
      }
      localStorage.setItem('ghost_item_wishlist', JSON.stringify(wishlist));
      updateModalWishlistBtn();
      filterShopItems();
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
      const interactiveWrapper = document.getElementById('interactiveMapWrapper');
      const staticWrapper = document.getElementById('staticMapWrapper');
      const img = document.getElementById('islandMapImg');
      const interactiveBtn = document.getElementById('mapViewInteractiveBtn');
      const poiBtn = document.getElementById('mapViewPoiBtn');
      const cleanBtn = document.getElementById('mapViewCleanBtn');

      [interactiveBtn, poiBtn, cleanBtn].forEach(b => {
        if (b) {
          b.style.background = '';
          b.style.borderColor = '';
          b.style.color = '';
        }
      });

      if (mode === 'interactive') {
        if (interactiveWrapper) interactiveWrapper.style.display = 'flex';
        if (staticWrapper) staticWrapper.style.display = 'none';
        if (interactiveBtn) {
          interactiveBtn.style.background = 'rgba(0, 168, 255, 0.2)';
          interactiveBtn.style.borderColor = 'var(--accent)';
          interactiveBtn.style.color = 'var(--accent)';
        }
      } else if (mode === 'clean') {
        if (interactiveWrapper) interactiveWrapper.style.display = 'none';
        if (staticWrapper) staticWrapper.style.display = 'flex';
        if (img && mapImages.blank) img.src = mapImages.blank;
        if (cleanBtn) {
          cleanBtn.style.background = 'rgba(0, 168, 255, 0.2)';
          cleanBtn.style.borderColor = 'var(--accent)';
          cleanBtn.style.color = 'var(--accent)';
        }
      } else {
        // mode === 'poi'
        if (interactiveWrapper) interactiveWrapper.style.display = 'none';
        if (staticWrapper) staticWrapper.style.display = 'flex';
        if (img) img.src = mapImages.pois || 'https://fortnite-api.com/images/map_en.png';
        if (poiBtn) {
          poiBtn.style.background = 'rgba(0, 168, 255, 0.2)';
          poiBtn.style.borderColor = 'var(--accent)';
          poiBtn.style.color = 'var(--accent)';
        }
      }
    }

    function toggleMapFullscreen() {
      const container = document.getElementById('mapCardContainer') || document.getElementById('interactiveMapWrapper');
      if (!container) return;
      if (!document.fullscreenElement) {
        if (container.requestFullscreen) {
          container.requestFullscreen();
        } else if (container.webkitRequestFullscreen) {
          container.webkitRequestFullscreen();
        }
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        }
      }
    }

    function reloadMapIframe() {
      const iframe = document.getElementById('fortniteGgIframe');
      if (iframe) {
        iframe.src = 'https://fortnite.gg/?t=' + Date.now();
        showToast('Reloading Fortnite.gg interactive map...');
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
        const deleteBtn = isAdmin ? `<button style="background: transparent; border: none; color: var(--error); cursor: pointer; font-size: 0.85rem; padding: 0 4px;" data-name="${safeName}" onclick="deleteCustomPoi(decodeURIComponent(this.dataset.name))" title="Delete custom spot">✕</button>` : '';
        return `
          <div class="custom-poi-chip">
            <span style="cursor: pointer;" data-name="${safeName}" onclick="selectDropSpot(decodeURIComponent(this.dataset.name))" title="Select as drop target">
              📍 <strong>${p.name}</strong> ${p.note ? `<span style="color: var(--text-muted); font-size: 0.75rem;">(${p.note})</span>` : ''}
            </span>
            ${deleteBtn}
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

    let linkPollInterval = null;

    function initDiscordLinkUI() {
      const box = document.getElementById('discordLinkStatusBox');
      if (!box) return;
      let linked = null;
      try {
        linked = JSON.parse(localStorage.getItem('ghost_linked_player') || 'null');
      } catch (e) {}

      if (linked && linked.discord_tag) {
        box.innerHTML = `
          <div style="display: flex; align-items: center; gap: 8px; background: rgba(88, 101, 242, 0.15); border: 1px solid rgba(88, 101, 242, 0.4); padding: 5px 12px; border-radius: 20px; font-size: 0.8rem;">
            <span style="color: #a5b4fc; font-weight: 700;">👤 ${linked.discord_tag}</span>
            <span style="color: var(--text-muted); font-size: 0.75rem;">(${linked.epic_name})</span>
            <button onclick="unlinkDiscordLocal()" style="background: transparent; border: none; color: var(--error); cursor: pointer; font-size: 0.8rem; margin-left: 4px;" title="Unlink profile">✕</button>
          </div>
        `;
      } else {
        box.innerHTML = `
          <button class="btn btn-secondary" style="background: rgba(88, 101, 242, 0.2); border: 1px solid rgba(88, 101, 242, 0.4); color: #a5b4fc; font-size: 0.8rem; padding: 6px 12px; display: flex; align-items: center; gap: 6px;" onclick="openDiscordLinkModal()">
            <span>🔗</span> Link Discord
          </button>
        `;
      }
    }

    function openDiscordLinkModal() {
      const modal = document.getElementById('discordLinkModal');
      modal.classList.add('open');
      document.getElementById('modalGenerateStep').style.display = 'block';
      document.getElementById('modalCodeDisplayStep').style.display = 'none';
      document.getElementById('modalSuccessStep').style.display = 'none';
      
      const epicInput = document.getElementById('modalEpicInput');
      let linked = null;
      try {
        linked = JSON.parse(localStorage.getItem('ghost_linked_player') || 'null');
      } catch (e) {}
      if (linked && linked.epic_name) {
        epicInput.value = linked.epic_name;
      }
    }

    function closeDiscordLinkModal() {
      const modal = document.getElementById('discordLinkModal');
      modal.classList.remove('open');
      cancelLinkPolling();
    }

    function cancelLinkPolling() {
      if (linkPollInterval) {
        clearInterval(linkPollInterval);
        linkPollInterval = null;
      }
      document.getElementById('modalGenerateStep').style.display = 'block';
      document.getElementById('modalCodeDisplayStep').style.display = 'none';
    }

    async function requestLinkCode() {
      const epicName = (document.getElementById('modalEpicInput').value || '').trim();
      const accountType = document.getElementById('modalPlatformSelect').value;
      if (!epicName) {
        showToast('Please enter your Epic Games or platform username');
        return;
      }

      try {
        const res = await fetch('/api/link-code/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ epic_name: epicName, account_type: accountType })
        });
        const data = await res.json();
        if (data.status !== 'success') {
          showToast(data.message || 'Error generating link code');
          return;
        }

        const code = data.code;
        document.getElementById('letter1').innerText = code[0] || 'M';
        document.getElementById('letter2').innerText = code[1] || 'O';
        document.getElementById('letter3').innerText = code[2] || 'D';
        document.getElementById('instructionCode').innerText = code;
        document.getElementById('instructionCode2').innerText = code;
        document.getElementById('instructionCode3').innerText = code;

        document.getElementById('modalGenerateStep').style.display = 'none';
        document.getElementById('modalCodeDisplayStep').style.display = 'block';

        // Poll for claim status every 2 seconds
        if (linkPollInterval) clearInterval(linkPollInterval);
        linkPollInterval = setInterval(async () => {
          try {
            const pollRes = await fetch(`/api/link-code/status?code=${code}`);
            const pollData = await pollRes.json();
            if (pollData.claimed) {
              clearInterval(linkPollInterval);
              linkPollInterval = null;
              
              const linkObj = {
                discord_id: pollData.discord_id,
                discord_tag: pollData.discord_tag,
                epic_name: pollData.epic_name || epicName,
                account_type: accountType,
                linked_at: new Date().toISOString()
              };
              localStorage.setItem('ghost_linked_player', JSON.stringify(linkObj));
              
              document.getElementById('modalCodeDisplayStep').style.display = 'none';
              document.getElementById('modalSuccessStep').style.display = 'block';
              document.getElementById('modalSuccessMsg').innerText = `Linked to @${pollData.discord_tag} for player '${pollData.epic_name || epicName}'!`;
              
              initDiscordLinkUI();
              loadSquadStats(true);
              showToast(`Linked to @${pollData.discord_tag}!`);
            }
          } catch (err) {
            console.error('Polling error:', err);
          }
        }, 2000);

      } catch (err) {
        showToast('Failed to connect to server: ' + err);
      }
    }

    function unlinkDiscordLocal() {
      if (confirm('Disconnect your Discord link on this browser?')) {
        localStorage.removeItem('ghost_linked_player');
        initDiscordLinkUI();
        loadSquadStats();
        showToast('Discord link disconnected.');
      }
    }

    window.onload = () => {
      checkAdminState();
      initDiscordLinkUI();
      loadSquadStats();
    };
  </script>
</body>
</html>
"""
