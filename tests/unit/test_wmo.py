# tabela do wmo
from app.domain.wmo import describe_wmo


def test_codigos_que_conheco():
    assert describe_wmo(0) == "Céu limpo"
    assert describe_wmo(63) == "Chuva moderada"


def test_codigo_estranho():
    assert describe_wmo(999) == "Condição desconhecida"
