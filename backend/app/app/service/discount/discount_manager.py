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
    list_discount = (DiscountProductMoreOneMonth, )

    @classmethod
    def check_product(cls, product: models.Product):
        for class_checker_discount in cls.list_discount:
            checker_discount = class_checker_discount(product)
            if checker_discount.check():
                discount = checker_discount.create_discount()
                product.add_discount(discount)

        return product

    @classmethod
    def check_products(cls, products: List[models.Product]) -> List[models.Product]:
        for product in products:
            cls.check_product(product)
        print(products)
        return products
