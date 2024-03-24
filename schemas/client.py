from pydantic import BaseModel


class ClientRead(BaseModel):
    id: int
    name: str
    region: str