from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from typing_extensions import Annotated

import config
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/info')
async def info(settings: Annotated[config.Settings, Depends(config.get_settings)]):
    return {
        'database_url': settings.database_url,
    }


@app.get('/users/', response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
