import discord
from typing import Dict, Any, List, Optional
from datetime import datetime
from config import (
    COLOR_DEFAULT, COLOR_SUCCESS, COLOR_ERROR, COLOR_FORTNITE,
    get_rarity_color
)

def format_number(val: Any) -> str:
    """Formats numeric values with commas or 2 decimal places."""
    if val is None:
        return "N/A"
    if isinstance(val, float):
        return f"{val:,.2f}"
    if isinstance(val, int):
        return f"{val:,}"
    return str(val)

def build_stats_embed(data: Dict[str, Any], time_window: str = "lifetime") -> discord.Embed:
    """Creates a rich embed for player statistics."""
    account = data.get("account", {})
    account_name = account.get("name", "Unknown Player")
    battle_pass = data.get("battlePass", {})
    bp_level = battle_pass.get("level", 0)

    stats_all = data.get("stats", {}).get("all", {})
    overall = stats_all.get("overall", {})

    wins = overall.get("wins", 0)
    kills = overall.get("kills", 0)
    kd = overall.get("kd", 0.0)
    win_rate = overall.get("winRate", 0.0)
    matches = overall.get("matches", 0)
    top3 = overall.get("top3", 0)
    top10 = overall.get("top10", 0)

    # Pick color based on KD or Win Rate
    if win_rate >= 20.0 or kd >= 4.0:
        color = 0xFFD700  # Gold
    elif win_rate >= 10.0 or kd >= 2.5:
        color = 0x9C27B0  # Purple
    else:
        color = COLOR_FORTNITE

    title = f"🏆 {account_name}'s Fortnite Stats ({time_window.capitalize()})"
    embed = discord.Embed(title=title, color=color, timestamp=datetime.utcnow())
    embed.set_footer(text="Fortnite-API.com • /stats", icon_url="https://fortnite-api.com/favicon.ico")

    # Battle pass & overview header
    desc = f"**Battle Pass Level:** `{bp_level}`\n"
    desc += f"**Total Matches:** `{format_number(matches)}`\n"
    embed.description = desc

    # Key stats in inline fields
    embed.add_field(name="👑 Victory Royales", value=f"**{format_number(wins)}**", inline=True)
    embed.add_field(name="🎯 K/D Ratio", value=f"**{format_number(kd)}**", inline=True)
    embed.add_field(name="📈 Win Rate", value=f"**{format_number(win_rate)}%**", inline=True)

    embed.add_field(name="⚔️ Total Kills", value=f"**{format_number(kills)}**", inline=True)
    embed.add_field(name="🥉 Top 3 Finishes", value=f"**{format_number(top3)}**", inline=True)
    embed.add_field(name="🏅 Top 10 Finishes", value=f"**{format_number(top10)}**", inline=True)

    # Mode breakdowns: Solo, Duo, Squad
    def format_mode_summary(mode_data: Optional[Dict[str, Any]]) -> str:
        if not mode_data or mode_data.get("matches", 0) == 0:
            return "No matches"
        m_wins = mode_data.get("wins", 0)
        m_kd = mode_data.get("kd", 0.0)
        m_wr = mode_data.get("winRate", 0.0)
        m_matches = mode_data.get("matches", 0)
        return f"Wins: **{m_wins}** ({m_wr:.1f}%) | K/D: **{m_kd:.2f}** | Matches: **{m_matches}**"

    solo = stats_all.get("solo")
    duo = stats_all.get("duo")
    squad = stats_all.get("squad")

    if solo or duo or squad:
        breakdown_text = ""
        if solo:
            breakdown_text += f"👤 **Solo**: {format_mode_summary(solo)}\n"
        if duo:
            breakdown_text += f"👥 **Duo**: {format_mode_summary(duo)}\n"
        if squad:
            breakdown_text += f"🛡️ **Squad**: {format_mode_summary(squad)}\n"
        embed.add_field(name="📊 Mode Breakdown", value=breakdown_text, inline=False)

    return embed

def build_shop_embeds(shop_data: Dict[str, Any]) -> List[discord.Embed]:
    """Builds clean embed(s) showcasing the current Fortnite Item Shop."""
    entries = shop_data.get("entries", [])
    shop_date = shop_data.get("date", "")
    vbuck_icon = shop_data.get("vbuckIcon", "https://fortnite-api.com/images/vbuck.png")

    try:
        dt = datetime.fromisoformat(shop_date.replace("Z", "+00:00"))
        formatted_date = dt.strftime("%B %d, %Y")
    except Exception:
        formatted_date = shop_date[:10] if len(shop_date) >= 10 else "Today"

    main_embed = discord.Embed(
        title=f"🛒 Fortnite Item Shop — {formatted_date}",
        description=f"Today's shop contains **{len(entries)}** items & bundles!\n*Resets daily at 00:00 UTC.*",
        color=COLOR_FORTNITE,
        timestamp=datetime.utcnow()
    )
    main_embed.set_thumbnail(url=vbuck_icon)
    main_embed.set_footer(text="Fortnite-API.com • Auto Shop Notification")

    # Group entries by category/layout if available
    categories: Dict[str, List[str]] = {}
    highlight_samples: List[str] = []

    for item in entries:
        regular_price = item.get("regularPrice", 0)
        final_price = item.get("finalPrice", regular_price)
        layout = item.get("layout", {})
        category_name = layout.get("category") if isinstance(layout, dict) else None
        if not category_name:
            category_name = "Featured & Daily"

        # Determine item display name
        br_items = item.get("brItems") or []
        if br_items and len(br_items) > 0:
            name = br_items[0].get("name", "Unknown Item")
            rarity = br_items[0].get("rarity", {}).get("displayValue", "")
        else:
            dev_name = item.get("devName", "Special Offer")
            name = dev_name.split("for")[0].strip() if "for" in dev_name else dev_name
            rarity = ""

        price_str = f"`{final_price:,}` 🪙"
        if final_price < regular_price:
            price_str = f"~~{regular_price:,}~~ `{final_price:,}` 🪙"

        entry_line = f"• **{name}** ({rarity}) — {price_str}" if rarity else f"• **{name}** — {price_str}"

        if category_name not in categories:
            categories[category_name] = []
        if len(categories[category_name]) < 6:
            categories[category_name].append(entry_line)

        if len(highlight_samples) < 8 and br_items:
            highlight_samples.append(f"• **{name}** — {price_str}")

    # Add top sections to main embed
    added_fields = 0
    for cat_name, items in categories.items():
        if added_fields >= 5:
            break
        text = "\n".join(items)
        if text:
            main_embed.add_field(name=f"✨ {cat_name}", value=text, inline=False)
            added_fields += 1

    return [main_embed]

def build_cosmetic_embed(cosmetic: Dict[str, Any]) -> discord.Embed:
    """Builds an embed for an individual cosmetic item."""
    name = cosmetic.get("name", "Unknown Cosmetic")
    description = cosmetic.get("description", "No description available.")
    ctype = cosmetic.get("type", {}).get("displayValue", "Item")
    rarity_data = cosmetic.get("rarity", {})
    rarity_name = rarity_data.get("displayValue", "Common")
    rarity_backend = rarity_data.get("value", "common")

    series_data = cosmetic.get("series")
    if series_data:
        rarity_name = f"{series_data.get('value', '')} Series"

    images = cosmetic.get("images", {})
    icon_url = images.get("icon") or images.get("featured") or images.get("smallIcon")

    color = get_rarity_color(series_data.get("backendValue") if series_data else rarity_backend)

    embed = discord.Embed(
        title=f"{name}",
        description=f"*{description}*",
        color=color,
        timestamp=datetime.utcnow()
    )

    if icon_url:
        embed.set_thumbnail(url=icon_url)

    embed.add_field(name="🏷️ Type", value=ctype, inline=True)
    embed.add_field(name="💎 Rarity", value=rarity_name, inline=True)

    set_info = cosmetic.get("set", {})
    if set_info and set_info.get("text"):
        embed.add_field(name="📦 Set", value=set_info.get("text"), inline=True)

    intro = cosmetic.get("introduction", {})
    if intro and intro.get("text"):
        embed.add_field(name="📅 Introduced", value=intro.get("text"), inline=True)

    # Check reactive or gameplay tags
    features = []
    if cosmetic.get("reactive"):
        features.append("⚡ Reactive")
    if cosmetic.get("builtInEmote"):
        features.append("💃 Built-in Emote")
    if cosmetic.get("copyrightedAudio"):
        features.append("🎵 Copyrighted Audio")

    if features:
        embed.add_field(name="✨ Features", value=", ".join(features), inline=True)

    embed.set_footer(text=f"ID: {cosmetic.get('id', 'N/A')} • /cosmetic")
    return embed

def build_map_embed(map_data: Dict[str, Any]) -> discord.Embed:
    """Builds an embed showing the current Battle Royale map with POIs."""
    images = map_data.get("images", {})
    map_url = images.get("pois") or images.get("blank") or "https://fortnite-api.com/images/map_en.png"
    pois = map_data.get("pois", [])

    embed = discord.Embed(
        title="🗺️ Fortnite Battle Royale Island Map",
        description=f"Current Island map with **{len(pois)}** active Named Locations & POIs.",
        color=COLOR_FORTNITE,
        timestamp=datetime.utcnow()
    )
    embed.set_image(url=map_url)
    embed.set_footer(text="Fortnite-API.com • /map")
    return embed

def build_drop_embed(poi_name: str, map_url: Optional[str] = None) -> discord.Embed:
    """Builds an embed for random landing spot roulette."""
    embed = discord.Embed(
        title="🎯 Squad Drop Chosen!",
        description=f"Lock in your jump coordinates:\n\n# 📍 **{poi_name}**\n\nDrop hot, gear up, and claim the Victory Royale!",
        color=0xFF7700,
        timestamp=datetime.utcnow()
    )
    if map_url:
        embed.set_thumbnail(url=map_url)
    embed.set_footer(text="Squad Landing Roulette • /drop")
    return embed

def build_news_embeds(news_data: Dict[str, Any]) -> List[discord.Embed]:
    """Builds embeds for Battle Royale news."""
    motds = news_data.get("motds", [])
    if not motds:
        return [discord.Embed(title="📰 Fortnite News", description="No current news entries found.", color=COLOR_FORTNITE)]

    embeds = []
    # Up to 4 top news items
    for item in motds[:4]:
        title = item.get("title") or item.get("tabTitle") or "Fortnite News"
        body = item.get("body", "")
        img = item.get("image") or item.get("tileImage")

        embed = discord.Embed(
            title=f"📰 {title}",
            description=body,
            color=COLOR_FORTNITE
        )
        if img:
            embed.set_image(url=img)
        embed.set_footer(text="Fortnite-API.com • In-Game News")
        embeds.append(embed)

    return embeds

def build_leaderboard_embed(
    guild_name: str,
    ranked_entries: List[Dict[str, Any]],
    metric: str = "wins"
) -> discord.Embed:
    """Builds server leaderboard comparing linked members."""
    metric_titles = {
        "wins": "Victory Royales 👑",
        "kd": "K/D Ratio 🎯",
        "winRate": "Win Rate % 📈",
        "kills": "Total Kills ⚔️",
        "matches": "Matches Played 🎮"
    }
    metric_label = metric_titles.get(metric, metric.capitalize())

    embed = discord.Embed(
        title=f"🏆 {guild_name} Fortnite Leaderboard",
        description=f"Ranked by **{metric_label}** among linked server members.\nLink your account with `/link <epic_name>` to join!\n",
        color=0xFFD700,
        timestamp=datetime.utcnow()
    )

    if not ranked_entries:
        embed.description += "\n*No server members have linked their Epic Games account yet! Type `/link <epic_name>` to get started.*"
        return embed

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    lines = []
    for idx, entry in enumerate(ranked_entries[:10]):
        rank_icon = medals[idx] if idx < len(medals) else f"`#{idx+1}`"
        user_mention = entry.get("mention", entry.get("discord_name", "Member"))
        epic_name = entry.get("epic_name", "Player")
        score = entry.get("score", 0)

        if metric in ["kd", "winRate"]:
            score_str = f"{score:.2f}"
            if metric == "winRate":
                score_str += "%"
        else:
            score_str = f"{int(score):,}"

        lines.append(f"{rank_icon} {user_mention} (`{epic_name}`) — **{score_str}**")

    embed.description += "\n".join(lines)
    embed.set_footer(text="Server Leaderboard • /leaderboard")
    return embed
