import pytest
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, schemas, models


TEST_PRODUCT_NAME = "TEST PRODUCT"


@pytest.fixture
def test_product(db: Session) -> models.Product:
    product = db.query(models.Product).filter(models.Product.name==TEST_PRODUCT_NAME).first()
    if not product:
        product = crud.product.create(db, obj_in=schemas.CreateProduct(
            name=TEST_PRODUCT_NAME,
            price=100
        ))
    return product


@pytest.fixture
def test_order_created(db: Session, test_product) -> models.Product:
    order = db.query(models.Order).filter(models.Order.product_id == test_product.id).first()
    if not order:
        order = crud.product.create(db, obj_in=schemas.CreateOrder(
            product_id=order.id
        ))
    order.status = models.OrderStatuses.created.value

    db.add(order)
    db.commit()
    db.refresh(order)
    return order


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
    return order


def test_create_bill_for_order(db: Session, test_order_created) -> None:
    order_ready = test_update_order_to_in_progress_and_ready(db, test_order_created)

    # check status to ready
    assert order_ready.status == models.OrderStatuses.ready.value

    bill = crud.bill.create(db, obj_in=schemas.CreateBill(
        order_id=order_ready.id,
    ))

    assert bill.order_id == order_ready.id
    assert bill.status == models.BillStatuses.awaiting.value
    assert bill.order_created_date == order_ready.created_date

    bill = crud.bill.update(db, db_obj=bill, obj_in=schemas.UpdateBill(
        status=models.BillStatuses.paid.value
    ))

    assert bill.status == models.BillStatuses.paid.value

