import asyncio
import logging
import random
import re
from typing import Optional, Literal
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
    get_bot_state,
    set_bot_state,
)
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

    async def setup_hook(self):
        logger.info("Initializing database...")
        await init_db()

        # Start web server for cloud host health checks (Render, Koyeb, etc.)
        try:
            app = web.Application()
            async def health_check(request):
                return web.Response(text="Fortnite Discord Bot is Online! 🚀", content_type="text/plain")
            app.router.add_get("/", health_check)
            app.router.add_get("/health", health_check)
            self._web_runner = web.AppRunner(app)
            await self._web_runner.setup()
            site = web.TCPSite(self._web_runner, "0.0.0.0", PORT)
            await site.start()
            logger.info(f"Health-check web server started on port {PORT}")
        except Exception as e:
            logger.warning(f"Could not start health-check web server: {e}")

        logger.info("Starting shop monitoring background task...")
        self.check_shop_loop.start()

        logger.info("Starting keep-alive background task...")
        self.keep_alive_loop.start()

        logger.info("Registering and syncing application slash commands...")
        try:
            synced = await self.tree.sync()
            logger.info(f"Successfully synced {len(synced)} slash commands globally.")
        except Exception as e:
            logger.error(f"Failed to sync slash commands: {e}")

    async def close(self):
        if self._web_runner:
            await self._web_runner.cleanup()
        self.keep_alive_loop.cancel()
        self.check_shop_loop.cancel()
        await self.fortnite.close()
        await super().close()

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

                embeds = build_shop_embeds(shop_data)

                # Broadcast to every guild the bot is in
                for guild in self.guilds:
                    try:
                        channel = await self.get_or_detect_shop_channel(guild)
                        if channel and channel.permissions_for(guild.me).send_messages:
                            await channel.send(
                                content="📢 **The Fortnite Item Shop has updated!**",
                                embeds=embeds
                            )
                            logger.info(f"Posted daily shop to #{channel.name} in {guild.name}")
                    except Exception as err:
                        logger.warning(f"Could not post shop in guild {guild.name}: {err}")
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

@bot.tree.command(name="link", description="Link your Discord account to your Epic Games username")
@app_commands.describe(epic_username="Your exact Epic Games display name")
async def link_cmd(interaction: discord.Interaction, epic_username: str):
    await interaction.response.defer(thinking=True)
    epic_username = epic_username.strip()

    # Verify if the username exists
    try:
        await bot.fortnite.get_player_stats(name=epic_username)
    except FortniteAPIError as e:
        if e.status_code == 404:
            # Note: Sometimes stats are private, but user still wants to link
            pass

    await link_user(interaction.user.id, epic_username)

    embed = discord.Embed(
        title="🔗 Account Linked Successfully!",
        description=(
            f"Linked {interaction.user.mention} to Epic Games account: **`{epic_username}`**\n\n"
            f"• You can now use `/stats` without typing your name.\n"
            f"• You will automatically appear on server `/leaderboard` rankings!"
        ),
        color=COLOR_SUCCESS
    )
    await interaction.followup.send(embed=embed)


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
        else:
            target_epic_name = player.strip()

    try:
        data = await bot.fortnite.get_player_stats(name=target_epic_name, time_window=window_val)
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
        map_data = await bot.fortnite.get_map()
        pois = map_data.get("pois", [])
        named_pois = [p for p in pois if p.get("name")]

        if not named_pois:
            poi_name = "Tilted Towers (Classic Fallback!)"
        else:
            selected = random.choice(named_pois)
            poi_name = selected.get("name", "Unknown Drop Zone")

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
