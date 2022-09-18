from datetime import timedelta, datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app import models, schemas
from app.service.discount import DiscountManager, DiscountProductMoreOneMonth


def manager_check_product(test_product: models.Product, db: Session):
    DiscountManager.list_discount = (DiscountProductMoreOneMonth,)
    test_product.created_date = datetime.now() - timedelta(days=32)

    db.add(test_product)
    db.commit()
    db.refresh(test_product)

    DiscountManager.check_product(test_product)

    assert len(test_product.discounts) == 1


def test_manager_check_products(test_product: models.Product, db: Session, mixer):
    DiscountManager.list_discount = (DiscountProductMoreOneMonth,)
    test_product.created_date = datetime.now() - timedelta(days=32)
    products = mixer.cycle(2).blend("app.models.Product", created_date=datetime.now())
    products.append(mixer.blend("app.models.Product", created_date=datetime.now() - timedelta(days=32), price=200))

    DiscountManager.check_products(products)

    assert products[0].discounts is None
    assert products[1].discounts is None
    assert len(products[2].discounts) == 1
