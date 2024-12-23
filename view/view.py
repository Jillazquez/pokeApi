from fastapi import APIRouter, HTTPException
from typing import List
from handler.handler import (
    get_water_type_url,
    fetch_water_pokemons,
    fetch_pokemon_by_id,
    fetch_pokemon_by_type,
)
from models.response import Pokemon  # Asegúrate de que el modelo Pokemon esté bien definido
from utils.Logger import Logger  # Ajusté la importación del Logger

logger = Logger()  # Crea una instancia del logger

router = APIRouter()

@router.get("/water_pokemons", response_model=List[Pokemon])
async def get_water_pokemons():
    water_url = get_water_type_url()
    if not water_url:
        logger.add_to_log("error", "No se encontró el tipo agua")  # Log de error
        raise HTTPException(status_code=404, detail="No se encontró el tipo agua")

    water_pokemons = await fetch_water_pokemons(water_url)
    if not water_pokemons:
        logger.add_to_log("error", "No se encontraron Pokémon de tipo agua")  # Log de error
        raise HTTPException(status_code=404, detail="No se encontraron Pokémon de tipo agua")
    
    return [Pokemon(name=name) for name in water_pokemons]

@router.get("/pokemon/{id}", response_model=Pokemon)
async def get_pokemon_by_id(id: int):
    """Obtiene un Pokémon por su número (ID)."""
    pokemon = await fetch_pokemon_by_id(id)
    if not pokemon:
        logger.add_to_log("error", f"Pokémon con ID {id} no encontrado")  # Log de error
        raise HTTPException(status_code=404, detail="Pokémon no encontrado")
    return Pokemon(name=pokemon)

@router.get("/type/{type_name}", response_model=List[Pokemon])
async def get_pokemon_by_type(type_name: str):
    """Obtiene Pokémon por su tipo."""
    pokemons = await fetch_pokemon_by_type(type_name)
    if not pokemons:
        logger.add_to_log("error", f"No se encontraron Pokémon del tipo {type_name}")  # Log de error
        raise HTTPException(status_code=404, detail=f"No se encontraron Pokémon del tipo {type_name}")
    return [Pokemon(name=name) for name in pokemons]


