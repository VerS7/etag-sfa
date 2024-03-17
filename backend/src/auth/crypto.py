"""
Cryptography
"""
import hashlib


def hash_password(password: str) -> str:
    """Returns hashed password"""
    method = hashlib.sha256()
    method.update(password.encode("utf-8"))
    return method.hexdigest()
