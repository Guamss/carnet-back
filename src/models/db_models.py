from datetime import datetime, UTC
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel

from src.database import engine


class User(SQLModel, table=True):
    name: str = Field(alias="username", unique=True, index=True)
    hashed_password: str
    id: int | None = Field(default=None, primary_key=True)

class QuoteType(str, Enum):
    CITATION = "CITATION"
    ACTION = "ACTION"

class Quote(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    type: QuoteType = Field(default=QuoteType.CITATION)
    said_by: str | None = Field(default=None, foreign_key="user.name")
    label: str
    instead_of: str
    date_added: datetime = Field(default_factory=lambda: datetime.now(UTC))

SQLModel.metadata.create_all(engine)
