from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import String, DateTime, func, Boolean, ForeignKey
from core.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


@dataclass
class User(Base):
    """사용자를 관리하는 클래스

    Attributes:
        id (int): 고유한 사용자 ID
        email (str): 사용자 이메일 주소
        hashed_password (str): 암호화된 비밀번호
        social (str, optional): 소셜 계정 정보
        created_at (datetime): 사용자 계정 생성일 (자동 기록)
        updated_at (datetime, optional): 사용자 계정 수정일 (수정된 경우 기록)
        is_active (bool): 사용자 활성 상태 (기본값: True)
        is_admin (bool): 관리자 여부 (기본값: False)
        client_id (int, optional): 고객 ID (ForeignKey로 연결된 clients 테이블의 ID)
        client (Client): 사용자와 연관된 고객 객체 (다대일 관계를 표현)
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    social: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.current_timestamp())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'), nullable=True)

    client = relationship("Client", back_populates="users")
