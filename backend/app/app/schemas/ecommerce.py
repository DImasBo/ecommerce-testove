from datetime import datetime
from decimal import Decimal
from app.models.ecommerce import OrderStatuses
from pydantic import BaseModel


# code for Product
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


# code for Order
class Order(BaseModel):
    id: int
    status: OrderStatuses
    product: Product
    created_date: datetime

    class Config:
        orm_mode = True


class CreateOrder(BaseModel):
    product_id: int


class UpdateOrder(BaseModel):
    status: OrderStatuses
