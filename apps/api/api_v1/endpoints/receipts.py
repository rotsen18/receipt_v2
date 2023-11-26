from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from apps import crud, models, schemas
from apps.api import deps

router = APIRouter()


@router.get('/', response_model=List[schemas.ReceiptList])
async def read_receipts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    return await crud.receipt.get_multi(db, skip=skip, limit=limit)


@router.post('/', response_model=schemas.ReceiptDetail)
async def create_receipt(
    *,
    db: Session = Depends(deps.get_db),
    receipt_in: schemas.ReceiptCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    item = await crud.receipt.create_with_author(db=db, obj_in=receipt_in, author_id=current_user.id)
    return item


@router.get('/{receipt_id}', response_model=schemas.ReceiptDetail)
async def read_item(
    *,
    db: Session = Depends(deps.get_db),
    receipt_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    receipt = await crud.receipt.get(db=db, id=receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail='Receipt not found')
    return receipt


@router.patch('/{receipt_id}', response_model=schemas.ReceiptDetail)
async def update_receipt(
    *,
    db: Session = Depends(deps.get_db),
    receipt_id: int,
    receipt_in: schemas.ReceiptUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    receipt = await crud.receipt.get(db=db, id=receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail='Receipt not found')
    receipt = await crud.receipt.update(db=db, db_obj=receipt, obj_in=receipt_in)
    return receipt


@router.post('/{receipt_id}/components', response_model=schemas.ReceiptComponentDetail)
async def create_receipt_component(
    *,
    db: Session = Depends(deps.get_db),
    receipt_id: int,
    component_in: schemas.ReceiptComponentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    receipt = await crud.receipt.get(db=db, id=receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail='Receipt not found')
    component = await crud.receipt_component.create_with_receipt(db=db, obj_in=component_in, receipt_id=receipt_id)
    return component


@router.patch('/components/{component_id}', response_model=schemas.ReceiptComponentDetail)
async def update_receipt_component(
    *,
    db: Session = Depends(deps.get_db),
    component_id: int,
    component_in: schemas.ReceiptComponentUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    component = await crud.receipt_component.get(db=db, id=component_id)
    if not component:
        raise HTTPException(status_code=404, detail='Receipt component not found')
    component = await crud.receipt_component.update(db=db, db_obj=component, obj_in=component_in)
    return component


@router.delete('/components/{component_id}')
async def delete_receipt_component(
    *,
    db: Session = Depends(deps.get_db),
    component_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    component = await crud.receipt_component.get(db=db, id=component_id)
    if not component:
        raise HTTPException(status_code=404, detail='Receipt component not found')
    await crud.receipt_component.remove(db=db, id=component_id)
    return {'message': 'Receipt component deleted'}
