from datetime import datetime, timezone

import jwt


class TokenHandler:
    def __init__(self, secret: str, algorithm: str, lifetime) -> None:
        self.secret = secret
        self.algorithm = algorithm
        self.lifetime = lifetime

    def generate_token(self, data: dict):
        data.update(exp=datetime.now(tz=timezone.utc) + self.lifetime)
        return jwt.encode(data, key=self.secret, algorithm=self.algorithm)

    def decode_token(self, token):
        try:
            return jwt.decode(token, key=self.secret, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            return None
