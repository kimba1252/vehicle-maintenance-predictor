"""Constants and enumerations for the application."""

from enum import Enum


class TripStatus(str, Enum):
    """Trip safety status enum."""

    SAFE = "SAFE"
    WARNING = "WARNING"
    CRITICAL_RISK = "CRITICAL_RISK"


class TemperatureRange(str, Enum):
    """Engine temperature ranges."""

    COLD = "COLD"
    NORMAL = "NORMAL"
    WARM = "WARM"
    HOT = "HOT"


# Temperature thresholds (Celsius)
TEMP_THRESHOLDS = {
    "cold": 70,
    "normal": 92,
    "warm": 100,
    "hot": 150,
}

# Temperature wear factors
TEMP_WEAR_FACTORS = {
    "cold": 0.8,
    "normal": 1.0,
    "warm": 1.3,
    "hot": 2.0,
}

# Locations on the Abidjan-Yamoussoukro route
LOCATIONS = {
    "abidjan": {"km": 0, "name": "Abidjan"},
    "singrobo": {"km": 120, "name": "Singrobo"},
    "toumodi": {"km": 185, "name": "Toumodi"},
    "yamoussoukro": {"km": 240, "name": "Yamoussoukro"},
}

# Location ranges for breakdown prediction
BREAKDOWN_ZONES = [
    {"min_km": 0, "max_km": 160, "zone": "Entre Abidjan et Singrobo"},
    {"min_km": 160, "max_km": 200, "zone": "Aux alentours de Toumodi (KM 185)"},
    {"min_km": 200, "max_km": 240, "zone": "Entre Toumodi et Yamoussoukro"},
]
