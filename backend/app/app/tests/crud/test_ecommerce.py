import pytest
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, schemas, models


# Tests CRUD Order
def test_create_order(db: Session, test_product) -> None:
    order = crud.order.create(db, obj_in=schemas.CreateOrder(
        product_id=test_product.id
    ))

    assert order.product == test_product
    assert order.id is not None
    assert order.status == models.OrderStatuses.created.value


def test_update_order_to_in_progress_and_ready(db: Session, test_order_created) -> models.Order:
    assert test_order_created.status == models.OrderStatuses.created.value
    order = crud.order.update(db, db_obj=test_order_created, obj_in=schemas.UpdateOrder(
        status=models.OrderStatuses.in_progress.value
    ))

    # status to in progress
    assert order.status == models.OrderStatuses.in_progress.value
    order = crud.order.update(db, db_obj=order, obj_in=schemas.UpdateOrder(
        status=models.OrderStatuses.ready.value
    ))

    # status to ready
    assert order.status == models.OrderStatuses.ready.value


def test_create_update_bill_for_order(db: Session, test_order_ready) -> None:
    bill = crud.bill.create(db, obj_in=schemas.CreateBill(
        order_id=test_order_ready.id,
    ))

    assert bill.order_id == test_order_ready.id
    assert bill.status == models.BillStatuses.awaiting.value
    assert bill.order_created_date == test_order_ready.created_date

    bill = crud.bill.update(db, db_obj=bill, obj_in=schemas.UpdateBill(
        status=models.BillStatuses.paid.value
    ))

    assert bill.status == models.BillStatuses.paid.value

