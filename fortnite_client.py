import aiohttp
import asyncio
import logging
import time
from typing import Optional, Dict, Any, List
from config import FORTNITE_API_BASE, FORTNITE_API_KEY

logger = logging.getLogger(__name__)

class FortniteAPIError(Exception):
    """Custom exception for Fortnite API errors with user-friendly messages."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code

class FortniteClient:
    def __init__(self, api_key: str = FORTNITE_API_KEY, base_url: str = FORTNITE_API_BASE):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._session: Optional[aiohttp.ClientSession] = None
        # In-memory TTL cache: key -> {"timestamp": float, "data": Any}
        self._cache: Dict[str, Dict[str, Any]] = {}

    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            headers = {}
            if self.api_key:
                headers["Authorization"] = self.api_key
            timeout = aiohttp.ClientTimeout(total=12)
            self._session = aiohttp.ClientSession(headers=headers, timeout=timeout)
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    def _make_cache_key(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        if not params:
            return endpoint
        sorted_params = sorted((k, str(v)) for k, v in params.items())
        param_str = "&".join(f"{k}={v}" for k, v in sorted_params)
        return f"{endpoint}?{param_str}"

    async def _get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        cache_ttl: Optional[int] = None,
        bypass_cache: bool = False
    ) -> Dict[str, Any]:
        cache_key = self._make_cache_key(endpoint, params)
        now = time.time()

        # 1. Return fresh cached copy if within TTL
        if not bypass_cache and cache_ttl is not None:
            cached_entry = self._cache.get(cache_key)
            if cached_entry and (now - cached_entry["timestamp"] < cache_ttl):
                return cached_entry["data"]

        session = await self.get_session()
        url = f"{self.base_url}{endpoint}"
        try:
            async with session.get(url, params=params) as resp:
                data = await resp.json(content_type=None)
                if resp.status == 200:
                    res_data = data.get("data", {})
                    # Store in cache
                    self._cache[cache_key] = {"timestamp": now, "data": res_data}
                    return res_data
                elif resp.status == 404:
                    err_msg = data.get("error", "Resource not found.") if isinstance(data, dict) else "Not found."
                    raise FortniteAPIError(f"Not found: {err_msg}", status_code=404)
                elif resp.status == 403:
                    err_msg = data.get("error", "") if isinstance(data, dict) else ""
                    if "not public" in err_msg.lower() or "private" in err_msg.lower():
                        raise FortniteAPIError("Account stats are Private. In Fortnite, go to Settings -> Account and Privacy -> turn on 'Show on Career Leaderboard'.", status_code=403)
                    raise FortniteAPIError(f"Access denied: {err_msg or 'Check your Fortnite API key.'}", status_code=403)
                elif resp.status == 429:
                    # Stale-if-error fallback on 429 rate limit
                    if cache_key in self._cache:
                        logger.warning(f"Fortnite API 429 hit. Serving stale cache for {cache_key}")
                        return self._cache[cache_key]["data"]
                    raise FortniteAPIError("Fortnite API rate limit reached. Please wait a moment.", status_code=429)
                else:
                    if cache_key in self._cache:
                        logger.warning(f"Fortnite API status {resp.status}. Serving stale cache for {cache_key}")
                        return self._cache[cache_key]["data"]
                    err_msg = data.get("error", f"API returned status {resp.status}") if isinstance(data, dict) else f"Error {resp.status}"
                    raise FortniteAPIError(f"Fortnite API error: {err_msg}", status_code=resp.status)
        except aiohttp.ClientConnectorError:
            if cache_key in self._cache:
                logger.warning(f"Connection error to Fortnite API. Serving stale cache for {cache_key}")
                return self._cache[cache_key]["data"]
            raise FortniteAPIError("Failed to connect to Fortnite API. Please check your network connection.")
        except TimeoutError:
            if cache_key in self._cache:
                logger.warning(f"Fortnite API timeout. Serving stale cache for {cache_key}")
                return self._cache[cache_key]["data"]
            raise FortniteAPIError("Request to Fortnite API timed out. Please try again.")

    async def get_player_stats(
        self,
        name: str,
        account_type: str = "epic",
        time_window: str = "lifetime",
        bypass_cache: bool = False
    ) -> Dict[str, Any]:
        """
        Fetches BR stats for a player name with 5-minute TTL caching.
        """
        params = {
            "name": name,
            "accountType": account_type,
            "timeWindow": time_window,
            "image": "all"
        }
        try:
            return await self._get("/v2/stats/br/v2", params=params, cache_ttl=300, bypass_cache=bypass_cache)
        except FortniteAPIError as e:
            if e.status_code == 404:
                raise FortniteAPIError(f"Player **{name}** was not found, or their account stats are set to Private in Fortnite settings.", status_code=404)
            raise

    async def get_shop(self, bypass_cache: bool = False) -> Dict[str, Any]:
        """Fetches the current live Item Shop with 10-minute TTL caching."""
        return await self._get("/v2/shop", cache_ttl=600, bypass_cache=bypass_cache)

    async def search_cosmetic(self, name: str, bypass_cache: bool = False) -> Dict[str, Any]:
        """Searches for a cosmetic (skin, emote, glider, pickaxe) by name with 24-hour TTL caching."""
        name = name.strip()
        try:
            return await self._get("/v2/cosmetics/br/search", params={"name": name, "matchMethod": "full"}, cache_ttl=86400, bypass_cache=bypass_cache)
        except FortniteAPIError as e:
            if e.status_code != 404:
                raise

        try:
            return await self._get("/v2/cosmetics/br/search", params={"name": name, "matchMethod": "contains"}, cache_ttl=86400, bypass_cache=bypass_cache)
        except FortniteAPIError as e:
            if e.status_code == 404:
                raise FortniteAPIError(f"No cosmetic found matching **{name}**.", status_code=404)
            raise

    async def get_map(self, bypass_cache: bool = False) -> Dict[str, Any]:
        """Fetches the current island map image and POIs with 1-hour TTL caching."""
        return await self._get("/v1/map", cache_ttl=3600, bypass_cache=bypass_cache)

    async def get_news(self, bypass_cache: bool = False) -> Dict[str, Any]:
        """Fetches latest Battle Royale in-game news with 15-minute TTL caching."""
        return await self._get("/v2/news/br", cache_ttl=900, bypass_cache=bypass_cache)

    async def get_creator_code(self, code: str, bypass_cache: bool = False) -> Dict[str, Any]:
        """Checks a Support-A-Creator code with 1-hour TTL caching."""
        params = {"name": code}
        try:
            return await self._get("/v2/creatorcode", params=params, cache_ttl=3600, bypass_cache=bypass_cache)
        except FortniteAPIError as e:
            if e.status_code == 404:
                raise FortniteAPIError(f"Creator code **{code}** is invalid or inactive.", status_code=404)
            raise

    async def get_all_cosmetics(self, bypass_cache: bool = False) -> List[Dict[str, Any]]:
        """Fetches all Battle Royale cosmetics with 24-hour TTL caching."""
        res = await self._get("/v2/cosmetics/br", cache_ttl=86400, bypass_cache=bypass_cache)
        return res if isinstance(res, list) else []

    async def search_cosmetics_catalog(
        self,
        query: str = "",
        cosmetic_type: str = "",
        limit: int = 60,
        bypass_cache: bool = False
    ) -> List[Dict[str, Any]]:
        """Fast in-memory catalog search across 16,000+ Fortnite cosmetics."""
        all_items = await self.get_all_cosmetics(bypass_cache=bypass_cache)
        clean_q = query.strip().lower()
        clean_type = cosmetic_type.strip().lower()

        if clean_type == "kicks":
            clean_type = "shoe"
        elif clean_type == "backbling":
            clean_type = "backpack"
        elif clean_type == "skin":
            clean_type = "outfit"

        results = []
        for item in all_items:
            # Type filter
            itype = ""
            if isinstance(item.get("type"), dict):
                itype = item["type"].get("value", "").lower()
            elif isinstance(item.get("type"), str):
                itype = item["type"].lower()

            if clean_type and clean_type != itype:
                continue

            # Query filter
            if clean_q:
                name = item.get("name", "").lower()
                set_text = ""
                if isinstance(item.get("set"), dict):
                    set_text = item["set"].get("text", "").lower()
                if clean_q not in name and clean_q not in set_text:
                    continue

            results.append(item)
            if len(results) >= limit:
                break

        return results
