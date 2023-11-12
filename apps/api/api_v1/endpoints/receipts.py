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


@router.get('/{id}', response_model=schemas.ReceiptDetail)
async def read_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    receipt = await crud.receipt.get(db=db, id=id)
    if not receipt:
        raise HTTPException(status_code=404, detail='Receipt not found')
    return receipt
