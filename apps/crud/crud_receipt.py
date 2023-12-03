from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from apps.crud.base import CRUDBase
from apps.models.receipt import Receipt, ReceiptComponent
from apps.schemas import ReceiptComponentCreate, ReceiptComponentUpdate, ReceiptCreate, ReceiptDetail, ReceiptUpdate


class CRUDReceipt(CRUDBase[Receipt, ReceiptCreate, ReceiptUpdate]):
    async def create_with_author(
        self, db: AsyncSession, *, obj_in: ReceiptCreate, author_id: int
    ) -> ReceiptDetail:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, author_id=author_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, id: int) -> Optional[ReceiptDetail]:
        query = select(Receipt).options(
            selectinload(Receipt.components).joinedload(ReceiptComponent.unit),
            selectinload(Receipt.components).joinedload(ReceiptComponent.ingredient),
        ).where(Receipt.id == id)
        users = await db.execute(query)
        return users.scalar()

    async def get_multi_by_author(
        self, db: AsyncSession, *, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[Receipt]:
        query = select(self.model).offset(skip).limit(limit).where(self.model.author_id == author_id)
        receipt_list = await db.execute(query)
        return [receipt_row[0] for receipt_row in receipt_list.fetchall()]


class CRUDReceiptComponent(CRUDBase[ReceiptComponent, ReceiptComponentCreate, ReceiptComponentUpdate]):
    async def get_multi_by_receipt(self, db: AsyncSession, *, receipt_id: int) -> List[Receipt]:
        query = select(ReceiptComponent).where(ReceiptComponent.receipt_id == receipt_id)
        receipt_component_list = await db.execute(query)
        return [component[0] for component in receipt_component_list.fetchall()]

    async def create_with_receipt(
        self,
        db: AsyncSession,
        *,
        obj_in: ReceiptComponentCreate,
        receipt_id: int,
    ) -> ReceiptComponent:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, receipt_id=receipt_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


receipt = CRUDReceipt(Receipt)
receipt_component = CRUDReceiptComponent(ReceiptComponent)
