import jwt
from fastapi.testclient import TestClient

from app.keys import the_active_key, the_old_key
from app.main import app

client = TestClient(app)

def test_jwks_returns_active_key():
    response = client.get("/jwks")

    assert response.status_code == 200

    the_keys = response.json()["keys"]

    assert len(the_keys) == 1
    assert the_keys[0]["kid"] == the_active_key.the_kid
    assert the_keys[0]["kty"] == "RSA"
    assert the_keys[0]["alg"] == "RS256"


def test_expired_key_not_in_jwks():
    response = client.get("/jwks")

    the_keys = response.json()["keys"]

    assert the_old_key.the_kid not in [key["kid"] for key in the_keys]


def test_auth_returns_token():
    response = client.post("/auth")

    assert response.status_code == 200

    the_token = response.json()["token"]
    the_header = jwt.get_unverified_header(the_token)

    assert the_header["kid"] == the_active_key.the_kid
    assert the_header["alg"] == "RS256"


def test_expired_auth_returns_expired_token():
    response = client.post("/auth?expired=true")

    assert response.status_code == 200

    the_token = response.json()["token"]
    the_header = jwt.get_unverified_header(the_token)
    the_payload = jwt.decode(
        the_token,
        options={"verify_signature": False}
    )

    assert the_header["kid"] == the_old_key.the_kid
    assert the_payload["exp"] < the_active_key.the_expires_at.timestamp()


def test_wrong_method_for_jwks():
    response = client.post("/jwks")

    assert response.status_code == 405


def test_wrong_method_for_auth():
    response = client.get("/auth")

    assert response.status_code == 405
