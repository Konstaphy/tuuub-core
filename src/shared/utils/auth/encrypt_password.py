from hashlib import sha256


def encrypt_password(password: str) -> str:
    return str(sha256(password.encode("utf-8")).hexdigest())
