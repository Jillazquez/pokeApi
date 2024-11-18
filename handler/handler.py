import requests
from typing import List, Union

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

def get_water_type_url() -> str:
    type_id = type_to_id.get("water")
    if not type_id:
        return ""
    return f"https://pokeapi.co/api/v2/type/{type_id}"

async def fetch_water_pokemons(water_url: str) -> List[str]:
    try:
        response = requests.get(water_url)
        response.raise_for_status()
        data = response.json()
        return [pokemon["pokemon"]["name"] for pokemon in data["pokemon"]]
    except Exception as e:
        print(f"Error al obtener Pokémon de tipo agua: {e}")
        return []

async def fetch_pokemon_by_id(pokemon_id: int) -> Union[str, None]:
    """Obtiene un Pokémon por su número (ID)."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["name"]
    except Exception as e:
        print(f"Error al obtener el Pokémon con ID {pokemon_id}: {e}")
        return None

async def fetch_pokemon_by_type(type_name: str) -> List[str]:
    """Obtiene Pokémon por tipo."""
    type_id = type_to_id.get(type_name.lower())
    if not type_id:
        return []

    url = f"https://pokeapi.co/api/v2/type/{type_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [pokemon["pokemon"]["name"] for pokemon in data["pokemon"]]
    except Exception as e:
        print(f"Error al obtener Pokémon del tipo {type_name}: {e}")
        return []
