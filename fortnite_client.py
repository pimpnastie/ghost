import aiohttp
from typing import Optional, Dict, Any, List
import logging
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

    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            headers = {}
            if self.api_key:
                headers["Authorization"] = self.api_key
            timeout = aiohttp.ClientTimeout(total=15)
            self._session = aiohttp.ClientSession(headers=headers, timeout=timeout)
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        session = await self.get_session()
        url = f"{self.base_url}{endpoint}"
        try:
            async with session.get(url, params=params) as resp:
                data = await resp.json(content_type=None)
                if resp.status == 200:
                    return data.get("data", {})
                elif resp.status == 404:
                    err_msg = data.get("error", "Resource not found.") if isinstance(data, dict) else "Not found."
                    raise FortniteAPIError(f"Not found: {err_msg}", status_code=404)
                elif resp.status == 403:
                    err_msg = data.get("error", "") if isinstance(data, dict) else ""
                    if "not public" in err_msg.lower() or "private" in err_msg.lower():
                        raise FortniteAPIError("Account stats are Private. In Fortnite, go to Settings -> Account and Privacy -> turn on 'Show on Career Leaderboard'.", status_code=403)
                    raise FortniteAPIError(f"Access denied: {err_msg or 'Check your Fortnite API key.'}", status_code=403)
                elif resp.status == 429:
                    raise FortniteAPIError("Fortnite API rate limit reached. Please wait a moment.", status_code=429)
                else:
                    err_msg = data.get("error", f"API returned status {resp.status}") if isinstance(data, dict) else f"Error {resp.status}"
                    raise FortniteAPIError(f"Fortnite API error: {err_msg}", status_code=resp.status)
        except aiohttp.ClientConnectorError:
            raise FortniteAPIError("Failed to connect to Fortnite API. Please check your network connection.")
        except TimeoutError:
            raise FortniteAPIError("Request to Fortnite API timed out. Please try again.")

    async def get_player_stats(self, name: str, account_type: str = "epic", time_window: str = "lifetime") -> Dict[str, Any]:
        """
        Fetches BR stats for a player name.
        time_window: 'lifetime' or 'season'
        account_type: 'epic', 'psn', 'xbl'
        """
        params = {
            "name": name,
            "accountType": account_type,
            "timeWindow": time_window,
            "image": "all"
        }
        try:
            return await self._get("/v2/stats/br/v2", params=params)
        except FortniteAPIError as e:
            if e.status_code == 404:
                raise FortniteAPIError(f"Player **{name}** was not found, or their account stats are set to Private in Fortnite settings.", status_code=404)
            raise

    async def get_shop(self) -> Dict[str, Any]:
        """Fetches the current live Item Shop."""
        return await self._get("/v2/shop")

    async def search_cosmetic(self, name: str) -> Dict[str, Any]:
        """Searches for a cosmetic (skin, emote, glider, pickaxe) by name.
        Tries exact full match first, then falls back to contains.
        """
        name = name.strip()
        # 1. Try exact match first
        try:
            return await self._get("/v2/cosmetics/br/search", params={"name": name, "matchMethod": "full"})
        except FortniteAPIError as e:
            if e.status_code != 404:
                raise

        # 2. Fall back to contains match
        try:
            return await self._get("/v2/cosmetics/br/search", params={"name": name, "matchMethod": "contains"})
        except FortniteAPIError as e:
            if e.status_code == 404:
                raise FortniteAPIError(f"No cosmetic found matching **{name}**.", status_code=404)
            raise

    async def get_map(self) -> Dict[str, Any]:
        """Fetches the current island map image and POIs."""
        return await self._get("/v1/map")

    async def get_news(self) -> Dict[str, Any]:
        """Fetches latest Battle Royale in-game news."""
        return await self._get("/v2/news/br")

    async def get_creator_code(self, code: str) -> Dict[str, Any]:
        """Checks a Support-A-Creator code."""
        params = {"name": code}
        try:
            return await self._get("/v2/creatorcode", params=params)
        except FortniteAPIError as e:
            if e.status_code == 404:
                raise FortniteAPIError(f"Creator code **{code}** is invalid or inactive.", status_code=404)
            raise
