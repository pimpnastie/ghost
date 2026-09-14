import asyncio
import os
import sys

from config import DISCORD_BOT_TOKEN, FORTNITE_API_KEY
from database import (
    init_db, link_user, get_linked_user, unlink_user,
    set_guild_shop_channel, get_guild_shop_channel,
    set_bot_state, get_bot_state, get_linked_users_for_members
)
from fortnite_client import FortniteClient
from embed_builder import (
    build_stats_embed, build_shop_embeds,
    build_cosmetic_embed, build_map_embed,
    build_drop_embed, build_news_embeds,
    build_leaderboard_embed
)

async def test_database():
    print("Testing Database...")
    await init_db()
    # Test link
    await link_user(123456789, "Ninja")
    linked = await get_linked_user(123456789)
    assert linked == "Ninja", f"Expected Ninja, got {linked}"

    # Test member lookup
    members_map = await get_linked_users_for_members([123456789, 999999999])
    assert members_map.get(123456789) == "Ninja"

    # Test guild channel
    await set_guild_shop_channel(111222, 333444)
    chan = await get_guild_shop_channel(111222)
    assert chan == 333444, f"Expected 333444, got {chan}"

    # Test bot state
    await set_bot_state("test_key", "test_value")
    val = await get_bot_state("test_key")
    assert val == "test_value"

    # Test squad tracking and export
    from database import track_player, untrack_player, export_all_data, get_all_linked_users_list
    await track_player("KING_CONDOR_")
    await track_player("p_lmpNastie")
    users = await get_all_linked_users_list()
    usernames = [u["epic_username"].lower() for u in users]
    assert "king_condor_" in usernames, "KING_CONDOR_ not found in user list"
    assert "p_lmpnastie" in usernames, "p_lmpNastie not found in user list"

    exported = await export_all_data()
    assert "user_links" in exported
    assert len(exported["user_links"]) >= 2
    print("  -> Squad tracking & JSON export PASSED!")

    # Test unlink
    await unlink_user(123456789)
    linked_after = await get_linked_user(123456789)
    assert linked_after is None
    print("  -> Database checks PASSED!")

async def test_fortnite_client():
    print("Testing Fortnite API Client...")
    client = FortniteClient()
    try:
        # 1. Stats
        print("  - Fetching Ninja stats...")
        stats = await client.get_player_stats("Ninja")
        assert "account" in stats
        embed_stats = build_stats_embed(stats)
        assert embed_stats.title is not None
        print("    -> Stats & Embed OK!")

        # 1b. Squad Players: KING_CONDOR_ and p_lmpNastie
        print("  - Fetching KING_CONDOR_ stats...")
        kc_stats = await client.get_player_stats("KING_CONDOR_")
        assert kc_stats.get("account", {}).get("name") == "KING_CONDOR_"
        print(f"    -> KING_CONDOR_ OK! Level: {kc_stats.get('battlePass', {}).get('level')}, Wins: {kc_stats.get('stats', {}).get('all', {}).get('overall', {}).get('wins')}")

        print("  - Fetching p_lmpNastie stats (now public)...")
        p_stats = await client.get_player_stats("p_lmpNastie")
        assert p_stats.get("account", {}).get("name") == "p_lmpNastie"
        print(f"    -> p_lmpNastie OK! Level: {p_stats.get('battlePass', {}).get('level')}, Wins: {p_stats.get('stats', {}).get('all', {}).get('overall', {}).get('wins')}")

        # 1c. Going__Ghost on PSN
        print("  - Fetching Going__Ghost on PSN...")
        gg_stats = await client.get_player_stats("Going__Ghost", account_type="psn")
        assert gg_stats.get("account", {}).get("name") == "Going__Ghost"
        print(f"    -> Going__Ghost (PSN) OK! Level: {gg_stats.get('battlePass', {}).get('level')}, Wins: {gg_stats.get('stats', {}).get('all', {}).get('overall', {}).get('wins')}")

        # 1d. QuietCoyote_ private check
        print("  - Testing QuietCoyote_ privacy status...")
        try:
            await client.get_player_stats("QuietCoyote_")
            print("    -> QuietCoyote_ public")
        except Exception as qe:
            assert "private" in str(qe).lower()
            print(f"    -> QuietCoyote_ privacy notice OK: {qe}")

        # 2. Shop
        print("  - Fetching live Item Shop...")
        shop = await client.get_shop()
        assert "entries" in shop
        shop_embeds = build_shop_embeds(shop)
        assert len(shop_embeds) > 0
        print(f"    -> Shop & Embed OK! ({len(shop.get('entries', []))} items)")

        # 3. Cosmetic search
        print("  - Searching cosmetic 'Peely'...")
        peely = await client.search_cosmetic("Peely")
        assert peely.get("name") == "Peely"
        peely_embed = build_cosmetic_embed(peely)
        assert peely_embed.title == "Peely"
        print("    -> Cosmetic search & Embed OK!")

        # 4. Map & Drop
        print("  - Fetching Map & POIs...")
        map_data = await client.get_map()
        pois = map_data.get("pois", [])
        assert len(pois) > 0
        map_embed = build_map_embed(map_data)
        assert map_embed.image.url is not None
        drop_embed = build_drop_embed(pois[0].get("name", "Test Spot"))
        assert drop_embed.title is not None
        print(f"    -> Map & Drop OK! ({len(pois)} POIs)")

        # 5. News
        print("  - Fetching News...")
        news = await client.get_news()
        news_embeds = build_news_embeds(news)
        assert len(news_embeds) > 0
        print(f"    -> News OK! ({len(news_embeds)} embeds)")

        # 6. Leaderboard embed
        leaderboard_sample = [
            {"discord_id": 1, "mention": "<@1>", "epic_name": "Ninja", "score": 11456},
            {"discord_id": 2, "mention": "<@2>", "epic_name": "TFue", "score": 8500}
        ]
        lb_embed = build_leaderboard_embed("Test Guild", leaderboard_sample, "wins")
        assert lb_embed.title is not None
        print("    -> Leaderboard Embed OK!")

    finally:
        await client.close()

async def main():
    print(f"Checking credentials:")
    print(f"  Discord Token set: {'YES' if DISCORD_BOT_TOKEN else 'NO'}")
    print(f"  Fortnite API Key set: {'YES' if FORTNITE_API_KEY else 'NO'}")
    await test_database()
    await test_fortnite_client()
    print("\nALL AUTOMATED TESTS PASSED!")

if __name__ == "__main__":
    asyncio.run(main())
