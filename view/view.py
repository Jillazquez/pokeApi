from fastapi import APIRouter, HTTPException
from typing import List
import sentry_sdk
from models.response import Pokemon  
from utils.Logger import Logger  
from handler.handler import (
    fetch_water_pokemons,
    fetch_pokemon_by_id,
    fetch_pokemons_by_type,
)


logger = Logger()


router = APIRouter()


sentry_sdk.init(
    dsn="https://7be9ca90ec906575e54116a2e5f31373@o4508807627735040.ingest.de.sentry.io/4508807629701200",
    send_default_pii=True,  
    traces_sample_rate=1.0,  
    _experiments={
        "continuous_profiling_auto_start": True, 
    },
)


@router.get("/pokemon/{id}", response_model=Pokemon)
async def get_pokemon_by_id(id: int):
    """Obtiene un Pokémon por su número (ID)."""
    pokemon = fetch_pokemon_by_id(id)
    if not pokemon:
        logger.add_to_log("error", f"Pokémon con ID {id} no encontrado")  
        raise HTTPException(status_code=404, detail="Pokémon no encontrado")
    return Pokemon(name=pokemon)


@router.get("/type/{type_name}", response_model=List[Pokemon])
async def get_pokemon_by_type(type_name: str):
    """Obtiene Pokémons de tipo agua y el añadido."""
    try:
        water_pokemons = fetch_water_pokemons()
        pokemons = fetch_pokemons_by_type(type_name)


        comunes = list(set(water_pokemons) & set(pokemons))

        
        if not comunes:
            error_message = f"No se encontraron Pokémon del tipo {type_name}"
            logger.add_to_log("error", error_message)  
            sentry_sdk.capture_message(error_message)  
            raise HTTPException(status_code=404, detail=error_message)

        
        return [Pokemon(name=name) for name in comunes]
    
    except Exception as e:
        
        sentry_sdk.capture_exception(e)  
        
        logger.add_to_log("error", f"Error al obtener Pokimon del tipo {type_name}: {e}")
        
        raise HTTPException(status_code=500, detail="Error interno al procesar la solicitud")
