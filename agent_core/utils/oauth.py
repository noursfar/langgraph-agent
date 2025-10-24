# agent_core/utils/oauth.py
from datetime import datetime, timedelta
from typing import Optional

import httpx
from agent_core.config.settings import settings
from agent_core.utils.logger import log
from agent_core.utils.exceptions import AuthenticationError


class OAuthManager:
    """Manages OAuth2 authentication with token caching."""

    def __init__(self):
        self.access_token: Optional[str] = None
        self.token_expiry: Optional[datetime] = None

    def is_token_valid(self):
        """Check if the cached token is still valid."""
        if not self.access_token or not self.token_expiry:
            return False
        return datetime.now() < self.token_expiry

    async def get_access_token(self):
        """Return a valid access token, fetching a new one if needed."""
        if self.is_token_valid():
            log.debug("Using cached OAuth token")
            return self.access_token  # type: ignore

        log.info("Requesting new OAuth token")
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    settings.nearcare_oauth_url,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    data={
                        "client_id": settings.CLIENT_ID,
                        "client_secret": settings.CLIENT_SECRET,
                        "grant_type": "client_credentials",
                    },
                )
                response.raise_for_status()

                token_data = response.json()
                self.access_token = token_data["access_token"]

                # Cache expiry with buffer
                expires_in = token_data.get("expires_in", 3600)
                buffer = getattr(settings, "token_cache_buffer_seconds", 60)
                self.token_expiry = datetime.now() + timedelta(seconds=expires_in - buffer)

                log.info(
                    f"OAuth token obtained, expires in {expires_in}s "
                    f"(cache until {self.token_expiry.strftime('%H:%M:%S')})"
                )
                return self.access_token

        except (httpx.HTTPStatusError, httpx.RequestError, KeyError) as e:
            msg = f"OAuth error: {str(e)}"
            log.error(msg)
            raise AuthenticationError(msg) from e


# Single instance to use across the app
oauth_manager = OAuthManager()
