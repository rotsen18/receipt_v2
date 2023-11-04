from datetime import datetime, timedelta
from typing import Annotated

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth import models, schemas
from apps.core.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def hash_password(password: str):
    """Generates a hashed version of the provided password."""
    pw = bytes(password, 'utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt).decode()


async def get_user(db: AsyncSession, user_id: int):
    query = select(models.User).where(models.User.id == user_id)
    users = await db.execute(query)
    return users.scalar()


async def get_user_by_email(db: AsyncSession, email: str):
    query = select(models.User).where(models.User.email == email)
    users = await db.execute(query)
    return users.first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100, email: str = None):
    query = select(models.User).offset(skip).limit(limit)
    if email:
        query = query.where(models.User.email.icontains(email))
    user_list = await db.execute(query)
    return [user[0] for user in user_list.fetchall()]


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    user_data = models.User(email=user.email, password=hashed_password, telegram_id=user.telegram_id)
    db.add(user_data)
    await db.commit()
    await db.refresh(user_data)
    return user_data


async def update_user(db: AsyncSession, user_id: int, payload: dict):
    query = update(models.User).where(models.User.id == user_id).values(**payload)
    await db.execute(query)
    await db.commit()
    return await get_user(db, user_id)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: AsyncSession, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
        token_obj = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=token_obj.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[schemas.UserDetail, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user
