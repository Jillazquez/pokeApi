from handler.handler import (
    fetch_pokemon_by_id,
)

def test_fetch_pokemon_by_id(monkeypatch):
    # Creamos un cliente de Redis "fake" para simular la caché.
    class FakeRedis:
        def __init__(self):
            self.data = {}
        def get(self, key):
            return self.data.get(key)
        def set(self, key, value):
            self.data[key] = value

    fake_redis = FakeRedis()

    # Simulamos la respuesta de la API.
    class FakeResponse:
        def __init__(self, json_data, status_code):
            self._json_data = json_data
            self.status_code = status_code
        def json(self):
            return self._json_data

    def fake_get(url):
        # Solo simulamos la respuesta para ID 1
        if url.endswith("/1"):
            return FakeResponse({'name': 'bulbasaur'}, 200)
        return FakeResponse({}, 404)

    # Monkeypatch de requests.get para usar la función fake_get
    monkeypatch.setattr(requests, "get", fake_get)

    # Primera llamada: no está cacheado, se hace la petición y se almacena en fake_redis.
    name = fetch_pokemon_by_id(1, redis_client=fake_redis)
    assert name == "bulbasaur"

    # Segunda llamada: ya debería obtenerse de la caché.
    # Para asegurarnos de que no se llame a requests.get, modificamos fake_get para que lance error.
    def fake_get_error(url):
        raise Exception("No se debió llamar a requests.get en la segunda llamada")

    monkeypatch.setattr(requests, "get", fake_get_error)

    name_cached = fetch_pokemon_by_id(1, redis_client=fake_redis)
    assert name_cached == "bulbasaur"