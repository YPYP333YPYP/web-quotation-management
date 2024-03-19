from pydantic import BaseModel


class QuotationCreate(BaseModel):
    client_id: int
