from dataclasses import dataclass

from sqlalchemy import String, Text
from core.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


@dataclass
class Client(Base):
    """거래처 정보를 관리하는 클래스

    Attributes:
        id (int): 고유한 거래처 ID
        name (str): 거래처 이름
        region (str, optional): 거래처 지역
        address (str): 거래처 주소
        comment (str, optional): 거래처에 대한 추가 정보 또는 비고
        quotations (List[Quotation]): 거래처의 견적서 리스트
        users (List[User]): 거래처와 연관된 유저 정보 리스트
    """
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    region: Mapped[str] = mapped_column(String(255), nullable=True)
    address: Mapped[str] = mapped_column(String(255))
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    quotations = relationship("Quotation", back_populates="client")
    users = relationship("User", back_populates="client")


