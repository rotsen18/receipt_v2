from typing import Optional

from pydantic import BaseModel

from apps.schemas.directory import IngredientNested, MeasureUnitNested


class ReceiptComponentBase(BaseModel):
    amount: float
    unit_id: int


class ReceiptComponentCreate(ReceiptComponentBase):
    ingredient_id: int
    receipt_id: int


class ReceiptComponentUpdate(ReceiptComponentBase):
    amount: Optional[float] = None
    unit_id: Optional[int] = None


class ReceiptComponentDetail(ReceiptComponentBase):
    class Config:
        from_attributes = True


class ReceiptComponentList(ReceiptComponentBase):
    ingredient_id: int

    class Config:
        from_attributes = True


class ReceiptComponentNested(ReceiptComponentBase):
    ingredient: IngredientNested
    unit: MeasureUnitNested

    class Config:
        from_attributes = True


class ReceiptBase(BaseModel):
    name: str
    description: Optional[str] = None


class ReceiptCreate(ReceiptBase):
    procedure: str
    source_link: Optional[str] = None


class ReceiptUpdate(ReceiptBase):
    name: Optional[str] = None
    description: Optional[str] = None
    procedure: Optional[str] = None
    source_link: Optional[str] = None


class ReceiptDetail(ReceiptBase):
    id: int
    name: str
    description: Optional[str] = None
    procedure: str
    source_link: Optional[str] = None
    components: list[ReceiptComponentNested] = []
    author_id: int
    cooking_type_id: Optional[int]
    category_id: Optional[int]

    class Config:
        from_attributes = True


class ReceiptList(ReceiptBase):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True
