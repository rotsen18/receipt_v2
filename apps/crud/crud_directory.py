from sqlalchemy import select

from apps import models
from apps.crud.base import CRUDBase
from apps.schemas.directory import IngredientCreate, IngredientUpdate


class CRUDIngredient(CRUDBase[models.Ingredient, IngredientCreate, IngredientUpdate]):
    async def get_by_name(self, db, *, name: str) -> models.Ingredient:
        query = select(self.model).where(self.model.name == name)
        result = await db.execute(query)
        return result.scalar()


class MeasureUnit(CRUDBase[models.MeasureUnit, IngredientCreate, IngredientUpdate]):
    async def get_by_symbol(self, db, *, symbol: str) -> models.MeasureUnit:
        query = select(self.model).where(self.model.symbol == symbol)
        result = await db.execute(query)
        return result.scalar()


ingredient = CRUDIngredient(models.Ingredient)
measure_unit = MeasureUnit(models.MeasureUnit)
