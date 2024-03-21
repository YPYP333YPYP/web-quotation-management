from pydantic import BaseModel


class QuotationCreate(BaseModel):
    client_id: int


class QuotationAdd(BaseModel):
    quotation_id: int
    product_id: int
    quantity: int