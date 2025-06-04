#!/usr/bin/env python3
"""Hash Password"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password input"""
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )
