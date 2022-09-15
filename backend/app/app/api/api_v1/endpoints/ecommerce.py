from typing import Any, List, Optional

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
    order_id: int = Body(..., embed=True),
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
    order_id: int = Body(..., embed=True),
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


# ========== routers for Bill
@router.post("/order/create/bill", response_model=schemas.Bill)
def create_bill_for_order(
    bill_in: schemas.CreateBill,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_cashier),
) -> Any:
    """
    Create Bill for order.
    Available login for users: Cashier.
    default:
        amount value will have the price of the product
        product_name amd product_price will have value of product
    """
    order = crud.order.get(db, id=bill_in.order_id)
    if not order:
        raise HTTPException(
            status_code=404,
            detail="order not found",
        )

    if order.bill:
        return order.bill

    if not order.status == models.OrderStatuses.ready.value:
        raise HTTPException(
            status_code=422,
            detail=f"order {order.id} not ready",
        )

    # setting default data if field is optional
    if not bill_in.product_name:
        bill_in.product_name = order.product.name

    if not bill_in.product_price:
        bill_in.product_price = order.product.price

    if not bill_in.amount:
        bill_in.amount = order.product.price

    bill = crud.bill.create(db, obj_in=bill_in)
    return bill


@router.get("/bill/", response_model=List[schemas.Bill])
def read_bills(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_cashier),
) -> Any:
    bills = crud.bill.get_multi(db, skip=skip, limit=limit)
    return bills


@router.put("/bill/pay", response_model=schemas.Bill)
def pay_bill(
    bill_id: int = Body(...),
    comment: Optional[str] = Body(None),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_cashier),
) -> Any:
    """
    paying Bill.
    Available login for users: Cashier.
    default:
        Order Status to paid
    """
    bill = crud.bill.get(db, id=bill_id)
    if not bill:
        raise HTTPException(
            status_code=404,
            detail="Bill not found",
        )

    if not bill.status == models.BillStatuses.awaiting:
        raise HTTPException(
            status_code=404,
            detail=f"Bill {bill.id} not valid. Bill: order_id={bill.order.id}, status={bill.status}",
        )

    bill_in = schemas.UpdateOrder(status=models.BillStatuses.paid.value)
    if comment:
        bill_in.comment = comment

    bill = crud.bill.update(db, db_obj=bill, obj_in=bill_in)

    order = crud.order.update(db, db_obj=bill.order, obj_in=schemas.UpdateOrder(
        status=models.OrderStatuses.paid.value
    ))

    return bill
