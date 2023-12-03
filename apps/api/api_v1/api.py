from fastapi import APIRouter

from apps.api.api_v1.endpoints import directory, login, receipts, users, utils

api_router = APIRouter()
api_router.include_router(login.router, tags=['login'])
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(utils.router, prefix='/utils', tags=['utils'])
api_router.include_router(receipts.router, prefix='/receipts', tags=['receipt'])
api_router.include_router(directory.router, prefix='/directory', tags=['directory'])
