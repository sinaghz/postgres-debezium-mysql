from typing import List

from pydantic import BaseModel


class Shipment(BaseModel):
    id: int
    date_created: str
    status: str
    order_id: int

    class Config:
        orm_mode = True


class Order(BaseModel):
    id: int
    price: str
    status: str
    date_created: str
    shipments: List[Shipment] = []

    class Config:
        orm_mode = True
