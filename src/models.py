from datetime import datetime, UTC
from sqlmodel import Field, SQLModel, Relationship
from src.database import engine

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(alias="username", unique=True, index=True)
    hashed_password: str

class QuoteLabelLink(SQLModel, table=True):
    quote_id: int | None = Field(default=None, foreign_key="quote.id", primary_key=True)
    label_id: int | None = Field(default=None, foreign_key="label.id", primary_key=True)

class Quote(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    said_by: str
    date_added: datetime = Field(default_factory=lambda: datetime.now(UTC))
    labels: list["Label"] = Relationship(back_populates="quotes", link_model=QuoteLabelLink)

class Label(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    quotes: list["Quote"] = Relationship(back_populates="labels", link_model=QuoteLabelLink)

SQLModel.metadata.create_all(engine)