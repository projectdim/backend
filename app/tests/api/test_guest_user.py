from typing import Dict

from fastapi.testclient import TestClient

from sqlalchemy.orm import Session

from app.core.config import settings


def test_user_get_otp(
        client: TestClient,
        db: Session
) -> None:

    phone_num = settings.TEST_USER_PHONE_NUM

    r = client.post(f'{settings.API_V1_STR}/guest/request-otp?phone_number={phone_num}')
    assert 200 <= r.status_code < 300
    

def test_user_incorrect_num(
        client: TestClient,
        db: Session
) -> None:

    pass


