from typing import List

from app import models
from .discounts import DiscountProductMoreOneMonth
from app.schemas import Discount


class Singleton(type):
    _instances = None

    def __call__(cls, *args, **kwargs):
        if not cls._instances:
            cls._instances = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances


class DiscountManager(metaclass=Singleton):
    """
    Manager Check for Any Discount on Products
    """
    list_discount = [DiscountProductMoreOneMonth, ]

    def check_product(self, product: models.Product):
        for class_checker_discount in self.list_discount:
            checker_discount = class_checker_discount()
            if checker_discount.check(product):
                discount = checker_discount.get_discount_with_new_price(
                    product_price=product.price
                )
                product.add_discount(discount)

        return product

    def check_products(self, products: List[models.Product]) -> List[models.Product]:
        for product in products:
            self.check_product(product)
        print(products)
        return products
