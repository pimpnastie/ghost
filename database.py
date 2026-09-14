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
            indexes = await _mongo_db.user_links.index_information()
            if "discord_user_id_1" in indexes and not indexes["discord_user_id_1"].get("sparse", False):
                await _mongo_db.user_links.drop_index("discord_user_id_1")
            await _mongo_db.user_links.create_index("discord_user_id", unique=True, sparse=True)
            await _mongo_db.user_links.create_index("epic_username_lower", unique=True)
            await _mongo_db.guild_settings.create_index("guild_id", unique=True)
            await _mongo_db.bot_state.create_index("key", unique=True)
            logger.info("MongoDB collections & indexes initialized.")
            return
        except Exception as e:
            logger.error(f"Error initializing MongoDB: {e}")

    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_links (
                discord_user_id INTEGER,
                epic_username TEXT NOT NULL COLLATE NOCASE,
                linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (epic_username)
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

async def track_player(epic_username: str, account_type: str = "epic", discord_user_id: Optional[int] = None) -> Dict[str, Any]:
    """Tracks a player in the persistent database with platform support."""
    clean_name = epic_username.strip()
    clean_acc = account_type.strip().lower() if account_type else "epic"
    lower_name = clean_name.lower()
    now = datetime.utcnow()

    if _mongo_db is not None:
        update_data: Dict[str, Any] = {
            "epic_username": clean_name,
            "epic_username_lower": lower_name,
            "account_type": clean_acc,
            "updated_at": now
        }
        if discord_user_id:
            update_data["discord_user_id"] = int(discord_user_id)
        await _mongo_db.user_links.update_one(
            {"epic_username_lower": lower_name},
            {"$set": update_data, "$setOnInsert": {"linked_at": now}},
            upsert=True
        )
        return {"epic_username": clean_name, "account_type": clean_acc, "discord_user_id": discord_user_id}

    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO user_links (discord_user_id, epic_username, linked_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(epic_username) DO UPDATE SET
                discord_user_id = COALESCE(excluded.discord_user_id, user_links.discord_user_id)
        """, (discord_user_id, clean_name))
        await db.commit()
        return {"epic_username": clean_name, "account_type": clean_acc, "discord_user_id": discord_user_id}

async def link_user(discord_id: int, epic_username: str):
    """Links or updates a Discord user's Epic Games username."""
    await track_player(epic_username, discord_user_id=discord_id)

async def untrack_player(identifier: Any) -> bool:
    """Removes a player by Epic username or Discord ID."""
    str_id = str(identifier).strip()
    if _mongo_db is not None:
        if str_id.isdigit():
            res = await _mongo_db.user_links.delete_one({
                "$or": [
                    {"discord_user_id": int(str_id)},
                    {"epic_username_lower": str_id.lower()}
                ]
            })
        else:
            res = await _mongo_db.user_links.delete_one({"epic_username_lower": str_id.lower()})
        return res.deleted_count > 0

    async with aiosqlite.connect(DATABASE_PATH) as db:
        if str_id.isdigit():
            cursor = await db.execute(
                "DELETE FROM user_links WHERE discord_user_id = ? OR epic_username = ?",
                (int(str_id), str_id)
            )
        else:
            cursor = await db.execute(
                "DELETE FROM user_links WHERE epic_username = ?",
                (str_id,)
            )
        await db.commit()
        return cursor.rowcount > 0

async def unlink_user(discord_id: int) -> bool:
    """Removes a Discord user's link. Returns True if a record was removed."""
    return await untrack_player(discord_id)

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

async def get_user_last_wins(discord_id: int) -> Optional[int]:
    """Gets cached win count for a linked user."""
    if _mongo_db is not None:
        doc = await _mongo_db.user_links.find_one({"discord_user_id": discord_id})
        return doc.get("last_wins") if doc else None

    # SQLite fallback: use bot_state
    raw = await get_bot_state(f"user_wins_{discord_id}")
    return int(raw) if raw is not None else None

async def set_user_last_wins(discord_id: int, wins: int):
    """Updates cached win count for a linked user."""
    if _mongo_db is not None:
        await _mongo_db.user_links.update_one(
            {"discord_user_id": discord_id},
            {"$set": {"last_wins": wins}},
            upsert=True
        )
        return

    # SQLite fallback
    await set_bot_state(f"user_wins_{discord_id}", str(wins))

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
    await save_guild_settings(guild_id, {"shop_channel_id": channel_id})

async def get_guild_shop_channel(guild_id: int) -> Optional[int]:
    """Gets the shop broadcast channel ID for a specific guild."""
    settings = await get_guild_settings(guild_id)
    return settings.get("shop_channel_id")

async def get_guild_settings(guild_id: int) -> Dict[str, Any]:
    """Retrieves routing settings for a specific guild."""
    defaults = {
        "shop_channel_id": None,
        "news_channel_id": None,
        "commands_channel_id": None,
        "auto_shop": True,
        "auto_news": False,
        "shop_format": "detailed"
    }
    if _mongo_db is not None:
        doc = await _mongo_db.guild_settings.find_one({"guild_id": guild_id})
        if doc:
            doc.pop("_id", None)
            defaults.update(doc)
        return defaults

    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT shop_channel_id FROM guild_settings WHERE guild_id = ?",
            (guild_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                defaults["shop_channel_id"] = row[0]
            return defaults

async def save_guild_settings(guild_id: int, settings: Dict[str, Any]):
    """Saves updated routing settings for a guild."""
    sanitized = {k: v for k, v in settings.items() if k != "_id"}
    sanitized["updated_at"] = datetime.utcnow()
    if _mongo_db is not None:
        await _mongo_db.guild_settings.update_one(
            {"guild_id": guild_id},
            {"$set": sanitized},
            upsert=True
        )
        return

    # SQLite fallback
    shop_id = sanitized.get("shop_channel_id")
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO guild_settings (guild_id, shop_channel_id, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(guild_id) DO UPDATE SET
                shop_channel_id = excluded.shop_channel_id,
                updated_at = CURRENT_TIMESTAMP
        """, (guild_id, shop_id))
        await db.commit()

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
                "account_type": doc.get("account_type", "epic"),
                "linked_at": str(doc.get("linked_at", ""))
            })
        return items

    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT discord_user_id, epic_username, linked_at FROM user_links") as cursor:
            rows = await cursor.fetchall()
            return [{"discord_user_id": r[0], "epic_username": r[1], "account_type": "epic", "linked_at": str(r[2])} for r in rows]

async def export_all_data() -> Dict[str, Any]:
    """Exports all database collections into a portable JSON-safe dictionary."""
    data: Dict[str, Any] = {
        "exported_at": datetime.utcnow().isoformat(),
        "user_links": [],
        "guild_settings": [],
        "bot_settings": {},
        "bot_state": {}
    }

    if _mongo_db is not None:
        async for doc in _mongo_db.user_links.find({}):
            doc.pop("_id", None)
            if "linked_at" in doc and isinstance(doc["linked_at"], datetime):
                doc["linked_at"] = doc["linked_at"].isoformat()
            if "updated_at" in doc and isinstance(doc["updated_at"], datetime):
                doc["updated_at"] = doc["updated_at"].isoformat()
            data["user_links"].append(doc)

        async for doc in _mongo_db.guild_settings.find({}):
            doc.pop("_id", None)
            if "updated_at" in doc and isinstance(doc["updated_at"], datetime):
                doc["updated_at"] = doc["updated_at"].isoformat()
            data["guild_settings"].append(doc)

        doc_cfg = await _mongo_db.bot_settings.find_one({"key": "global_config"})
        if doc_cfg:
            doc_cfg.pop("_id", None)
            doc_cfg.pop("key", None)
            data["bot_settings"] = doc_cfg
        else:
            data["bot_settings"] = DEFAULT_CONFIG.copy()

        async for doc in _mongo_db.bot_state.find({}):
            doc.pop("_id", None)
            k = doc.get("key")
            v = doc.get("value")
            if k:
                data["bot_state"][k] = v

        return data

    # SQLite fallback
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT discord_user_id, epic_username, linked_at FROM user_links") as cur:
            for r in await cur.fetchall():
                data["user_links"].append({
                    "discord_user_id": r[0],
                    "epic_username": r[1],
                    "linked_at": str(r[2])
                })
        async with db.execute("SELECT guild_id, shop_channel_id, updated_at FROM guild_settings") as cur:
            for r in await cur.fetchall():
                data["guild_settings"].append({
                    "guild_id": r[0],
                    "shop_channel_id": r[1],
                    "updated_at": str(r[2])
                })
        data["bot_settings"] = await get_global_config()
        async with db.execute("SELECT key, value FROM bot_state") as cur:
            for r in await cur.fetchall():
                data["bot_state"][r[0]] = r[1]

    return data

async def get_custom_pois() -> List[Dict[str, Any]]:
    """Fetches custom squad drop spots from database."""
    if _mongo_db is not None:
        cursor = _mongo_db.custom_pois.find({})
        items = []
        async for doc in cursor:
            items.append({
                "name": doc.get("name"),
                "note": doc.get("note", ""),
                "created_at": str(doc.get("created_at", ""))
            })
        return items

    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS custom_pois (
                name TEXT PRIMARY KEY,
                note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        async with db.execute("SELECT name, note, created_at FROM custom_pois") as cur:
            rows = await cur.fetchall()
            return [{"name": r[0], "note": r[1], "created_at": str(r[2])} for r in rows]

async def add_custom_poi(name: str, note: str = "") -> Dict[str, Any]:
    """Adds or updates a custom squad drop spot."""
    clean_name = name.strip()
    clean_note = note.strip()
    now = datetime.utcnow()
    if _mongo_db is not None:
        await _mongo_db.custom_pois.update_one(
            {"name": clean_name},
            {"$set": {"name": clean_name, "note": clean_note, "updated_at": now}, "$setOnInsert": {"created_at": now}},
            upsert=True
        )
        return {"name": clean_name, "note": clean_note}

    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS custom_pois (
                name TEXT PRIMARY KEY,
                note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            INSERT INTO custom_pois (name, note, created_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(name) DO UPDATE SET note = excluded.note
        """, (clean_name, clean_note))
        await db.commit()
        return {"name": clean_name, "note": clean_note}

async def delete_custom_poi(name: str) -> bool:
    """Removes a custom squad drop spot."""
    clean_name = name.strip()
    if _mongo_db is not None:
        res = await _mongo_db.custom_pois.delete_one({"name": clean_name})
        return res.deleted_count > 0

    async with aiosqlite.connect(DATABASE_PATH) as db:
        cur = await db.execute("DELETE FROM custom_pois WHERE name = ?", (clean_name,))
        await db.commit()
        return cur.rowcount > 0

