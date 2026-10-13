# Weather API Aggregator

## Objectivo

O objectivo deste trabalho é fazer um backend em Python que vai buscar o tempo a uma API externa (usei a Open-Meteo porque é grátis e não pede key) e devolve os dados num formato nosso, mais simples e sempre igual.

A ideia era praticar DDD, TDD e SOLID num exemplo pequeno mas completo:
- DDD para separar dominio / aplicação / infraestrutura / apresentação
- TDD, fiz os testes antes do código
- SOLID para dar para trocar de provider sem partir tudo

## Como está organizado

- `app/domain/` -> o que é o tempo para nós (Weather, Coordinates, etc), a tabela do WMO e os contratos. Não importa nada de fora aqui.
- `app/application/` -> o caso de uso `GetWeather`, recebe cidade ou lat/lon.
- `app/infrastructure/` -> quem fala com a Open-Meteo e converte para o nosso formato.
- `app/presentation/` -> o FastAPI, só recebe o pedido e chama o caso de uso.
- `tests/` -> testes unitários e de integração.

Sobre o SOLID, tentei aplicar assim:
- cada classe faz uma coisa (o client http só faz http, o mapper só converte)
- se quiser meter outro provider é só criar outra classe igual, o caso de uso não muda
- o caso de uso só conhece as interfaces, não o httpx. Nos testes uso fakes.

TDD: comecei pelas coordenadas e pelo caso de uso com fakes, depois o mapeamento e por fim a rota. Está tudo em `tests/`.

## O formato que devolvemos

Exemplo do `GET /api/v1/weather?city=Lisboa`:

```json
{
  "location": {"latitude": 38.72, "longitude": -9.14, "city": "Lisboa", "country": "Portugal"},
  "temperature": {"current": 21.5, "feels_like": 22.1, "min": 15.2, "max": 25.0, "unit": "C"},
  "humidity": 58,
  "wind": {"speed": 12.3, "direction": 200, "unit": "km/h"},
  "condition": {"code": 2, "description": "Parcialmente nublado"},
  "observed_at": "2026-10-13T12:00",
  "provider": "open-meteo"
}
```

## Para correr

```bash
pip install -r requirements.txt
pytest -v
uvicorn main:app --reload
```

Depois abrir:
- `GET /health` para ver se está vivo
- `GET /api/v1/weather?latitude=38.72&longitude=-9.14`
- `GET /api/v1/weather?city=Lisboa`
- docs em `http://localhost:8000/docs`

Se a cidade não existir dá 404, se faltarem parâmetros dá 422, se a Open-Meteo for abaixo dá 502.
