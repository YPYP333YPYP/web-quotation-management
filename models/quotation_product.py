from dataclasses import dataclass

from sqlalchemy import ForeignKey, Column, Integer, func, DateTime
from sqlalchemy.orm import class_mapper

from core.db.database import Base


@dataclass
class QuotationProduct(Base):
    __tablename__ = 'quotation_product'

    quotation_id = Column('quotation_id', Integer, ForeignKey('quotations.id'), primary_key=True)
    product_id = Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
    price = Column("price", Integer)
    quantity = Column("quantity", Integer)
    created_at = Column("created_at", DateTime, default=func.now(), nullable=False)
    updated_at = Column("updated_at", DateTime, nullable=True, onupdate=func.now())

    def to_dict(self):
        mapper = class_mapper(self.__class__)
        columns = [column.key for column in mapper.columns]
        return {column: getattr(self, column) for column in columns}