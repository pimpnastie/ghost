# ⚡ Fortnite Discord Bot

A feature-packed, modern Discord bot powered by `discord.py` (v2.x) and `fortnite-api.com`.

---

## 🚀 1-Click Server Invite Link

Click the link below to invite your bot (**Ghost**) to your friend's Discord server:

👉 **[Invite Bot to Your Discord Server](https://discord.com/oauth2/authorize?client_id=1549031914730557552&permissions=277025778752&scope=bot%20applications.commands)**

> Required permissions included: Send Messages, Embed Links, Attach Files, Read History, and Use Application Commands.

---

## 🏃 How to Start the Bot

### Option 1: Double-click (Easiest)
Simply double-click `run.bat` in this folder. It will use the pre-configured virtual environment and start the bot immediately.

### Option 2: From PowerShell or Terminal
```powershell
cd C:\Users\edhal\.gemini\antigravity\scratch\fortnite-discord-bot
.\venv\Scripts\python.exe bot.py
```

---

## 🛒 Automatic Daily Item Shop Setup

1. In Discord, go to the text channel where you want shop updates posted (e.g. `#item-shop` or `#general`).
2. Run the slash command:
   ```
   /setshopchannel
   ```
   *(Or `/setshopchannel channel:#item-shop`)*
3. **That's it!** The bot will check every 5 minutes in the background and automatically broadcast the new shop as soon as Epic Games resets it at 00:00 UTC.
4. Want to test it right now? Run:
   ```
   /postshop
   ```

---

## 🔗 Player Account Linking & Server Leaderboard

- **Link your Epic Games name**:
  ```
  /link epic_username:YourEpicName
  ```
  Once linked:
  - Simply type `/stats` with no arguments to see your own stats!
  - Check a friend's stats with `/stats player:@friend`
  - See what Epic name a member has linked with `/whois member:@friend`

- **Server Leaderboard**:
  ```
  /leaderboard metric:Wins
  ```
  Compete with everyone in your server! Choose between:
  - 👑 **Wins** (Victory Royales)
  - 🎯 **K/D Ratio**
  - 📈 **Win Rate %**
  - ⚔️ **Total Kills**
  - 🎮 **Matches Played**

---

## 📋 Full Command Directory

| Command | Arguments | Description |
| :--- | :--- | :--- |
| `/link` | `epic_username` | Link your Discord account to your Epic Games username |
| `/unlink` | *none* | Disconnect your linked Epic Games username |
| `/whois` | `[member]` | See which Epic Games account a member is linked to |
| `/stats` | `[player]`, `[time_window]` | View Battle Royale stats (Lifetime or Season) |
| `/leaderboard` | `[metric]` | Rank all linked server members on a leaderboard |
| `/shop` | *none* | View today's live Item Shop highlights & categories |
| `/setshopchannel` | `[channel]` | Set the auto-announcement channel for daily shops (Admin) |
| `/postshop` | *none* | Manually post today's shop into the current channel |
| `/drop` | *none* | Random landing spot roulette for your squad |
| `/cosmetic` | `name` | Look up any skin, emote, pickaxe, glider, or wrap |
| `/map` | *none* | View the current island map with named POIs |
| `/news` | *none* | Read the latest in-game Battle Royale news & updates |
| `/creator` | `code` | Check if a Support-A-Creator code is valid and verified |
| `/ping` | *none* | Check bot response latency |
| `/help` | *none* | View the in-Discord interactive command directory |

---

## 🛠️ Configuration & Credentials

Stored securely in [.env](file:///C:/Users/edhal/.gemini/antigravity/scratch/fortnite-discord-bot/.env):
- `DISCORD_BOT_TOKEN`: Your Discord Application Bot Token
- `FORTNITE_API_KEY`: Your `fortnite-api.com` API Key
- `bot_data.db`: Local SQLite database storing user links and guild channel preferences
