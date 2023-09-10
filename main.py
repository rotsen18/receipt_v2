from fastapi import FastAPI

from api import api_router
from apps.auth import models
from apps.database.core import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router)


@app.get('/info/')
async def info():
    return {
        'status': 'ok',
    }
