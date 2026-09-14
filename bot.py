import asyncio
from datetime import datetime, timezone, timedelta
import difflib
import json
import logging
import random
import re
import time
from typing import Optional, Literal, Dict, Any, List
from aiohttp import web
import discord
from discord import app_commands
from discord.ext import commands, tasks

from config import (
    DISCORD_BOT_TOKEN,
    PORT,
    COLOR_DEFAULT,
    COLOR_SUCCESS,
    COLOR_ERROR,
    COLOR_WARNING,
    COLOR_FORTNITE,
)
from database import (
    init_db,
    link_user,
    get_linked_user,
    unlink_user,
    get_linked_users_for_members,
    set_guild_shop_channel,
    get_guild_shop_channel,
    get_all_guild_shop_channels,
    get_guild_settings,
    save_guild_settings,
    get_bot_state,
    set_bot_state,
    get_user_last_wins,
    set_user_last_wins,
    get_global_config,
    save_global_config,
    get_all_linked_users_list,
    track_player,
    untrack_player,
    export_all_data,
    get_custom_pois,
    add_custom_poi,
    delete_custom_poi,
)
from dashboard_templates import get_dashboard_html
from fortnite_client import FortniteClient, FortniteAPIError
from embed_builder import (
    build_stats_embed,
    build_shop_embeds,
    build_cosmetic_embed,
    build_map_embed,
    build_drop_embed,
    build_news_embeds,
    build_leaderboard_embed,
)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("fortnite_bot")

class FortniteBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True  # Useful for server leaderboard member lists

        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )
        self.fortnite = FortniteClient()
        self._web_runner = None
        self._squad_stats_cache = {"timestamp": 0, "data": []}
        self._shop_cache = {"timestamp": 0, "data": None}
        self._map_cache = {"timestamp": 0, "data": None}
        self._link_codes: Dict[str, Dict[str, Any]] = {}

    def generate_link_code(self, epic_name: str, account_type: str = "epic") -> str:
        """Generates a unique 3-letter verification code using letters from 'MODA'."""
        chars = ["M", "O", "D", "A"]
        now = time.time()
        # Clean up codes older than 15 minutes (900 seconds)
        self._link_codes = {k: v for k, v in self._link_codes.items() if (now - v["time"] < 900) and not v.get("claimed")}

        # Try to generate an unused code
        code = "".join(random.choices(chars, k=3))
        for _ in range(50):
            if code not in self._link_codes:
                break
            code = "".join(random.choices(chars, k=3))

        self._link_codes[code] = {
            "code": code,
            "epic_name": epic_name,
            "account_type": account_type,
            "time": now,
            "claimed": False,
            "discord_id": None,
            "discord_tag": None
        }
        logger.info(f"Generated MODA link code: {code} for '{epic_name}'")
        return code

    async def claim_link_code(self, code: str, discord_user: discord.User | discord.Member) -> Optional[Dict[str, Any]]:
        """Validates and claims a 3-letter MODA verification code from Discord."""
        code_upper = code.strip().upper()
        now = time.time()
        entry = self._link_codes.get(code_upper)
        if not entry:
            return None
        if entry.get("claimed"):
            return None
        if now - entry["time"] > 900:
            return None

        epic_name = entry["epic_name"]
        acc_type = entry.get("account_type", "epic")
        await link_user(discord_user.id, epic_name)
        await track_player(epic_name, account_type=acc_type, discord_user_id=discord_user.id)
        entry["claimed"] = True
        entry["discord_id"] = discord_user.id
        entry["discord_tag"] = str(discord_user)

        # Invalidate squad cache to refresh immediately
        self._squad_stats_cache["timestamp"] = 0
        logger.info(f"MODA code {code_upper} claimed by {discord_user} for '{epic_name}'")
        return entry

    async def refresh_squad_telemetry(self) -> List[Dict[str, Any]]:
        """Concurrently fetches stats for all tracked squad members and updates persistent cache."""
        players = await get_all_linked_users_list()
        existing_map = {x.get("epic_name", "").lower(): x for x in self._squad_stats_cache.get("data", []) if not x.get("error")}
        sem = asyncio.Semaphore(2)

        async def fetch_one(p):
            ename = p.get("epic_username")
            did = p.get("discord_user_id")
            acc_type = p.get("account_type", "epic")
            discord_tag = None
            if did:
                u = self.get_user(int(did))
                discord_tag = str(u) if u else None

            async with sem:
                for attempt in range(3):
                    try:
                        stats = await self.fortnite.get_player_stats(name=ename, account_type=acc_type, time_window="lifetime")
                        bp = stats.get("battlePass", {}).get("level", 1)
                        all_stats = stats.get("stats", {}).get("all", {})
                        overall = all_stats.get("overall", {})
                        solo = all_stats.get("solo", {})
                        duo = all_stats.get("duo", {})
                        squad = all_stats.get("squad", {})
                        gamepad = stats.get("stats", {}).get("gamepad", {}).get("overall", {})
                        kbm = stats.get("stats", {}).get("keyboardMouse", {}).get("overall", {})
                        return {
                            "discord_id": did,
                            "discord_tag": discord_tag,
                            "epic_name": ename,
                            "account_type": acc_type,
                            "bp_level": bp,
                            "overall": {
                                "wins": overall.get("wins", 0),
                                "kills": overall.get("kills", 0),
                                "kd": overall.get("kd", 0.0),
                                "winRate": overall.get("winRate", 0.0),
                                "matches": overall.get("matches", 0),
                                "top3": overall.get("top3", 0),
                                "top5": overall.get("top5", 0),
                                "top6": overall.get("top6", 0),
                                "top10": overall.get("top10", 0),
                                "top12": overall.get("top12", 0),
                                "top25": overall.get("top25", 0),
                                "killsPerMatch": overall.get("killsPerMatch", 0.0),
                                "playersOutlived": overall.get("playersOutlived", 0),
                                "minutesPlayed": overall.get("minutesPlayed", 0),
                                "score": overall.get("score", 0),
                            },
                            "solo": solo,
                            "duo": duo,
                            "squad": squad,
                            "gamepad": {
                                "matches": gamepad.get("matches", 0),
                                "wins": gamepad.get("wins", 0),
                                "kills": gamepad.get("kills", 0),
                                "kd": gamepad.get("kd", 0.0)
                            },
                            "kbm": {
                                "matches": kbm.get("matches", 0),
                                "wins": kbm.get("wins", 0),
                                "kills": kbm.get("kills", 0),
                                "kd": kbm.get("kd", 0.0)
                            },
                            "has_controller": bool(gamepad.get("matches", 0) > 0 or acc_type in ["psn", "xbl"]),
                            "has_kbm": bool(kbm.get("matches", 0) > 0),
                            "is_private": False
                        }
                    except FortniteAPIError as fe:
                        if fe.status_code == 429 and attempt < 2:
                            await asyncio.sleep(1.5 * (attempt + 1))
                            continue
                        if existing_map.get(ename.lower()) and fe.status_code != 403:
                            logger.info(f"Preserving cached stats for {ename} due to rate limit/error: {fe}")
                            cached_res = existing_map[ename.lower()].copy()
                            cached_res["discord_id"] = did
                            cached_res["discord_tag"] = discord_tag
                            return cached_res
                        is_priv = fe.status_code == 403 or "private" in str(fe).lower()
                        return {
                            "discord_id": did,
                            "discord_tag": discord_tag,
                            "epic_name": ename,
                            "account_type": acc_type,
                            "error": str(fe),
                            "is_private": is_priv
                        }
                    except Exception as err:
                        if existing_map.get(ename.lower()):
                            logger.info(f"Preserving cached stats for {ename} due to exception: {err}")
                            cached_res = existing_map[ename.lower()].copy()
                            cached_res["discord_id"] = did
                            cached_res["discord_tag"] = discord_tag
                            return cached_res
                        is_priv = "private" in str(err).lower()
                        return {
                            "discord_id": did,
                            "discord_tag": discord_tag,
                            "epic_name": ename,
                            "account_type": acc_type,
                            "error": str(err),
                            "is_private": is_priv
                        }
                    finally:
                        await asyncio.sleep(0.3)

        results = await asyncio.gather(*[fetch_one(p) for p in players])
        now = time.time()
        edt = timezone(timedelta(hours=-4))
        last_up = datetime.now(edt).strftime("%I:%M %p EDT")
        cache_obj = {
            "timestamp": now,
            "last_updated_str": last_up,
            "data": results
        }
        self._squad_stats_cache = cache_obj
        try:
            await set_bot_state("squad_stats_cache", json.dumps(cache_obj))
        except Exception as e:
            logger.debug(f"Could not persist squad stats cache: {e}")
        return results

    async def setup_hook(self):
        logger.info("Initializing database...")
        await init_db()

        # Seed and synchronize active squad members
        try:
            await untrack_player("Going_Ghost")  # Remove accidental single-underscore account
            await track_player("KING_CONDOR_", account_type="epic")
            await track_player("Going__Ghost", account_type="psn")
            await track_player("p_lmpNastie", account_type="epic")
            await track_player("QuietCoyote_", account_type="epic")
            logger.info("Synchronized squad tracking: KING_CONDOR_, Going__Ghost (PSN), p_lmpNastie, QuietCoyote_")
        except Exception as e:
            logger.warning(f"Error seeding squad players: {e}")

        # Load and apply initial saved configuration
        initial_cfg = await get_global_config()

        # Restore squad stats cache from MongoDB if available
        try:
            cached_squad_str = await get_bot_state("squad_stats_cache")
            if cached_squad_str:
                self._squad_stats_cache = json.loads(cached_squad_str)
                logger.info("Restored squad stats cache from database state.")
        except Exception as e:
            logger.debug(f"Could not restore squad stats cache: {e}")

        # Start web dashboard and health-check control plane
        try:
            app = web.Application()

            async def index(request):
                return web.Response(text=get_dashboard_html(), content_type="text/html")

            async def health(request):
                return web.Response(text="Ghost Control Plane is Online! 🚀", content_type="text/plain")

            async def api_status(request):
                last_hash = await get_bot_state("last_shop_hash")
                return web.json_response({
                    "online": self.is_ready(),
                    "ping": round(self.latency * 1000) if self.latency else 0,
                    "guild_count": len(self.guilds),
                    "user": str(self.user) if self.user else "Ghost",
                    "last_shop_hash": last_hash or "N/A"
                })

            async def api_config_get(request):
                cfg = await get_global_config()
                return web.json_response(cfg)

            async def api_config_post(request):
                try:
                    data = await request.json()
                    await save_global_config(data)
                    await self.apply_config(data)
                    return web.json_response({"status": "success", "config": data})
                except Exception as e:
                    return web.json_response({"status": "error", "message": str(e)}, status=400)

            async def api_shop_broadcast(request):
                try:
                    posted = await self.broadcast_shop()
                    return web.json_response({"status": "success", "posted_to": posted})
                except Exception as e:
                    return web.json_response({"status": "error", "message": str(e)}, status=500)

            async def api_guilds_channels(request):
                guild_list = []
                for guild in self.guilds:
                    channels = [
                        {"id": str(ch.id), "name": ch.name}
                        for ch in guild.text_channels
                        if ch.permissions_for(guild.me).send_messages
                    ]
                    settings = await get_guild_settings(guild.id)
                    guild_list.append({
                        "id": str(guild.id),
                        "name": guild.name,
                        "channels": channels,
                        "settings": {
                            "shop_channel_id": str(settings.get("shop_channel_id") or ""),
                            "news_channel_id": str(settings.get("news_channel_id") or ""),
                            "commands_channel_id": str(settings.get("commands_channel_id") or ""),
                            "auto_shop": settings.get("auto_shop", True),
                            "auto_news": settings.get("auto_news", False),
                            "shop_format": settings.get("shop_format", "detailed")
                        }
                    })
                return web.json_response(guild_list)

            async def api_guild_settings_post(request):
                try:
                    data = await request.json()
                    guild_id = int(data.get("guild_id", 0))
                    if not guild_id:
                        return web.json_response({"status": "error", "message": "Missing guild_id"}, status=400)

                    shop_ch = int(data.get("shop_channel_id")) if data.get("shop_channel_id") else None
                    news_ch = int(data.get("news_channel_id")) if data.get("news_channel_id") else None
                    cmds_ch = int(data.get("commands_channel_id")) if data.get("commands_channel_id") else None

                    await save_guild_settings(guild_id, {
                        "shop_channel_id": shop_ch,
                        "news_channel_id": news_ch,
                        "commands_channel_id": cmds_ch,
                        "auto_shop": bool(data.get("auto_shop", True)),
                        "auto_news": bool(data.get("auto_news", False)),
                        "shop_format": data.get("shop_format", "detailed")
                    })
                    logger.info(f"Updated channel routing for guild {guild_id}")
                    return web.json_response({"status": "success"})
                except Exception as e:
                    return web.json_response({"status": "error", "message": str(e)}, status=400)

            async def api_news_broadcast(request):
                try:
                    posted = await self.broadcast_news()
                    return web.json_response({"status": "success", "posted_to": posted})
                except Exception as e:
                    return web.json_response({"status": "error", "message": str(e)}, status=500)

            async def api_squad_stats(request):
                force = request.query.get("refresh") == "1"
                now = time.time()
                # Return cached data if present and not forced
                if not force and self._squad_stats_cache.get("data"):
                    cached_data = self._squad_stats_cache["data"]
                    last_updated = self._squad_stats_cache.get("last_updated_str", "Active Cache")
                    return web.json_response({
                        "squad": cached_data,
                        "last_updated": last_updated,
                        "cached": True
                    })

                # Refresh live via parallel fetch
                results = await self.refresh_squad_telemetry()
                last_updated = self._squad_stats_cache.get("last_updated_str", "Just now")
                return web.json_response({
                    "squad": results,
                    "last_updated": last_updated,
                    "cached": False
                })

            async def api_live_shop(request):
                force = request.query.get("refresh") == "1"
                now = time.time()
                if not force and (now - self._shop_cache["timestamp"] < 3600) and self._shop_cache["data"]:
                    return web.json_response(self._shop_cache["data"])

                try:
                    shop_data = await self.fortnite.get_shop()
                    entries = shop_data.get("entries", [])
                    parsed_items = []
                    shop_date_str = str(shop_data.get("date", ""))[:10]

                    for e in entries:
                        br = e.get("brItems") or []
                        tracks = e.get("tracks") or []
                        cars = e.get("cars") or []
                        layout = e.get("layout") or {}
                        cat = layout.get("category") if isinstance(layout, dict) else None

                        name = ""
                        icon = ""
                        item_type = "Cosmetic"
                        rarity = "Common"

                        if br:
                            first = br[0]
                            name = first.get("name", "")
                            rarity = first.get("rarity", {}).get("displayValue", "Common")
                            imgs = first.get("images", {})
                            icon = imgs.get("icon") or imgs.get("featured") or imgs.get("smallIcon") or ""
                            item_type = first.get("type", {}).get("displayValue", "Cosmetic")
                        elif tracks:
                            first = tracks[0]
                            title = first.get("title", "Jam Track")
                            artist = first.get("artist", "")
                            name = f"{title} - {artist}".strip(" -")
                            icon = first.get("albumArt", "")
                            item_type = "Jam Track"
                            rarity = "Icon Series"
                        elif cars:
                            first = cars[0]
                            name = first.get("name", "Vehicle")
                            imgs = first.get("images", {})
                            icon = imgs.get("large") or imgs.get("small") or ""
                            item_type = "Vehicle"
                            rarity = "Rare"
                        else:
                            dev = e.get("devName", "")
                            if "tbd" in dev.lower() or "placeholder" in dev.lower():
                                continue
                            name = dev.replace("[VIRTUAL]1 x ", "").split(" for ")[0].strip()

                        # Filter out empty names or broken test placeholders
                        if not name or "tbd" in name.lower() or "placeholder" in name.lower():
                            continue

                        banner = e.get("banner") or {}
                        banner_val = str(banner.get("value", "")).strip() if isinstance(banner, dict) else ""
                        in_date = str(e.get("inDate", ""))[:10]
                        is_new = (banner_val.lower() == "new") or (in_date == shop_date_str)

                        rarity_clean = rarity.lower().replace(" ", "").replace("_", "")

                        parsed_items.append({
                            "name": name,
                            "price": e.get("finalPrice", 0),
                            "regularPrice": e.get("regularPrice", 0),
                            "rarity": rarity,
                            "rarity_clean": rarity_clean,
                            "icon": icon,
                            "item_type": item_type,
                            "category": cat or item_type,
                            "is_new": is_new,
                            "banner": banner_val
                        })

                    resp_data = {
                        "date": shop_data.get("date", ""),
                        "hash": shop_data.get("hash", ""),
                        "total": len(parsed_items),
                        "new_total": len([i for i in parsed_items if i.get("is_new")]),
                        "items": parsed_items
                    }
                    self._shop_cache = {"timestamp": now, "data": resp_data}
                    return web.json_response(resp_data)
                except Exception as e:
                    return web.json_response({"error": str(e)}, status=500)

            async def api_link_code_generate(request):
                try:
                    data = await request.json()
                    epic_name = str(data.get("epic_name", "")).strip()
                    acc_type = str(data.get("account_type", "epic")).strip().lower()
                    if not epic_name:
                        return web.json_response({"status": "error", "message": "Missing epic_name"}, status=400)
                    code = self.generate_link_code(epic_name, acc_type)
                    return web.json_response({
                        "status": "success",
                        "code": code,
                        "epic_name": epic_name,
                        "account_type": acc_type,
                        "expires_in_seconds": 900
                    })
                except Exception as e:
                    return web.json_response({"status": "error", "message": str(e)}, status=500)

            async def api_link_code_status(request):
                code = str(request.query.get("code", "")).strip().upper()
                entry = self._link_codes.get(code)
                if not entry:
                    return web.json_response({"status": "not_found", "claimed": False}, status=404)
                return web.json_response({
                    "status": "success",
                    "code": code,
                    "claimed": bool(entry.get("claimed")),
                    "discord_id": entry.get("discord_id"),
                    "discord_tag": entry.get("discord_tag"),
                    "epic_name": entry.get("epic_name")
                })

            async def api_live_map(request):
                try:
                    now = time.time()
                    if not self._map_cache["data"] or (now - self._map_cache["timestamp"] > 3600):
                        map_data = await self.fortnite.get_map()
                        self._map_cache = {"timestamp": now, "data": map_data}
                    else:
                        map_data = self._map_cache["data"]

                    custom_pois = await get_custom_pois()
                    return web.json_response({
                        "images": map_data.get("images", {}),
                        "pois": map_data.get("pois", []),
                        "custom_pois": custom_pois
                    })
                except Exception as e:
                    return web.json_response({"error": str(e)}, status=500)

            async def api_pois_custom_post(request):
                try:
                    data = await request.json()
                    name = str(data.get("name", "")).strip()
                    note = str(data.get("note", "")).strip()
                    if not name:
                        return web.json_response({"status": "error", "message": "Missing name"}, status=400)
                    saved = await add_custom_poi(name, note)
                    self._map_cache["timestamp"] = 0
                    return web.json_response({"status": "success", "poi": saved})
                except Exception as e:
                    return web.json_response({"status": "error", "message": str(e)}, status=500)

            async def api_pois_custom_delete(request):
                try:
                    data = await request.json()
                    name = str(data.get("name", "")).strip()
                    if not name:
                        return web.json_response({"status": "error", "message": "Missing name"}, status=400)
                    removed = await delete_custom_poi(name)
                    self._map_cache["timestamp"] = 0
                    return web.json_response({"status": "success", "removed": removed})
                except Exception as e:
                    return web.json_response({"status": "error", "message": str(e)}, status=500)

            async def api_drop_broadcast(request):
                try:
                    data = await request.json()
                    poi_name = str(data.get("poi_name", "Random Drop")).strip()
                    posted_count = 0
                    for guild in self.guilds:
                        ch = await self.get_or_detect_shop_channel(guild)
                        if ch and ch.permissions_for(guild.me).send_messages:
                            embed = build_drop_embed(poi_name)
                            await ch.send(embed=embed)
                            posted_count += 1
                    return web.json_response({"status": "success", "posted_to": posted_count, "poi": poi_name})
                except Exception as e:
                    return web.json_response({"status": "error", "message": str(e)}, status=500)

            async def api_live_news(request):
                try:
                    news_data = await self.fortnite.get_news()
                    return web.json_response(news_data)
                except Exception as e:
                    return web.json_response({"error": str(e)}, status=500)

            async def api_players_get(request):
                players = await get_all_linked_users_list()
                return web.json_response(players)

            async def api_players_track(request):
                try:
                    data = await request.json()
                    epic_name = str(data.get("epic_name", "")).strip()
                    req_plat = str(data.get("account_type", "auto")).strip().lower()
                    if not epic_name:
                        return web.json_response({"status": "error", "message": "Missing player name"}, status=400)

                    is_private = False
                    resolved_platform = req_plat if req_plat in ["epic", "psn", "xbl"] else None
                    names_to_try = [epic_name]
                    if " " in epic_name:
                        names_to_try.append(epic_name.replace(" ", "_"))
                        names_to_try.append(epic_name.replace(" ", "__"))

                    found_name = epic_name
                    for cand in names_to_try:
                        for plat in platforms_to_try:
                            try:
                                await self.fortnite.get_player_stats(name=cand, account_type=plat)
                                resolved_platform = plat
                                found_name = cand
                                found = True
                                is_private = False
                                break
                            except FortniteAPIError as fe:
                                if fe.status_code == 403:
                                    resolved_platform = plat
                                    found_name = cand
                                    found = True
                                    is_private = True
                                    break
                                elif fe.status_code == 404:
                                    continue
                                else:
                                    continue
                        if found:
                            break

                    if not found:
                        return web.json_response({
                            "status": "error",
                            "message": f"Player '{epic_name}' not found on Epic Games, PlayStation, or Xbox."
                        }, status=404)

                    await track_player(found_name, account_type=resolved_platform)
                    self._squad_stats_cache["timestamp"] = 0
                    logger.info(f"Tracked squad player: {found_name} on {resolved_platform} (private={is_private})")
                    return web.json_response({
                        "status": "success",
                        "epic_name": found_name,
                        "account_type": resolved_platform,
                        "is_private": is_private,
                        "message": f"Player added ({resolved_platform.upper()})!" if not is_private else f"Player added ({resolved_platform.upper()})! Note: stats are set to Private."
                    })
                except Exception as e:
                    return web.json_response({"status": "error", "message": str(e)}, status=500)

            async def api_players_untrack(request):
                try:
                    data = await request.json()
                    target = data.get("epic_name") or data.get("discord_id") or data.get("identifier")
                    if not target:
                        return web.json_response({"status": "error", "message": "Missing player identifier"}, status=400)
                    removed = await untrack_player(target)
                    self._squad_stats_cache["timestamp"] = 0
                    logger.info(f"Untracked player: {target} (removed={removed})")
                    return web.json_response({"status": "success", "removed": removed})
                except Exception as e:
                    return web.json_response({"status": "error", "message": str(e)}, status=500)

            async def api_players_unlink(request):
                data = await request.json()
                target = data.get("discord_id") or data.get("epic_name")
                if target:
                    await untrack_player(target)
                    self._squad_stats_cache["timestamp"] = 0
                return web.json_response({"status": "success"})

            async def api_backup_export(request):
                try:
                    backup_data = await export_all_data()
                    return web.json_response(
                        backup_data,
                        headers={"Content-Disposition": 'attachment; filename="ghost_squad_backup.json"'}
                    )
                except Exception as e:
                    return web.json_response({"status": "error", "message": str(e)}, status=500)

            app.router.add_get("/", index)
            app.router.add_get("/health", health)
            app.router.add_get("/api/status", api_status)
            app.router.add_get("/api/config", api_config_get)
            app.router.add_post("/api/config", api_config_post)
            app.router.add_post("/api/shop/broadcast", api_shop_broadcast)
            app.router.add_post("/api/news/broadcast", api_news_broadcast)
            app.router.add_get("/api/guilds-channels", api_guilds_channels)
            app.router.add_post("/api/guild-settings", api_guild_settings_post)
            app.router.add_get("/api/players", api_players_get)
            app.router.add_post("/api/players/track", api_players_track)
            app.router.add_post("/api/players/untrack", api_players_untrack)
            app.router.add_post("/api/players/unlink", api_players_unlink)
            app.router.add_get("/api/squad-stats", api_squad_stats)
            app.router.add_get("/api/live-shop", api_live_shop)
            app.router.add_get("/api/live-map", api_live_map)
            app.router.add_post("/api/pois/custom", api_pois_custom_post)
            app.router.add_post("/api/pois/custom/delete", api_pois_custom_delete)
            app.router.add_post("/api/drop/broadcast", api_drop_broadcast)
            app.router.add_get("/api/live-news", api_live_news)
            app.router.add_get("/api/backup/export", api_backup_export)
            app.router.add_post("/api/link-code/generate", api_link_code_generate)
            app.router.add_get("/api/link-code/status", api_link_code_status)

            self._web_runner = web.AppRunner(app)
            await self._web_runner.setup()
            site = web.TCPSite(self._web_runner, "0.0.0.0", PORT)
            await site.start()
            logger.info(f"Dashboard control plane online at port {PORT}")
        except Exception as e:
            logger.warning(f"Could not start dashboard web server: {e}")

        logger.info("Starting scheduled squad sync loop (7:00 PM & 10:00 PM EDT)...")
        self.scheduled_sync_loop.start()

        logger.info("Starting shop monitoring background task...")
        self.check_shop_loop.start()

        logger.info("Starting news monitoring background task...")
        self.check_news_loop.start()

        logger.info("Starting victory royale win monitoring task...")
        self.check_wins_loop.start()

        logger.info("Starting keep-alive background task...")
        self.keep_alive_loop.start()

        logger.info("Registering and syncing application slash commands...")
        try:
            synced = await self.tree.sync()
            logger.info(f"Successfully synced {len(synced)} slash commands globally.")
        except Exception as e:
            logger.error(f"Failed to sync slash commands: {e}")

    async def apply_config(self, cfg: dict):
        """Applies configuration updates live to the bot."""
        try:
            status_text = cfg.get("status_text", "Fortnite Item Shop & /help")
            act_type_str = cfg.get("activity_type", "watching").lower()
            act_map = {
                "playing": discord.ActivityType.playing,
                "watching": discord.ActivityType.watching,
                "listening": discord.ActivityType.listening,
                "competing": discord.ActivityType.competing,
            }
            act_type = act_map.get(act_type_str, discord.ActivityType.watching)

            pres_str = cfg.get("presence_status", "online").lower()
            pres_map = {
                "online": discord.Status.online,
                "idle": discord.Status.idle,
                "dnd": discord.Status.dnd
            }
            pres = pres_map.get(pres_str, discord.Status.online)

            activity = discord.Activity(type=act_type, name=status_text)
            await self.change_presence(status=pres, activity=activity)
            logger.info(f"Applied live presence: {act_type_str} '{status_text}' [{pres_str}]")
        except Exception as e:
            logger.error(f"Error applying config: {e}")

    async def broadcast_shop(self) -> int:
        """Broadcasts the current Item Shop to all target channels using active template."""
        shop_data = await self.fortnite.get_shop()
        embeds = build_shop_embeds(shop_data)
        cfg = await get_global_config()

        custom_msg = cfg.get("shop_message", "📢 **The Fortnite Item Shop has updated!**")
        role_ping = cfg.get("shop_role_ping", "none")
        role_id = cfg.get("shop_role_id", "").strip()

        prefix_text = custom_msg
        if role_ping == "everyone":
            prefix_text = f"@everyone {custom_msg}"
        elif role_ping == "here":
            prefix_text = f"@here {custom_msg}"
        elif role_ping == "role" and role_id:
            prefix_text = f"<@&{role_id}> {custom_msg}"

        count = 0
        for guild in self.guilds:
            try:
                channel = await self.get_or_detect_shop_channel(guild)
                if channel and channel.permissions_for(guild.me).send_messages:
                    await channel.send(content=prefix_text, embeds=embeds)
                    logger.info(f"Broadcasted shop to #{channel.name} in '{guild.name}'")
                    count += 1
            except Exception as e:
                logger.warning(f"Could not broadcast shop to guild '{guild.name}': {e}")
        return count

    async def broadcast_news(self) -> int:
        """Broadcasts the latest in-game Battle Royale news to designated news channels."""
        news_data = await self.fortnite.get_news()
        embeds = build_news_embeds(news_data)
        count = 0
        for guild in self.guilds:
            try:
                settings = await get_guild_settings(guild.id)
                ch_id = settings.get("news_channel_id")
                if ch_id:
                    channel = guild.get_channel(int(ch_id))
                    if channel and channel.permissions_for(guild.me).send_messages:
                        await channel.send(
                            content="📰 **Fortnite Battle Royale In-Game News Update!**",
                            embeds=embeds
                        )
                        logger.info(f"Broadcasted news to #{channel.name} in '{guild.name}'")
                        count += 1
            except Exception as e:
                logger.warning(f"Could not broadcast news to guild '{guild.name}': {e}")
        return count

    async def close(self):
        if self._web_runner:
            await self._web_runner.cleanup()
        self.keep_alive_loop.cancel()
        self.check_shop_loop.cancel()
        self.check_news_loop.cancel()
        self.check_wins_loop.cancel()
        self.scheduled_sync_loop.cancel()
        await self.fortnite.close()
        await super().close()

    @tasks.loop(minutes=1)
    async def scheduled_sync_loop(self):
        """Performs scheduled squad stats cache refresh at 7:00 PM and 10:00 PM EDT."""
        try:
            edt = timezone(timedelta(hours=-4))
            now_edt = datetime.now(edt)
            # Fire at 19:00 (7 PM) and 22:00 (10 PM) EDT at minute 0
            if now_edt.hour in (19, 22) and now_edt.minute == 0:
                logger.info(f"Triggering scheduled squad telemetry refresh at {now_edt.strftime('%I:%M %p EDT')}...")
                await self.refresh_squad_telemetry()
        except Exception as e:
            logger.error(f"Error in scheduled_sync_loop: {e}")

    @scheduled_sync_loop.before_loop
    async def before_scheduled_sync_loop(self):
        await self.wait_until_ready()

    @tasks.loop(minutes=15)
    async def check_news_loop(self):
        """Monitors in-game news and broadcasts when new announcements drop."""
        try:
            news_data = await self.fortnite.get_news()
            motds = news_data.get("motds", [])
            if not motds:
                return

            latest_id = motds[0].get("id")
            if not latest_id:
                return

            last_id = await get_bot_state("last_news_id")
            if last_id is None:
                await set_bot_state("last_news_id", latest_id)
                return

            if latest_id != last_id:
                logger.info(f"New Fortnite in-game news detected ({latest_id}). Broadcasting...")
                await set_bot_state("last_news_id", latest_id)
                await self.broadcast_news()
        except Exception as e:
            logger.error(f"Error in news monitoring loop: {e}")

    @check_news_loop.before_loop
    async def before_check_news_loop(self):
        await self.wait_until_ready()

    @tasks.loop(minutes=10)
    async def check_wins_loop(self):
        """Monitors linked squad members and announces new Victory Royales in Discord."""
        try:
            edt = timezone(timedelta(hours=-4))
            now_edt = datetime.now(edt)
            # Only poll during evening gaming window (6:00 PM - 1:00 AM EDT)
            if not (18 <= now_edt.hour <= 23 or now_edt.hour == 0):
                return

            players = await get_all_linked_users_list()
            for p in players:
                did = p.get("discord_user_id")
                epic_name = p.get("epic_username")
                if not did or not epic_name:
                    continue

                try:
                    stats = await self.fortnite.get_player_stats(name=epic_name, time_window="lifetime")
                    current_wins = stats.get("stats", {}).get("all", {}).get("overall", {}).get("wins", 0)
                    last_wins = await get_user_last_wins(did)

                    if last_wins is None:
                        await set_user_last_wins(did, current_wins)
                        continue

                    if current_wins > last_wins:
                        diff = current_wins - last_wins
                        await set_user_last_wins(did, current_wins)

                        embed = discord.Embed(
                            title="👑 SQUAD VICTORY ROYALE!",
                            description=(
                                f"🎉 **{epic_name}** (<@{did}>) just secured a Victory Royale in Fortnite!\n\n"
                                f"🏆 Total Wins: **{current_wins:,}** (+{diff})\n"
                                f"🎯 K/D: **{stats.get('stats', {}).get('all', {}).get('overall', {}).get('kd', 0.0):.2f}**"
                            ),
                            color=0xFFD700
                        )
                        embed.set_footer(text="Squad Victory Announcer • Ghost")

                        for guild in self.guilds:
                            member = guild.get_member(did)
                            if member:
                                ch = await self.get_or_detect_shop_channel(guild)
                                if ch and ch.permissions_for(guild.me).send_messages:
                                    await ch.send(embed=embed)
                                    logger.info(f"Announced win for {epic_name} in {guild.name}")
                except Exception as err:
                    logger.debug(f"Win check note for {epic_name}: {err}")
        except Exception as e:
            logger.error(f"Error in check_wins_loop: {e}")

    @check_wins_loop.before_loop
    async def before_check_wins_loop(self):
        await self.wait_until_ready()

    @tasks.loop(minutes=10)
    async def keep_alive_loop(self):
        """Self-pings the public web server to prevent free cloud hosts (like Render) from sleeping."""
        import os
        ping_url = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("PING_URL")
        if ping_url:
            try:
                session = await self.fortnite.get_session()
                async with session.get(ping_url) as resp:
                    logger.info(f"Self-ping keep-alive sent to {ping_url} (HTTP {resp.status})")
            except Exception as e:
                logger.debug(f"Self-ping note: {e}")

    @keep_alive_loop.before_loop
    async def before_keep_alive_loop(self):
        await self.wait_until_ready()

    @tasks.loop(minutes=5)
    async def check_shop_loop(self):
        """Monitors Item Shop resets and automatically posts to configured or auto-detected #fortnite channels."""
        try:
            cfg = await get_global_config()
            if not cfg.get("auto_shop_enabled", True):
                return

            shop_data = await self.fortnite.get_shop()
            current_hash = shop_data.get("hash")
            if not current_hash:
                return

            last_hash = await get_bot_state("last_shop_hash")

            # First run: record initial hash without spamming channels
            if last_hash is None:
                await set_bot_state("last_shop_hash", current_hash)
                logger.info(f"Initialized shop hash to {current_hash}")
                return

            # Check if new shop has rotated
            if current_hash != last_hash:
                logger.info(f"New Item Shop detected (old: {last_hash}, new: {current_hash}). Broadcasting...")
                await set_bot_state("last_shop_hash", current_hash)
                await self.broadcast_shop()
        except Exception as e:
            logger.error(f"Error in shop monitoring loop: {e}")

    @check_shop_loop.before_loop
    async def before_check_shop_loop(self):
        await self.wait_until_ready()

    async def get_or_detect_shop_channel(self, guild: discord.Guild) -> Optional[discord.TextChannel]:
        """Gets configured shop channel or auto-detects #fortnite / #item-shop."""
        # 1. Check database setting
        channel_id = await get_guild_shop_channel(guild.id)
        if channel_id:
            ch = guild.get_channel(channel_id)
            if ch and isinstance(ch, discord.TextChannel):
                return ch

        # 2. Auto-detect channel named #fortnite or variants
        for ch in guild.text_channels:
            name_clean = ch.name.lower().replace("-", "").replace("_", "")
            if name_clean in ["fortnite", "fortniteshop", "itemshop", "fnshop"]:
                # Automatically save it as the guild's shop channel
                await set_guild_shop_channel(guild.id, ch.id)
                logger.info(f"Auto-configured #{ch.name} for server '{guild.name}'")
                return ch

        return None

bot = FortniteBot()

@bot.event
async def on_ready():
    logger.info(f"Bot connected as {bot.user} (ID: {bot.user.id})")
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="Fortnite Item Shop & /help"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)

    # Check and log shop channels for connected guilds
    for guild in bot.guilds:
        target_ch = await bot.get_or_detect_shop_channel(guild)
        if target_ch:
            logger.info(f"Guild '{guild.name}': Shop updates targeted to #{target_ch.name}")
        else:
            logger.info(f"Guild '{guild.name}': No #fortnite channel found yet. Create #fortnite or use /setshopchannel")

@bot.event
async def on_guild_join(guild: discord.Guild):
    logger.info(f"Joined new guild: {guild.name} (ID: {guild.id})")
    await bot.get_or_detect_shop_channel(guild)


# ==============================================================================
# Helper functions
# ==============================================================================

def extract_mention_id(text: str) -> Optional[int]:
    """Extracts discord user ID from <@123456789> format or raw ID."""
    match = re.search(r"<@!?(\d+)>", text)
    if match:
        return int(match.group(1))
    if text.isdigit():
        return int(text)
    return None


# ==============================================================================
# Slash Commands
# ==============================================================================

@bot.tree.command(name="link", description="Link your Discord account to your Epic Games username or 3-digit website code")
@app_commands.describe(epic_username="Your exact Epic Games display name OR 3-digit code from website (e.g. MOD)")
async def link_cmd(interaction: discord.Interaction, epic_username: str):
    await interaction.response.defer(thinking=True)
    clean_val = epic_username.strip()

    # Check if this is a 3-letter MODA verification code from the website
    if len(clean_val) == 3 and all(c.upper() in "MODA" for c in clean_val):
        claim = await bot.claim_link_code(clean_val, interaction.user)
        if claim:
            target_epic = claim["epic_name"]
            acc_type = claim.get("account_type", "epic").upper()
            embed = discord.Embed(
                title="🔗 Website Profile Linked Successfully!",
                description=(
                    f"Verified 3-digit website code **`{clean_val.upper()}`**!\n\n"
                    f"Linked {interaction.user.mention} to Epic profile: **`{target_epic}`** ({acc_type})\n\n"
                    f"• Your online website profile is now permanently linked.\n"
                    f"• You can now use `/stats` without typing your name.\n"
                    f"• You will automatically appear on squad rankings and victory announcements!"
                ),
                color=COLOR_SUCCESS
            )
            await interaction.followup.send(embed=embed)
            return

    # Regular Epic Games username linking
    try:
        await bot.fortnite.get_player_stats(name=clean_val)
    except FortniteAPIError as e:
        if e.status_code == 404:
            pass

    await link_user(interaction.user.id, clean_val)
    await track_player(clean_val, account_type="epic", discord_user_id=interaction.user.id)

    embed = discord.Embed(
        title="🔗 Account Linked Successfully!",
        description=(
            f"Linked {interaction.user.mention} to Epic Games account: **`{clean_val}`**\n\n"
            f"• You can now use `/stats` without typing your name.\n"
            f"• You will automatically appear on server `/leaderboard` rankings!"
        ),
        color=COLOR_SUCCESS
    )
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="verify", description="Verify and link your Discord account using the 3-letter code from the website")
@app_commands.describe(code="The 3-letter code from the website (e.g. MOD)")
async def verify_cmd(interaction: discord.Interaction, code: str):
    await interaction.response.defer(thinking=True)
    clean_code = code.strip().upper()
    claim = await bot.claim_link_code(clean_code, interaction.user)
    if claim:
        target_epic = claim["epic_name"]
        acc_type = claim.get("account_type", "epic").upper()
        embed = discord.Embed(
            title="🔗 Website Profile Linked Successfully!",
            description=(
                f"Verified website code **`{clean_code}`**!\n\n"
                f"Linked {interaction.user.mention} to Epic profile: **`{target_epic}`** ({acc_type})\n\n"
                f"• Your online website profile is now permanently linked.\n"
                f"• You can now use `/stats` without typing your name.\n"
                f"• You will automatically appear on squad rankings and victory announcements!"
            ),
            color=COLOR_SUCCESS
        )
    else:
        embed = discord.Embed(
            title="❌ Invalid or Expired Code",
            description=(
                f"Code **`{clean_code}`** was not found or has expired (15-minute expiration).\n\n"
                f"Please open the website dashboard, click **Link Discord**, and generate a new 3-letter code."
            ),
            color=COLOR_ERROR
        )
    await interaction.followup.send(embed=embed)


@bot.command(name="link")
async def prefix_link(ctx: commands.Context, *, code_or_name: str):
    clean_val = code_or_name.strip()
    if len(clean_val) == 3 and all(c.upper() in "MODA" for c in clean_val):
        claim = await bot.claim_link_code(clean_val, ctx.author)
        if claim:
            target_epic = claim["epic_name"]
            acc_type = claim.get("account_type", "epic").upper()
            await ctx.reply(f"🔗 **Linked!** Verified code `{clean_val.upper()}`. Linked {ctx.author.mention} to **`{target_epic}`** ({acc_type})!")
            return
    await link_user(ctx.author.id, clean_val)
    await track_player(clean_val, account_type="epic", discord_user_id=ctx.author.id)
    await ctx.reply(f"🔗 **Linked!** Linked {ctx.author.mention} to Epic Games account: **`{clean_val}`**.")


@bot.command(name="verify")
async def prefix_verify(ctx: commands.Context, code: str):
    clean_code = code.strip().upper()
    claim = await bot.claim_link_code(clean_code, ctx.author)
    if claim:
        target_epic = claim["epic_name"]
        acc_type = claim.get("account_type", "epic").upper()
        await ctx.reply(f"🔗 **Linked!** Verified code `{clean_code}`. Linked {ctx.author.mention} to **`{target_epic}`** ({acc_type})!")
    else:
        await ctx.reply(f"❌ **Code `{clean_code}` is invalid or expired.** Generate a new 3-letter code on the website.")


@bot.tree.command(name="unlink", description="Unlink your Epic Games account from Discord")
async def unlink_cmd(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    removed = await unlink_user(interaction.user.id)
    if removed:
        embed = discord.Embed(
            title="🔓 Account Unlinked",
            description="Your Epic Games account has been disconnected from your Discord profile.",
            color=COLOR_DEFAULT
        )
    else:
        embed = discord.Embed(
            title="Notice",
            description="You don't have any Epic Games account linked yet.",
            color=COLOR_WARNING
        )
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="whois", description="Check which Epic Games account a member has linked")
@app_commands.describe(member="The Discord member to check (defaults to you)")
async def whois_cmd(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    await interaction.response.defer(thinking=True)
    target = member or interaction.user
    linked = await get_linked_user(target.id)

    if linked:
        embed = discord.Embed(
            title=f"👤 Player Info: {target.display_name}",
            description=f"{target.mention} is linked to Epic Games username: **`{linked}`**",
            color=COLOR_FORTNITE
        )
        embed.set_thumbnail(url=target.display_avatar.url)
    else:
        embed = discord.Embed(
            title=f"👤 Player Info: {target.display_name}",
            description=f"{target.mention} has not linked an Epic Games account yet. Use `/link <name>` to link.",
            color=COLOR_WARNING
        )
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="stats", description="View Fortnite Battle Royale stats for yourself, a friend, or any player")
@app_commands.describe(
    player="Epic username or @mention a Discord member (leave blank for your linked account)",
    time_window="Lifetime stats or current season stats"
)
@app_commands.choices(time_window=[
    app_commands.Choice(name="Lifetime", value="lifetime"),
    app_commands.Choice(name="Current Season", value="season")
])
async def stats_cmd(
    interaction: discord.Interaction,
    player: Optional[str] = None,
    time_window: Optional[app_commands.Choice[str]] = None
):
    await interaction.response.defer(thinking=True)
    window_val = time_window.value if time_window else "lifetime"

    target_epic_name: Optional[str] = None
    target_platform: str = "epic"

    if not player:
        # Check linked account for caller
        target_epic_name = await get_linked_user(interaction.user.id)
        if not target_epic_name:
            embed = discord.Embed(
                title="⚠️ No Epic Account Linked",
                description=(
                    "You haven't linked your Epic Games username yet!\n\n"
                    "• Run `/link <your_epic_name>` once to link your account.\n"
                    "• Or search directly: `/stats player:Ninja`"
                ),
                color=COLOR_WARNING
            )
            await interaction.followup.send(embed=embed)
            return
        squad_members = await get_all_linked_users_list()
        for m in squad_members:
            if str(m.get("discord_user_id")) == str(interaction.user.id):
                target_platform = m.get("account_type", "epic")
                break
    else:
        # Check if player is a mention or Discord ID
        mention_id = extract_mention_id(player)
        if mention_id:
            target_epic_name = await get_linked_user(mention_id)
            if not target_epic_name:
                embed = discord.Embed(
                    title="⚠️ Member Not Linked",
                    description=f"<@{mention_id}> has not linked an Epic account yet. They can run `/link <name>` to link.",
                    color=COLOR_WARNING
                )
                await interaction.followup.send(embed=embed)
                return
            squad_members = await get_all_linked_users_list()
            for m in squad_members:
                if str(m.get("discord_user_id")) == str(mention_id):
                    target_platform = m.get("account_type", "epic")
                    break
        else:
            raw_input = player.strip()
            squad_members = await get_all_linked_users_list()
            matched_squad_member = None

            # 1. Exact match (case-insensitive)
            for m in squad_members:
                if m.get("epic_username", "").lower() == raw_input.lower():
                    matched_squad_member = m
                    break

            # 2. Substring match
            if not matched_squad_member:
                for m in squad_members:
                    ename = m.get("epic_username", "")
                    if raw_input.lower() in ename.lower() or ename.lower() in raw_input.lower():
                        matched_squad_member = m
                        break

            # 3. Fuzzy match via difflib
            if not matched_squad_member and squad_members:
                names_map = {m.get("epic_username", "").lower(): m for m in squad_members}
                close = difflib.get_close_matches(raw_input.lower(), list(names_map.keys()), n=1, cutoff=0.55)
                if close:
                    matched_squad_member = names_map[close[0]]

            if matched_squad_member:
                target_epic_name = matched_squad_member.get("epic_username")
                target_platform = matched_squad_member.get("account_type", "epic")
            else:
                target_epic_name = raw_input
                target_platform = "epic"

    try:
        data = await bot.fortnite.get_player_stats(name=target_epic_name, account_type=target_platform, time_window=window_val)
        embed = build_stats_embed(data, time_window=window_val)
        await interaction.followup.send(embed=embed)
    except FortniteAPIError as e:
        embed = discord.Embed(title="❌ Stats Lookup Error", description=str(e), color=COLOR_ERROR)
        await interaction.followup.send(embed=embed)
    except Exception as e:
        logger.exception("Error in /stats")
        embed = discord.Embed(title="❌ Unexpected Error", description=f"Could not retrieve stats: {e}", color=COLOR_ERROR)
        await interaction.followup.send(embed=embed)


@bot.tree.command(name="shop", description="View today's Fortnite Item Shop")
async def shop_cmd(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    try:
        shop_data = await bot.fortnite.get_shop()
        embeds = build_shop_embeds(shop_data)
        await interaction.followup.send(embeds=embeds)
    except FortniteAPIError as e:
        embed = discord.Embed(title="❌ Item Shop Error", description=str(e), color=COLOR_ERROR)
        await interaction.followup.send(embed=embed)


@bot.tree.command(name="setshopchannel", description="Set the channel where new Item Shops will be automatically posted")
@app_commands.describe(channel="The channel for item shop announcements (defaults to current channel)")
@app_commands.checks.has_permissions(manage_channels=True)
async def set_shop_channel_cmd(
    interaction: discord.Interaction,
    channel: Optional[discord.TextChannel] = None
):
    await interaction.response.defer(thinking=True)
    if not interaction.guild_id:
        await interaction.followup.send("This command must be run inside a Discord server.")
        return

    target_channel = channel or interaction.channel
    await set_guild_shop_channel(interaction.guild_id, target_channel.id)

    embed = discord.Embed(
        title="📢 Shop Channel Configured!",
        description=(
            f"Daily Fortnite Item Shops will now be posted to {target_channel.mention}!\n\n"
            f"• The bot checks every 5 minutes and broadcasts as soon as Epic resets the shop (00:00 UTC).\n"
            f"• You can test posting immediately with `/postshop`."
        ),
        color=COLOR_SUCCESS
    )
    await interaction.followup.send(embed=embed)


@set_shop_channel_cmd.error
async def set_shop_channel_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        embed = discord.Embed(
            title="🚫 Permission Denied",
            description="You need the **Manage Channels** permission to configure the item shop channel.",
            color=COLOR_ERROR
        )
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="postshop", description="Manually post the current Item Shop to this channel")
async def post_shop_cmd(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    try:
        shop_data = await bot.fortnite.get_shop()
        embeds = build_shop_embeds(shop_data)
        await interaction.followup.send(
            content="🛒 **Here is the current Fortnite Item Shop:**",
            embeds=embeds
        )
    except Exception as e:
        embed = discord.Embed(title="❌ Error", description=f"Could not post shop: {e}", color=COLOR_ERROR)
        await interaction.followup.send(embed=embed)


@bot.tree.command(name="leaderboard", description="Compare stats for all linked members in this Discord server")
@app_commands.describe(metric="Metric to rank players by")
@app_commands.choices(metric=[
    app_commands.Choice(name="Wins (Victory Royales)", value="wins"),
    app_commands.Choice(name="K/D Ratio", value="kd"),
    app_commands.Choice(name="Win Rate %", value="winRate"),
    app_commands.Choice(name="Total Kills", value="kills"),
    app_commands.Choice(name="Matches Played", value="matches")
])
async def leaderboard_cmd(
    interaction: discord.Interaction,
    metric: Optional[app_commands.Choice[str]] = None
):
    await interaction.response.defer(thinking=True)
    if not interaction.guild:
        await interaction.followup.send("This command must be run inside a Discord server.")
        return

    chosen_metric = metric.value if metric else "wins"
    guild = interaction.guild

    # Get all members in the guild and find linked accounts
    member_ids = [m.id for m in guild.members if not m.bot]
    links = await get_linked_users_for_members(member_ids)

    if not links:
        embed = discord.Embed(
            title=f"🏆 {guild.name} Fortnite Leaderboard",
            description=(
                "No one on this server has linked an Epic Games account yet!\n\n"
                "Use `/link <your_epic_username>` to link your account and join the leaderboard."
            ),
            color=COLOR_WARNING
        )
        await interaction.followup.send(embed=embed)
        return

    # Fetch stats for each linked member
    entries = []

    async def fetch_member_score(d_id: int, epic_name: str):
        try:
            stats = await bot.fortnite.get_player_stats(name=epic_name, time_window="lifetime")
            overall = stats.get("stats", {}).get("all", {}).get("overall", {})
            score = overall.get(chosen_metric, 0)
            member_obj = guild.get_member(d_id)
            return {
                "discord_id": d_id,
                "mention": member_obj.mention if member_obj else f"<@{d_id}>",
                "discord_name": member_obj.display_name if member_obj else epic_name,
                "epic_name": epic_name,
                "score": score
            }
        except Exception:
            return None

    tasks_list = [fetch_member_score(did, ename) for did, ename in links.items()]
    results = await asyncio.gather(*tasks_list, return_exceptions=True)

    for res in results:
        if res and isinstance(res, dict):
            entries.append(res)

    entries.sort(key=lambda x: x["score"], reverse=True)

    embed = build_leaderboard_embed(
        guild_name=guild.name,
        ranked_entries=entries,
        metric=chosen_metric
    )
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="drop", description="Pick a random Point of Interest (POI) on the island to land")
async def drop_cmd(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    try:
        cfg = await get_global_config()
        custom_pois = cfg.get("custom_pois", [])

        map_data = await bot.fortnite.get_map()
        pois = map_data.get("pois", [])
        named_pois = [p.get("name") for p in pois if p.get("name")]

        all_candidates = named_pois + custom_pois

        if not all_candidates:
            poi_name = "Tilted Towers (Classic Fallback!)"
        else:
            poi_name = random.choice(all_candidates)

        images = map_data.get("images", {})
        map_icon = images.get("pois") or images.get("blank")

        embed = build_drop_embed(poi_name, map_icon)
        await interaction.followup.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="❌ Error", description=f"Could not select drop spot: {e}", color=COLOR_ERROR)
        await interaction.followup.send(embed=embed)


@bot.tree.command(name="cosmetic", description="Search for any Fortnite skin, emote, pickaxe, glider, or wrap")
@app_commands.describe(name="Name of the cosmetic item (e.g. Peely, Renegade Raider, Scenario)")
async def cosmetic_cmd(interaction: discord.Interaction, name: str):
    await interaction.response.defer(thinking=True)
    try:
        cosmetic_data = await bot.fortnite.search_cosmetic(name=name)
        embed = build_cosmetic_embed(cosmetic_data)
        await interaction.followup.send(embed=embed)
    except FortniteAPIError as e:
        embed = discord.Embed(title="🔍 Cosmetic Search", description=str(e), color=COLOR_WARNING)
        await interaction.followup.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="❌ Error", description=f"Could not search cosmetic: {e}", color=COLOR_ERROR)
        await interaction.followup.send(embed=embed)


@bot.tree.command(name="map", description="View the current Fortnite Battle Royale island map")
async def map_cmd(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    try:
        map_data = await bot.fortnite.get_map()
        embed = build_map_embed(map_data)
        await interaction.followup.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="❌ Error", description=f"Could not load map: {e}", color=COLOR_ERROR)
        await interaction.followup.send(embed=embed)


@bot.tree.command(name="news", description="View the latest in-game Battle Royale news and announcements")
async def news_cmd(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    try:
        news_data = await bot.fortnite.get_news()
        embeds = build_news_embeds(news_data)
        await interaction.followup.send(embeds=embeds)
    except Exception as e:
        embed = discord.Embed(title="❌ Error", description=f"Could not load news: {e}", color=COLOR_ERROR)
        await interaction.followup.send(embed=embed)


@bot.tree.command(name="season", description="View Fortnite Battle Royale season info, timeline, and countdown")
async def season_cmd(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    try:
        news_data = await bot.fortnite.get_news()
        motds = news_data.get("motds", [])
        banner = motds[0].get("image") if motds else None

        embed = discord.Embed(
            title="⏳ Fortnite Season Timeline & Info",
            description="Live Battle Royale season status and countdown details.",
            color=COLOR_FORTNITE
        )
        embed.add_field(name="🎮 Island", value="Active Season", inline=True)
        embed.add_field(name="⚡ Battle Pass", value="Active In-Game", inline=True)
        embed.add_field(name="🕒 Shop Reset", value="Daily at `00:00 UTC`", inline=True)

        if banner:
            embed.set_image(url=banner)
        embed.set_footer(text="Squad Season Tracker • /season")
        await interaction.followup.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="❌ Error", description=f"Could not load season data: {e}", color=COLOR_ERROR)
        await interaction.followup.send(embed=embed)


@bot.tree.command(name="creator", description="Check if a Support-A-Creator code is valid")
@app_commands.describe(code="Support-A-Creator code name")
async def creator_cmd(interaction: discord.Interaction, code: str):
    await interaction.response.defer(thinking=True)
    try:
        data = await bot.fortnite.get_creator_code(code=code)
        c_code = data.get("code", code)
        status = data.get("status", "ACTIVE")
        verified = data.get("verified", False)
        account = data.get("account", {})

        embed = discord.Embed(
            title=f"⭐ Creator Code: {c_code}",
            description=f"Status: **{status}** {'(Verified ✅)' if verified else ''}",
            color=COLOR_SUCCESS if status == "ACTIVE" else COLOR_WARNING
        )
        if account.get("name"):
            embed.add_field(name="Account Name", value=account.get("name"), inline=True)

        await interaction.followup.send(embed=embed)
    except FortniteAPIError as e:
        embed = discord.Embed(title="⭐ Creator Code", description=str(e), color=COLOR_WARNING)
        await interaction.followup.send(embed=embed)


@bot.tree.command(name="ping", description="Check the bot's connection latency")
async def ping_cmd(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Gateway Latency: **{latency}ms**",
        color=COLOR_SUCCESS
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="help", description="List all available Fortnite bot commands")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="⚡ Fortnite Discord Bot — Commands & Features",
        description="Here is everything you can do with the bot in this server:\n",
        color=COLOR_FORTNITE
    )

    embed.add_field(
        name="👤 Player Linking & Stats",
        value=(
            "`/link <epic_name>` — Link your Discord account to your Epic username\n"
            "`/unlink` — Disconnect your linked Epic account\n"
            "`/whois [member]` — See which Epic account a friend is linked to\n"
            "`/stats [player] [time_window]` — View Battle Royale stats, K/D, Wins, & Rank\n"
            "`/leaderboard [metric]` — Compare server members by Wins, K/D, or Kills"
        ),
        inline=False
    )

    embed.add_field(
        name="🛒 Item Shop & Drops",
        value=(
            "`/shop` — View today's live Item Shop\n"
            "`/setshopchannel [channel]` — Auto-post the new shop here daily (Admin)\n"
            "`/postshop` — Post the current shop to this channel right now\n"
            "`/drop` — Pick a random landing spot for your squad"
        ),
        inline=False
    )

    embed.add_field(
        name="🔍 Cosmetics & Info",
        value=(
            "`/cosmetic <name>` — Look up skins, emotes, pickaxes, and rarity\n"
            "`/map` — View the current Battle Royale island map\n"
            "`/news` — Read the latest in-game news\n"
            "`/creator <code>` — Check Support-A-Creator code status\n"
            "`/ping` — Check bot response latency"
        ),
        inline=False
    )

    embed.set_footer(text="Tip: Link your account once with /link to use /stats with zero arguments!")
    await interaction.response.send_message(embed=embed)


# ==============================================================================
# Main Runner Entrypoint
# ==============================================================================

def main():
    if not DISCORD_BOT_TOKEN:
        print("ERROR: DISCORD_BOT_TOKEN is missing from .env!")
        return
    logger.info("Starting Fortnite Discord Bot...")
    bot.run(DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    main()
