from contextlib import asynccontextmanager
from sqlmodel import Session, select
from src.database import check_db_connexion
from src.config import ORIGINS, TAGS_METADATA, DESCRIPTION
from fastapi import FastAPI, Query
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

async def create_in_db(item):
    with Session(engine) as session :
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

async def list_in_db(item, offset):
    with Session(engine) as session :
        statement = select(item).offset(offset).limit(25)
        results = session.exec(statement)
        return results.all()
@app.get("/quotes", status_code=200)
async def get_quotes(offset: int | None = 0):
    return await list_in_db(Quote,offset)
@app.post("/quotes", status_code=201, response_model=Quote)
async def create_quote(quote: QuoteBase):
    db_quote = Quote.model_validate(quote)
    return await create_in_db(db_quote)

@app.post("/labels", status_code=201, response_model=Label)
async def create_label(label: LabelBase):
    db_label = Label.model_validate(label)
    return await create_in_db(db_label)