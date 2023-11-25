from typing import Optional

from pydantic import BaseModel


class IngredientBase(BaseModel):
    name: str
    description: Optional[str] = None


class IngredientCreate(IngredientBase):
    product_url: Optional[str] = None
    product_data: Optional[dict] = None


class IngredientUpdate(IngredientBase):
    name: Optional[str] = None
    product_url: Optional[str] = None
    product_data: Optional[dict] = None


class IngredientNested(IngredientBase):
    pass


class IngredientList(IngredientBase):
    id: int
    product_url: Optional[str] = None
    product_data: Optional[dict] = None


class IngredientDetail(IngredientBase):
    id: int
    product_url: Optional[str] = None
    product_data: Optional[dict] = None


class MeasureUnitBase(BaseModel):
    name: str
    symbol: str


class MeasureUnitCreate(MeasureUnitBase):
    pass


class MeasureUnitUpdate(MeasureUnitBase):
    name: Optional[str] = None
    symbol: Optional[str] = None


class MeasureUnitNested(MeasureUnitBase):
    pass


class MeasureUnitList(MeasureUnitBase):
    id: int


class MeasureUnitDetail(MeasureUnitBase):
    id: int


class CookingTypeBase(BaseModel):
    name: str


class CookingTypeCreate(CookingTypeBase):
    pass


class CookingTypeUpdate(CookingTypeBase):
    pass


class CookingTypeList(CookingTypeBase):
    id: int


class CookingTypeDetail(CookingTypeBase):
    id: int
