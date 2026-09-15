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

    /* FITTING ROOM & LOADOUT STUDIO */
    .fitting-stage {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: radial-gradient(circle at center, #1e1b4b 0%, #0b0f19 80%);
      border: 1px solid rgba(147, 51, 234, 0.35);
      border-radius: 16px;
      padding: 24px;
      position: relative;
      overflow: hidden;
      min-height: 380px;
      box-shadow: 0 10px 40px rgba(147, 51, 234, 0.15);
    }
    .fitting-mannequin-preview {
      width: 220px;
      height: 220px;
      object-fit: contain;
      filter: drop-shadow(0 12px 24px rgba(0,0,0,0.8));
      transition: transform 0.3s ease;
      z-index: 2;
    }
    .fitting-pedestal {
      position: absolute;
      bottom: 20px;
      width: 220px;
      height: 30px;
      background: radial-gradient(ellipse at center, rgba(147, 51, 234, 0.6) 0%, rgba(147, 51, 234, 0) 70%);
      border-radius: 50%;
      filter: blur(4px);
    }
    .slots-container {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 12px;
      margin-top: 20px;
      width: 100%;
    }
    .slot-card {
      background: rgba(15, 23, 42, 0.8);
      border: 1px dashed rgba(255, 255, 255, 0.18);
      border-radius: 12px;
      padding: 12px 8px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      cursor: pointer;
      position: relative;
      transition: all 0.2s ease;
      min-height: 140px;
    }
    .slot-card:hover {
      border-color: var(--accent);
      background: rgba(15, 23, 42, 0.95);
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(0, 168, 255, 0.2);
    }
    .slot-card.equipped {
      border-style: solid;
      border-color: rgba(147, 51, 234, 0.5);
      background: linear-gradient(180deg, rgba(30, 27, 75, 0.4) 0%, rgba(15, 23, 42, 0.8) 100%);
    }
    .slot-icon-img {
      width: 64px;
      height: 64px;
      object-fit: contain;
      filter: drop-shadow(0 4px 8px rgba(0,0,0,0.5));
    }
    .slot-title {
      font-size: 0.72rem;
      color: var(--text-muted);
      font-weight: 700;
      text-transform: uppercase;
      margin-bottom: 4px;
      letter-spacing: 0.5px;
    }
    .slot-item-name {
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--text);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 110px;
    }
    .slot-clear-btn {
      position: absolute;
      top: 6px;
      right: 6px;
      background: rgba(0,0,0,0.6);
      border: 1px solid rgba(255,255,255,0.2);
      border-radius: 50%;
      width: 20px;
      height: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.65rem;
      color: var(--text-muted);
      cursor: pointer;
    }
    .slot-clear-btn:hover {
      background: var(--error);
      color: #fff;
    }

    /* LOCKERS & INVENTORY */
    .locker-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
      gap: 12px;
    }
    .locker-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
      position: relative;
      transition: all 0.2s ease;
      cursor: pointer;
    }
    .locker-card:hover {
      border-color: var(--accent);
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 168, 255, 0.25);
    }
    .locker-card-img {
      width: 70px;
      height: 70px;
      object-fit: contain;
      filter: drop-shadow(0 4px 8px rgba(0,0,0,0.4));
    }
    .shared-badge {
      position: absolute;
      top: 6px;
      left: 6px;
      background: linear-gradient(135deg, #8b5cf6, #3b82f6);
      color: #fff;
      font-size: 0.62rem;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 6px;
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
      <button class="nav-btn" onclick="switchTab('fitting')">👗 Fitting Room</button>
      <button class="nav-btn" onclick="switchTab('lockers')">🎒 Squad Lockers</button>
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

    <!-- TAB: FITTING ROOM / COMBO STUDIO -->
    <section id="tab-fitting" class="tab-content">
      <div class="card" style="border-color: rgba(147, 51, 234, 0.35); margin-bottom: 20px;">
        <div class="card-title">
          <span>👗 Ghost Fitting Room & Combo Studio</span>
          <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <button class="btn btn-secondary" onclick="randomizeCombo()">🎲 Randomize</button>
            <button class="btn btn-secondary" onclick="clearFittingRoom()">🗑️ Clear</button>
            <button class="btn btn-secondary" onclick="openSaveComboModal()">💾 Save Combo</button>
            <button class="btn btn-primary" onclick="broadcastCurrentCombo()">📢 Post to Discord</button>
          </div>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">
          Mix and match Fortnite outfits, back blings, pickaxes, shoes, gliders, and wraps just like Fortnite.gg! See your combo before you buy in today's Item Shop, inspect items in full 3D, and calculate squad savings.
        </p>

        <!-- Mannequin Stage & Slots -->
        <div style="display: grid; grid-template-columns: minmax(280px, 360px) 1fr; gap: 20px; align-items: start;">
          <!-- Mannequin Podium -->
          <div class="fitting-stage">
            <div style="position: absolute; top: 14px; left: 16px; font-size: 0.75rem; color: var(--accent); font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;">
              🎭 Mannequin Stage
            </div>
            <button class="btn btn-secondary" id="btnFitting3dInspect" style="position: absolute; top: 12px; right: 14px; padding: 4px 10px; font-size: 0.72rem; display: none;" onclick="inspectEquippedIn3D()">
              🌐 Inspect 3D
            </button>

            <!-- Character / Skin Visual Centerpiece -->
            <img id="stageOutfitImg" src="https://fortnite-api.com/images/cosmetics/br/cid_001_athena_commando_f_default/icon.png" class="fitting-mannequin-preview" alt="Mannequin" onerror="this.src='https://fortnite-api.com/images/cosmetics/br/cid_001_athena_commando_f_default/icon.png'">
            <div class="fitting-pedestal"></div>

            <div id="stageOutfitName" style="font-size: 1.15rem; font-weight: 800; margin-top: 14px; text-align: center; z-index: 2;">
              Select an Outfit
            </div>
            <div id="stageOutfitRarity" style="font-size: 0.75rem; color: var(--text-muted); z-index: 2;">
              Click the Outfit slot below to browse
            </div>

            <!-- Shop Price & Value Tracker -->
            <div id="stageShopBanner" style="display: none; margin-top: 12px; background: rgba(34, 197, 94, 0.15); border: 1px solid rgba(34, 197, 94, 0.4); padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; color: #4ade80; font-weight: 700; z-index: 2;">
              🛒 In Today's Shop: <span id="stageShopPrice">0</span> V-Bucks
            </div>
          </div>

          <!-- Equipped Slots Grid & Shop Cost Calculator -->
          <div>
            <div class="slots-container">
              <!-- Slot: Outfit -->
              <div class="slot-card" id="slotCard_outfit" onclick="openSlotDrawer('outfit')">
                <div class="slot-title">👔 Outfit / Skin</div>
                <img id="slotImg_outfit" class="slot-icon-img" src="https://fortnite-api.com/images/cosmetics/br/cid_001_athena_commando_f_default/icon.png" alt="Outfit">
                <div class="slot-item-name" id="slotName_outfit">None Selected</div>
                <div class="slot-clear-btn" onclick="event.stopPropagation(); clearSlot('outfit');" title="Remove">✕</div>
              </div>

              <!-- Slot: Back Bling -->
              <div class="slot-card" id="slotCard_backpack" onclick="openSlotDrawer('backpack')">
                <div class="slot-title">🎒 Back Bling</div>
                <img id="slotImg_backpack" class="slot-icon-img" src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='64' height='64' fill='none' viewBox='0 0 24 24' stroke='%2364748b'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4'/></svg>" alt="Backpack">
                <div class="slot-item-name" id="slotName_backpack">Empty</div>
                <div class="slot-clear-btn" onclick="event.stopPropagation(); clearSlot('backpack');" title="Remove">✕</div>
              </div>

              <!-- Slot: Pickaxe -->
              <div class="slot-card" id="slotCard_pickaxe" onclick="openSlotDrawer('pickaxe')">
                <div class="slot-title">⛏️ Pickaxe</div>
                <img id="slotImg_pickaxe" class="slot-icon-img" src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='64' height='64' fill='none' viewBox='0 0 24 24' stroke='%2364748b'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z'/></svg>" alt="Pickaxe">
                <div class="slot-item-name" id="slotName_pickaxe">Empty</div>
                <div class="slot-clear-btn" onclick="event.stopPropagation(); clearSlot('pickaxe');" title="Remove">✕</div>
              </div>

              <!-- Slot: Shoes / Kicks -->
              <div class="slot-card" id="slotCard_shoe" onclick="openSlotDrawer('shoe')">
                <div class="slot-title">👟 Shoes / Kicks</div>
                <img id="slotImg_shoe" class="slot-icon-img" src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='64' height='64' fill='none' viewBox='0 0 24 24' stroke='%2364748b'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M3.5 18h17a1.5 1.5 0 0 0 1.5-1.5V14a5 5 0 0 0-5-5H12L8 4H4a2 2 0 0 0-2 2v10a2 2 0 0 0 1.5 2z'/></svg>" alt="Shoes">
                <div class="slot-item-name" id="slotName_shoe">Empty</div>
                <div class="slot-clear-btn" onclick="event.stopPropagation(); clearSlot('shoe');" title="Remove">✕</div>
              </div>

              <!-- Slot: Glider -->
              <div class="slot-card" id="slotCard_glider" onclick="openSlotDrawer('glider')">
                <div class="slot-title">🪂 Glider</div>
                <img id="slotImg_glider" class="slot-icon-img" src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='64' height='64' fill='none' viewBox='0 0 24 24' stroke='%2364748b'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M12 3v18m0-18C7 3 2 7 2 12c0 3 3 6 10 9m0-21c5 0 10 4 10 9 0 3-3 6-10 9'/></svg>" alt="Glider">
                <div class="slot-item-name" id="slotName_glider">Empty</div>
                <div class="slot-clear-btn" onclick="event.stopPropagation(); clearSlot('glider');" title="Remove">✕</div>
              </div>

              <!-- Slot: Wrap -->
              <div class="slot-card" id="slotCard_wrap" onclick="openSlotDrawer('wrap')">
                <div class="slot-title">🎨 Wrap</div>
                <img id="slotImg_wrap" class="slot-icon-img" src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='64' height='64' fill='none' viewBox='0 0 24 24' stroke='%2364748b'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01'/></svg>" alt="Wrap">
                <div class="slot-item-name" id="slotName_wrap">Empty</div>
                <div class="slot-clear-btn" onclick="event.stopPropagation(); clearSlot('wrap');" title="Remove">✕</div>
              </div>
            </div>

            <!-- Today's Shop Cost & Savings Calculator -->
            <div style="background: rgba(0, 0, 0, 0.35); border: 1px solid var(--card-border); border-radius: 12px; padding: 16px; margin-top: 16px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 0.85rem; font-weight: 700; color: #a5b4fc;">🪙 Today's Shop Cost Calculator</span>
                <span id="comboShopBadge" class="cache-pill">Checking Shop...</span>
              </div>
              <div style="display: flex; gap: 16px; flex-wrap: wrap; align-items: center;">
                <div>
                  <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 700;">TOTAL SHOP COST</div>
                  <div style="font-size: 1.4rem; font-weight: 900; color: var(--gold); font-family: 'JetBrains Mono', monospace;" id="comboTotalCost">0 V-Bucks</div>
                </div>
                <div style="border-left: 1px solid var(--card-border); padding-left: 16px;">
                  <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 700;">AVAILABLE TODAY</div>
                  <div style="font-size: 1rem; font-weight: 700; color: var(--text);" id="comboShopAvailable">0 of 0 items in shop</div>
                </div>
                <div style="border-left: 1px solid var(--card-border); padding-left: 16px;">
                  <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 700;">OWNED BY SQUAD</div>
                  <div style="font-size: 1rem; font-weight: 700; color: #38bdf8;" id="comboSquadOwned">0 items owned</div>
                </div>
              </div>
            </div>

            <!-- Saved Squad Combos Shelf -->
            <div style="margin-top: 16px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 0.85rem; font-weight: 700; color: var(--text);">Saved Squad Combos</span>
                <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 0.72rem;" onclick="loadSavedCombos()">🔄 Refresh</button>
              </div>
              <div id="savedCombosList" style="display: flex; gap: 10px; overflow-x: auto; padding-bottom: 8px;">
                <p style="font-size: 0.8rem; color: var(--text-muted);">No saved combos yet. Mix items above and click 'Save Combo'!</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB: SQUAD LOCKERS & INVENTORY -->
    <section id="tab-lockers" class="tab-content">
      <div class="card" style="border-color: rgba(59, 130, 246, 0.35); margin-bottom: 20px;">
        <div class="card-title">
          <span>🎒 Squad Lockers & Combined Inventory</span>
          <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <button class="btn btn-secondary" onclick="loadSquadLockers(true)">🔄 Refresh Lockers</button>
            <button class="btn btn-primary" onclick="openAddLockerModal()">➕ Add Item</button>
            <button class="btn btn-secondary" onclick="openBulkImportModal()">📥 Bulk Import</button>
          </div>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">
          View everyone's locker inventory in one unified studio. Inspect what cosmetics squad members own, find matching twin outfits for team games, and transfer items straight into the Fitting Room!
        </p>

        <!-- Player Switcher & Valuation Bar -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; margin-bottom: 20px;">
          <div style="background: rgba(0,0,0,0.3); padding: 14px; border-radius: 12px; border: 1px solid var(--card-border);">
            <label style="font-size: 0.72rem; color: var(--text-muted); font-weight: 700; text-transform: uppercase;">Active Squad Locker</label>
            <select id="lockerPlayerSelect" onchange="onLockerPlayerChange()" style="margin-top: 6px; width: 100%;">
              <option value="all">👥 All Squad (Combined Inventory)</option>
            </select>
          </div>

          <div style="background: rgba(0,0,0,0.3); padding: 14px; border-radius: 12px; border: 1px solid var(--card-border);">
            <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 700; text-transform: uppercase;">Total Items Owned</div>
            <div style="font-size: 1.4rem; font-weight: 900; color: #38bdf8; margin-top: 4px;" id="lockerTotalCount">0</div>
          </div>

          <div style="background: rgba(0,0,0,0.3); padding: 14px; border-radius: 12px; border: 1px solid var(--card-border);">
            <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 700; text-transform: uppercase;">Estimated Locker Value</div>
            <div style="font-size: 1.4rem; font-weight: 900; color: var(--gold); margin-top: 4px; font-family: 'JetBrains Mono', monospace;" id="lockerTotalValue">0 V-Bucks</div>
          </div>

          <div style="background: rgba(0,0,0,0.3); padding: 14px; border-radius: 12px; border: 1px solid var(--card-border);">
            <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 700; text-transform: uppercase;">Squad Matching Twins</div>
            <div style="font-size: 1.4rem; font-weight: 900; color: #a855f7; margin-top: 4px;" id="lockerSharedCount">0 Items</div>
          </div>
        </div>

        <!-- Squad Shared / Matching Outfits Highlight Section -->
        <div id="sharedItemsSection" style="margin-bottom: 20px; background: linear-gradient(180deg, rgba(88, 28, 135, 0.25) 0%, rgba(15, 23, 42, 0.4) 100%); border: 1px solid rgba(168, 85, 247, 0.35); border-radius: 12px; padding: 16px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="font-size: 1.1rem;">👯</span>
              <h4 style="font-size: 0.95rem; font-weight: 800; color: #c084fc;">Matching Squad Outfits & Shared Items</h4>
            </div>
            <span style="font-size: 0.75rem; color: var(--text-muted);">Items owned by 2+ squad members</span>
          </div>
          <div id="sharedItemsList" style="display: flex; gap: 12px; overflow-x: auto; padding-bottom: 8px;">
            <p style="font-size: 0.8rem; color: var(--text-muted);">No matching shared items yet. Add cosmetics to player lockers to find squad matches!</p>
          </div>
        </div>

        <!-- Search & Filter Controls -->
        <div style="background: rgba(0, 0, 0, 0.25); border: 1px solid var(--card-border); border-radius: 12px; padding: 14px; margin-bottom: 16px;">
          <div style="display: flex; flex-wrap: wrap; gap: 12px; align-items: center;">
            <div style="flex: 2; min-width: 200px;">
              <input type="text" id="lockerSearchInput" placeholder="🔍 Search locker by name..." oninput="filterLockerItems()">
            </div>
            <div style="min-width: 150px;">
              <select id="lockerSortSelect" onchange="filterLockerItems()">
                <option value="recent">🕒 Recently Added</option>
                <option value="name-asc">🔤 Name: A to Z</option>
                <option value="rarity">✨ By Rarity</option>
              </select>
            </div>
          </div>
          <div class="filter-pills" id="lockerTypePills" style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px;">
            <button class="filter-pill active" onclick="setLockerFilter('all', this)">All Items</button>
            <button class="filter-pill" onclick="setLockerFilter('outfit', this)">👕 Outfits</button>
            <button class="filter-pill" onclick="setLockerFilter('backpack', this)">🎒 Back Blings</button>
            <button class="filter-pill" onclick="setLockerFilter('pickaxe', this)">⛏️ Pickaxes</button>
            <button class="filter-pill" onclick="setLockerFilter('shoe', this)">👟 Shoes</button>
            <button class="filter-pill" onclick="setLockerFilter('glider', this)">🪂 Gliders</button>
            <button class="filter-pill" onclick="setLockerFilter('wrap', this)">🎨 Wraps</button>
            <button class="filter-pill" onclick="setLockerFilter('emote', this)">💃 Emotes</button>
          </div>
        </div>

        <!-- Locker Grid -->
        <div id="lockerItemsContainer" class="locker-grid">
          <p style="color: var(--text-muted);">Loading locker inventory...</p>
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
            <iframe id="fortniteGgIframe" src="about:blank" data-src="https://fortnite.gg/" style="width: 100%; height: 100%; border: none;" allowfullscreen loading="lazy"></iframe>
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

        <div id="threeJsCanvasContainer" style="width: 100%; height: 320px; background: radial-gradient(circle at center, #1e293b 0%, #090d16 80%); border: 1px solid var(--card-border); border-radius: 12px; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center;">
          <canvas id="cosmeticThreeCanvas" style="width: 100%; height: 100%; cursor: grab;"></canvas>
          <div style="position: absolute; bottom: 8px; left: 10px; font-size: 0.7rem; color: var(--text-muted); background: rgba(0,0,0,0.6); padding: 2px 8px; border-radius: 6px; pointer-events: none;">
            🖱️ Drag to rotate 360° • Scroll to zoom
          </div>
          <div id="threeLoadingNotice" style="display: none; position: absolute; top: 12px; right: 12px; font-size: 0.72rem; color: var(--accent); background: rgba(0,0,0,0.7); padding: 3px 8px; border-radius: 6px;">
            ⚡ Sculpting 3D Mesh...
          </div>
        </div>

        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; align-items: center;">
          <button class="btn btn-primary" style="font-size: 0.8rem; padding: 8px 14px; background: linear-gradient(135deg, #9333ea, #00a8ff); gap: 6px;" onclick="exportCosmeticObj('textured')">
            <span>📦</span> Export .OBJ (Textured)
          </button>
          <button class="btn btn-secondary" style="font-size: 0.8rem; padding: 8px 14px; gap: 6px;" onclick="exportCosmeticObj('relief')">
            <span>🗿</span> Export 3D Relief Sculpt
          </button>
          <button class="btn btn-secondary" style="font-size: 0.8rem; padding: 8px 12px; gap: 6px;" onclick="downloadCosmeticMtl()">
            <span>🎨</span> Download .MTL
          </button>
          <a id="inspectSketchfabBtn" href="#" target="_blank" class="btn btn-secondary" style="font-size: 0.8rem; padding: 8px 12px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px;">
            <span>↗</span> Sketchfab 3D Models
          </a>
          <a id="inspect3dBtn" href="#" target="_blank" class="btn btn-secondary" style="font-size: 0.8rem; padding: 8px 12px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px;">
            <span>↗</span> Fortnite.gg Details
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
  <!-- SLOT PICKER & COSMETICS CATALOG MODAL -->
  <div id="slotPickerModal" class="modal-backdrop">
    <div class="modal-box" style="max-width: 680px; max-height: 90vh; display: flex; flex-direction: column;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <h3 style="font-size: 1.15rem; font-weight: 800; display: flex; align-items: center; gap: 8px;">
          <span id="pickerTitleIcon">👗</span> <span id="pickerModalTitle">Select Cosmetic</span>
        </h3>
        <button onclick="closeSlotPickerModal()" style="background: transparent; border: none; color: var(--text-muted); font-size: 1.2rem; cursor: pointer;">✕</button>
      </div>

      <!-- Filter Tabs & Search -->
      <div style="display: flex; gap: 8px; margin-bottom: 10px;">
        <input type="text" id="pickerSearchInput" placeholder="Type to search cosmetics..." style="flex: 1;" oninput="onPickerSearchInput()">
        <select id="pickerSourceSelect" onchange="onPickerSourceChange()" style="width: 170px;">
          <option value="catalog">🌐 All 16K+ Items</option>
          <option value="shop">🛒 In Today's Shop</option>
          <option value="locker">🎒 Squad Locker</option>
        </select>
      </div>

      <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 8px; display: flex; justify-content: space-between;" id="pickerStatusRow">
        <span id="pickerStatusText">Select an item to equip:</span>
        <span id="pickerItemCount">0 items</span>
      </div>

      <!-- Item Grid with scroll -->
      <div id="pickerItemsContainer" style="flex: 1; overflow-y: auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: 10px; padding: 4px; min-height: 280px; max-height: 55vh;">
        <p style="color: var(--text-muted); grid-column: 1/-1;">Searching catalog...</p>
      </div>
    </div>
  </div>

  <!-- SAVE COMBO MODAL -->
  <div id="saveComboModal" class="modal-backdrop">
    <div class="modal-box" style="max-width: 420px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <h3 style="font-size: 1.15rem; font-weight: 800; display: flex; align-items: center; gap: 8px;">
          <span>💾</span> Save Outfit Combo
        </h3>
        <button onclick="closeSaveComboModal()" style="background: transparent; border: none; color: var(--text-muted); font-size: 1.2rem; cursor: pointer;">✕</button>
      </div>

      <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">
        Save this loadout to the squad database so friends can view it in the studio or in Discord via <code>/combo</code>!
      </p>

      <div class="form-group" style="margin-bottom: 12px;">
        <label>Combo Title</label>
        <input type="text" id="comboTitleInput" placeholder="e.g. Neon Assassin, Golden God, OG Peely">
      </div>

      <div class="form-group" style="margin-bottom: 16px;">
        <label>Creator / Squad Member</label>
        <input type="text" id="comboCreatorInput" placeholder="e.g. Mom, Dad, King Condor">
      </div>

      <div style="display: flex; gap: 10px;">
        <button class="btn btn-secondary" style="flex: 1; justify-content: center;" onclick="closeSaveComboModal()">Cancel</button>
        <button class="btn btn-primary" style="flex: 1; justify-content: center;" onclick="submitSaveCombo()">Save Combo ✓</button>
      </div>
    </div>
  </div>

  <!-- BULK IMPORT LOCKER MODAL -->
  <div id="bulkImportModal" class="modal-backdrop">
    <div class="modal-box" style="max-width: 500px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <h3 style="font-size: 1.15rem; font-weight: 800; display: flex; align-items: center; gap: 8px;">
          <span>📥</span> Bulk Import Player Locker
        </h3>
        <button onclick="closeBulkImportModal()" style="background: transparent; border: none; color: var(--text-muted); font-size: 1.2rem; cursor: pointer;">✕</button>
      </div>

      <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 14px; line-height: 1.4;">
        Enter the squad member's Epic name and paste cosmetic names (one per line). Dadmom will automatically match them against the 16,000+ cosmetic catalog and populate their persistent locker!
      </p>

      <div class="form-group" style="margin-bottom: 12px;">
        <label>Player Epic Username</label>
        <input type="text" id="importPlayerInput" placeholder="e.g. p_lmpNastie, Going__Ghost">
      </div>

      <div class="form-group" style="margin-bottom: 16px;">
        <label>Cosmetic Names (One per line)</label>
        <textarea id="importCosmeticsText" rows="6" placeholder="Peely&#10;Travis Scott&#10;Reaper&#10;Black Knight&#10;Star Wand&#10;Leviathan Axe" style="width: 100%; font-family: monospace; font-size: 0.82rem;"></textarea>
      </div>

      <div style="display: flex; gap: 10px;">
        <button class="btn btn-secondary" style="flex: 1; justify-content: center;" onclick="closeBulkImportModal()">Cancel</button>
        <button class="btn btn-primary" id="btnSubmitImport" style="flex: 1; justify-content: center;" onclick="submitBulkImport()">Import Items 🚀</button>
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
      if (tabId === 'fitting') loadFittingRoom();
      if (tabId === 'lockers') loadSquadLockers();
      if (tabId === 'map') {
        ensureMapIframeLoaded();
        loadMap();
      }
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

    function bindSquadSessionBanner(session) {
      const banner = document.getElementById('squadSessionBanner');
      if (!banner) return;
      if (!session) {
        banner.style.display = 'none';
        return;
      }
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

    async function loadSquadStats(force = false) {
      const container = document.getElementById('squadContainer');
      const statusElem = document.getElementById('squadCacheStatus');

      // 1. Instant Cache Render (Stale-While-Revalidate)
      let hasRenderedCache = false;
      try {
        const cachedRaw = localStorage.getItem('ghost_squad_cache');
        if (cachedRaw) {
          const cachedData = JSON.parse(cachedRaw);
          const cachedSquad = Array.isArray(cachedData) ? cachedData : (cachedData.squad || []);
          if (cachedSquad.length > 0) {
            lastSquadData = cachedSquad;
            bindSquadSessionBanner(cachedData.session);
            renderSquadCards(cachedSquad);
            hasRenderedCache = true;
            if (statusElem) statusElem.innerText = '• ' + (cachedData.last_updated ? cachedData.last_updated + ' (local cache)' : 'Local Cache');
          }
        }
      } catch (err) {
        console.warn('Squad local cache read error:', err);
      }

      if (!hasRenderedCache) {
        container.innerHTML = '<p style="color: var(--text-muted);">Fetching detailed squad telemetry from Fortnite API...</p>';
      }

      // 2. Fetch fresh data in background with timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 15000);

      try {
        const url = force ? '/api/squad-stats?refresh=1' : '/api/squad-stats';
        const res = await fetch(url, { signal: controller.signal });
        clearTimeout(timeoutId);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const resData = await res.json();
        const squad = Array.isArray(resData) ? resData : (resData.squad || []);
        lastSquadData = squad;
        localStorage.setItem('ghost_squad_cache', JSON.stringify(resData));

        const lastUpdated = resData.last_updated || 'Live';
        if (statusElem) statusElem.innerText = '• ' + lastUpdated;

        bindSquadSessionBanner(resData.session);
        renderSquadCards(squad);
      } catch (e) {
        clearTimeout(timeoutId);
        console.warn('Squad telemetry refresh notice:', e);
        if (!hasRenderedCache) {
          const isTimeout = e.name === 'AbortError';
          container.innerHTML = `
            <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 8px; padding: 18px; color: var(--text-main); margin-top: 10px;">
              <p style="color: var(--error); margin: 0 0 8px 0; font-weight: 600;">
                ${isTimeout ? '⏳ Server Waking Up (Cold Start)' : '⚠️ Squad Telemetry Unavailable'}
              </p>
              <p style="color: var(--text-muted); font-size: 0.85rem; margin: 0 0 14px 0;">
                ${isTimeout ? 'The server is warming up or rate-limited. Please retry in a few seconds.' : (e.message || e)}
              </p>
              <button class="btn btn-secondary" onclick="loadSquadStats(true)">🔄 Retry Squad Load</button>
            </div>
          `;
        } else if (statusElem) {
          statusElem.innerText += ' (refresh delayed)';
        }
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

      // 1. Instant Cache Render (Stale-While-Revalidate)
      let hasRenderedCache = false;
      try {
        const cachedRaw = localStorage.getItem('ghost_shop_cache');
        if (cachedRaw) {
          const cachedData = JSON.parse(cachedRaw);
          rawShopItems = cachedData.items || [];
          if (rawShopItems.length > 0) {
            const dateStr = cachedData.date ? cachedData.date.slice(0, 10) : 'Today';
            const hashStr = cachedData.hash ? cachedData.hash.slice(0, 10) : 'Latest';
            const newCount = cachedData.new_total || rawShopItems.filter(i => i.is_new).length;
            const metaElem = document.getElementById('shopMetaDate');
            if (metaElem) metaElem.innerText = `Date: ${dateStr} • Hash: ${hashStr} • Total Items: ${rawShopItems.length} (${newCount} new today) [Cached]`;
            const badgeElem = document.getElementById('newItemsBadge');
            if (badgeElem) badgeElem.innerText = newCount;
            filterShopItems();
            hasRenderedCache = true;
          }
        }
      } catch (err) {
        console.warn('Shop local cache read error:', err);
      }

      if (!hasRenderedCache) {
        container.innerHTML = '<p style="color: var(--text-muted);">Loading live item shop from Fortnite-API...</p>';
      }

      // 2. Fetch fresh data
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 15000);

      try {
        const res = await fetch('/api/live-shop', { signal: controller.signal });
        clearTimeout(timeoutId);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        rawShopItems = data.items || [];
        localStorage.setItem('ghost_shop_cache', JSON.stringify(data));

        const dateStr = data.date ? data.date.slice(0, 10) : 'Today';
        const hashStr = data.hash ? data.hash.slice(0, 10) : 'Latest';
        const newCount = data.new_total || rawShopItems.filter(i => i.is_new).length;
        const metaElem = document.getElementById('shopMetaDate');
        if (metaElem) metaElem.innerText = `Date: ${dateStr} • Hash: ${hashStr} • Total Items: ${rawShopItems.length} (${newCount} new today)`;
        const badgeElem = document.getElementById('newItemsBadge');
        if (badgeElem) badgeElem.innerText = newCount;

        filterShopItems();
      } catch (e) {
        clearTimeout(timeoutId);
        console.warn('Shop refresh notice:', e);
        if (!hasRenderedCache) {
          container.innerHTML = `<p style="color: var(--error);">Error loading shop: ${e.message || e}</p>`;
        }
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
    let activeCroppedData = null;

    function initThreeJsViewport() {
      const canvas = document.getElementById('cosmeticThreeCanvas');
      const container = document.getElementById('threeJsCanvasContainer');
      if (!canvas || !container || typeof THREE === 'undefined') return;

      if (isThreeInitialized && threeRenderer) {
        const width = container.clientWidth || 400;
        const height = container.clientHeight || 320;
        if (threeCamera) {
          threeCamera.aspect = width / height;
          threeCamera.updateProjectionMatrix();
        }
        threeRenderer.setSize(width, height);
        return;
      }

      const width = container.clientWidth || 400;
      const height = container.clientHeight || 320;

      threeScene = new THREE.Scene();
      threeCamera = new THREE.PerspectiveCamera(42, width / height, 0.1, 100);
      threeCamera.position.set(0, 0, 4.2);

      threeRenderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
      threeRenderer.setSize(width, height);
      threeRenderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

      // Studio Lighting
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.95);
      threeScene.add(ambientLight);

      const keyLight = new THREE.DirectionalLight(0xffffff, 1.3);
      keyLight.position.set(5, 8, 6);
      threeScene.add(keyLight);

      const fillLight = new THREE.DirectionalLight(0x38bdf8, 0.85);
      fillLight.position.set(-5, -4, -3);
      threeScene.add(fillLight);

      const rimLight = new THREE.DirectionalLight(0xa855f7, 0.7);
      rimLight.position.set(0, 5, -5);
      threeScene.add(rimLight);

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
        threeMesh.rotation.x = Math.max(-Math.PI * 0.42, Math.min(Math.PI * 0.42, threeMesh.rotation.x));

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
        threeCamera.position.z = Math.max(2.2, Math.min(7.5, threeCamera.position.z));
      }, { passive: false });

      isThreeInitialized = true;
      animateThree();
    }

    function animateThree() {
      requestAnimationFrame(animateThree);
      const now = performance.now() * 0.001;
      if (threeAutoRotate && !isDragging3d && threeMesh) {
        threeMesh.rotation.y += 0.012;
        threeMesh.position.y = Math.sin(now * 2.0) * 0.04;
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
        threeMesh.traverse(child => {
          if (child.geometry) child.geometry.dispose();
          if (child.material) {
            if (Array.isArray(child.material)) child.material.forEach(m => m.dispose());
            else child.material.dispose();
          }
        });
        threeMesh = null;
      }

      const notice = document.getElementById('threeLoadingNotice');
      if (notice) notice.style.display = 'block';

      const textureUrl = item.images?.featured || item.images?.icon || item.icon;
      if (!textureUrl) {
        if (notice) notice.style.display = 'none';
        return;
      }

      let rimColorHex = 0x38bdf8;
      if (item.rarity_clean === 'legendary') rimColorHex = 0xf59e0b;
      else if (item.rarity_clean === 'epic') rimColorHex = 0xa855f7;
      else if (item.rarity_clean === 'rare') rimColorHex = 0x0ea5e9;
      else if (item.rarity_clean === 'uncommon') rimColorHex = 0x22c55e;

      const img = new Image();
      img.crossOrigin = 'anonymous';
      img.onload = () => {
        if (notice) notice.style.display = 'none';

        const canvas2d = document.createElement('canvas');
        canvas2d.width = img.naturalWidth || img.width;
        canvas2d.height = img.naturalHeight || img.height;
        const ctx = canvas2d.getContext('2d');
        ctx.drawImage(img, 0, 0);

        let minX = canvas2d.width, maxX = 0, minY = canvas2d.height, maxY = 0;
        let hasOpaque = false;
        let imgData = null;
        try {
          imgData = ctx.getImageData(0, 0, canvas2d.width, canvas2d.height);
          const data = imgData.data;
          for (let y = 0; y < canvas2d.height; y++) {
            for (let x = 0; x < canvas2d.width; x++) {
              const a = data[(y * canvas2d.width + x) * 4 + 3];
              if (a > 15) {
                hasOpaque = true;
                if (x < minX) minX = x;
                if (x > maxX) maxX = x;
                if (y < minY) minY = y;
                if (y > maxY) maxY = y;
              }
            }
          }
        } catch (e) {
          console.warn('Canvas pixel read notice:', e);
        }

        if (!hasOpaque) {
          minX = 0; minY = 0; maxX = canvas2d.width - 1; maxY = canvas2d.height - 1;
        }

        // Add 3% margin
        const padX = Math.max(2, Math.round((maxX - minX) * 0.03));
        const padY = Math.max(2, Math.round((maxY - minY) * 0.03));
        minX = Math.max(0, minX - padX);
        minY = Math.max(0, minY - padY);
        maxX = Math.min(canvas2d.width - 1, maxX + padX);
        maxY = Math.min(canvas2d.height - 1, maxY + padY);

        const cropW = Math.max(1, maxX - minX + 1);
        const cropH = Math.max(1, maxY - minY + 1);
        const aspect = cropW / cropH;

        // Front texture canvas
        const frontCanvas = document.createElement('canvas');
        frontCanvas.width = cropW;
        frontCanvas.height = cropH;
        const fCtx = frontCanvas.getContext('2d');
        fCtx.drawImage(canvas2d, minX, minY, cropW, cropH, 0, 0, cropW, cropH);

        // Mirrored back texture canvas (realistic 3D back presentation)
        const backCanvas = document.createElement('canvas');
        backCanvas.width = cropW;
        backCanvas.height = cropH;
        const bCtx = backCanvas.getContext('2d');
        bCtx.translate(cropW, 0);
        bCtx.scale(-1, 1);
        bCtx.drawImage(frontCanvas, 0, 0);

        activeCroppedData = {
          cropCanvas: frontCanvas,
          aspect: aspect,
          width: cropW,
          height: cropH,
          imgData: imgData,
          minX: minX,
          minY: minY,
          sourceW: canvas2d.width,
          sourceH: canvas2d.height
        };

        const frontTex = new THREE.CanvasTexture(frontCanvas);
        frontTex.anisotropy = 4;
        const backTex = new THREE.CanvasTexture(backCanvas);
        backTex.anisotropy = 4;

        let meshW = 2.4;
        let meshH = 2.4;
        if (aspect >= 1) {
          meshW = 2.6;
          meshH = 2.6 / aspect;
        } else {
          meshH = 2.6;
          meshW = 2.6 * aspect;
        }

        const modelGroup = new THREE.Group();

        // 1. Front plate (alphaTest discards transparent pixels completely)
        const frontGeo = new THREE.PlaneGeometry(meshW, meshH);
        const frontMat = new THREE.MeshStandardMaterial({
          map: frontTex,
          transparent: true,
          alphaTest: 0.12,
          roughness: 0.35,
          metalness: 0.2,
          side: THREE.FrontSide
        });
        const frontMesh = new THREE.Mesh(frontGeo, frontMat);
        frontMesh.position.z = 0.05;
        modelGroup.add(frontMesh);

        // 2. Back plate (Mirrored so cosmetic looks continuous in 3D)
        const backGeo = new THREE.PlaneGeometry(meshW, meshH);
        const backMat = new THREE.MeshStandardMaterial({
          map: backTex,
          transparent: true,
          alphaTest: 0.12,
          roughness: 0.4,
          metalness: 0.2,
          side: THREE.FrontSide
        });
        const backMesh = new THREE.Mesh(backGeo, backMat);
        backMesh.position.z = -0.05;
        backMesh.rotation.y = Math.PI;
        modelGroup.add(backMesh);

        // 3. Middle core slices (Creates tangible physical thickness matching the silhouette)
        const midMat = new THREE.MeshStandardMaterial({
          map: frontTex,
          transparent: true,
          alphaTest: 0.15,
          color: rimColorHex,
          roughness: 0.2,
          metalness: 0.8,
          side: THREE.DoubleSide
        });
        [-0.025, 0.0, 0.025].forEach(zPos => {
          const slice = new THREE.Mesh(frontGeo, midMat);
          slice.position.z = zPos;
          modelGroup.add(slice);
        });

        // 4. Sleek 3D Studio Pedestal
        const pedRadius = Math.max(1.0, Math.max(meshW, meshH) * 0.55);
        const pedGeo = new THREE.CylinderGeometry(pedRadius, pedRadius * 1.06, 0.1, 32);
        const pedMat = new THREE.MeshStandardMaterial({
          color: 0x0f172a,
          metalness: 0.9,
          roughness: 0.25
        });
        const pedMesh = new THREE.Mesh(pedGeo, pedMat);
        pedMesh.position.y = -meshH / 2 - 0.28;
        modelGroup.add(pedMesh);

        // Glowing rarity ring on pedestal
        const ringGeo = new THREE.RingGeometry(pedRadius * 0.76, pedRadius * 0.92, 32);
        const ringMat = new THREE.MeshBasicMaterial({
          color: rimColorHex,
          side: THREE.DoubleSide
        });
        const ringMesh = new THREE.Mesh(ringGeo, ringMat);
        ringMesh.rotation.x = -Math.PI / 2;
        ringMesh.position.y = -meshH / 2 - 0.22;
        modelGroup.add(ringMesh);

        threeScene.add(modelGroup);
        threeMesh = modelGroup;
        threeMesh.rotation.set(0, 0, 0);

        if (threeCamera) {
          const maxDim = Math.max(meshW, meshH);
          threeCamera.position.set(0, 0, Math.max(3.2, maxDim * 1.35));
        }
      };

      img.onerror = (e) => {
        if (notice) notice.style.display = 'none';
        console.warn('Image load error for 3D viewport:', e);
      };
      img.src = textureUrl;
    }

    function toggle3dWireframe() {
      if (!threeMesh) return;
      threeMesh.traverse(child => {
        if (child.isMesh && child.material) {
          if (Array.isArray(child.material)) {
            child.material.forEach(m => { m.wireframe = !m.wireframe; });
          } else {
            child.material.wireframe = !child.material.wireframe;
          }
        }
      });
    }

    function toggle3dRotation() {
      threeAutoRotate = !threeAutoRotate;
      const btn = document.getElementById('btn3dRotateToggle');
      if (btn) {
        btn.innerText = threeAutoRotate ? '⏸️ Pause' : '▶️ Rotate';
      }
    }

    function reset3dCamera() {
      if (threeMesh) {
        threeMesh.rotation.set(0, 0, 0);
        threeMesh.position.set(0, 0, 0);
      }
      if (threeCamera && activeCroppedData) {
        const w = activeCroppedData.aspect >= 1 ? 2.6 : 2.6 * activeCroppedData.aspect;
        const h = activeCroppedData.aspect >= 1 ? 2.6 / activeCroppedData.aspect : 2.6;
        const maxDim = Math.max(w, h);
        threeCamera.position.set(0, 0, Math.max(3.2, maxDim * 1.35));
      } else if (threeCamera) {
        threeCamera.position.set(0, 0, 4.2);
      }
    }

    function getSafeItemName(item) {
      return (item?.name || 'cosmetic').toLowerCase().replace(/[^a-z0-9]/g, '_');
    }

    function exportCosmeticObj(mode = 'textured') {
      if (!activeModalItem) {
        showToast('No active cosmetic selected!');
        return;
      }
      const safeName = getSafeItemName(activeModalItem);
      const mtlName = `${safeName}.mtl`;

      if (mode === 'relief' && activeCroppedData) {
        exportReliefSculptObj(safeName, mtlName);
        return;
      }

      // Standard Textured 3D Mesh with Front, Back, and Beveled Sides
      const w = activeCroppedData ? (activeCroppedData.aspect >= 1 ? 2.4 : 2.4 * activeCroppedData.aspect) : 2.0;
      const h = activeCroppedData ? (activeCroppedData.aspect >= 1 ? 2.4 / activeCroppedData.aspect : 2.4) : 2.0;
      const d = 0.08;

      const hw = (w / 2).toFixed(4);
      const hh = (h / 2).toFixed(4);
      const hd = d.toFixed(4);

      const objContent = [
        `# Wavefront .OBJ 3D Model`,
        `# Exported from Ghost Fortnite Assistant`,
        `# Cosmetic: ${activeModalItem.name} (${activeModalItem.item_type || 'Item'})`,
        `mtllib ${mtlName}`,
        `o ${safeName}`,
        ``,
        `# Front Vertices (+Z)`,
        `v -${hw} -${hh} ${hd}`,
        `v ${hw} -${hh} ${hd}`,
        `v ${hw} ${hh} ${hd}`,
        `v -${hw} ${hh} ${hd}`,
        ``,
        `# Back Vertices (-Z)`,
        `v ${hw} -${hh} -${hd}`,
        `v -${hw} -${hh} -${hd}`,
        `v -${hw} ${hh} -${hd}`,
        `v ${hw} ${hh} -${hd}`,
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
        `# Front Face`,
        `usemtl FrontMat_${safeName}`,
        `s 1`,
        `f 1/1/1 2/2/1 3/3/1`,
        `f 1/1/1 3/3/1 4/4/1`,
        ``,
        `# Back Face (Mirrored)`,
        `usemtl BackMat_${safeName}`,
        `f 5/1/2 6/2/2 7/3/2`,
        `f 5/1/2 7/3/2 8/4/2`,
        ``,
        `# Edge Bevels`,
        `usemtl RimMat_${safeName}`,
        `f 4/4/3 3/3/3 8/2/3`,
        `f 4/4/3 8/2/3 7/1/3`,
        `f 5/1/4 6/2/4 2/3/4`,
        `f 5/1/4 2/3/4 1/4/4`,
        `f 2/1/5 5/2/5 8/3/5`,
        `f 2/1/5 8/3/5 3/4/5`,
        `f 6/1/6 1/2/6 4/3/6`,
        `f 6/1/6 4/3/6 7/4/6`
      ].join('\\n');

      const blob = new Blob([objContent], { type: 'text/plain;charset=utf-8' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `${safeName}.obj`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      showToast(`Exported ${activeModalItem.name} as Textured .OBJ! 📦`);
    }

    function exportReliefSculptObj(safeName, mtlName) {
      if (!activeCroppedData || !activeCroppedData.cropCanvas) return;
      const { cropCanvas, aspect } = activeCroppedData;
      const gridX = 32;
      const gridY = Math.max(12, Math.min(48, Math.round(32 / aspect)));
      const sampleCanvas = document.createElement('canvas');
      sampleCanvas.width = gridX;
      sampleCanvas.height = gridY;
      const sCtx = sampleCanvas.getContext('2d');
      sCtx.drawImage(cropCanvas, 0, 0, gridX, gridY);

      const sData = sCtx.getImageData(0, 0, gridX, gridY).data;
      const verts = [];
      const uvs = [];
      const faces = [];

      const scaleX = 2.4;
      const scaleY = 2.4 / aspect;
      const vertIndexMap = {};
      let vCount = 1;

      for (let y = 0; y < gridY; y++) {
        for (let x = 0; x < gridX; x++) {
          const idx = (y * gridX + x) * 4;
          const a = sData[idx + 3];
          if (a > 25) {
            const r = sData[idx], g = sData[idx + 1], b = sData[idx + 2];
            const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0;
            const zFront = 0.05 + luminance * 0.12;
            const zBack = -0.05;

            const posX = ((x / gridX) - 0.5) * scaleX;
            const posY = (0.5 - (y / gridY)) * scaleY;

            verts.push(`v ${posX.toFixed(4)} ${posY.toFixed(4)} ${zFront.toFixed(4)}`);
            verts.push(`v ${posX.toFixed(4)} ${posY.toFixed(4)} ${zBack.toFixed(4)}`);
            uvs.push(`vt ${(x / gridX).toFixed(4)} ${(1 - (y / gridY)).toFixed(4)}`);

            vertIndexMap[`${x},${y}`] = { front: vCount, back: vCount + 1, uv: Math.floor(vCount / 2) + 1 };
            vCount += 2;
          }
        }
      }

      for (let y = 0; y < gridY - 1; y++) {
        for (let x = 0; x < gridX - 1; x++) {
          const p00 = vertIndexMap[`${x},${y}`];
          const p10 = vertIndexMap[`${x + 1},${y}`];
          const p11 = vertIndexMap[`${x + 1},${y + 1}`];
          const p01 = vertIndexMap[`${x},${y + 1}`];

          if (p00 && p10 && p11 && p01) {
            faces.push(`f ${p00.front}/${p00.uv} ${p10.front}/${p10.uv} ${p11.front}/${p11.uv}`);
            faces.push(`f ${p00.front}/${p00.uv} ${p11.front}/${p11.uv} ${p01.front}/${p01.uv}`);
            faces.push(`f ${p10.back}/${p10.uv} ${p00.back}/${p00.uv} ${p01.back}/${p01.uv}`);
            faces.push(`f ${p10.back}/${p10.uv} ${p01.back}/${p01.uv} ${p11.back}/${p11.uv}`);
          }
        }
      }

      const sculptContent = [
        `# Wavefront .OBJ 3D Relief Sculpt`,
        `# Exported from Ghost Fortnite Assistant`,
        `# Cosmetic: ${activeModalItem.name}`,
        `mtllib ${mtlName}`,
        `o ${safeName}_relief_sculpt`,
        ``,
        `# Sculpt Vertices`,
        ...verts,
        ``,
        `# Texture Coordinates`,
        ...uvs,
        ``,
        `# Normals`,
        `vn 0.0000 0.0000 1.0000`,
        ``,
        `usemtl FrontMat_${safeName}`,
        `s 1`,
        ...faces
      ].join('\\n');

      const blob = new Blob([sculptContent], { type: 'text/plain;charset=utf-8' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `${safeName}_relief_sculpt.obj`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      showToast(`Exported ${activeModalItem.name} 3D Relief Sculpt! 🗿`);
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
        `Ns 60.0`,
        `d 1.0`,
        `illum 2`,
        `map_Kd ${textureUrl}`,
        ``,
        `newmtl BackMat_${safeName}`,
        `Ka 0.900 0.900 0.900`,
        `Kd 0.900 0.900 0.900`,
        `Ks 0.200 0.200 0.200`,
        `Ns 60.0`,
        `d 1.0`,
        `illum 2`,
        `map_Kd ${textureUrl}`,
        ``,
        `newmtl RimMat_${safeName}`,
        `Ka 0.200 0.200 0.250`,
        `Kd 0.350 0.400 0.500`,
        `Ks 0.850 0.850 0.950`,
        `Ns 120.0`,
        `d 1.0`,
        `illum 2`
      ].join('\\n');

      const blob = new Blob([mtlContent], { type: 'text/plain;charset=utf-8' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `${safeName}.mtl`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      showToast(`Downloaded ${activeModalItem.name} .MTL Material! 🎨`);
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

      const sketchfabBtn = document.getElementById('inspectSketchfabBtn');
      if (sketchfabBtn) {
        sketchfabBtn.href = `https://sketchfab.com/search?q=${encodeURIComponent(item.name + ' fortnite')}&type=models`;
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

    function ensureMapIframeLoaded() {
      const iframe = document.getElementById('fortniteGgIframe');
      if (iframe && iframe.getAttribute('data-src')) {
        const targetSrc = iframe.getAttribute('data-src');
        if (!iframe.src || iframe.src === 'about:blank' || !iframe.src.includes('fortnite.gg')) {
          iframe.src = targetSrc;
        }
      }
    }

    async function loadMap() {
      // 1. Instant Cache Render (Stale-While-Revalidate)
      try {
        const cachedRaw = localStorage.getItem('ghost_map_cache');
        if (cachedRaw) {
          const cdata = JSON.parse(cachedRaw);
          mapImages = cdata.images || {};
          islandPois = (cdata.pois || []).filter(p => p.name);
          customPois = cdata.custom_pois || [];
          if (mapImages.pois) {
            const img = document.getElementById('islandMapImg');
            if (img && (!img.src || img.src.includes('about:blank'))) img.src = mapImages.pois;
          }
          renderCustomPois();
          renderOfficialPois(islandPois);
        }
      } catch (err) {
        console.warn('Map local cache read error:', err);
      }

      // 2. Fetch fresh data
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 12000);

      try {
        const res = await fetch('/api/live-map', { signal: controller.signal });
        clearTimeout(timeoutId);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        mapImages = data.images || {};
        islandPois = (data.pois || []).filter(p => p.name);
        customPois = data.custom_pois || [];
        localStorage.setItem('ghost_map_cache', JSON.stringify(data));

        if (mapImages.pois) {
          const img = document.getElementById('islandMapImg');
          if (img) img.src = mapImages.pois;
        }

        renderCustomPois();
        renderOfficialPois(islandPois);
      } catch (e) {
        clearTimeout(timeoutId);
        console.error('Map fetch error:', e);
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
        ensureMapIframeLoaded();
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
      let hasRenderedCache = false;
      try {
        const cachedRaw = localStorage.getItem('ghost_news_cache');
        if (cachedRaw) {
          const cdata = JSON.parse(cachedRaw);
          const motds = cdata.motds || [];
          if (motds.length > 0) {
            container.innerHTML = motds.map(n => `
              <div class="news-card">
                ${n.image ? `<img src="${n.image}" loading="lazy">` : ''}
                <div class="news-body">
                  <div class="news-title">${n.title || n.tabTitle || 'News'}</div>
                  <div class="news-text">${n.body || ''}</div>
                </div>
              </div>
            `).join('');
            hasRenderedCache = true;
          }
        }
      } catch (err) {
        console.warn('News local cache error:', err);
      }

      if (!hasRenderedCache) {
        container.innerHTML = '<p style="color: var(--text-muted);">Fetching news...</p>';
      }

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 12000);

      try {
        const res = await fetch('/api/live-news', { signal: controller.signal });
        clearTimeout(timeoutId);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const motds = data.motds || [];
        localStorage.setItem('ghost_news_cache', JSON.stringify(data));
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
        clearTimeout(timeoutId);
        if (!hasRenderedCache) {
          container.innerHTML = `<p style="color: var(--error);">Error loading news: ${e.message || e}</p>`;
        }
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

    // ==========================================
    // FITTING ROOM (COMBO STUDIO) & SQUAD LOCKERS
    // ==========================================

    let equippedCombo = {
      outfit: null,
      backpack: null,
      pickaxe: null,
      shoe: null,
      glider: null,
      wrap: null
    };
    let activePickerSlot = 'outfit';
    let pickerTargetMode = 'equip';
    let savedCombos = [];
    let squadLockersData = { players: {}, shared_items: [] };
    let activeLockerFilter = 'all';
    let activeLockerSort = 'recent';
    let pickerDebounceTimer = null;

    function loadFittingRoom() {
      updateFittingStageUI();
      loadSavedCombos();
      if (!cachedShopItems || cachedShopItems.length === 0) {
        fetch('/api/live-shop').then(r => r.json()).then(items => {
          cachedShopItems = Array.isArray(items) ? items : (items.items || []);
          updateComboShopCalculator();
        }).catch(console.error);
      } else {
        updateComboShopCalculator();
      }
    }

    function updateFittingStageUI() {
      const outfit = equippedCombo.outfit;
      const stageImg = document.getElementById('stageOutfitImg');
      const stageName = document.getElementById('stageOutfitName');
      const stageRarity = document.getElementById('stageOutfitRarity');
      const btn3d = document.getElementById('btnFitting3dInspect');

      if (outfit) {
        const icon = outfit.icon || outfit.image_url || (outfit.images && (outfit.images.featured || outfit.images.icon || outfit.images.smallIcon)) || '';
        stageImg.src = icon || 'https://fortnite-api.com/images/cosmetics/br/cid_001_athena_commando_f_default/icon.png';
        stageName.innerText = outfit.name || outfit.item_name || 'Custom Outfit';
        stageRarity.innerText = (outfit.rarity || 'Common') + ' • Outfit';
        btn3d.style.display = 'inline-flex';
      } else {
        stageImg.src = 'https://fortnite-api.com/images/cosmetics/br/cid_001_athena_commando_f_default/icon.png';
        stageName.innerText = 'Select an Outfit';
        stageRarity.innerText = 'Click the Outfit slot below to browse';
        btn3d.style.display = 'none';
      }

      const slotTypes = ['outfit', 'backpack', 'pickaxe', 'shoe', 'glider', 'wrap'];
      const defaultSlotIcons = {
        outfit: 'https://fortnite-api.com/images/cosmetics/br/cid_001_athena_commando_f_default/icon.png',
        backpack: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='64' height='64' fill='none' viewBox='0 0 24 24' stroke='%2364748b'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4'/></svg>",
        pickaxe: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='64' height='64' fill='none' viewBox='0 0 24 24' stroke='%2364748b'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z'/></svg>",
        shoe: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='64' height='64' fill='none' viewBox='0 0 24 24' stroke='%2364748b'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M3.5 18h17a1.5 1.5 0 0 0 1.5-1.5V14a5 5 0 0 0-5-5H12L8 4H4a2 2 0 0 0-2 2v10a2 2 0 0 0 1.5 2z'/></svg>",
        glider: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='64' height='64' fill='none' viewBox='0 0 24 24' stroke='%2364748b'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M12 3v18m0-18C7 3 2 7 2 12c0 3 3 6 10 9m0-21c5 0 10 4 10 9 0 3-3 6-10 9'/></svg>",
        wrap: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='64' height='64' fill='none' viewBox='0 0 24 24' stroke='%2364748b'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01'/></svg>"
      };

      slotTypes.forEach(st => {
        const card = document.getElementById('slotCard_' + st);
        const img = document.getElementById('slotImg_' + st);
        const nameEl = document.getElementById('slotName_' + st);
        const item = equippedCombo[st];

        if (card && img && nameEl) {
          if (item) {
            card.classList.add('equipped');
            const icon = item.icon || item.image_url || (item.images && (item.images.icon || item.images.smallIcon)) || '';
            img.src = icon || defaultSlotIcons[st];
            nameEl.innerText = item.name || item.item_name || 'Equipped';
          } else {
            card.classList.remove('equipped');
            img.src = defaultSlotIcons[st];
            nameEl.innerText = (st === 'outfit') ? 'None Selected' : 'Empty';
          }
        }
      });

      updateComboShopCalculator();
    }

    function clearSlot(slotType) {
      equippedCombo[slotType] = null;
      updateFittingStageUI();
      showToast('Cleared ' + slotType + ' slot');
    }

    function clearFittingRoom() {
      equippedCombo = {
        outfit: null,
        backpack: null,
        pickaxe: null,
        shoe: null,
        glider: null,
        wrap: null
      };
      updateFittingStageUI();
      showToast('Fitting room cleared.');
    }

    function inspectEquippedIn3D() {
      if (equippedCombo.outfit) {
        openCosmeticModal(equippedCombo.outfit);
      } else {
        showToast('Please equip an Outfit to view in 3D');
      }
    }

    function updateComboShopCalculator() {
      let totalShopCost = 0;
      let shopAvailableCount = 0;
      let equippedCount = 0;
      let squadOwnedCount = 0;

      const allSquadItems = [];
      if (squadLockersData && squadLockersData.players) {
        Object.values(squadLockersData.players).forEach(pItems => {
          if (Array.isArray(pItems)) allSquadItems.push(...pItems);
        });
      }

      Object.entries(equippedCombo).forEach(([slot, item]) => {
        if (!item) return;
        equippedCount++;

        const matchShop = (cachedShopItems || []).find(si => {
          const sName = (si.name || '').toLowerCase();
          const iName = (item.name || item.item_name || '').toLowerCase();
          const sId = (si.id || '').toLowerCase();
          const iId = (item.id || item.item_id || '').toLowerCase();
          return (sId && iId && sId === iId) || (sName && iName && sName === iName);
        });

        if (matchShop) {
          shopAvailableCount++;
          const price = parseInt(matchShop.price || matchShop.finalPrice || 0, 10);
          totalShopCost += price;
        }

        const matchLocker = allSquadItems.find(li => {
          const lName = (li.item_name || '').toLowerCase();
          const iName = (item.name || item.item_name || '').toLowerCase();
          const lId = (li.item_id || '').toLowerCase();
          const iId = (item.id || item.item_id || '').toLowerCase();
          return (lId && iId && lId === iId) || (lName && iName && lName === iName);
        });
        if (matchLocker) {
          squadOwnedCount++;
        }
      });

      const costEl = document.getElementById('comboTotalCost');
      const availEl = document.getElementById('comboShopAvailable');
      const ownedEl = document.getElementById('comboSquadOwned');
      const badgeEl = document.getElementById('comboShopBadge');
      const bannerEl = document.getElementById('stageShopBanner');
      const stagePriceEl = document.getElementById('stageShopPrice');

      if (costEl) costEl.innerText = totalShopCost.toLocaleString() + ' V-Bucks';
      if (availEl) availEl.innerText = shopAvailableCount + ' of ' + equippedCount + ' items in shop';
      if (ownedEl) ownedEl.innerText = squadOwnedCount + ' items owned';

      if (badgeEl) {
        if (shopAvailableCount > 0) {
          badgeEl.innerText = "✓ " + shopAvailableCount + " Item(s) in Today's Shop";
          badgeEl.style.color = '#4ade80';
        } else {
          badgeEl.innerText = "Vaulted / Not in Today's Shop";
          badgeEl.style.color = 'var(--text-muted)';
        }
      }

      if (bannerEl && stagePriceEl) {
        if (equippedCombo.outfit) {
          const outfitShop = (cachedShopItems || []).find(si => {
            const sName = (si.name || '').toLowerCase();
            const iName = (equippedCombo.outfit.name || equippedCombo.outfit.item_name || '').toLowerCase();
            return sName === iName;
          });
          if (outfitShop) {
            bannerEl.style.display = 'block';
            stagePriceEl.innerText = (outfitShop.price || 1500).toLocaleString();
          } else {
            bannerEl.style.display = 'none';
          }
        } else {
          bannerEl.style.display = 'none';
        }
      }
    }

    function openSlotDrawer(slotType) {
      activePickerSlot = slotType;
      pickerTargetMode = 'equip';
      const slotTitles = {
        outfit: 'Select Outfit / Skin',
        backpack: 'Select Back Bling',
        pickaxe: 'Select Harvesting Tool / Pickaxe',
        shoe: 'Select Shoes / Kicks',
        glider: 'Select Glider',
        wrap: 'Select Weapon / Vehicle Wrap'
      };
      document.getElementById('pickerModalTitle').innerText = slotTitles[slotType] || 'Select Cosmetic';
      document.getElementById('pickerSearchInput').value = '';
      document.getElementById('pickerSourceSelect').value = 'catalog';
      document.getElementById('slotPickerModal').classList.add('open');

      fetchPickerCosmetics('', slotType, 'catalog');
    }

    function closeSlotPickerModal() {
      document.getElementById('slotPickerModal').classList.remove('open');
    }

    function onPickerSearchInput() {
      clearTimeout(pickerDebounceTimer);
      pickerDebounceTimer = setTimeout(() => {
        const q = (document.getElementById('pickerSearchInput').value || '').trim();
        const source = document.getElementById('pickerSourceSelect').value;
        fetchPickerCosmetics(q, activePickerSlot, source);
      }, 250);
    }

    function onPickerSourceChange() {
      const q = (document.getElementById('pickerSearchInput').value || '').trim();
      const source = document.getElementById('pickerSourceSelect').value;
      fetchPickerCosmetics(q, activePickerSlot, source);
    }

    async function fetchPickerCosmetics(query, cosmeticType, source) {
      const container = document.getElementById('pickerItemsContainer');
      const countEl = document.getElementById('pickerItemCount');
      container.innerHTML = '<p style="color: var(--text-muted); grid-column: 1/-1;">Searching cosmetics...</p>';

      try {
        if (source === 'shop') {
          let items = (cachedShopItems || []).filter(item => {
            const rawType = (item.type || '').toLowerCase();
            let matchesType = true;
            if (cosmeticType === 'outfit') matchesType = rawType.includes('outfit') || rawType.includes('skin');
            else if (cosmeticType === 'backpack') matchesType = rawType.includes('back') || rawType.includes('backpack');
            else if (cosmeticType === 'pickaxe') matchesType = rawType.includes('pickaxe');
            else if (cosmeticType === 'shoe') matchesType = rawType.includes('shoe') || rawType.includes('kick');
            else if (cosmeticType === 'glider') matchesType = rawType.includes('glider');
            else if (cosmeticType === 'wrap') matchesType = rawType.includes('wrap');
            if (query) {
              matchesType = matchesType && (item.name || '').toLowerCase().includes(query.toLowerCase());
            }
            return matchesType;
          });
          renderPickerItems(items);
        } else if (source === 'locker') {
          let items = [];
          if (squadLockersData && squadLockersData.players) {
            Object.values(squadLockersData.players).forEach(pList => {
              if (Array.isArray(pList)) items.push(...pList);
            });
          }
          if (cosmeticType) {
            items = items.filter(it => {
              const itType = (it.item_type || '').toLowerCase();
              let m = (itType === cosmeticType.toLowerCase()) || (cosmeticType === 'backpack' && itType === 'backpack');
              if (query) m = m && (it.item_name || '').toLowerCase().includes(query.toLowerCase());
              return m;
            });
          }
          renderPickerItems(items);
        } else {
          const res = await fetch('/api/cosmetics/catalog?q=' + encodeURIComponent(query) + '&type=' + encodeURIComponent(cosmeticType) + '&limit=60');
          const data = await res.json();
          const results = data.results || [];
          renderPickerItems(results);
        }
      } catch (err) {
        container.innerHTML = '<p style="color: var(--error); grid-column: 1/-1;">Failed to load cosmetics: ' + err + '</p>';
      }
    }

    function renderPickerItems(items) {
      const container = document.getElementById('pickerItemsContainer');
      const countEl = document.getElementById('pickerItemCount');
      if (countEl) countEl.innerText = items.length + ' found';

      if (!items || items.length === 0) {
        container.innerHTML = '<p style="color: var(--text-muted); grid-column: 1/-1;">No cosmetics found matching your criteria.</p>';
        return;
      }

      container.innerHTML = '';
      items.forEach(item => {
        const card = document.createElement('div');
        card.style.background = 'rgba(0, 0, 0, 0.4)';
        card.style.border = '1px solid var(--card-border)';
        card.style.borderRadius = '10px';
        card.style.padding = '8px';
        card.style.display = 'flex';
        card.style.flexDirection = 'column';
        card.style.alignItems = 'center';
        card.style.cursor = 'pointer';
        card.style.transition = 'all 0.2s ease';
        card.style.position = 'relative';

        const name = item.name || item.item_name || 'Cosmetic';
        const icon = item.icon || item.image_url || (item.images && (item.images.icon || item.images.smallIcon || item.images.featured)) || '';
        const rarity = item.rarity || 'Common';

        card.onmouseenter = () => { card.style.borderColor = 'var(--accent)'; card.style.transform = 'translateY(-2px)'; };
        card.onmouseleave = () => { card.style.borderColor = 'var(--card-border)'; card.style.transform = 'translateY(0)'; };

        card.innerHTML = `
          <img src="${icon}" style="width: 60px; height: 60px; object-fit: contain; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.5));" onerror="this.src='https://fortnite-api.com/images/cosmetics/br/cid_001_athena_commando_f_default/icon.png'">
          <div style="font-size: 0.72rem; font-weight: 700; color: var(--text); margin-top: 6px; text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 100%;">${name}</div>
          <div style="font-size: 0.65rem; color: var(--text-muted);">${rarity}</div>
        `;

        card.onclick = () => {
          if (pickerTargetMode === 'equip') {
            equippedCombo[activePickerSlot] = item;
            updateFittingStageUI();
            closeSlotPickerModal();
            showToast('Equipped ' + name + '!');
          } else if (pickerTargetMode === 'add_to_locker') {
            saveItemToPlayerLockerDirect(item);
          }
        };

        container.appendChild(card);
      });
    }

    async function randomizeCombo() {
      showToast('🎲 Randomizing combo...');
      try {
        const slots = ['outfit', 'backpack', 'pickaxe', 'shoe', 'glider', 'wrap'];
        for (const s of slots) {
          const res = await fetch('/api/cosmetics/catalog?type=' + s + '&limit=40');
          const data = await res.json();
          if (data.results && data.results.length > 0) {
            const rand = data.results[Math.floor(Math.random() * data.results.length)];
            equippedCombo[s] = rand;
          }
        }
        updateFittingStageUI();
        showToast('🎲 Random combo rolled!');
      } catch (err) {
        showToast('Error rolling combo: ' + err);
      }
    }

    function openSaveComboModal() {
      if (!equippedCombo.outfit && !equippedCombo.backpack && !equippedCombo.pickaxe) {
        showToast('Equip at least one cosmetic before saving a combo!');
        return;
      }
      document.getElementById('comboTitleInput').value = '';
      const linked = localStorage.getItem('ghost_linked_player');
      if (linked) {
        try {
          const lObj = JSON.parse(linked);
          document.getElementById('comboCreatorInput').value = lObj.epic_name || '';
        } catch (e) {}
      }
      document.getElementById('saveComboModal').classList.add('open');
    }

    function closeSaveComboModal() {
      document.getElementById('saveComboModal').classList.remove('open');
    }

    async function submitSaveCombo() {
      const title = (document.getElementById('comboTitleInput').value || '').trim() || 'Custom Combo';
      const creator = (document.getElementById('comboCreatorInput').value || '').trim() || 'Squad Member';

      try {
        const res = await fetch('/api/combos/save', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            creator_name: creator,
            combo_title: title,
            combo_data: equippedCombo
          })
        });
        const data = await res.json();
        if (data.status === 'success') {
          closeSaveComboModal();
          loadSavedCombos();
          showToast('Saved combo "' + title + '"! ✓');
        } else {
          showToast('Failed to save combo: ' + (data.message || ''));
        }
      } catch (err) {
        showToast('Error saving combo: ' + err);
      }
    }

    async function loadSavedCombos() {
      const container = document.getElementById('savedCombosList');
      if (!container) return;
      try {
        const res = await fetch('/api/combos');
        const data = await res.json();
        savedCombos = data.combos || [];

        if (savedCombos.length === 0) {
          container.innerHTML = '<p style="font-size: 0.8rem; color: var(--text-muted);">No saved combos yet. Mix items above and click "Save Combo"!</p>';
          return;
        }

        container.innerHTML = '';
        savedCombos.forEach(c => {
          const cData = c.combo_data || {};
          const outfit = cData.outfit || {};
          const icon = outfit.icon || outfit.image_url || (outfit.images && (outfit.images.icon || outfit.images.smallIcon)) || 'https://fortnite-api.com/images/cosmetics/br/cid_001_athena_commando_f_default/icon.png';

          const card = document.createElement('div');
          card.style.background = 'rgba(0,0,0,0.4)';
          card.style.border = '1px solid var(--card-border)';
          card.style.borderRadius = '10px';
          card.style.padding = '8px 12px';
          card.style.minWidth = '160px';
          card.style.display = 'flex';
          card.style.alignItems = 'center';
          card.style.gap = '10px';
          card.style.cursor = 'pointer';
          card.style.transition = 'all 0.2s ease';

          card.onmouseenter = () => { card.style.borderColor = 'var(--accent-purple)'; card.style.transform = 'translateY(-2px)'; };
          card.onmouseleave = () => { card.style.borderColor = 'var(--card-border)'; card.style.transform = 'translateY(0)'; };

          card.innerHTML = `
            <img src="${icon}" style="width: 44px; height: 44px; object-fit: contain; border-radius: 8px;">
            <div style="flex: 1; min-width: 0;">
              <div style="font-size: 0.78rem; font-weight: 800; color: #c084fc; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${c.combo_title || 'Combo'}</div>
              <div style="font-size: 0.68rem; color: var(--text-muted);">by ${c.creator_name || 'Squad'}</div>
            </div>
            <button class="btn btn-secondary" style="padding: 2px 6px; font-size: 0.68rem;" title="Equip to Mannequin">👗</button>
          `;

          card.onclick = () => {
            equipSavedCombo(c);
          };

          container.appendChild(card);
        });
      } catch (err) {
        console.error('Error loading saved combos:', err);
      }
    }

    function equipSavedCombo(combo) {
      if (!combo || !combo.combo_data) return;
      equippedCombo = Object.assign({
        outfit: null,
        backpack: null,
        pickaxe: null,
        shoe: null,
        glider: null,
        wrap: null
      }, combo.combo_data);
      updateFittingStageUI();
      showToast('Equipped combo "' + (combo.combo_title || 'Saved Combo') + '"!');
    }

    async function broadcastCurrentCombo() {
      if (!equippedCombo.outfit && !equippedCombo.backpack && !equippedCombo.pickaxe) {
        showToast('Equip a combo before broadcasting to Discord!');
        return;
      }
      showToast('📢 Broadcasting combo to Discord...');
      try {
        const linked = localStorage.getItem('ghost_linked_player');
        let creator = 'Squad Member';
        if (linked) {
          try { creator = JSON.parse(linked).epic_name || creator; } catch (e) {}
        }
        const title = (equippedCombo.outfit ? equippedCombo.outfit.name : 'Squad') + ' Combo';

        const res = await fetch('/api/combos/broadcast', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            creator_name: creator,
            combo_title: title,
            combo_data: equippedCombo
          })
        });
        const data = await res.json();
        if (data.status === 'success') {
          showToast('📢 Posted combo to Discord! (' + data.posted_to + ' channel(s))');
        } else {
          showToast('Failed to broadcast: ' + (data.message || ''));
        }
      } catch (err) {
        showToast('Broadcast error: ' + err);
      }
    }

    // ==========================================
    // SQUAD LOCKERS & INVENTORY SYSTEM
    // ==========================================

    async function loadSquadLockers(force = false) {
      try {
        const res = await fetch('/api/lockers');
        const data = await res.json();
        squadLockersData = data || { players: {}, shared_items: [] };

        populateLockerPlayerSelect();
        renderLockerStats();
        renderSharedItemsShelf();
        filterLockerItems();
      } catch (err) {
        console.error('Error loading squad lockers:', err);
      }
    }

    function populateLockerPlayerSelect() {
      const sel = document.getElementById('lockerPlayerSelect');
      if (!sel) return;
      const currentVal = sel.value;
      sel.innerHTML = '<option value="all">👥 All Squad (Combined Inventory)</option>';

      const players = Object.keys(squadLockersData.players || {});
      players.sort().forEach(p => {
        const count = (squadLockersData.players[p] || []).length;
        const opt = document.createElement('option');
        opt.value = p;
        opt.innerText = '👤 ' + p + ' (' + count + ' cosmetics)';
        sel.appendChild(opt);
      });

      if (currentVal && (currentVal === 'all' || players.includes(currentVal))) {
        sel.value = currentVal;
      }
    }

    function onLockerPlayerChange() {
      renderLockerStats();
      filterLockerItems();
    }

    function renderLockerStats() {
      const sel = document.getElementById('lockerPlayerSelect');
      const player = sel ? sel.value : 'all';

      let items = [];
      if (player === 'all') {
        Object.values(squadLockersData.players || {}).forEach(pList => {
          if (Array.isArray(pList)) items.push(...pList);
        });
      } else {
        items = (squadLockersData.players || {})[player] || [];
      }

      const rarityValues = {
        legendary: 2000,
        epic: 1500,
        rare: 1200,
        uncommon: 800,
        common: 500,
        icon: 1500,
        marvel: 1500,
        dc: 1500,
        gaminglegends: 1500,
        starwars: 1500
      };

      let totalVal = 0;
      items.forEach(it => {
        const r = (it.rarity || 'common').toLowerCase().replace(/[^a-z]/g, '');
        totalVal += (rarityValues[r] || 800);
      });

      const countEl = document.getElementById('lockerTotalCount');
      const valEl = document.getElementById('lockerTotalValue');
      const sharedEl = document.getElementById('lockerSharedCount');

      if (countEl) countEl.innerText = items.length.toLocaleString();
      if (valEl) valEl.innerText = totalVal.toLocaleString() + ' V-Bucks';
      if (sharedEl) sharedEl.innerText = ((squadLockersData.shared_items || []).length) + ' Matching Sets';
    }

    function renderSharedItemsShelf() {
      const container = document.getElementById('sharedItemsList');
      if (!container) return;
      const shared = squadLockersData.shared_items || [];

      if (shared.length === 0) {
        container.innerHTML = '<p style="font-size: 0.8rem; color: var(--text-muted);">No matching shared items yet. Add cosmetics to player lockers to find squad matches!</p>';
        return;
      }

      container.innerHTML = '';
      shared.forEach(it => {
        const card = document.createElement('div');
        card.style.background = 'rgba(0,0,0,0.4)';
        card.style.border = '1px solid rgba(168, 85, 247, 0.4)';
        card.style.borderRadius = '10px';
        card.style.padding = '8px 12px';
        card.style.minWidth = '170px';
        card.style.display = 'flex';
        card.style.alignItems = 'center';
        card.style.gap = '10px';
        card.style.position = 'relative';

        const ownersList = (it.owners || []).join(', ');
        card.innerHTML = `
          <img src="${it.image_url || 'https://fortnite-api.com/images/cosmetics/br/cid_001_athena_commando_f_default/icon.png'}" style="width: 44px; height: 44px; object-fit: contain; border-radius: 8px;">
          <div style="flex: 1; min-width: 0;">
            <div style="font-size: 0.78rem; font-weight: 800; color: #e9d5ff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${it.item_name}</div>
            <div style="font-size: 0.68rem; color: #a855f7; font-weight: 700;">👯 Owned by ${it.owner_count} players</div>
            <div style="font-size: 0.65rem; color: var(--text-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${ownersList}">${ownersList}</div>
          </div>
          <button class="btn btn-secondary" style="padding: 2px 6px; font-size: 0.68rem;" title="Equip to Fitting Room">👗</button>
        `;

        card.onclick = () => {
          equipItemToAppropriateSlot(it);
        };

        container.appendChild(card);
      });
    }

    function setLockerFilter(type, btn) {
      activeLockerFilter = type;
      document.querySelectorAll('#lockerTypePills .filter-pill').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      filterLockerItems();
    }

    function filterLockerItems() {
      const sel = document.getElementById('lockerPlayerSelect');
      const player = sel ? sel.value : 'all';
      const q = (document.getElementById('lockerSearchInput').value || '').trim().toLowerCase();
      const sort = document.getElementById('lockerSortSelect').value;

      let items = [];
      if (player === 'all') {
        Object.entries(squadLockersData.players || {}).forEach(([pName, pList]) => {
          if (Array.isArray(pList)) {
            pList.forEach(it => {
              items.push(Object.assign({}, it, { owner_name: pName }));
            });
          }
        });
      } else {
        items = ((squadLockersData.players || {})[player] || []).map(it => Object.assign({}, it, { owner_name: player }));
      }

      if (activeLockerFilter !== 'all') {
        items = items.filter(it => {
          const t = (it.item_type || '').toLowerCase();
          return t === activeLockerFilter.toLowerCase() || (activeLockerFilter === 'backpack' && t === 'backpack');
        });
      }

      if (q) {
        items = items.filter(it => {
          const n = (it.item_name || '').toLowerCase();
          const o = (it.owner_name || '').toLowerCase();
          return n.includes(q) || o.includes(q);
        });
      }

      if (sort === 'name-asc') {
        items.sort((a, b) => (a.item_name || '').localeCompare(b.item_name || ''));
      } else if (sort === 'rarity') {
        const rOrder = { legendary: 1, epic: 2, rare: 3, uncommon: 4, common: 5 };
        items.sort((a, b) => (rOrder[(a.rarity || '').toLowerCase()] || 99) - (rOrder[(b.rarity || '').toLowerCase()] || 99));
      }

      renderLockerCards(items);
    }

    function renderLockerCards(items) {
      const container = document.getElementById('lockerItemsContainer');
      if (!container) return;

      if (!items || items.length === 0) {
        container.innerHTML = '<p style="color: var(--text-muted); grid-column: 1/-1;">No locker items found matching your filters. Click "➕ Add Item" or "📥 Bulk Import" to build this squad member locker!</p>';
        return;
      }

      container.innerHTML = '';
      items.forEach(it => {
        const card = document.createElement('div');
        card.className = 'locker-card';

        const name = it.item_name || 'Cosmetic';
        const icon = it.image_url || 'https://fortnite-api.com/images/cosmetics/br/cid_001_athena_commando_f_default/icon.png';
        const rarity = it.rarity || 'Common';
        const typeStr = (it.item_type || 'Cosmetic').toUpperCase();

        card.innerHTML = `
          <img class="locker-card-img" src="${icon}" onerror="this.src='https://fortnite-api.com/images/cosmetics/br/cid_001_athena_commando_f_default/icon.png'">
          <div style="font-size: 0.78rem; font-weight: 800; color: var(--text); margin-top: 8px; text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 100%;">${name}</div>
          <div style="font-size: 0.68rem; color: var(--accent); font-weight: 700;">${typeStr}</div>
          <div style="font-size: 0.65rem; color: var(--text-muted);">${it.owner_name ? '👤 ' + it.owner_name : rarity}</div>
          <div style="display: flex; gap: 6px; margin-top: 8px; width: 100%;">
            <button class="btn btn-secondary btn-equip-locker" style="flex: 1; padding: 4px; font-size: 0.68rem; justify-content: center;" title="Equip to Fitting Room">👗 Equip</button>
            <button class="btn btn-secondary btn-remove-locker" style="padding: 4px 8px; font-size: 0.68rem; color: var(--error);" title="Remove from Locker">✕</button>
          </div>
        `;

        card.querySelector('.btn-equip-locker').onclick = (e) => {
          e.stopPropagation();
          equipItemToAppropriateSlot(it);
        };
        card.querySelector('.btn-remove-locker').onclick = (e) => {
          e.stopPropagation();
          removeLockerItem(it.owner_name || '', it.item_id);
        };

        container.appendChild(card);
      });
    }

    function equipItemToAppropriateSlot(item) {
      const rawType = (item.item_type || '').toLowerCase();
      let slot = 'outfit';
      if (rawType.includes('back') || rawType.includes('backpack')) slot = 'backpack';
      else if (rawType.includes('pickaxe')) slot = 'pickaxe';
      else if (rawType.includes('shoe') || rawType.includes('kick')) slot = 'shoe';
      else if (rawType.includes('glider')) slot = 'glider';
      else if (rawType.includes('wrap')) slot = 'wrap';

      equippedCombo[slot] = {
        id: item.item_id,
        name: item.item_name,
        type: item.item_type,
        rarity: item.rarity,
        icon: item.image_url
      };

      updateFittingStageUI();
      switchTab('fitting');
      showToast('Equipped ' + item.item_name + ' to ' + slot + ' in Fitting Room!');
    }

    async function removeLockerItem(player, itemId) {
      if (!player) {
        const sel = document.getElementById('lockerPlayerSelect');
        player = sel ? sel.value : '';
      }
      if (!player || player === 'all') {
        showToast('Please select a specific player to remove items from their locker.');
        return;
      }
      if (!confirm("Remove this cosmetic from " + player + "'s locker?")) return;

      try {
        const res = await fetch('/api/lockers/remove', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ player_id: player, item_id: itemId })
        });
        const data = await res.json();
        if (data.status === 'success') {
          showToast('Removed item from locker.');
          loadSquadLockers();
        } else {
          showToast('Failed to remove: ' + (data.message || ''));
        }
      } catch (err) {
        showToast('Error removing item: ' + err);
      }
    }

    function openAddLockerModal() {
      const sel = document.getElementById('lockerPlayerSelect');
      let player = sel ? sel.value : '';
      if (!player || player === 'all') {
        const linked = localStorage.getItem('ghost_linked_player');
        if (linked) {
          try { player = JSON.parse(linked).epic_name; } catch (e) {}
        }
      }
      if (!player || player === 'all') {
        player = prompt('Enter the Epic Games username of the squad member:') || '';
      }
      if (!player) return;

      activePickerSlot = 'outfit';
      pickerTargetMode = 'add_to_locker';
      window._currentLockerAddPlayer = player;

      document.getElementById('pickerModalTitle').innerText = "Add Item to " + player + "'s Locker";
      document.getElementById('pickerSearchInput').value = '';
      document.getElementById('pickerSourceSelect').value = 'catalog';
      document.getElementById('slotPickerModal').classList.add('open');

      fetchPickerCosmetics('', '', 'catalog');
    }

    async function saveItemToPlayerLockerDirect(item) {
      const player = window._currentLockerAddPlayer;
      if (!player) return;

      const itemPayload = {
        item_id: item.id || item.item_id,
        item_name: item.name || item.item_name,
        item_type: item.type || 'cosmetic',
        rarity: item.rarity || 'Common',
        image_url: item.icon || item.image_url || (item.images && (item.images.icon || item.images.smallIcon || item.images.featured)) || ''
      };

      try {
        const res = await fetch('/api/lockers/add', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ player_id: player, item: itemPayload })
        });
        const data = await res.json();
        if (data.status === 'success') {
          showToast("Added " + itemPayload.item_name + " to " + player + "'s locker!");
          closeSlotPickerModal();
          loadSquadLockers();
        } else {
          showToast('Error: ' + (data.message || ''));
        }
      } catch (err) {
        showToast('Error adding to locker: ' + err);
      }
    }

    function openBulkImportModal() {
      const sel = document.getElementById('lockerPlayerSelect');
      let player = sel ? sel.value : '';
      if (!player || player === 'all') {
        const linked = localStorage.getItem('ghost_linked_player');
        if (linked) {
          try { player = JSON.parse(linked).epic_name; } catch (e) {}
        }
      }
      if (player && player !== 'all') {
        document.getElementById('importPlayerInput').value = player;
      }
      document.getElementById('importCosmeticsText').value = '';
      document.getElementById('bulkImportModal').classList.add('open');
    }

    function closeBulkImportModal() {
      document.getElementById('bulkImportModal').classList.remove('open');
    }

    async function submitBulkImport() {
      const player = (document.getElementById('importPlayerInput').value || '').trim();
      const text = document.getElementById('importCosmeticsText').value || '';
      if (!player) {
        showToast("Please enter the player's Epic username");
        return;
      }
      const lines = text.split(String.fromCharCode(10)).map(l => l.trim()).filter(Boolean);
      if (lines.length === 0) {
        showToast('Please enter at least one cosmetic name');
        return;
      }

      const btn = document.getElementById('btnSubmitImport');
      btn.innerText = 'Matching & Importing...';
      btn.disabled = true;

      try {
        const itemsToImport = [];
        for (const line of lines) {
          try {
            const res = await fetch('/api/cosmetics/catalog?q=' + encodeURIComponent(line) + '&limit=1');
            const data = await res.json();
            if (data.results && data.results.length > 0) {
              const match = data.results[0];
              itemsToImport.push({
                item_id: match.id,
                item_name: match.name,
                item_type: match.type || 'cosmetic',
                rarity: match.rarity || 'Common',
                image_url: match.icon || (match.images && (match.images.icon || match.images.featured)) || ''
              });
            } else {
              itemsToImport.push({
                item_id: 'custom_' + line.toLowerCase().replace(/[^a-z0-9]/g, '_'),
                item_name: line,
                item_type: 'cosmetic',
                rarity: 'Common',
                image_url: 'https://fortnite-api.com/images/cosmetics/br/cid_001_athena_commando_f_default/icon.png'
              });
            }
          } catch (e) {
            console.error(e);
          }
        }

        const importRes = await fetch('/api/lockers/import', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ player_id: player, items: itemsToImport })
        });
        const importData = await importRes.json();
        closeBulkImportModal();
        showToast('Imported ' + (importData.imported_count || itemsToImport.length) + ' items for ' + player + '! 🚀');
        loadSquadLockers();
      } catch (err) {
        showToast('Import error: ' + err);
      } finally {
        btn.innerText = 'Import Items 🚀';
        btn.disabled = false;
      }
    }

    function bootstrapDashboard() {
      checkAdminState();
      initDiscordLinkUI();
      loadSquadStats();
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', bootstrapDashboard);
    } else {
      bootstrapDashboard();
    }
  </script>
</body>
</html>
"""
