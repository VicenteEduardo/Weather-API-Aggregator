# contratos. o application so conhece isto, nao conhece httpx nem fastapi
from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities import Coordinates, Weather


class WeatherProvider(ABC):
    @abstractmethod
    def get_current(self, coords: Coordinates) -> Weather:
        pass


class GeocodingProvider(ABC):
    @abstractmethod
    def resolve_city(self, city: str) -> Optional[Coordinates]:
        pass


class CityResolver(ABC):
    @abstractmethod
    def resolve(self, city: str):
        # devolve (coords, nome, pais) ou None
        pass
