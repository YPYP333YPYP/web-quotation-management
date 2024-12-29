from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func, TEXT
from core.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column


@dataclass
class CustomProduct(Base):
    """자사 제품을 관리하는 클래스

    Attributes:
        id (int): 고유한 제품 ID
        name (str): 제품 이름
        image_url (str, optional): 제품 이미지 URL
        description (str, optional): 제품 설명
        category (str): 제품 카테고리
        unit (str): 제품 단위 (예: 개, 박스 등)
        price (int): 제품 가격
        created_at (datetime): 제품 생성일 (자동 기록)
        updated_at (datetime, optional): 제품 수정일 (수정된 경우 기록)
    """
    __tablename__ = "custom_products"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(TEXT, nullable=True)
    category: Mapped[str] = mapped_column(String(255), index=True)
    unit: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(Integer())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.current_timestamp())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

