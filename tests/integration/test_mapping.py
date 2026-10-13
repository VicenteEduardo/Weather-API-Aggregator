# ve se o map da open-meteo para o nosso formato esta bem
from app.domain.entities import Coordinates
from app.infrastructure.open_meteo import map_forecast_to_weather

EXEMPLO = {
    "current": {
        "time": "2026-10-13T12:00",
        "temperature_2m": 21.5,
        "relative_humidity_2m": 58,
        "apparent_temperature": 22.1,
        "weather_code": 2,
        "wind_speed_10m": 12.3,
        "wind_direction_10m": 200,
    },
    "daily": {
        "temperature_2m_max": [25.0],
        "temperature_2m_min": [15.2],
    },
}


def test_mapeamento():
    w = map_forecast_to_weather(EXEMPLO, Coordinates(38.72, -9.14))
    assert w.temperature.current == 21.5
    assert w.temperature.max == 25.0
    assert w.humidity == 58
    assert w.condition.description == "Parcialmente nublado"


def test_payload_vazio_nao_crash():
    w = map_forecast_to_weather({}, Coordinates(0, 0))
    assert w.temperature.current == 0.0
