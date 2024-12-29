from dataclasses import dataclass

from sqlalchemy import ForeignKey, Column, Integer, func, DateTime
from sqlalchemy.orm import class_mapper, relationship

from core.db.database import Base


@dataclass
class QuotationProduct(Base):
    """견적서와 제품 간의 다대다 연관 관계를 관리하는 클래스

    Attributes:
        quotation_id (int): 견적서 ID (ForeignKey로 연결된 quotations 테이블의 ID)
        product_id (int): 제품 ID (ForeignKey로 연결된 products 테이블의 ID)
        price (int): 제품의 수량에 따른 총 가격
        quantity (int): 제품의 수량
        created_at (datetime): 레코드 생성일 (자동 기록)
        updated_at (datetime, optional): 레코드 수정일 (수정된 경우 자동 갱신)
        quotation (Quotation): 연관된 견적서 객체 (다대일 관계를 표현)
        product (Product): 연관된 제품 객체 (다대일 관계를 표현)
    """
    __tablename__ = 'quotation_product'

    quotation_id = Column('quotation_id', Integer, ForeignKey('quotations.id'), primary_key=True)
    product_id = Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
    price = Column("price", Integer)
    quantity = Column("quantity", Integer)
    created_at = Column("created_at", DateTime, default=func.now(), nullable=False)
    updated_at = Column("updated_at", DateTime, nullable=True, onupdate=func.now())

    quotation = relationship("Quotation", lazy='joined')
    product = relationship("Product", lazy='joined')

    def to_dict(self):
        mapper = class_mapper(self.__class__)
        columns = [column.key for column in mapper.columns]
        return {column: getattr(self, column) for column in columns}