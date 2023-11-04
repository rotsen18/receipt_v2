from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth import crud, schemas
from apps.auth.crud import authenticate_user, create_access_token
from apps.auth.schemas import Token
from apps.core.config import settings
from dependencies import get_db

router = APIRouter()


@router.get('/users/', response_model=list[schemas.UserList])
async def read_users(skip: int = 0, limit: int = 100, email: str = None, db: AsyncSession = Depends(get_db)):
    users = await crud.get_users(db, skip=skip, limit=limit, email=email)
    return users


@router.post('/users/', response_model=schemas.UserDetail, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=[{'msg': 'Email already registered'}])
    created_user = await crud.create_user(db=db, user=user)
    return created_user


@router.get('/users/{user_id}/', response_model=schemas.UserDetail)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': 'User not found'}])
    return db_user


@router.patch('/users/{user_id}/', response_model=schemas.UserDetail)
async def update_user(user_id: int, user: schemas.UserUpdate, db: AsyncSession = Depends(get_db)):
    payload = user.model_dump(exclude_unset=True)
    db_user = await crud.update_user(db, user_id=user_id, payload=payload)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{'msg': 'User not found'}])
    return db_user


@router.post('/token/', response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db)
):
    user = authenticate_user(db=db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}


# @router.get('/users/me/', response_model=User)
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     return current_user
