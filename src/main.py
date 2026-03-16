from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from src.config import ORIGINS, TAGS_METADATA, DESCRIPTION
from src.database import check_db_connexion
from src.models import *
from src.utils import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    check_db_connexion()
    yield


app = FastAPI(
    openapi_tags=TAGS_METADATA,
    title="Carnet API",
    description=DESCRIPTION,
    summary="La documentation swagger du carnet",
    version="0.0.1",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/quotes", tags=["Quote"], status_code=200)
def get_quotes(offset: int | None = 0):
    return list_all_in_db(Quote, offset)


@app.get("/labels", tags=["Label"], status_code=200)
def get_labels(offset: int | None = 0):
    return list_all_in_db(Label, offset)


@app.get("/labels/{label_id}", tags=["Label"], status_code=200)
def filter_label(label_id: int):
    print(list_in_db(Label, label_id))
    return list_in_db(Label, label_id)


@app.delete("/labels/{label_id}", tags=["Label"], status_code=202)
def delete_label(label_id: int):
    return delete_in_db(Label, label_id)


@app.delete("/quotes/{quote_id}", tags=["Quote"], status_code=202)
def delete_quote(quote_id: int):
    return delete_in_db(Quote, quote_id)


@app.get("/quotes/{quote_id}", tags=["Quote"], status_code=200)
def filter_quote(quote_id: int):
    return list_in_db(Quote, quote_id)


@app.post("/quotes", status_code=201, tags=["Quote"], response_model=Quote)
def create_quote(quote: QuoteCreate):
    db_quote = Quote.model_validate(quote)
    return create_in_db(db_quote)


@app.post("/labels", status_code=201, tags=["Label"], response_model=Label)
def create_label(label: LabelCreate):
    db_label = Label.model_validate(label)
    return create_in_db(db_label)


@app.put("/quotes/{quote_id}", status_code=200, tags=["Quote"], response_model=Quote)
def modify_quote(quote_id: int, quote_data: QuoteUpdate):
    update_data = quote_data.model_dump(exclude_unset=True)
    return update_in_db(Quote, quote_id, update_data)


@app.put("/labels/{label_id}", status_code=200, tags=["Label"], response_model=Label)
def modify_label(label_id: int, label_data: LabelUpdate):
    update_data = label_data.model_dump(exclude_unset=True)
    return update_in_db(Label, label_id, update_data)


@app.post("/token", tags=["User"])
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.post("/users", tags=["User"], status_code=201)
def register_user(user_dao: UserDAO)-> UserDTO:
    created_user = create_in_db(User(name=user_dao.username, hashed_password=get_password_hash(user_dao.password)))
    return UserDTO(id=created_user.id, username=created_user.name)


@app.get("/users/me", tags=["User"])
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserDTO:
    return UserDTO(id=current_user.id, username=current_user.name)
