"""Switch platform for Scher-khan Auto."""
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN, DEFAULT_NAME, CONF_CARS


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    websocket_coordinator = hass.data[DOMAIN][f"{entry.entry_id}_websocket"]

    cars = hass.data[DOMAIN][CONF_CARS].keys()
    api = hass.data[DOMAIN][f"{entry.entry_id}_api"]

    async_add_devices(
        [ScherKhanAutoAlarmSwitch(websocket_coordinator, id, api) for id in cars]
    )


class ScherKhanAutoAlarmSwitch(CoordinatorEntity, SwitchEntity):
    """scher_khan_auto switch class."""

    _attr_has_entity_name = True
    name = "Блокировка"
    device_class = "switch"

    def __init__(self, coordinator, car_id, api):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.car_id = car_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, car_id)},
        )
        self.api = api
        self._attr_unique_id = f"{DEFAULT_NAME}_car_{self.car_id}_is_locked"

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        await self.api.async_send_car_command(car_id=self.car_id, command="arm")

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        await self.api.async_send_car_command(car_id=self.car_id, command="disarm")

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return self.coordinator.data.get(self.car_id, {}).get("is_locked")
