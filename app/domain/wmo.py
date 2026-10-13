# tabela WMO, fui buscar a doc da open-meteo
# https://open-meteo.com/en/docs
# meti so a descricao em pt

CODIGOS = {
    0: "Céu limpo",
    1: "Quase limpo",
    2: "Parcialmente nublado",
    3: "Encoberto",
    45: "Nevoeiro",
    48: "Nevoeiro com geada",
    51: "Chuvisco leve",
    53: "Chuvisco moderado",
    55: "Chuvisco intenso",
    56: "Chuvisco gelado leve",
    57: "Chuvisco gelado intenso",
    61: "Chuva leve",
    63: "Chuva moderada",
    65: "Chuva forte",
    66: "Chuva gelada leve",
    67: "Chuva gelada forte",
    71: "Neve leve",
    73: "Neve moderada",
    75: "Neve forte",
    77: "Granizo de neve",
    80: "Aguaceiros leves",
    81: "Aguaceiros moderados",
    82: "Aguaceiros fortes",
    85: "Aguaceiros de neve leves",
    86: "Aguaceiros de neve fortes",
    95: "Trovoada",
    96: "Trovoada com granizo leve",
    99: "Trovoada com granizo forte",
}

# para nao partir se aparecer um codigo novo
WMO_DESCRIPTIONS = CODIGOS


def describe_wmo(code: int) -> str:
    if code in CODIGOS:
        return CODIGOS[code]
    return "Condição desconhecida"
