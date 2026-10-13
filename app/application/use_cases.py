# caso de uso principal. recebe lat/lon ou cidade e devolve Weather
from dataclasses import dataclass
from typing import Optional

from app.domain.entities import Coordinates, Location, Weather
from app.domain.exceptions import CityNotFound, InvalidQuery


@dataclass(frozen=True)
class WeatherQuery:
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None


class GetWeather:
    def __init__(self, weather_provider, geocoding=None, city_resolver=None):
        self.weather = weather_provider
        self.geocoding = geocoding
        self.cities = city_resolver

    def execute(self, query: WeatherQuery) -> Weather:
        # por cidade
        if query.city:
            nome = query.city.strip()
            if not nome:
                raise InvalidQuery("city nao pode ser vazia")

            coords = None
            cidade_nome = nome
            pais = None

            if self.cities is not None:
                achou = self.cities.resolve(nome)
                if achou is None:
                    raise CityNotFound("Cidade nao encontrada: " + nome)
                coords, cidade_nome, pais = achou
            elif self.geocoding is not None:
                coords = self.geocoding.resolve_city(nome)
                if coords is None:
                    raise CityNotFound("Cidade nao encontrada: " + nome)
            else:
                raise InvalidQuery("pesquisa por cidade nao esta ligada")

            w = self.weather.get_current(coords)

            # mete o nome da cidade na resposta
            return Weather(
                location=Location(coordinates=w.location.coordinates, city=cidade_nome, country=pais),
                temperature=w.temperature,
                humidity=w.humidity,
                wind=w.wind,
                condition=w.condition,
                observed_at=w.observed_at,
                provider=w.provider,
            )

        # por coordenadas
        if query.latitude is None or query.longitude is None:
            raise InvalidQuery("Tens de passar city ou latitude+longitude")

        c = Coordinates(latitude=query.latitude, longitude=query.longitude)
        return self.weather.get_current(c)
