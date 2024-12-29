from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from core.db.database import Base


@dataclass
class PastOrder(Base):
    """즐겨찾기를 관리하는 클래스

    Attributes:
        id (int): 고유한 즐겨찾기 ID
        client_id (int): 고객 ID (ForeignKey로 연결된 clients 테이블의 ID)
        name (str): 즐겨찾기 이름
        product_ids (str): 즐겨찾기에 포함된 제품 ID 목록 (쉼표로 구분된 문자열)
        created_at (datetime): 즐겨찾기 생성일 (자동 기록)
        updated_at (datetime): 즐겨찾기 수정일 (수정된 경우 자동 갱신)
    """
    __tablename__ = "past_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"), index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    product_ids: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())
