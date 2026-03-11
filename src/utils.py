from fastapi import HTTPException
from sqlmodel import Session, select
from src.database import engine

def create_in_db(item):
    with Session(engine) as session :
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
    with Session(engine) as session :
        statement = select(item).offset(offset).limit(25)
        results = session.exec(statement)
        return results.all()

def list_in_db(item, item_id):
    with Session(engine) as session :
        statement = select(item).where(item.id == item_id)
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