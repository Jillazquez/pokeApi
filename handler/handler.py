import requests
from typing import List
from utils.Logger import Logger
import redis
from utils.redis_client import connect_to_redis  # Importar la función de conexión Redis

type_to_id = {
    "normal": 1,
    "fighting": 2,
    "flying": 3,
    "poison": 4,
    "ground": 5,
    "rock": 6,
    "bug": 7,
    "ghost": 8,
    "steel": 9,
    "fire": 10,
    "water": 11,
    "grass": 12,
    "electric": 13,
    "psychic": 14,
    "ice": 15,
    "dragon": 16,
    "dark": 17,
    "fairy": 18
}

def fetch_pokemons_by_type(type_name: str, redis_client: redis.Redis) -> List[str]:
    """Obtiene Pokémon por tipo, usando el nombre del tipo."""
    type_id = type_to_id.get(type_name.lower())
    if not type_id:
        return []

    # Cache key for Redis
    cache_key = f"pokemons:type:{type_name.lower()}"
    cached_data = redis_client.get(cache_key)

    if cached_data:
        # Si está en caché, devolver directamente la lista
        return cached_data.decode("utf-8").split(",")  # Decodificar y convertir a lista

    url = f"https://pokeapi.co/api/v2/type/{type_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        pokemon_names = [pokemon["pokemon"]["name"] for pokemon in data["pokemon"]]

        # Almacenar el resultado en Redis con un tiempo de expiración de 24 horas
        redis_client.set(cache_key, ",".join(pokemon_names), ex=86400)

        return pokemon_names
    except Exception as e:
        logger = Logger()
        logger.add_to_log("error", f"Error al obtener Pokémon del tipo {type_name}: {e}")
        return []

def fetch_pokemon_by_id(pokemon_id, redis_client=default_redis_client):
    """
    Busca el nombre de un Pokémon por su ID.
    Primero revisa en Redis si el resultado ya está cacheado; 
    si no, hace la petición a la API y lo guarda en cache.
    """
    cache_key = f'pokemon:{pokemon_id}'
    
    # Revisa si el dato ya existe en cache.
    cached_value = redis_client.get(cache_key)
    if cached_value:
        return cached_value.decode('utf-8')
    
    # Si no está cacheado, se hace la petición a la API.
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
    if response.status_code == 200:
        data = response.json()
        pokemon_name = data['name']
        # Almacena el resultado en Redis para futuras peticiones.
        redis_client.set(cache_key, pokemon_name)
        return pokemon_name
    
    return None