from datetime import datetime, UTC
from sqlmodel import Field, Relationship, SQLModel
from src.database import engine


class User(SQLModel, table=True):
    name: str = Field(alias="username", unique=True, index=True)
    hashed_password: str
    id: int | None = Field(default=None, primary_key=True)


class QuoteLabelLink(SQLModel, table=True):
    quote_id: int | None = Field(
        default=None, foreign_key="quote.id", primary_key=True
    )
    label_id: int | None = Field(
        default=None, foreign_key="label.id", primary_key=True
    )


class Quote(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    labels: list["Label"] = Relationship(
        back_populates="quotes", link_model=QuoteLabelLink
    )


class Label(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    quotes: list["Quote"] = Relationship(
        back_populates="labels", link_model=QuoteLabelLink
    )

SQLModel.metadata.create_all(engine)
