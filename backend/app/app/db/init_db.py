from sqlalchemy.orm import Session
from app.models.user import RoleUser
from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

SALES_CONSULTANT_USER = "Sales-consultant@example.com"
CASHIER_USER = "cashier@example.com"
ACCOUNTANT_USER = "accountant@example.com"
PASSWORD_USER = "changethis"


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    if not settings.DEBUG:
        return
    # creating data for dev
    # superuser
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)

    # Продавець консультант
    user = crud.user.get_by_email(db, email=SALES_CONSULTANT_USER)
    if not user:
        user_in = schemas.UserCreate(
            email=SALES_CONSULTANT_USER,
            password=PASSWORD_USER,
            role=RoleUser.sales_consultant.value
        )
        user = crud.user.create(db, obj_in=user_in)

    # Касир
    user = crud.user.get_by_email(db, email=CASHIER_USER)
    if not user:
        user_in = schemas.UserCreate(
            email=CASHIER_USER,
            password=PASSWORD_USER,
            role=RoleUser.cashier.value
        )
        user = crud.user.create(db, obj_in=user_in)

    # Бухгалтер
    user = crud.user.get_by_email(db, email=ACCOUNTANT_USER)
    if not user:
        user_in = schemas.UserCreate(
            email=ACCOUNTANT_USER,
            password=PASSWORD_USER,
            role=RoleUser.accountant.value
        )
        user = crud.user.create(db, obj_in=user_in)
