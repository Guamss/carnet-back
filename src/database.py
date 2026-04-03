import os
from sqlalchemy.exc import OperationalError
from sqlmodel import create_engine
from dotenv import dotenv_values

config = dotenv_values(".env")

db_user = os.getenv("DB_USER") or config.get("DB_USER")
db_password = os.getenv("DB_PASSWORD") or config.get("DB_PASSWORD")
db_address = os.getenv("DB_ADDRESS") or config.get("DB_ADDRESS")
db_port = os.getenv("DB_PORT") or config.get("DB_PORT")
db_name = os.getenv("DB_NAME") or config.get("DB_NAME")

database_url = (
    f"postgresql://{db_user}:{db_password}@"
    f"{db_address}:{db_port}/{db_name}"
)
engine = create_engine(database_url, echo=True)


def check_db_connexion():
    try:
        with engine.connect() as connection:
            print("Connexion reussie")
    except OperationalError as e:
        print(f"Erreur de connexion à la bdd {e}")
        raise e
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")
        raise e
