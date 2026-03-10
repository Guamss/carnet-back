from contextlib import asynccontextmanager

from src.database import *
from src.config import ORIGINS, TAGS_METADATA, DESCRIPTION
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    check_db_connexion()
    yield


app = FastAPI(
    openapi_tags=TAGS_METADATA,
    title="API template",
    description=DESCRIPTION,
    summary="La documentation swagger du template d'API",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    lifespan=lifespan,
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def hello():
    return print("hello")
