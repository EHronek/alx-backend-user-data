#!/usr/bin/env python3
"""Hash Password"""
import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes a password input"""
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )


class Auth:
    """Authentication"""
    def __init__(self):
        """Initializes a new Auth instance"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if a users login details are valid"""
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password
                )
        except NoResultFound:
            return False
        return False
