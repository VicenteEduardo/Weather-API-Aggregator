# testa a api com fakes
from datetime import datetime

from fastapi.testclient import TestClient

from app.application.use_cases import GetWeather
from app.domain.entities import Coordinates, Location, Temperature, Weather, Wind, Condition
from app.presentation.app import create_app, get_use_case


def fake_uc():
    class Prov:
        def get_current(self, coords):
            return Weather(
                location=Location(coordinates=coords, city="Lisboa", country="Portugal"),
                temperature=Temperature(current=20.5, feels_like=21.0, min=16.0, max=24.0),
                humidity=55,
                wind=Wind(speed=11.0, direction=180),
                condition=Condition(code=1, description="Quase limpo"),
                observed_at=datetime(2026, 10, 13, 12, 0, 0),
            )

    class Cidades:
        def resolve(self, city):
            if city.lower() == "lisboa":
                return Coordinates(38.72, -9.14), "Lisboa", "Portugal"
            return None

    return GetWeather(weather_provider=Prov(), city_resolver=Cidades())


def make_client():
    app = create_app()
    app.dependency_overrides[get_use_case] = fake_uc
    return TestClient(app)


def test_health():
    r = make_client().get("/health")
    assert r.status_code == 200


def test_por_coords():
    r = make_client().get("/api/v1/weather", params={"latitude": 38.72, "longitude": -9.14})
    assert r.status_code == 200
    assert r.json()["temperature"]["current"] == 20.5


def test_por_cidade():
    r = make_client().get("/api/v1/weather", params={"city": "Lisboa"})
    assert r.status_code == 200
    assert r.json()["location"]["city"] == "Lisboa"


def test_cidade_errada_da_404():
    r = make_client().get("/api/v1/weather", params={"city": "XyzInexistente123"})
    assert r.status_code == 404


def test_sem_params_da_422():
    r = make_client().get("/api/v1/weather")
    assert r.status_code == 422
