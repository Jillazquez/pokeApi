from fastapi import APIRouter, HTTPException
from typing import List
import sentry_sdk
from models.response import Pokemon  # Asegúrate de que el modelo Pokemon esté bien definido
from utils.Logger import Logger  # Logger para agregar logs
from handler.handler import (
    fetch_water_pokemons,
    fetch_pokemon_by_id,
    fetch_pokemons_by_type,
    explota,
    example
)

# Inicializa el logger
logger = Logger()

# Inicializa el router de FastAPI
router = APIRouter()

# Configura Sentry con la DSN proporcionada
sentry_sdk.init(
    dsn="https://7be9ca90ec906575e54116a2e5f31373@o4508807627735040.ingest.de.sentry.io/4508807629701200",
    send_default_pii=True,  # Enviar información del usuario (si aplica)
    traces_sample_rate=1.0,  # Captura el 100% de las transacciones
    _experiments={
        "continuous_profiling_auto_start": True,  # Habilita el profiling automático
    },
)

# Ruta para obtener Pokémon por ID
@router.get("/pokemon/{id}", response_model=Pokemon)
async def get_pokemon_by_id(id: int):
    """Obtiene un Pokémon por su número (ID)."""
    pokemon = fetch_pokemon_by_id(id)
    if not pokemon:
        logger.add_to_log("error", f"Pokémon con ID {id} no encontrado")  # Log de error
        raise HTTPException(status_code=404, detail="Pokémon no encontrado")
    return Pokemon(name=pokemon)

# Ruta para obtener Pokémon por tipo
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

# Ruta para probar un error intencional y capturarlo en Sentry
@router.get("/sentry-debug")
async def trigger_error():
    """Ruta para probar un error y capturarlo en Sentry."""
    division_by_zero = 1 / 0

@router.get("/example")
async def examplefun():
    example()

@router.get("/explota")
async def explotafun():
    explota()