from datetime import datetime
from enum import Enum

from sqlalchemy import Integer, String, Column, Numeric, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    price = Column(Numeric, nullable=False)
    created_date = Column(
        DateTime, default=datetime.now, server_default=func.now()
    )
    orders = relationship("Order", back_populates="product")

    _discounts: list = []

    @property
    def discounts(self):
        return [
            {
                "discount": 20,
                "name": "test",
                "discount_price": 20
            }
        ]

    def add_discount(self, discount):
        self._discounts.append(discount)


class OrderStatuses(str, Enum):
    created = "CREATED"
    in_progress = "IN PROGRESS"
    ready = "READY"


class Order(Base):
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product", back_populates="orders")
    status = Column(String, default=OrderStatuses.created.value, nullable=False)
    created_date = Column(
        DateTime, default=datetime.now, server_default=func.now()
    )


class BillStatuses(str, Enum):
    awaiting = "awaiting"
    paid = "paid"
    declined = "declined"


class Bill(Base):
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    product_price = Column(Numeric, nullable=False)
    created_order_date = Column(DateTime)
    created_date = Column(
        DateTime, default=datetime.now, server_default=func.now()
    )
    status = Column(String, default=BillStatuses.awaiting.value)
