# testes do dominio, fiz primeiro
import pytest
from app.domain.entities import Coordinates


def test_coordinates_validas():
    c = Coordinates(latitude=38.7223, longitude=-9.1393)
    assert c.latitude == 38.7223


def test_latitude_errada_rebenta():
    with pytest.raises(ValueError):
        Coordinates(latitude=200, longitude=0)


def test_longitude_errada_rebenta():
    with pytest.raises(ValueError):
        Coordinates(latitude=0, longitude=500)
