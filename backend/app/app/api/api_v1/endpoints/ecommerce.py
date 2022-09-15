from typing import Any, List

from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.api import deps

router = APIRouter()


# ========== routers for Product
@router.get("/product/", response_model=List[schemas.Product])
def read_products(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve products.
    Available login for users: Super User.
    """
    products = crud.product.get_multi(db, skip=skip, limit=limit)
    return products


@router.post("/product/", response_model=schemas.Product)
def create_product(
    *,
    product_in: schemas.CreateProduct,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    create product.
    Available login for users: Super User.
    """
    product = crud.product.create(db, obj_in=product_in)
    return product


# ========== routers for Order
@router.post("/order/", response_model=schemas.Order)
def create_order(
    *,
    order_in: schemas.CreateOrder,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_cashier),
) -> Any:
    """
    create order.
    Available login for users: Cashier.
    """
    order = crud.order.create(db, obj_in=order_in)
    return order


@router.get("/order/", response_model=List[schemas.Order])
def read_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_sales_consultant),
) -> Any:
    """
    show orders with status.
    Available login for users: Sales Consultant.
    """
    orders = crud.order.get_multi(db, skip=skip, limit=limit)
    return orders


@router.put("/order/pick_up", response_model=schemas.Order)
def pick_up_order(
    order_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_sales_consultant),
) -> Any:
    """
    pick up order.
    Available login for users: Sales Consultant.
    """

    order = crud.order.get(db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=404,
            detail="order not found",
        )
    order = crud.order.update(
        db,
        db_obj=order,
        obj_in=schemas.UpdateOrder(
            status=models.OrderStatuses.in_progress.value
        )
    )
    return order


@router.put("/order/set/ready", response_model=schemas.Order)
def set_order_to_ready(
    order_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_sales_consultant),
) -> Any:
    """
    make order to Ready.
    Available login for users: Sales Consultant.
    """

    order = crud.order.get(db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=404,
            detail="order not found",
        )
    order = crud.order.update(
        db,
        db_obj=order,
        obj_in=schemas.UpdateOrder(
            status=models.OrderStatuses.ready.value
        )
    )
    return order

