from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app import models
from app.service.discount import calculate_discount_price, DiscountProductMoreOneMonth


def test_calculate_discount_price():
    # 20 pro cent
    new_price = calculate_discount_price(20, 100)

    assert 80 == new_price

    new_price = calculate_discount_price(20, 200)
    assert 160 == new_price


def test_create_discount_more_one_month(test_product: models.Product, db: Session):
    # update date product to more one month
    test_product.created_date = datetime.now() - timedelta(days=32)
    test_product.price = 200

    db.add(test_product)
    db.commit()
    db.refresh(test_product)

    discount_check = DiscountProductMoreOneMonth(test_product)

    is_check = discount_check.check()
    assert is_check is True

    discount = discount_check.create_discount()
    # checking price with discount
    assert discount.discount_price == 160

    test_product.created_date = datetime.now()

    db.add(test_product)
    db.commit()
    db.refresh(test_product)

    is_check = discount_check.check()
    assert is_check is False

