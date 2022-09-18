from datetime import datetime
from decimal import Decimal

from typing import Optional, List

from app.models.ecommerce import OrderStatuses, BillStatuses
from pydantic import BaseModel, Field, validator


# code for Product
class ProductBase(BaseModel):
    name: str
    price: Decimal


class CreateProduct(ProductBase):
    pass


class Discount(BaseModel):
    name: str
    discount: int = Field(1, gt=1, lt=100)
    discount_price: Decimal


class Product(ProductBase):
    id: int
    created_date: datetime
    discounts: Optional[List[Discount]] = None

    @validator("discounts")
    def format_discounts(cls, value):
        if not value:
            return None
        return value

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


class CreateBill(BaseModel):
    order_id: int

    product_name: Optional[str]
    product_price: Optional[Decimal]

    amount: Optional[Decimal]
    comment: Optional[str]


class Bill(BaseModel):
    id: int
    order: Order
    order_created_date: datetime
    amount: Decimal
    status: BillStatuses
    product_name: Optional[str]
    product_price: Optional[Decimal]
    created_date: datetime

    class Config:
        orm_mode = True


class UpdateBill(BaseModel):
    status: BillStatuses
    comment: Optional[str]
