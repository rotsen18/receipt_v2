from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from apps.api.api_v1.api import api_router
from apps.core.config import settings

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
    docs_url=settings.SWAGGER_URL,
    openapi_url=f'{settings.SWAGGER_URL}/openapi.json',
)
app.include_router(api_router, prefix=settings.API_V1_STR)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def health_check():
    return {
        'name': settings.PROJECT_NAME,
    }
