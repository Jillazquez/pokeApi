from handler.handler import (
    fetch_water_pokemons,
    fetch_pokemon_by_id,
    fetch_pokemons_by_type,
)

def test_fetch_pokemon_by_id():
    assert fetch_pokemon_by_id(1) == "bulbasaur"