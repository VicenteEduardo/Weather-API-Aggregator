# fastapi, so recebe o pedido e chama o use case
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel

from app.application.use_cases import GetWeather, WeatherQuery
from app.domain.exceptions import CityNotFound, InvalidQuery, ProviderUnavailable
from app.infrastructure.open_meteo import (
    OpenMeteoCityResolver,
    OpenMeteoHttpClient,
    OpenMeteoWeatherRepository,
)


class LocationOut(BaseModel):
    latitude: float
    longitude: float
    city: Optional[str] = None
    country: Optional[str] = None


class TemperatureOut(BaseModel):
    current: float
    feels_like: float
    min: float
    max: float
    unit: str = "C"


class WindOut(BaseModel):
    speed: float
    direction: int
    unit: str = "km/h"


class ConditionOut(BaseModel):
    code: int
    description: str


class WeatherOut(BaseModel):
    location: LocationOut
    temperature: TemperatureOut
    humidity: int
    wind: WindOut
    condition: ConditionOut
    observed_at: str
    provider: str


def build_use_case():
    http = OpenMeteoHttpClient()
    repo = OpenMeteoWeatherRepository(http)
    cidades = OpenMeteoCityResolver(http)
    return GetWeather(weather_provider=repo, city_resolver=cidades)


def get_use_case():
    return build_use_case()


def create_app(use_case_factory=get_use_case):
    app = FastAPI(title="Weather API Aggregator", version="1.0.0")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/api/v1/weather", response_model=WeatherOut)
    def get_weather(
        latitude: Optional[float] = Query(default=None, ge=-90, le=90),
        longitude: Optional[float] = Query(default=None, ge=-180, le=180),
        city: Optional[str] = Query(default=None, min_length=2),
        use_case=Depends(use_case_factory),
    ):
        try:
            w = use_case.execute(WeatherQuery(latitude=latitude, longitude=longitude, city=city))
        except CityNotFound as e:
            raise HTTPException(status_code=404, detail=str(e))
        except InvalidQuery as e:
            raise HTTPException(status_code=422, detail=str(e))
        except ProviderUnavailable as e:
            raise HTTPException(status_code=502, detail=str(e))
        return w.to_dict()

    return app


app = create_app()
