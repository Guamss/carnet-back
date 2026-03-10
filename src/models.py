from datetime import datetime, UTC
from sqlmodel import Field, SQLModel
from src.database import engine

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(alias="username", unique=True, index=True)
    hashed_password: str

class Quote(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    said_by: str
    date_added: datetime = Field(default_factory=lambda: datetime.now(UTC))

class Label(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

SQLModel.metadata.create_all(engine)