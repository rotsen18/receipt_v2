from typing import Any, Dict, Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps import models
from apps.core.security import get_password_hash, verify_password
from apps.crud.base import CRUDBase
from apps.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[models.User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[models.User]:
        query = select(self.model).where(self.model.email == email)
        result = await db.execute(query)
        return result.scalar()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> models.User:
        db_obj = models.User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: models.User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> models.User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if update_data.get('password'):
            hashed_password = get_password_hash(update_data['password'])
            del update_data['password']
            update_data['password'] = hashed_password
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> Optional[models.User]:
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    @staticmethod
    def is_active(user: models.User) -> bool:
        return user.is_active

    @staticmethod
    def is_superuser(user: models.User) -> bool:
        return user.user_type == models.UserTypeEnum.ADMIN


user = CRUDUser(models.User)
