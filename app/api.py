from fastapi import FastAPI
from app.routes.index import user

app= FastAPI()

app.include_router(user)