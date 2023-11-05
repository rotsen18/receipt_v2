from fastapi import FastAPI

from apps.api.api_v1.api import api_router
from apps.core.config import settings

app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}
