from app.crud.base import CRUDBase
from app import models
from app.schemas.ecommerce import Product, CreateProduct


class CRUDProduct(CRUDBase[Product, CreateProduct, CreateProduct]):
    pass


product = CRUDProduct(models.Product)

