"""Constants for Scher-khan Auto."""
# Base component constants
NAME = "Scher-khan Auto"
DOMAIN = "scher_khan_auto"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.0"

ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
ISSUE_URL = "https://github.com/iredun/scher-khan-auto/issues"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
SWITCH = "switch"
# COVER = "cover"
PLATFORMS = [BINARY_SENSOR, SENSOR, SWITCH]

# Doors names
CAR_DOORS = {
    "is_trunk_open": "Багажник",
    "is_hood_open": "Капот",
    "is_fl_door_open": "Передняя левая дверь",
    "is_fr_door_open": "Передняя правая дверь",
    "is_rl_door_open": "Задняя левая дверь",
    "is_rr_door_open": "Задняя правая дверь",
}


# Configuration and options
CONF_ENABLED = "enabled"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_TOKEN = "token"
CONF_CAR = "car"
CONF_CARS = "cars"

# Defaults
DEFAULT_NAME = DOMAIN
WEBSOCKET_URL = "wss://ws.mf-t.ru/state/"


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
