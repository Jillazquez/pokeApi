from fastapi import APIRouter, HTTPException
from typing import List
from handler.handler import (
    fetch_water_pokemons,
    fetch_pokemon_by_id,
    fetch_pokemons_by_type,
)
from models.response import Pokemon  # Asegúrate de que el modelo Pokemon esté bien definido
from utils.Logger import Logger  # Ajusté la importación del Logger

logger = Logger()  # Crea una instancia del logger

router = APIRouter()

@router.get("/pokemon/{id}", response_model=Pokemon)
async def get_pokemon_by_id(id: int):
    """Obtiene un Pokémon por su número (ID)."""
    pokemon = fetch_pokemon_by_id(id)
    if not pokemon:
        logger.add_to_log("error", f"Pokémon con ID {id} no encontrado")  # Log de error
        raise HTTPException(status_code=404, detail="Pokémon no encontrado")
    return Pokemon(name=pokemon)

@router.get("/type/{type_name}", response_model=List[Pokemon])
async def get_pokemon_by_type(type_name: str):
    """Obtiene Pokémon por su tipo."""
    pokemons = fetch_pokemons_by_type(type_name)
    if not pokemons:
        logger.add_to_log("error", f"No se encontraron Pokémon del tipo {type_name}")  # Log de error
        raise HTTPException(status_code=404, detail=f"No se encontraron Pokémon del tipo {type_name}")
    return [Pokemon(name=name) for name in pokemons]
