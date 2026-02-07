from contextlib import asynccontextmanager

from database import create_table_if_not_exists
from fastapi import FastAPI
from routers import voting


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table_if_not_exists()
    yield


app = FastAPI(title="High-Scale Voting System", lifespan=lifespan)

app.include_router(voting.router)


@app.get("/")
async def root():
    return {"message": "RS Final Projekt 🧑🏻‍💻"}
