from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    price: Decimal


class CreateProduct(ProductBase):
    pass


class Product(ProductBase):
    id: int
    created_date: datetime

    class Config:
        orm_mode = True
