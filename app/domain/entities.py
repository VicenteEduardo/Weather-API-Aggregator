# cenas base do dominio, nao depende de nada de fora
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Coordinates:
    latitude: float
    longitude: float

    def __post_init__(self):
        # valida rapido para nao rebentar mais a frente
        if not -90 <= self.latitude <= 90:
            raise ValueError("latitude invalida")
        if not -180 <= self.longitude <= 180:
            raise ValueError("longitude invalida")


@dataclass(frozen=True)
class Location:
    coordinates: Coordinates
    city: Optional[str] = None
    country: Optional[str] = None


@dataclass(frozen=True)
class Temperature:
    current: float
    feels_like: float
    min: float
    max: float
    unit: str = "C"


@dataclass(frozen=True)
class Wind:
    speed: float
    direction: int
    unit: str = "km/h"


@dataclass(frozen=True)
class Condition:
    code: int
    description: str


@dataclass(frozen=True)
class Weather:
    # isto e o nosso formato, o que a API devolve para fora
    location: Location
    temperature: Temperature
    humidity: int
    wind: Wind
    condition: Condition
    observed_at: datetime
    provider: str = "open-meteo"

    def to_dict(self):
        loc = self.location
        return {
            "location": {
                "latitude": loc.coordinates.latitude,
                "longitude": loc.coordinates.longitude,
                "city": loc.city,
                "country": loc.country,
            },
            "temperature": {
                "current": self.temperature.current,
                "feels_like": self.temperature.feels_like,
                "min": self.temperature.min,
                "max": self.temperature.max,
                "unit": self.temperature.unit,
            },
            "humidity": self.humidity,
            "wind": {
                "speed": self.wind.speed,
                "direction": self.wind.direction,
                "unit": self.wind.unit,
            },
            "condition": {
                "code": self.condition.code,
                "description": self.condition.description,
            },
            "observed_at": self.observed_at.isoformat(),
            "provider": self.provider,
        }
