import base64

import jwt
from fastapi import FastAPI, Query

from app.keys import the_active_key, the_old_key

app = FastAPI()


def make_jwk(the_key):
    the_public_key = the_key.the_private.public_key()
    the_numbers = the_public_key.public_numbers()

    the_modulus = base64.urlsafe_b64encode(
        the_numbers.n.to_bytes(
            (the_numbers.n.bit_length() + 7) // 8,
            "big"
        )
    ).rstrip(b"=").decode()

    the_exponent = base64.urlsafe_b64encode(
        the_numbers.e.to_bytes(
            (the_numbers.e.bit_length() + 7) // 8,
            "big"
        )
    ).rstrip(b"=").decode()

    return {
        "kty": "RSA",
        "kid": the_key.the_kid,
        "use": "sig",
        "alg": "RS256",
        "n": the_modulus,
        "e": the_exponent
    }


@app.get("/jwks")
def get_jwks():
    return {
        "keys": [make_jwk(the_active_key)]
    }


@app.post("/auth")
def create_token(expired: bool = Query(False)):
    if expired:
        the_key = the_old_key
    else:
        the_key = the_active_key

    the_payload = {
        "sub": "fake-user",
        "exp": int(the_key.the_expires_at.timestamp())
    }

    the_token = jwt.encode(
        the_payload,
        the_key.the_private,
        algorithm="RS256",
        headers={"kid": the_key.the_kid}
    )

    return {"token": the_token}

