# teste do use case com fakes para nao precisar de net
from datetime import datetime

import pytest

from app.application.use_cases import GetWeather, WeatherQuery
from app.domain.entities import Coordinates, Location, Temperature, Weather, Wind, Condition
from app.domain.exceptions import CityNotFound, InvalidQuery


class FakeWeather:
    def __init__(self, w):
        self.w = w
        self.chamadas = []

    def get_current(self, coords):
        self.chamadas.append(coords)
        return self.w


class FakeCidades:
    def __init__(self, res=None):
        self.res = res

    def resolve(self, city):
        return self.res


def faz_tempo():
    return Weather(
        location=Location(coordinates=Coordinates(38.72, -9.14)),
        temperature=Temperature(current=20.0, feels_like=21.0, min=15.0, max=25.0),
        humidity=60,
        wind=Wind(speed=10.0, direction=180),
        condition=Condition(code=2, description="Parcialmente nublado"),
        observed_at=datetime(2026, 1, 1, 12, 0, 0),
    )


def test_por_coords():
    f = FakeWeather(faz_tempo())
    uc = GetWeather(weather_provider=f)
    out = uc.execute(WeatherQuery(latitude=38.72, longitude=-9.14))
    assert out.temperature.current == 20.0
    assert f.chamadas[0].latitude == 38.72


def test_sem_nada_da_erro():
    uc = GetWeather(weather_provider=FakeWeather(faz_tempo()))
    with pytest.raises(InvalidQuery):
        uc.execute(WeatherQuery())


def test_cidade_que_nao_existe():
    uc = GetWeather(
        weather_provider=FakeWeather(faz_tempo()),
        city_resolver=FakeCidades(res=None),
    )
    with pytest.raises(CityNotFound):
        uc.execute(WeatherQuery(city="AtlantisXYZ"))


def test_por_cidade_mete_nome():
    coords = Coordinates(38.72, -9.14)
    uc = GetWeather(
        weather_provider=FakeWeather(faz_tempo()),
        city_resolver=FakeCidades(res=(coords, "Lisboa", "Portugal")),
    )
    out = uc.execute(WeatherQuery(city="Lisboa"))
    assert out.location.city == "Lisboa"
    assert out.location.country == "Portugal"


def test_formato_que_devolvemos():
    d = faz_tempo().to_dict()
    assert d["provider"] == "open-meteo"
    assert d["temperature"]["unit"] == "C"
    assert "location" in d
    assert "condition" in d
