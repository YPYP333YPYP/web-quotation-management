from pydantic import BaseModel

from models import Product


class ProductRead(BaseModel):
    id: int
    category: str
    name: str
    unit: str
    price: float

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    category: str
    name: str
    unit: str
    price: float


class ProductCount(BaseModel):
    id: int
    category: str
    name: str
    unit: str
    count: int


def to_product_read(product: Product) -> ProductRead:
    return ProductRead(
        id=product.id,
        category=product.category,
        name=product.name,
        unit=product.unit,
        price=product.price
    )


def to_product_count(product: ProductCount, count: int) -> ProductCount:
    return ProductCount(
        id=product.id,
        category=product.category,
        name=product.name,
        unit=product.unit,
        count=count
    )
