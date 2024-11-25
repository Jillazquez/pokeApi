from fastapi import FastAPI
from view.view import router
from utils.Logger import Logger
logger = Logger()

logger.add_to_log("info", "La aplicación FastAPI ha comenzado correctamente.")

app = FastAPI(title="Pokémon API")

# Registrar las rutas desde el router
app.include_router(router)
