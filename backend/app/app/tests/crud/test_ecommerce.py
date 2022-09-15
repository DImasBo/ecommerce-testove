from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, schemas, models


# Tests CRUD Order
def test_create_order(db: Session, mixer) -> None:
    product = mixer.blend("app.models.Product")
    order = crud.order.create(db, obj_in=schemas.CreateOrder(
        product_id=product.id
    ))

    assert order.product == product
    assert order.id is not None
    assert order.status == models.OrderStatuses.created.value


def test_update_order(db: Session, mixer) -> None:
    product = mixer.blend("app.models.Product")
    order = crud.order.create(db, obj_in=schemas.CreateOrder(
        product_id=product.id
    ))
    assert order.status == models.OrderStatuses.created.value
    order = crud.order.update(db, db_obj=order, obj_in=schemas.UpdateOrder(
        status=models.OrderStatuses.in_progress.value
    ))

    # status to in progress
    assert order.status == models.OrderStatuses.in_progress.value
    order = crud.order.update(db, db_obj=order, obj_in=schemas.UpdateOrder(
        status=models.OrderStatuses.ready.value
    ))

    # status to ready
    assert order.status == models.OrderStatuses.ready.value
