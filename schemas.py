from pydantic import BaseModel


class Data(BaseModel):
    phone: str
    address: str