from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models
from app.core.config import settings
from app.db.session import SessionLocal
from app.main import app
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers
from mixer.backend.sqlalchemy import Mixer


TEST_SALES_CONSULTANT_USER = "sales-consultant@test.com"


@pytest.fixture(scope="session")
def db() -> Generator:
    session: Session = SessionLocal()
    yield db
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
def mixer(db: Session):
    return Mixer(session=db, commit=True)
