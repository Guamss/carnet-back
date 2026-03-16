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


# ---------------------------------------------------------------------------
# Authentication token schemas
# ---------------------------------------------------------------------------

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# ---------------------------------------------------------------------------
# Quote related schemas
# ---------------------------------------------------------------------------

class QuoteCreate(SQLModel):
    text: str
    said_by: str
    date_added: datetime = Field(default_factory=lambda: datetime.now(UTC))


class QuoteUpdate(SQLModel):
    text: Optional[str] = None
    said_by: Optional[str] = None


# ---------------------------------------------------------------------------
# Label related schemas
# ---------------------------------------------------------------------------

class LabelCreate(SQLModel):
    name: str


class LabelUpdate(SQLModel):
    name: Optional[str] = None