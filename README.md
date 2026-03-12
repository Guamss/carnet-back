# Template FastAPI

## Pour installer le projet
```
poetry install
```
créer au préalable un `.env` à la racine du projet
```
docker compose up -d
```

## Lancer le projet
```
poetry run fastapi dev src/main.py
```

## Générer une secret key 
```
openssl rand -hex 32
```
## TO DO LIST :
- [ ] Faire fonctionner le Many-to-Many
- [ ] Faire l'Authentification et le hash du password
- [ ] Potentiel refacto du code
- [ ] Evolutivité (Alembic ?) (Non obligatoire si projet fixe) 