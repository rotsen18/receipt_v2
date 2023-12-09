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
    name = ingredient_in.name
    ingredient = await crud.ingredient.get_by_name(db, name=name)
    if ingredient:
        raise HTTPException(
            status_code=400,
            detail=f'Ingredient with "{name}" name already exists in the system.',
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


@router.get('/measure_units/', response_model=List[schemas.MeasureUnitList])
async def read_measure_units(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    measure_units = await crud.measure_unit.get_multi(db, skip=skip, limit=limit)
    return measure_units


@router.post('/measure_units/', response_model=schemas.MeasureUnitCreate)
async def create_measure_unit(
    *,
    db: AsyncSession = Depends(deps.get_db),
    measure_unit_in: schemas.MeasureUnitCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    symbol = measure_unit_in.symbol
    measure_unit = await crud.measure_unit.get_by_symbol(db, symbol=symbol)
    if measure_unit:
        raise HTTPException(
            status_code=400,
            detail=f'Measure unit with "{symbol}" symbol already exists in the system.',
        )
    measure_unit = await crud.measure_unit.create(db, obj_in=measure_unit_in)
    return measure_unit


@router.patch('/measure_units/{measure_unit_id}/', response_model=schemas.MeasureUnitDetail)
async def update_measure_unit(
    *,
    db: AsyncSession = Depends(deps.get_db),
    measure_unit_id: int,
    measure_unit_in: schemas.MeasureUnitUpdate,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    measure_unit = await crud.measure_unit.get(db, id=measure_unit_id)
    if not measure_unit:
        raise HTTPException(
            status_code=404,
            detail='The measure unit with this id does not exist in the system',
        )
    updated_measure_unit = await crud.measure_unit.update(db, db_obj=measure_unit, obj_in=measure_unit_in)
    return updated_measure_unit


@router.get('/cooking_types/', response_model=List[schemas.CookingTypeList])
async def read_cooking_types(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    cooking_types = await crud.cooking_type.get_multi(db, skip=skip, limit=limit)
    return cooking_types


@router.get('/cooking_types/{cooking_type_id}/', response_model=schemas.CookingTypeDetail)
async def read_cooking_type(
    cooking_type_id: int,
    db: AsyncSession = Depends(deps.get_db),
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    cooking_types = await crud.cooking_type.get(db, id=cooking_type_id)
    if not cooking_types:
        raise HTTPException(
            status_code=404,
            detail=f'Cooking type with with this id={cooking_type_id} does not exist.',
        )
    return cooking_types


@router.post('/cooking_types/', response_model=schemas.CookingTypeDetail)
async def create_cooking_type(
    *,
    db: AsyncSession = Depends(deps.get_db),
    cooking_type_in: schemas.CookingTypeCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    name = cooking_type_in.name
    cooking_type = await crud.cooking_type.get_by_name(db, name=name)
    if cooking_type:
        raise HTTPException(
            status_code=400,
            detail=f'Cooking type with "{name}" name already exists in the system.',
        )
    cooking_type = await crud.cooking_type.create(db, obj_in=cooking_type_in)
    return cooking_type


@router.patch('/cooking_types/{cooking_type_id}/', response_model=schemas.CookingTypeDetail)
async def update_cooking_type(
    *,
    db: AsyncSession = Depends(deps.get_db),
    cooking_type_id: int,
    cooking_type_in: schemas.CookingTypeUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    cooking_type = await crud.cooking_type.get(db, id=cooking_type_id)
    if not cooking_type:
        raise HTTPException(
            status_code=404,
            detail='The cooking type with this id does not exist in the system',
        )
    updated_cooking_type = await crud.cooking_type.update(db, db_obj=cooking_type, obj_in=cooking_type_in)
    return updated_cooking_type


@router.get('/culinary_categories/', response_model=List[schemas.CulinaryCategoryList])
async def read_culinary_categories(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    culinary_categories = await crud.culinary_category.get_multi(db, skip=skip, limit=limit)
    return culinary_categories


@router.get('/culinary_categories/{culinary_category_id}/', response_model=schemas.CulinaryCategoryList)
async def read_culinary_category(
    culinary_category_id: int,
    db: AsyncSession = Depends(deps.get_db),
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    culinary_category = await crud.culinary_category.get(db, id=culinary_category_id)
    if not culinary_category:
        raise HTTPException(
            status_code=404,
            detail=f'Ingredient with with this id={culinary_category_id} does not exist.',
        )
    return culinary_category


@router.post('/culinary_categories/', response_model=schemas.CulinaryCategoryList)
async def create_culinary_category(
    *,
    db: AsyncSession = Depends(deps.get_db),
    culinary_category_in: schemas.CulinaryCategoryCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    name = culinary_category_in.name
    culinary_category = await crud.culinary_category.get_by_name(db, name=name)
    if culinary_category:
        raise HTTPException(
            status_code=400,
            detail=f'Culinary category with "{name}" name already exists in the system.',
        )
    culinary_category = await crud.culinary_category.create(db, obj_in=culinary_category_in)
    return culinary_category


@router.patch('/culinary_categories/{culinary_category_id}/', response_model=schemas.CulinaryCategoryList)
async def update_culinary_category(
    *,
    db: AsyncSession = Depends(deps.get_db),
    culinary_category_id: int,
    culinary_category_in: schemas.CulinaryCategoryUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    culinary_category = await crud.culinary_category.get(db, id=culinary_category_id)
    if not culinary_category:
        raise HTTPException(
            status_code=404,
            detail='The culinary category with this id does not exist in the system',
        )
    updated_culinary_category = await crud.culinary_category.update(
        db,
        db_obj=culinary_category,
        obj_in=culinary_category_in,
    )
    return updated_culinary_category
