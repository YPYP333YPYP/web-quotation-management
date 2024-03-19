from sqlalchemy import ForeignKey, Table, Column, Integer
from core.db.database import Base


quotation_product_table = Table('quotation_product', Base.metadata,
    Column('quotation_id', Integer, ForeignKey('quotations.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)