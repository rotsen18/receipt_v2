from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps import crud, models
from apps.api import deps
from apps.schemas import directory as schemas

router = APIRouter()


@router.get('/ingredients/', response_model=List[schemas.IngredientList])
async def read_ingredients(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    ingredients = await crud.ingredient.get_multi(db, skip=skip, limit=limit)
    return ingredients


@router.post('/ingredients/', response_model=schemas.IngredientCreate)
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


@router.get('/ingredients/{ingredient_id}/', response_model=schemas.IngredientDetail)
async def read_ingredient_by_id(
    ingredient_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    ingredient = await crud.ingredient.get(db, id=ingredient_id)
    return ingredient


@router.patch('/ingredients/{ingredient_id}/', response_model=schemas.IngredientDetail)
async def update_ingredient(
    *,
    db: AsyncSession = Depends(deps.get_db),
    ingredient_id: int,
    ingredient_in: schemas.IngredientUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    ingredient = await crud.ingredient.get(db, id=ingredient_id)
    if not ingredient:
        raise HTTPException(
            status_code=404,
            detail='The ingredient with this id does not exist in the system',
        )
    updated_ingredient = await crud.ingredient.update(db, db_obj=ingredient, obj_in=ingredient_in)
    return updated_ingredient
