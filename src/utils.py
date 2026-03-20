from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from dotenv import dotenv_values
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pwdlib import PasswordHash
from sqlmodel import Session, select

from src.models import Quote
from src.database import engine
from src.models import User, TokenData

PASSWORD_HASH = PasswordHash.recommended()
SECRET_KEY = dotenv_values(".env")['SECRET_KEY']
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_in_db(item):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


def delete_in_db(item, item_id):
    with Session(engine) as session:
        statement = select(item).where(item.id == item_id)
        result = session.exec(statement).first()
        if not result:
            raise HTTPException(status_code=404, detail="Élément non trouvé")
        session.delete(result)
        session.commit()
        return {"message": "Supprimé avec succès"}


def list_all_in_db(item, offset):
    with Session(engine) as session:
        statement = select(item).offset(offset).limit(25)
        results = session.exec(statement)
        return results.all()


def list_in_db(item, item_id):
    with Session(engine) as session:
        statement = select(item).where(item.id == item_id)
        result = session.exec(statement)
        return result.first()

def list_user_by_password_and_username(username: str, password: str):
    with Session(engine) as session:
        statement = select(User).where(User.name == username and User.password == password)
        result = session.exec(statement)
        return result.first()

def list_carnet_by_user(user_id: int):
    with Session(engine) as session:
        statement = select(Quote).where(Quote.said_by == user_id)
        result = session.exec(statement)
        return result.all()

# username est unique donc ça marche mgl
def list_user_in_db(username: str):
    with Session(engine) as session:
        statement = select(User).where(User.name == username)
        result = session.exec(statement)
        return result.first()


def update_in_db(model, item_id: int, data_to_update: dict):
    with Session(engine) as session:
        db_item = session.get(model, item_id)

        if not db_item:
            raise HTTPException(status_code=404, detail="Pas trouve")

        for key, value in data_to_update.items():
            setattr(db_item, key, value)

        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item


def verify_password(plain_password, hashed_password):
    return PASSWORD_HASH.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = list_user_in_db(username=token_data.username)
    if not user:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user

def get_password_hash(password):
    return PASSWORD_HASH.hash(password)

def authenticate_user(username: str, password: str):
    return list_user_by_password_and_username(username, password)


