# aqui fala com a open-meteo e converte para o nosso formato
from datetime import datetime
from typing import Optional

import httpx

from app.domain.entities import Condition, Coordinates, Location, Temperature, Weather, Wind
from app.domain.exceptions import ProviderUnavailable
from app.domain.wmo import describe_wmo

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


class OpenMeteoHttpClient:
    def __init__(self, client=None):
        # deixo passar client por fora para dar para testar sem net
        if client is None:
            self.client = httpx.Client(timeout=10)
        else:
            self.client = client

    def get_forecast(self, coords: Coordinates):
        try:
            r = self.client.get(FORECAST_URL, params={
                "latitude": coords.latitude,
                "longitude": coords.longitude,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m",
                "daily": "temperature_2m_max,temperature_2m_min",
                "timezone": "auto",
            })
            r.raise_for_status()
            return r.json()
        except Exception as e:
            raise ProviderUnavailable("open-meteo falhou: %s" % e)

    def search_city(self, city: str):
        try:
            r = self.client.get(GEOCODING_URL, params={
                "name": city, "count": 1, "language": "pt", "format": "json"
            })
            r.raise_for_status()
            return r.json()
        except Exception as e:
            raise ProviderUnavailable("geocoding falhou: %s" % e)


def map_forecast_to_weather(payload, coords, city=None, country=None):
    cur = payload.get("current", {}) if payload else {}
    daily = payload.get("daily", {}) if payload else {}

    code = int(cur.get("weather_code", 0) or 0)

    # as vezes vem sem nada, meto defaults para nao crashar
    tmax = daily.get("temperature_2m_max", [0])
    tmin = daily.get("temperature_2m_min", [0])
    vmax = tmax[0] if tmax else 0
    vmin = tmin[0] if tmin else 0

    quando = cur.get("time")
    try:
        if quando:
            observed = datetime.fromisoformat(quando)
        else:
            observed = datetime.utcnow()
    except:
        observed = datetime.utcnow()

    return Weather(
        location=Location(coordinates=coords, city=city, country=country),
        temperature=Temperature(
            current=float(cur.get("temperature_2m", 0) or 0),
            feels_like=float(cur.get("apparent_temperature", 0) or 0),
            min=float(vmin),
            max=float(vmax),
        ),
        humidity=int(cur.get("relative_humidity_2m", 0) or 0),
        wind=Wind(
            speed=float(cur.get("wind_speed_10m", 0) or 0),
            direction=int(cur.get("wind_direction_10m", 0) or 0),
        ),
        condition=Condition(code=code, description=describe_wmo(code)),
        observed_at=observed,
        provider="open-meteo",
    )


class OpenMeteoWeatherRepository:
    # so faz get_current, o http fica no client
    def __init__(self, http: OpenMeteoHttpClient):
        self.http = http

    def get_current(self, coords: Coordinates) -> Weather:
        data = self.http.get_forecast(coords)
        return map_forecast_to_weather(data, coords)


class OpenMeteoCityResolver:
    def __init__(self, http: OpenMeteoHttpClient):
        self.http = http

    def resolve(self, city: str):
        data = self.http.search_city(city)
        res = data.get("results") or []
        if len(res) == 0:
            return None
        f = res[0]
        c = Coordinates(latitude=float(f["latitude"]), longitude=float(f["longitude"]))
        return c, f.get("name", city), f.get("country")

    def resolve_city(self, city: str) -> Optional[Coordinates]:
        r = self.resolve(city)
        if r is None:
            return None
        return r[0]
