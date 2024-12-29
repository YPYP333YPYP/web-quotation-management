from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from models import CustomProduct


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


class CustomProductUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    price: Optional[int] = None


def to_custom_product_read(custom_product: CustomProduct):
    return CustomProductRead(
        id=custom_product.id,
        name=custom_product.name,
        image_url=custom_product.image_url,
        description=custom_product.description,
        category=custom_product.category,
        unit=custom_product.unit,
        price=custom_product.price,
        created_at=custom_product.created_at,
        updated_at=custom_product.updated_at
    )