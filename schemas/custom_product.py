from typing import Optional

from pydantic import BaseModel


class CustomProductCreate(BaseModel):
    name: str
    image_url: Optional[str] = None
    description: Optional[str] = None
    category: str
    unit: str
    price: int