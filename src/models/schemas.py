from datetime import datetime, UTC
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel

# ---------------------------------------------------------------------------
# User related schemas
# ---------------------------------------------------------------------------

class UserCreate(SQLModel):
    name: str = Field(alias="username", unique=True, index=True)
    hashed_password: str


class UserDAO(BaseModel):
    username: str
    password: str


class UserDTO(BaseModel):
    id: int
    username: str
    carnets: list[QuoteCreate] = []


# ---------------------------------------------------------------------------
# Authentication token schemas
# ---------------------------------------------------------------------------

class Token(BaseModel):
    access_token: str
    token_type: str
    expire_in: int

class PasswordUpdate(BaseModel):
    new_pwd: str
    confirm_new_pwd: str

class TokenData(BaseModel):
    username: Optional[str] = None


# ---------------------------------------------------------------------------
# Quote related schemas
# ---------------------------------------------------------------------------

QUOTE_CITATION = "CITATION"
QUOTE_ACTION = "ACTION"

class QuoteCreate(SQLModel):
    text: str
    said_by: str
    type: str
    instead_of: str
    label: str
    date_added: datetime = Field(default_factory=lambda: datetime.now(UTC))


class QuoteUpdate(SQLModel):
    text: Optional[str] = None
    label: Optional[str] = None
    type: Optional[str] = None
    instead_of: Optional[str] = None
    said_by: Optional[int] = None