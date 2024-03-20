"""
Cryptography
"""
import hashlib


def sha256_hash_function(to_hash: str) -> str:
    method = hashlib.sha256()
    method.update(to_hash.encode("utf-8"))
    return method.hexdigest()


hash_func = sha256_hash_function


def hash_password(password: str) -> str:
    """Returns hashed password"""
    return hash_func(password)
