from contextlib import asynccontextmanager
from src.database import check_db_connexion
from src.config import ORIGINS, TAGS_METADATA, DESCRIPTION
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.models import *
from src.utils import *

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

@app.get("/quotes", status_code=200)
def get_quotes(offset: int | None = 0):
    return list_all_in_db(Quote,offset)

@app.get("/labels", status_code=200)
def get_labels(offset: int | None = 0):
    return list_all_in_db(Label,offset)

@app.get("/labels/{label_id}", status_code=200)
def filter_label(label_id: int):
    return list_in_db(Label,label_id)

@app.delete("/labels/{label_id}", status_code=202)
def delete_label(label_id: int):
    return delete_in_db(Label,label_id)

@app.delete("/quotes/{quote_id}", status_code=202)
def delete_quote(quote_id: int):
    return delete_in_db(Quote,quote_id)
@app.get("/quotes/{quote_id}", status_code=200)
def filter_quote(quote_id: int):
    return list_in_db(Quote,quote_id)
@app.post("/quotes", status_code=201, response_model=Quote)
def create_quote(quote: QuoteBase):
    db_quote = Quote.model_validate(quote)
    return create_in_db(db_quote)

@app.post("/labels", status_code=201, response_model=Label)
def create_label(label: LabelBase):
    db_label = Label.model_validate(label)
    return create_in_db(db_label)

@app.patch("/quotes/{quote_id}", status_code=200, response_model=Quote)
def modify_quote(quote_id: int, quote_data: QuoteUpdate):
    update_data = quote_data.model_dump(exclude_unset=True)
    print(update_data)
    return update_in_db(Quote, quote_id, update_data)

@app.patch("/labels/{label_id}", status_code=200, response_model=Label)
def modify_label(label_id: int, label_data: LabelUpdate):
    update_data = label_data.model_dump(exclude_unset=True)
    return update_in_db(Label, label_id, update_data)