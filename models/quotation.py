from dataclasses import dataclass
from datetime import datetime, date

from sqlalchemy import ForeignKey, Integer, DateTime, func, String, Text, Date
from core.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship, class_mapper


@dataclass
class Quotation(Base):
    """견적서(Quotation)를 관리하는 클래스

    Attributes:
        id (int): 고유한 견적서 ID
        client_id (int): 고객 ID (ForeignKey로 연결된 clients 테이블의 ID)
        name (str): 견적서 이름
        total_price (int): 총 견적 금액
        status (str): 견적 상태 (기본값: "CREATED")
        input_date (date): 견적서 요청일
        created_at (datetime): 견적 생성일 (자동 기록)
        updated_at (datetime, optional): 견적 수정일 (수정된 경우 기록)
        particulars (str, optional): 세부사항 또는 비고
        products (List[Product]): 견적과 연관된 제품 리스트 (다대다 관계를 표현)
        client (Client): 견적과 연관된 고객 객체 (다대일 관계를 표현)
    """
    __tablename__ = 'quotations'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    client_id = mapped_column(Integer, ForeignKey('clients.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    total_price: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="CREATED", nullable=False)
    input_date: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.current_timestamp())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    particulars: Mapped[str] = mapped_column(Text, nullable=True)

    products = relationship("Product", secondary="quotation_product", back_populates="quotations")
    client = relationship("Client", back_populates="quotations")

    def to_dict(self):
        mapper = class_mapper(self.__class__)
        columns = [column.key for column in mapper.columns]
        return {column: getattr(self, column) for column in columns}

