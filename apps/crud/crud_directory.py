from sqlalchemy import select

from apps import models
from apps.crud.base import CRUDBase
from apps.schemas.directory import IngredientCreate, IngredientUpdate


class CRUDIngredient(CRUDBase[models.Ingredient, IngredientCreate, IngredientUpdate]):
    async def get_by_name(self, db, *, name: str) -> models.Ingredient:
        query = select(self.model).where(self.model.name == name)
        result = await db.execute(query)
        return result.scalar()


ingredient = CRUDIngredient(models.Ingredient)
