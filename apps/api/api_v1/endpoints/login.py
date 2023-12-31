from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from apps import crud, models, schemas
from apps.api import deps
from apps.core import security
from apps.core.config import settings
from apps.core.security import get_password_hash
from apps.utils import generate_password_reset_token, send_reset_password_email, verify_password_reset_token

router = APIRouter()


@router.post('/login/access-token/', response_model=schemas.Token)
async def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = await crud.user.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail='Incorrect email or password')
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail='Inactive user')
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        'access_token': security.create_access_token(user.id, expires_delta=access_token_expires),
        'token_type': 'bearer',
    }


@router.post('/login/test-token/', response_model=schemas.UserDetail)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    return current_user


@router.post('/password-recovery/{email}/', response_model=schemas.Msg)
def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
    user = crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail='The user with this username does not exist in the system.',
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {'msg': 'Password recovery email sent'}


@router.post('/reset-password/', response_model=schemas.Msg)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
) -> Any:
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail='Invalid token')
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail='The user with this username does not exist in the system.',
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail='Inactive user')
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return {'msg': 'Password updated successfully'}
