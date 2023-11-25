from sqlalchemy import JSON, Column, String
from sqlalchemy.orm import relationship

from apps.models import mixins


class Ingredient(mixins.IDPrimaryKeyABC, mixins.NameABC):
    __tablename__ = 'ingredient'

    description = Column(String, default='', index=True)
    product_url = Column(String, default='')
    product_data = Column(JSON, nullable=True, default=dict)

    components = relationship('ReceiptComponent', back_populates='ingredient')


class ReceiptComponentType(mixins.IDPrimaryKeyABC, mixins.NameABC):
    __tablename__ = 'receipt_component_type'


class MeasureUnit(mixins.IDPrimaryKeyABC, mixins.NameABC):
    __tablename__ = 'measure_unit'

    symbol = Column(String, unique=True, index=True)

    components = relationship('ReceiptComponent', back_populates='unit')


class CookingType(mixins.IDPrimaryKeyABC, mixins.NameABC):
    __tablename__ = 'cooking_type'

    receipts = relationship('Receipt', back_populates='cooking_type')
