from contextlib import asynccontextmanager

from sqlmodel import Session

from src.database import check_db_connexion
from src.config import ORIGINS, TAGS_METADATA, DESCRIPTION
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.models import *

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

@app.post("/quotes", status_code=201)
async def create_quote(quote: Quote):
    session = Session(engine)
    session.add(quote)
    session.commit()
    return {quote.id: quote}

@app.post("/labels", status_code=201)
async def create_label(label: Label):
    session = Session(engine)
    session.add(label)
    session.commit()
    return {label.id: label}