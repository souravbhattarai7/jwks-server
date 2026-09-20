import uuid
from datetime import datetime, timedelta, timezone

from cryptography.hazmat.primitives.asymmetric import rsa


class TheKeyPair:
    def __init__(self, is_expired=False):
        self.the_kid = uuid.uuid4().hex
        self.the_private = self.create_rsa_key()

        the_expiry_hours = -1 if is_expired else 1
        self.the_expires_at = (
            datetime.now(timezone.utc)
            + timedelta(hours=the_expiry_hours)
        )

    @staticmethod
    def create_rsa_key():
        return rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )


the_active_key = TheKeyPair()
the_old_key = TheKeyPair(is_expired=True)
