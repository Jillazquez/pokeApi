import requests
from typing import Union
from models.response import PokemonList

# Diccionario de tipos de Pokémon y sus IDs
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

def fetch_pokemon_list() -> Union[dict, str]:
    url = "https://pokeapi.co/api/v2/pokemon/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Error con la excepción: {e}"

def fetch_pokemon_by_type(type_name: str) -> Union[PokemonListResponse, str]:
    poke_dict = []
    type_id = type_to_id.get(type_name)

    if not type_id:
        return "Tipo no encontrado"

    url = f"https://pokeapi.co/api/v2/type/{type_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        for pokemon in data['pokemon']:
            poke = pokemon['pokemon']['name']
            poke_dict.append(poke)
        return PokemonListResponse(pokemon_names=poke_dict)
    except Exception as e:
        return f"Error con la excepción: {e}"
