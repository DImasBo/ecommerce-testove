from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models, crud, schemas
from app.core.config import settings
from app.db.session import SessionLocal
from app.main import app
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers
from mixer.backend.sqlalchemy import Mixer

TEST_SALES_CONSULTANT_USER = "sales-consultant@test.com"
TEST_CASHIER_USER = "cashier@test.com"
TEST_PRODUCT_NAME = "TEST PRODUCT"


@pytest.fixture(scope="session")
def db() -> Generator:
    session: Session = SessionLocal()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )


@pytest.fixture(scope="module")
def sales_consultant_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_email(
        client=client, email=TEST_SALES_CONSULTANT_USER, db=db, role=models.RoleUser.sales_consultant.value
    )


@pytest.fixture(scope="module")
def cashier_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_email(
        client=client, email=TEST_CASHIER_USER, db=db, role=models.RoleUser.cashier.value
    )


@pytest.fixture(scope="module")
def mixer(db: Session):
    return Mixer(session=db, commit=False)


@pytest.fixture
def test_product(db: Session) -> models.Product:
    product = db.query(models.Product).filter(models.Product.name == TEST_PRODUCT_NAME).first()
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
    if order.bill:
        crud.bill.remove(db, id=order.bill.id)

    order.status = models.OrderStatuses.created.value

    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@pytest.fixture
def test_order_ready(db: Session, test_order_created) -> models.Product:
    test_order_created.status = models.OrderStatuses.ready.value

    db.add(test_order_created)
    db.commit()
    db.refresh(test_order_created)
    return test_order_created
