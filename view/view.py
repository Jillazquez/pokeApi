from fastapi import APIRouter, HTTPException
from typing import List
from handler.handler import (
    fetch_water_pokemons,
    fetch_pokemon_by_id,
    fetch_pokemons_by_type,
)
import sentry_sdk
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
    """Obtiene Pokémons de tipo agua y el añadido."""
    try:
        # Llamadas a las funciones para obtener los pokémons
        water_pokemons = fetch_water_pokemons()
        pokemons = fetch_pokemons_by_type(type_name)

        # Encuentra los pokémons comunes
        comunes = list(set(water_pokemons) & set(pokemons))

        # Si no hay pokémons comunes, genera un error y lo loggea
        if not comunes:
            error_message = f"No se encontraron Pokémon del tipo {type_name}"
            logger.add_to_log("error", error_message)  # Log de error
            sentry_sdk.capture_message(error_message)  # Enviar mensaje a Sentry
            raise HTTPException(status_code=404, detail=error_message)

        # Si todo está bien, devuelve los Pokémon comunes
        return [Pokemon(name=name) for name in comunes]
    
    except Exception as e:
        # Capturar cualquier otro error y enviarlo a Sentry
        sentry_sdk.capture_exception(e)  # Captura el error en Sentry
        # Agregar el error al log
        logger.add_to_log("error", f"Error al obtener Pokimon del tipo {type_name}: {e}")
        # Vuelve a lanzar la excepción para que se maneje correctamente por FastAPI
        raise HTTPException(status_code=500, detail="Error interno al procesar la solicitud")

@router.get("/error")
async def error():
    """Ruta para probar Sentry con un error intencional."""
    try:
        raise Exception("¡Error intencional para probar Sentry!")
    except Exception as e:
        sentry_sdk.capture_exception(e)  # Captura el error en Sentry
        raise HTTPException(status_code=500, detail="Error interno del servidor")