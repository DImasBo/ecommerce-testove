from app.crud.base import CRUDBase
from app import models
from app.schemas.ecommerce import (
    Product, CreateProduct,
    Order, UpdateOrder, CreateOrder
)


class CRUDProduct(CRUDBase[Product, CreateProduct, CreateProduct]):
    pass


class CRUDOrder(CRUDBase[Order, CreateOrder, UpdateOrder]):
    pass


product = CRUDProduct(models.Product)
order = CRUDOrder(models.Order)

