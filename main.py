from fastapi import FastAPI
from view.view import router

app = FastAPI(title="Pokémon API")

# Registrar las rutas desde el router
app.include_router(router)
