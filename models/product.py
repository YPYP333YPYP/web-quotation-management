from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func
from core.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


@dataclass
class Product(Base):
    """제품을 관리하는 클래스

    Attributes:
        id (int): 고유한 제품 ID
        name (str): 제품 이름
        category (str): 제품 카테고리
        unit (str): 제품 단위 (예: 개, 박스 등)
        price (int): 제품 가격
        created_at (datetime): 제품 생성일 (자동 기록)
        updated_at (datetime, optional): 제품 수정일 (수정된 경우 기록)
        quotations (List[Quotation]): 제품과 연관된 견적 리스트 (다대다 관계를 표현)
    """
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    category: Mapped[str] = mapped_column(String(255), index=True)
    unit: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(Integer())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.current_timestamp())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    quotations = relationship("Quotation", secondary="quotation_product", back_populates="products")
