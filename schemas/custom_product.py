from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CustomProductCreate(BaseModel):
    name: str
    image_url: Optional[str] = None
    description: Optional[str] = None
    category: str
    unit: str
    price: int


class CustomProductRead(BaseModel):
    id: int
    name: str
    image_url: Optional[str] = None
    description: Optional[str] = None
    category: str
    unit: str
    price: int
    created_at: datetime
    updated_at: Optional[datetime] = None