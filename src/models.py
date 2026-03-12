from datetime import datetime, UTC

from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Relationship

from src.database import engine


class UserBase(SQLModel):
    name: str = Field(alias="username", unique=True, index=True)
    hashed_password: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class QuoteLabelLink(SQLModel, table=True):
    quote_id: int | None = Field(default=None, foreign_key="quote.id", primary_key=True)
    label_id: int | None = Field(default=None, foreign_key="label.id", primary_key=True)


class QuoteBase(SQLModel):
    text: str
    said_by: str
    date_added: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Quote(QuoteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    labels: list["Label"] = Relationship(back_populates="quotes", link_model=QuoteLabelLink)


class QuoteUpdate(SQLModel):
    text: str | None = None
    said_by: str | None = None


class LabelBase(SQLModel):
    name: str


class Label(LabelBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    quotes: list["Quote"] = Relationship(back_populates="labels", link_model=QuoteLabelLink)


class LabelUpdate(SQLModel):
    name: str | None = None


SQLModel.metadata.create_all(engine)

class UserDAO(BaseModel):
    username: str
    password: str

class UserDTO(BaseModel):
    id: int
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
