from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models
from app.core.config import settings


def test_pick_up_order(db: Session, client: TestClient, sales_consultant_user_token_headers, mixer) -> None:
    order = mixer.blend("app.models.Order", product_id=mixer.blend("app.models.Product").id)

    r = client.put(f"{settings.API_V1_STR}/ecommerce/order/pick_up",
                   headers=sales_consultant_user_token_headers,
                   params={"order_id": order.id})
    data = r.json()

    assert r.status_code == 200
    assert data['status'] == models.OrderStatuses.in_progress.value

    # check in db
    db.refresh(order)
    assert order.status == models.OrderStatuses.in_progress.value


def test_set_order_to_ready(db: Session, client: TestClient, sales_consultant_user_token_headers, mixer) -> None:
    order = mixer.blend("app.models.Order", product_id=mixer.blend("app.models.Product").id)

    r = client.put(f"{settings.API_V1_STR}/ecommerce/order/set/ready",
                   headers=sales_consultant_user_token_headers,
                   params={"order_id": order.id})
    data = r.json()

    assert r.status_code == 200
    assert data['status'] == models.OrderStatuses.ready.value

    # check in db
    db.refresh(order)
    assert order.status == models.OrderStatuses.ready.value
