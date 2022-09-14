from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.api import deps

router = APIRouter()


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
