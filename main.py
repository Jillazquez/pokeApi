from fastapi import FastAPI
from view.view import router

app = FastAPI()

app.include_router(router)