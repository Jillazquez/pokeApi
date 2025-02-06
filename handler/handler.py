import os
import requests
import redis
from typing import List
from utils.Logger import Logger

# Conectar a Redis (asumimos que el servidor Redis está en "localhost" o en el contenedor "redis")
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)


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

def fetch_pokemons_by_type(type_name: str) -> List[str]:
    """Obtiene Pokémon por tipo, usando el nombre del tipo."""
    type_id = type_to_id.get(type_name.lower())
    if not type_id:
        return []

    # Primero, intenta obtener los datos de Redis
    cached_data = redis_client.get(type_name)
    if cached_data:
        # Si los datos están en cache, devolverlos
        return cached_data.split(',')

    url = f"https://pokeapi.co/api/v2/type/{type_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        pokemons = [pokemon["pokemon"]["name"] for pokemon in data["pokemon"]]
        
        # Guardar los resultados en Redis para futuras consultas
        redis_client.setex(type_name, 3600, ','.join(pokemons))  # Guarda los datos durante 1 hora (3600 segundos)
        
        return pokemons
    except Exception as e:
        logger = Logger()
        logger.add_to_log("error", f"Error al obtener Pokémon del tipo {type_name}: {e}")
        return []

def fetch_water_pokemons() -> List[str]:
    """Obtiene Pokémon de tipo agua desde una URL dada."""
    return fetch_pokemons_by_type("water")

def fetch_pokemon_by_id(pokemon_id: int) -> str:
    """Obtiene un Pokémon por su número (ID)."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["name"]
    except Exception as e:
        logger = Logger()
        logger.add_to_log("error", f"Error al obtener el Pokémon con ID {pokemon_id}: {e}")
        return ""
