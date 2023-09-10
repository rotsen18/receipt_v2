from fastapi import APIRouter

from apps.auth.routers import router as auth_router

api_router = APIRouter(prefix='/api/v1')


api_router.include_router(auth_router, prefix='/auth', tags=['auth'])
