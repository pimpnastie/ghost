import aiosqlite
from typing import Optional, Dict, List, Tuple, Any
from datetime import datetime
import logging
from config import DATABASE_PATH, MONGODB_URI

logger = logging.getLogger(__name__)

# Initialize MongoDB client if MONGODB_URI is provided
_mongo_client = None
_mongo_db = None

if MONGODB_URI:
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        _mongo_client = AsyncIOMotorClient(MONGODB_URI)
        _mongo_db = _mongo_client.get_default_database("fortnite_bot")
        logger.info("MongoDB database client initialized successfully.")
    except Exception as e:
        logger.warning(f"Could not initialize MongoDB client ({e}). Falling back to SQLite.")
        _mongo_client = None
        _mongo_db = None

async def init_db():
    """Initializes the database schema if not already present."""
    if _mongo_db is not None:
        try:
            await _mongo_db.user_links.create_index("discord_user_id", unique=True)
            await _mongo_db.guild_settings.create_index("guild_id", unique=True)
            await _mongo_db.bot_state.create_index("key", unique=True)
            logger.info("MongoDB collections & indexes initialized.")
            return
        except Exception as e:
            logger.error(f"Error initializing MongoDB: {e}")

    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_links (
                discord_user_id INTEGER PRIMARY KEY,
                epic_username TEXT NOT NULL COLLATE NOCASE,
                linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS guild_settings (
                guild_id INTEGER PRIMARY KEY,
                shop_channel_id INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS bot_state (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        await db.commit()

async def link_user(discord_id: int, epic_username: str):
    """Links or updates a Discord user's Epic Games username."""
    if _mongo_db is not None:
        await _mongo_db.user_links.update_one(
            {"discord_user_id": discord_id},
            {"$set": {"epic_username": epic_username, "linked_at": datetime.utcnow()}},
            upsert=True
        )
        return

    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO user_links (discord_user_id, epic_username, linked_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(discord_user_id) DO UPDATE SET
                epic_username = excluded.epic_username,
                linked_at = CURRENT_TIMESTAMP
        """, (discord_id, epic_username))
        await db.commit()

async def get_linked_user(discord_id: int) -> Optional[str]:
    """Gets the linked Epic username for a Discord user ID."""
    if _mongo_db is not None:
        doc = await _mongo_db.user_links.find_one({"discord_user_id": discord_id})
        return doc.get("epic_username") if doc else None

    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT epic_username FROM user_links WHERE discord_user_id = ?",
            (discord_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

async def unlink_user(discord_id: int) -> bool:
    """Removes a Discord user's link. Returns True if a record was removed."""
    if _mongo_db is not None:
        res = await _mongo_db.user_links.delete_one({"discord_user_id": discord_id})
        return res.deleted_count > 0

    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "DELETE FROM user_links WHERE discord_user_id = ?",
            (discord_id,)
        )
        await db.commit()
        return cursor.rowcount > 0

async def get_linked_users_for_members(discord_ids: List[int]) -> Dict[int, str]:
    """Returns a mapping of discord_id -> epic_username for the given member IDs."""
    if not discord_ids:
        return {}

    if _mongo_db is not None:
        cursor = _mongo_db.user_links.find({"discord_user_id": {"$in": discord_ids}})
        results = {}
        async for doc in cursor:
            results[doc["discord_user_id"]] = doc["epic_username"]
        return results

    placeholders = ",".join("?" for _ in discord_ids)
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            f"SELECT discord_user_id, epic_username FROM user_links WHERE discord_user_id IN ({placeholders})",
            discord_ids
        ) as cursor:
            rows = await cursor.fetchall()
            return {row[0]: row[1] for row in rows}

async def set_guild_shop_channel(guild_id: int, channel_id: int):
    """Sets or updates the daily item shop broadcast channel for a guild."""
    if _mongo_db is not None:
        await _mongo_db.guild_settings.update_one(
            {"guild_id": guild_id},
            {"$set": {"shop_channel_id": channel_id, "updated_at": datetime.utcnow()}},
            upsert=True
        )
        return

    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO guild_settings (guild_id, shop_channel_id, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(guild_id) DO UPDATE SET
                shop_channel_id = excluded.shop_channel_id,
                updated_at = CURRENT_TIMESTAMP
        """, (guild_id, channel_id))
        await db.commit()

async def get_guild_shop_channel(guild_id: int) -> Optional[int]:
    """Gets the shop broadcast channel ID for a specific guild."""
    if _mongo_db is not None:
        doc = await _mongo_db.guild_settings.find_one({"guild_id": guild_id})
        return doc.get("shop_channel_id") if doc else None

    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT shop_channel_id FROM guild_settings WHERE guild_id = ?",
            (guild_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

async def get_all_guild_shop_channels() -> List[Tuple[int, int]]:
    """Returns list of (guild_id, shop_channel_id) for all configured guilds."""
    if _mongo_db is not None:
        cursor = _mongo_db.guild_settings.find({"shop_channel_id": {"$ne": None}})
        results = []
        async for doc in cursor:
            results.append((doc["guild_id"], doc["shop_channel_id"]))
        return results

    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT guild_id, shop_channel_id FROM guild_settings WHERE shop_channel_id IS NOT NULL"
        ) as cursor:
            return await cursor.fetchall()

async def remove_guild_shop_channel(guild_id: int):
    """Removes shop channel configuration for a guild."""
    if _mongo_db is not None:
        await _mongo_db.guild_settings.delete_one({"guild_id": guild_id})
        return

    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "DELETE FROM guild_settings WHERE guild_id = ?",
            (guild_id,)
        )
        await db.commit()

async def get_bot_state(key: str) -> Optional[str]:
    """Fetches a state variable by key."""
    if _mongo_db is not None:
        doc = await _mongo_db.bot_state.find_one({"key": key})
        return doc.get("value") if doc else None

    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT value FROM bot_state WHERE key = ?", (key,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

async def set_bot_state(key: str, value: str):
    """Sets or updates a bot state variable."""
    if _mongo_db is not None:
        await _mongo_db.bot_state.update_one(
            {"key": key},
            {"$set": {"value": value}},
            upsert=True
        )
        return

    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO bot_state (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """, (key, value))
        await db.commit()

DEFAULT_CONFIG = {
    "status_text": "Fortnite Item Shop & /help",
    "activity_type": "watching",
    "presence_status": "online",
    "shop_message": "📢 **The Fortnite Item Shop has updated!**",
    "shop_role_ping": "none",
    "shop_role_id": "",
    "auto_shop_enabled": True,
    "embed_color": "#00A8FF",
    "embed_footer": "Fortnite-API.com • Ghost Bot",
    "custom_pois": [],
    "admin_pin": "ghost123"
}

async def get_global_config() -> Dict[str, Any]:
    """Fetches global dashboard settings from database."""
    if _mongo_db is not None:
        doc = await _mongo_db.bot_settings.find_one({"key": "global_config"})
        if doc:
            doc.pop("_id", None)
            doc.pop("key", None)
            merged = DEFAULT_CONFIG.copy()
            merged.update(doc)
            return merged
        return DEFAULT_CONFIG.copy()

    # SQLite fallback
    raw = await get_bot_state("global_config_json")
    if raw:
        import json
        try:
            cfg = json.loads(raw)
            merged = DEFAULT_CONFIG.copy()
            merged.update(cfg)
            return merged
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()

async def save_global_config(config: Dict[str, Any]):
    """Saves updated global settings."""
    sanitized = {k: v for k, v in config.items() if k != "_id"}
    if _mongo_db is not None:
        await _mongo_db.bot_settings.update_one(
            {"key": "global_config"},
            {"$set": sanitized},
            upsert=True
        )
        return

    import json
    await set_bot_state("global_config_json", json.dumps(sanitized))

async def get_all_linked_users_list() -> List[Dict[str, Any]]:
    """Returns a list of all linked Discord user IDs and Epic usernames."""
    if _mongo_db is not None:
        cursor = _mongo_db.user_links.find({})
        items = []
        async for doc in cursor:
            items.append({
                "discord_user_id": doc.get("discord_user_id"),
                "epic_username": doc.get("epic_username"),
                "linked_at": str(doc.get("linked_at", ""))
            })
        return items

    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT discord_user_id, epic_username, linked_at FROM user_links") as cursor:
            rows = await cursor.fetchall()
            return [{"discord_user_id": r[0], "epic_username": r[1], "linked_at": str(r[2])} for r in rows]

