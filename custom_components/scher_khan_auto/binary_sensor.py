"""Binary sensor platform for Scher-khan Auto."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import (
    CONF_CARS,
    CAR_DOORS,
    BINARY_SENSOR_DEVICE_CLASS,
    DEFAULT_NAME,
    DOMAIN,
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    websocket_coordinator = hass.data[DOMAIN][f"{entry.entry_id}_websocket"]

    cars = hass.data[DOMAIN][CONF_CARS].keys()

    async_add_devices(
        [ScherKhanAutoInternetBinarySensor(coordinator, id) for id in cars]
    )

    async_add_devices(
        [
            ScherKhanAutoDoorsBinarySensor(websocket_coordinator, id, door, name)
            for id in cars
            for door, name in CAR_DOORS.items()
        ]
    )


class ScherKhanAutoInternetBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """scher_khan_auto binary_sensor class."""

    _attr_has_entity_name = True
    name = "Доступ в интернет"
    device_class = BINARY_SENSOR_DEVICE_CLASS

    def __init__(self, coordinator, car_id):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.car_id = car_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, car_id)},
        )
        self._attr_unique_id = f"{DEFAULT_NAME}_car_{self.car_id}_internet"

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return (
            self.coordinator.data.get(self.car_id)
            .get("device")
            .get("has_internet_connection")
        )


class ScherKhanAutoLockedBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """scher_khan_auto binary_sensor class."""

    _attr_has_entity_name = True
    name = "Состояние блокировки"
    device_class = "lock"

    def __init__(self, coordinator, car_id):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.car_id = car_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, car_id)},
        )
        self._attr_unique_id = f"{DEFAULT_NAME}_car_{self.car_id}_is_locked"

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return not self.coordinator.data.get(self.car_id, {}).get("is_locked")


class ScherKhanAutoDoorsBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """scher_khan_auto doors binary_sensor class."""

    _attr_has_entity_name = True
    device_class = "door"
    icon = "mdi:car-door"

    def __init__(self, coordinator, car_id, door, name):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.car_id = car_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, car_id)},
        )
        self._attr_name = name
        self.door = door
        self._attr_unique_id = f"{DEFAULT_NAME}_car_{self.car_id}_{self.door}"

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return self.coordinator.data.get(self.car_id, {}).get(self.door)
