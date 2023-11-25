
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from apps.models import mixins


class Receipt(mixins.IDPrimaryKeyABC, mixins.DateTimeABC):
    __tablename__ = 'receipt'

    name = Column(String, index=True)
    description = Column(String, nullable=True, index=True)
    procedure = Column(String)
    source_link = Column(String, nullable=True)

    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship('User', back_populates='receipts')
    cooking_type_id = Column(Integer, ForeignKey('cooking_type.id'))
    cooking_type = relationship('CookingType', back_populates='receipts')
    components = relationship('ReceiptComponent', back_populates='receipt')


class ReceiptComponent(mixins.IDPrimaryKeyABC, mixins.DateTimeABC):
    __tablename__ = 'receipt_component'

    amount = Column(Float)

    unit_id = Column(Integer, ForeignKey('measure_unit.id'))
    unit = relationship('MeasureUnit', back_populates='components')
    receipt_id = Column(Integer, ForeignKey('receipt.id'))
    receipt = relationship('Receipt', back_populates='components')
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'))
    ingredient = relationship('Ingredient', back_populates='components')
