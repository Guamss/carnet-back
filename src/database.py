from sqlalchemy.exc import OperationalError
from sqlmodel import create_engine
from dotenv import dotenv_values

config = dotenv_values(".env")

database_url = (
    f"postgresql://{config['DB_USER']}:{config['DB_PASSWORD']}@"
    f"{config['DB_ADDRESS']}:{config['DB_PORT']}/{config['DB_NAME']}"
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