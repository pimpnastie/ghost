import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "").strip()
FORTNITE_API_KEY = os.getenv("FORTNITE_API_KEY", "").strip()
MONGODB_URI = os.getenv("MONGODB_URI", "").strip()
PORT = int(os.getenv("PORT", "8080"))

FORTNITE_API_BASE = "https://fortnite-api.com"
DATABASE_PATH = str(BASE_DIR / "bot_data.db")

# Colors for Discord Embeds
COLOR_DEFAULT = 0x5865F2    # Discord Blurple
COLOR_SUCCESS = 0x57F287    # Green
COLOR_ERROR = 0xED4245      # Red
COLOR_WARNING = 0xFEE75C    # Yellow
COLOR_FORTNITE = 0x00A8FF   # Fortnite Blue

# Fortnite Rarity Colors
RARITY_COLORS = {
    "common": 0xB0B0B0,
    "uncommon": 0x4CAF50,
    "rare": 0x2196F3,
    "epic": 0x9C27B0,
    "legendary": 0xFF9800,
    "mythic": 0xFFD700,
    "exotic": 0x00FFFF,
    "transcendent": 0xFF1493,
    "icon": 0x00C8FF,
    "marvel": 0xED1D24,
    "dc": 0x0047AB,
    "starwars": 0xFEE123,
    "gaming": 0x5E35B1,
    "shadow": 0x333333,
    "lava": 0xD84315,
    "frozen": 0x80D8FF,
    "dark": 0x7B1FA2,
    "slurp": 0x00E5FF,
}

def get_rarity_color(rarity_value: str) -> int:
    if not rarity_value:
        return COLOR_FORTNITE
    key = rarity_value.lower().strip()
    return RARITY_COLORS.get(key, COLOR_FORTNITE)
