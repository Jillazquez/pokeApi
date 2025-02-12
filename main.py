from fastapi import FastAPI
from view import router  # Importa el router con las rutas definidas

app = FastAPI()

# Registra el router con las rutas definidas
app.include_router(router)

# Asegúrate de que FastAPI está ejecutándose correctamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
