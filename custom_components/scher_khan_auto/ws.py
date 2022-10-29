from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.core import HomeAssistant
from .const import WEBSOCKET_URL
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)
import aiohttp
import logging


class ScherKhanAutoWebSocketCoordinator(DataUpdateCoordinator):
    pass


class ScherKhanAutoWebSocket:
    """Class to manage fetching data from the WebSocket."""

    def __init__(
        self, hass: HomeAssistant, coordinator: any, token: str, logger: any = None
    ) -> None:
        """Initialize."""
        self.user_token = token
        self.coordinator = coordinator
        if logger is None:
            self.logger = logging.getLogger(__package__)
        else:
            self.logger = logger
        self.ws = async_get_clientsession(hass)
        self.last_state = {}

    async def start_ws(self):
        self.coordinator.async_set_updated_data({})
        async with self.ws.ws_connect(WEBSOCKET_URL) as ws:
            await ws.send_json({"type": "auth", "data": self.user_token})
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    result = msg.json()
                    if result["type"] == "state":
                        print(result)
                        self.coordinator.async_set_updated_data(
                            {result["car_id"]: result.get("data")}
                        )
