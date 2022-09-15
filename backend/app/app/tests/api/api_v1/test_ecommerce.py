from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models
from app.core.config import settings


def test_pick_up_order(db: Session, client: TestClient, sales_consultant_user_token_headers,
                       test_order_created) -> None:
    order = test_order_created
    r = client.put(f"{settings.API_V1_STR}/ecommerce/order/pick_up",
                   headers=sales_consultant_user_token_headers,
                   params={"order_id": order.id})
    data = r.json()

    assert r.status_code == 200
    assert data['status'] == models.OrderStatuses.in_progress.value

    # check in db
    db.refresh(order)
    assert order.status == models.OrderStatuses.in_progress.value


def test_set_order_to_ready(db: Session, client: TestClient, sales_consultant_user_token_headers,
                            test_order_created) -> None:
    order = test_order_created
    r = client.put(f"{settings.API_V1_STR}/ecommerce/order/set/ready",
                   headers=sales_consultant_user_token_headers,
                   params={"order_id": order.id})
    data = r.json()

    assert r.status_code == 200
    assert data['status'] == models.OrderStatuses.ready.value

    # check in db
    db.refresh(order)
    assert order.status == models.OrderStatuses.ready.value


def test_create_bill_for_order(client: TestClient, test_order_ready, cashier_user_token_headers):
    r = client.post(f"{settings.API_V1_STR}/ecommerce/order/create/bill",
                    headers=cashier_user_token_headers,
                    json={"order_id": test_order_ready.id})

    data = r.json()

    assert r.status_code == 200
    assert data['order']['id'] == test_order_ready.id
    assert data['status'] == models.BillStatuses.awaiting.value
    assert data['product_name'] == test_order_ready.product.name
    assert data['product_price'] == test_order_ready.product.price
    assert data['amount'] == test_order_ready.product.price


def test_pay_bill(client: TestClient, test_order_ready, cashier_user_token_headers):
    r = client.post(f"{settings.API_V1_STR}/ecommerce/order/create/bill",
                    headers=cashier_user_token_headers,
                    json={"order_id": test_order_ready.id})

    data = r.json()

    assert data['status'] == models.BillStatuses.awaiting.value

    r = client.post(f"{settings.API_V1_STR}/ecommerce/bill/pay",
                    headers=cashier_user_token_headers,
                    json={"bill_id": data['id']})
    data = r.json()

    assert r.status_code == 200
    assert data['order']['status'] == models.OrderStatuses.paid.value
    assert data['status'] == models.BillStatuses.paid.value
