from datetime import datetime, UTC
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

class LabelBase(SQLModel):
    name: str

class Label(LabelBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    quotes: list["Quote"] = Relationship(back_populates="labels", link_model=QuoteLabelLink)

SQLModel.metadata.create_all(engine)