from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app import models
from app.schemas.ecommerce import (
    Product, CreateProduct,
    Order, UpdateOrder, CreateOrder,
    Bill, CreateBill, UpdateBill
)


class CRUDProduct(CRUDBase[Product, CreateProduct, CreateProduct]):
    pass


class CRUDOrder(CRUDBase[Order, CreateOrder, UpdateOrder]):
    pass


product = CRUDProduct(models.Product)
order = CRUDOrder(models.Order)


class CRUDBill(CRUDBase[Bill, CreateBill, UpdateBill]):

    def create(self, db: Session, *, obj_in: CreateBill) -> models.Bill:
        order_obj = order.get(db, id=obj_in.order_id)

        if not obj_in.product_name:
            obj_in.product_name = order_obj.product.name

        if not obj_in.product_price:
            obj_in.product_price = order_obj.product.price

        if not obj_in.amount:
            obj_in.amount = order_obj.product.price

        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore

        # set default order_created_date
        db_obj.order_created_date = order_obj.created_date

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

bill = CRUDBill(models.Bill)
