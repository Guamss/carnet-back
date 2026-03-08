from src import database
from typing import Union
from src.config import ORIGINS, TAGS_METADATA, DESCRIPTION
from uuid import uuid4, UUID
from src.models.person import PersonIn, PersonOut
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(
    openapi_tags=TAGS_METADATA,
    title="API template",
    description=DESCRIPTION,
    summary="La documentation swagger du template d'API",
    version="0.0.1",
    terms_of_service="http://example.com/terms/"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
    Section Persons
"""
@app.get("/persons", tags=["Persons"], response_model=list[PersonOut])
def list_persons():
    return [PersonOut(
        id=uuid4(), 
        name="alexis", 
        age=20,
        address="mlf")]

@app.get("/persons/{id}", tags=["Persons"], response_model=PersonOut)
def get_person_by_id(id: UUID):
    return PersonOut(
        id=id, 
        name="Baptiste", 
        age=20,
        address="baise pascal")

@app.post("/persons", tags=["Persons"], response_model=PersonOut, status_code=201)
def create_person(person: PersonIn):
    if person.age < 1: raise HTTPException(status_code=400, detail="Age non valide")
    return PersonOut(
        id=uuid4(),
        name=person.name,
        age=person.age,
        address=person.address)

@app.put("/persons/{id}", tags=["Persons"], response_model=PersonOut)
def update_person(id: UUID, updated_person: PersonIn):
    if updated_person.age < 1: raise HTTPException(status_code=400, detail="Age non valide")
    return PersonOut(
        id=id,
        name=updated_person.name,
        age=updated_person.age,
        address=updated_person.address)

@app.delete("/persons/{id}", tags=["Persons"])
def delete_person(id: UUID):
    return

"""
    Section items
"""
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}