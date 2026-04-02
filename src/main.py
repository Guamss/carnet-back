from contextlib import asynccontextmanager

from fastapi import FastAPI
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

@app.delete("/quotes/{quote_id}", tags=["Quote"], status_code=202)
def delete_quote(quote_id: int):
    return delete_in_db(Quote, quote_id)


@app.get("/quotes/{quote_id}", tags=["Quote"], status_code=200)
def get_quote_by_id(current_user: Annotated[User, Depends(get_current_active_user)], quote_id: int):
    return list_in_db(Quote, quote_id)

@app.post("/quotes", status_code=201, tags=["Quote"], response_model=Quote)
def create_quote(current_user: Annotated[User, Depends(get_current_active_user)], quote: QuoteCreate):
    if quote.type == QUOTE_ACTION or quote.type == QUOTE_CITATION:
        db_quote = Quote(
            text=quote.text,
            said_by=quote.said_by,
            label=quote.label,
            type=quote.type,
            instead_of=quote.instead_of,
            date_added=quote.date_added
        )
        return create_in_db(db_quote)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le type d'action n'est pas valide",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.put("/quotes/{quote_id}", status_code=200, tags=["Quote"], response_model=Quote)
def modify_quote(current_user: Annotated[User, Depends(get_current_active_user)], quote_id: int, quote_data: QuoteUpdate):
    update_data = quote_data.model_dump(exclude_unset=True)
    return update_in_db(Quote, quote_id, update_data)

@app.put("/users", status_code=200, tags=["User"])
def change_pwd(current_user: Annotated[User, Depends(get_current_active_user)], pwd_update: PasswordUpdate) -> UserDTO:
    if pwd_update.new_pwd == pwd_update.confirm_new_pwd:
        current_user.hashed_password = get_password_hash(pwd_update.new_pwd)
        update_in_db(User, current_user.id, current_user.model_dump())
        return UserDTO(id=current_user.id, username=current_user.name, carnets=list_carnet_by_user(current_user.name))
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Les mots de passe ne correspondent pas.",
            headers={"WWW-Authenticate": "Bearer"},
        )
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
    return Token(access_token=access_token, token_type="bearer", expire_in=int(access_token_expires.total_seconds()))


@app.post("/users", tags=["User"], status_code=201)
def register_user(user_dao: UserDAO) -> UserDTO:
    u = list_user_in_db(user_dao.username)
    if not u:
        created_user = create_in_db(User(name=user_dao.username, hashed_password=get_password_hash(user_dao.password)))
        return UserDTO(id=created_user.id, username=created_user.name)
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/users/me", tags=["User"])
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserDTO:
    return UserDTO(id=current_user.id, username=current_user.name, carnets=list_carnet_by_user(current_user.name))

@app.get("/users", tags=["User"])
async def list_users() -> list[UserDTO]:
    users = list_all_in_db(User, 0)
    return list(map(lambda u : UserDTO(id=u.id, username=u.name, carnets=[]), users))


@app.get("/users/{user_id}", tags=["User"])
async def read_user_by_id(
        current_user: Annotated[User, Depends(get_current_active_user)],
        user_id: int
) -> UserDTO:
    user = list_in_db(User, user_id)
    if user:
        return UserDTO(id=user.id, username=user.name, carnets=list_carnet_by_user(user.name))
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
        headers={"WWW-Authenticate": "Bearer"},
    )
