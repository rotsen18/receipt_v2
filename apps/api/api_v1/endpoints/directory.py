from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps import crud, models
from apps.api import deps
from apps.schemas import directory as schemas

router = APIRouter()


@router.get('/', response_model=List[schemas.IngredientList])
async def read_ingredients(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    ingredients = await crud.ingredient.get_multi(db, skip=skip, limit=limit)
    return ingredients


@router.post('/', response_model=schemas.IngredientCreate)
async def create_ingredient(
    *,
    db: AsyncSession = Depends(deps.get_db),
    ingredient_in: schemas.IngredientCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    ingredient = await crud.ingredient.get_by_name(db, name=ingredient_in.name)
    if ingredient:
        raise HTTPException(
            status_code=400,
            detail='ingredient with this name already exists in the system.',
        )
    ingredient = await crud.ingredient.create(db, obj_in=ingredient_in)
    return ingredient


# @router.patch('/me/', response_model=schemas.UserDetail)
# async def update_user_me(
#     *,
#     db: AsyncSession = Depends(deps.get_db),
#     password: str = Body(None),
#     full_name: str = Body(None),
#     email: EmailStr = Body(None),
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     current_user_data = jsonable_encoder(current_user)
#     user_in = schemas.UserUpdate(**current_user_data)
#     if password is not None:
#         user_in.password = password
#     if full_name is not None:
#         user_in.full_name = full_name
#     if email is not None:
#         user_in.email = email
#     user = await crud.user.update(db, db_obj=current_user, obj_in=user_in)
#     return user
#
#
# @router.get('/me/', response_model=schemas.UserDetail)
# def read_user_me(
#     db: AsyncSession = Depends(deps.get_db),
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     return current_user
#
#
# @router.post('/registration/', response_model=schemas.UserDetail)
# async def register_new_user(
#     *,
#     db: AsyncSession = Depends(deps.get_db),
#     user_in: schemas.UserCreate
# ) -> Any:
#     if not settings.USERS_OPEN_REGISTRATION:
#         raise HTTPException(
#             status_code=403,
#             detail='Open user registration is forbidden on this server',
#         )
#     user = await crud.user.get_by_email(db, email=user_in.email)
#     if user:
#         raise HTTPException(
#             status_code=400,
#             detail='The user with this username already exists in the system',
#         )
#     user = await crud.user.create(db, obj_in=user_in)
#     return user
#
#
# @router.get('/{user_id}/', response_model=schemas.UserDetail)
# async def read_user_by_id(
#     user_id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
#     db: AsyncSession = Depends(deps.get_db),
# ) -> Any:
#     user = await crud.user.get(db, id=user_id)
#     if user == current_user:
#         return user
#     if not crud.user.is_superuser(current_user):
#         raise HTTPException(
#             status_code=400, detail="The user doesn't have enough privileges"
#         )
#     return user
#
#
# @router.patch('/{user_id}/', response_model=schemas.UserDetail)
# async def update_user(
#     *,
#     db: AsyncSession = Depends(deps.get_db),
#     user_id: int,
#     user_in: schemas.UserUpdate,
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     user = await crud.user.get(db, id=user_id)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail='The user with this username does not exist in the system',
#         )
#     user = await crud.user.update(db, db_obj=user, obj_in=user_in)
#     return user
