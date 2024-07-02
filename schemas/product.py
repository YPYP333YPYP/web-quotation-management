from pydantic import BaseModel

from models import Product


class ProductRead(BaseModel):
    id: int
    category: str
    name: str
    unit: str
    price: float


class ProductCreate(BaseModel):
    category: str
    name: str
    unit: str
    price: float


def to_product_read(product: Product) -> ProductRead:
    return ProductRead(
        id=product.id,
        category=product.category,
        name=product.name,
        unit=product.unit,
        price=product.price
    )
