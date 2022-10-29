"""Sensor platform for Scher-khan Auto."""
from .const import DEFAULT_NAME
from .const import DOMAIN
from .const import CONF_CARS
from .const import SENSOR
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    websocket_coordinator = hass.data[DOMAIN][f"{entry.entry_id}_websocket"]

    cars = hass.data[DOMAIN][CONF_CARS].keys()

    classes = [
        ScherKhanAutoTempSensor,
        ScherKhanAutoSimBalanceSensor,
        ScherKhanAutoOdometerSensor,
        ScherKhanAutoVoltageSensor,
    ]

    async_add_devices(
        [cls(websocket_coordinator, id) for id in cars for cls in classes]
    )


class ScherKhanAutoTempSensor(CoordinatorEntity, SensorEntity):
    """scher_khan_auto temp class."""

    _attr_has_entity_name = True
    native_unit_of_measurement = "°C"
    device_class = "temperature"
    name = "Температура салона"

    def __init__(self, coordinator, car_id):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.car_id = car_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, car_id)},
        )
        self._attr_unique_id = f"{DEFAULT_NAME}_car_{self.car_id}_{SENSOR}_temperature"

    @property
    def native_value(self):
        """Return de device class of the sensor."""
        return self.coordinator.data.get(self.car_id, {}).get("temperature", 0)


class ScherKhanAutoSimBalanceSensor(CoordinatorEntity, SensorEntity):
    """scher_khan_auto temp class."""

    _attr_has_entity_name = True
    device_class = "monetary"
    name = "Баланс SIM"

    def __init__(self, coordinator, car_id):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.car_id = car_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, car_id)},
        )
        self._attr_unique_id = f"{DEFAULT_NAME}_car_{self.car_id}_{SENSOR}_sim_balance"

    @property
    def native_value(self):
        """Return de device class of the sensor."""
        balance = self.coordinator.data.get(self.car_id, {}).get("sim_balance", 0)
        currency = self.coordinator.data.get(self.car_id, {}).get("sim_currency", "")
        return f"{balance} {currency.upper()}"


class ScherKhanAutoOdometerSensor(CoordinatorEntity, SensorEntity):
    """scher_khan_auto temp class."""

    _attr_has_entity_name = True
    native_unit_of_measurement = "km"
    device_class = "distance"
    name = "Пробег"

    def __init__(self, coordinator, car_id):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.car_id = car_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, car_id)},
        )
        self._attr_unique_id = f"{DEFAULT_NAME}_car_{self.car_id}_{SENSOR}_odometer"

    @property
    def native_value(self):
        """Return de device class of the sensor."""
        return self.coordinator.data.get(self.car_id, {}).get("odometer", 0)


class ScherKhanAutoVoltageSensor(CoordinatorEntity, SensorEntity):
    """scher_khan_auto temp class."""

    _attr_has_entity_name = True
    native_unit_of_measurement = "V"
    device_class = "voltage"
    name = "Напряжение батареи"

    def __init__(self, coordinator, car_id):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.car_id = car_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, car_id)},
        )
        self._attr_unique_id = f"{DEFAULT_NAME}_car_{self.car_id}_{SENSOR}_voltage"

    @property
    def native_value(self):
        """Return de device class of the sensor."""
        return (
            self.coordinator.data.get(self.car_id, {})
            .get("battery_voltage", {})
            .get("value", 0)
        )
