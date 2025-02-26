import sentry_sdk
import os
import requests
import redis
from typing import List
from utils.Logger import Logger


sentry_sdk.init(
    dsn="https://7be9ca90ec906575e54116a2e5f31373@o4508807627735040.ingest.de.sentry.io/4508807629701200",
    send_default_pii=True,  
    traces_sample_rate=1.0,  
    _experiments={
        "continuous_profiling_auto_start": True,  
    },
)


redis_host = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)


TYPE_TO_ID = {
    "normal": 1, "fighting": 2, "flying": 3, "poison": 4, "ground": 5, "rock": 6,
    "bug": 7, "ghost": 8, "steel": 9, "fire": 10, "water": 11, "grass": 12,
    "electric": 13, "psychic": 14, "ice": 15, "dragon": 16, "dark": 17, "fairy": 18
}


def fetch_pokemons_by_type(type_name: str) -> List[str]:
    """Get a pokemon list with a type."""
    type_id = type_to_id.get(type_name.lower(), None)
    if not type_id:
        return []

    cached_data = redis_client.get(type_name)
    if cached_data:
        return cached_data.split(',')

    url = f"https://pokeapi.co/api/v2/type/{type_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        pokemons = [pokemon["pokemon"]["name"] for pokemon in data["pokemon"]]

        redis_client.setex(type_name, 3600, ','.join(pokemons))  
        return pokemons
    except Exception as e:
        logger = Logger()
        logger.add_to_log("error", f"Error obtaining  {type_name} type pokemons: {e}")
        sentry_sdk.capture_exception(e)  
        return []


def fetch_water_pokemons() -> List[str]:
    """Get water type pokemons"""
    return fetch_pokemons_by_type("water")


def fetch_pokemon_by_id(pokemon_id: int) -> str:
    """Get pokemon with ID."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"

    cached_data = redis_client.get(str(pokemon_id))
    if cached_data:
        return cached_data
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        redis_client.setex(str(pokemon_id), 3600, data["name"]) 
        return data["name"]
    except Exception as e:
        logger = Logger()
        logger.add_to_log("error", f"Error obtaining pokemon with id {pokemon_id}: {e}")
        sentry_sdk.capture_exception(e)  
        return ""

def explota():
    """Throws an exception."""
    logger = Logger()
    logger.add_to_log("error", "Exception thrown")
    sentry_sdk.capture_message("Exception thrown")
    return 1/0