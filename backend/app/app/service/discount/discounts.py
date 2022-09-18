from calendar import monthrange
from datetime import datetime, timedelta
from app.schemas import Discount
from decimal import Decimal
from pydantic import BaseModel, Field

from app import models


def calculate_discount_price(discount, price):
    return price * (discount / 100)


class DiscountCheckerBase:
    """
    Base Class For create item Discount Checker values  for Product
    """
    discount: Discount

    @staticmethod
    def check(product: models.Product):
        pass

    def get_schema(self, product_price):
        pass


class DiscountProductMoreOneMonth(DiscountCheckerBase):
    """
    First implement Discount when Product more one Month
    """
    discount = Discount(
        discount=20,
        name="More than one per Month"
    )

    def check(self, product: models.Product):
        _, count_day = monthrange(self.created_date.year, self.created_date.month)
        if datetime.now() - self.created_date > timedelta(days=count_day):
            return True

    def get_discount_with_new_price(self, product_price):
        discount_price = calculate_discount_price(product_price)
        self.discount.discount_price = discount_price
        return self.discount
