#!/usr/bin/env python3
"""
Encrypting passwords
"""
import bcrypt


def hash_password(password) -> bytes:
    """
    Function to encrypt passwords
    Args:
        password: Variable to be encrypted

    Returns: a salted, hashed password, which is a byte string

    """
    encoded = password.encode()
    hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if hashed password and password are identical
    Args:
        hashed_password: hashed instance of password argument
        password: user password

    Returns: a boolean

    """
    encode_password = password.encode()
    if bcrypt.checkpw(encode_password, hashed_password):
        return True
    else:
        return False
