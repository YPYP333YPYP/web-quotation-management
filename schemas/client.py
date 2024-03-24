from pydantic import BaseModel


class ClientRead(BaseModel):
    id: int
    name: str
    region: str


class ClientCreate(BaseModel):
    name: str
    region: str

class ClientUpdate(BaseModel):
    name: str
    region: str