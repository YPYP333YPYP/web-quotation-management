from dataclasses import dataclass

from sqlalchemy import ForeignKey, Column, Integer, func, DateTime
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