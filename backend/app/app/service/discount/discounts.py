from calendar import monthrange
from datetime import datetime, timedelta
from app.schemas import Discount
from decimal import Decimal
from pydantic import BaseModel, Field

from app import models


def calculate_discount_price(discount, price) -> float:
    return price - price * (discount / Decimal(100))


class DiscountCheckerBase:
    """
    Base Class For create item Discount Checker values  for Product
    """
    discount: Discount

    def __init__(self, product: models.Product):
        self.product = product

    def check(self):
        pass

    def create_discount(self):
        pass


class DiscountProductMoreOneMonth(DiscountCheckerBase):
    """
    First implement Discount when Product more one Month
    """
    discount = Discount(
        discount=20,
        name="More than one per Month"
    )
    # describe default data for discount

    def check(self) -> bool:
        _, count_day = monthrange(self.product.created_date.year, self.product.created_date.month)
        if datetime.now() - self.product.created_date > timedelta(days=count_day):
            return True
        return False

    def create_discount(self):
        discount_price = calculate_discount_price(self.discount.discount, self.product.price)
        self.discount.discount_price = discount_price
        return self.discount
