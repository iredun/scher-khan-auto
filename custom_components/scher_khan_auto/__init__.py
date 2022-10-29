"""
Custom integration to integrate Scher-khan Auto with Home Assistant.

For more details about this integration, please refer to
https://github.com/iredun/scher-khan-auto
"""
import asyncio
import logging
from datetime import timedelta
import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers import device_registry as dr


from .api import ScherKhanAutoApiClient
from .const import (
    CONF_CARS,
    CONF_TOKEN,
    DOMAIN,
    PLATFORMS,
    STARTUP_MESSAGE,
    WEBSOCKET_URL,
)
from .ws import ScherKhanAutoWebSocket, ScherKhanAutoWebSocketCoordinator


SCAN_INTERVAL = timedelta(minutes=60)
SCAN_INTERVAL_WEBSOCKET = timedelta(seconds=30)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {CONF_CARS: {}})
        _LOGGER.info(STARTUP_MESSAGE)

    token = entry.data.get(CONF_TOKEN)

    session = async_get_clientsession(hass)
    client = ScherKhanAutoApiClient(user_token=token, session=session)

    coordinator = ScherKhanAutoDataUpdateCoordinator(hass, client=client)
    websocket_coordinator = ScherKhanAutoWebSocketCoordinator(
        hass,
        logger=_LOGGER,
        name=DOMAIN,
    )
    websocket = ScherKhanAutoWebSocket(
        hass, token=client.user_token, coordinator=websocket_coordinator
    )

    await coordinator.async_refresh()

    asyncio.create_task(websocket.start_ws())

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator
    hass.data[DOMAIN][f"{entry.entry_id}_api"] = client
    hass.data[DOMAIN][f"{entry.entry_id}_websocket"] = websocket_coordinator

    device_registry = dr.async_get(hass)

    for car in coordinator.data.values():
        car_id = car.get("id")
        car_device = device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            identifiers={(DOMAIN, car_id)},
            name=car.get("name"),
            model=car.get("device").get("msisdn"),
        )
        hass.data[DOMAIN][CONF_CARS][car_id] = {
            "ha_device": car_device,
            "info": car,
        }

    for platform in PLATFORMS:
        if entry.options.get(platform, True):
            coordinator.platforms.append(platform)
            hass.async_add_job(
                hass.config_entries.async_forward_entry_setup(entry, platform)
            )

    entry.add_update_listener(async_reload_entry)
    return True


class ScherKhanAutoDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: ScherKhanAutoApiClient,
    ) -> None:
        """Initialize."""
        self.api = client
        self.platforms = []
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self):
        """Update data via library."""
        try:
            print("_async_update_data")
            result = await self.api.async_get_cars()
            return {car["id"]: car for car in result}
        except Exception as exception:
            raise UpdateFailed() from exception


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
