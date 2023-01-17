from fastapi import FastAPI, Depends

from src.api import router

app = FastAPI()

app.include_router(router)
