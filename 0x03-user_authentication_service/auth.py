#!/usr/bin/env python3
"""
define a _hash_password method that takes in a password string
arguments and returns bytes
"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4


def _generate_uuid():
    return str(uuid4())

class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def _hash_password(self, pwd: str) -> bytes:
        """hash password using bycrypt
        """
        pwd_byte = pwd.encode()
        hashed_pwd = bcrypt.hashpw(pwd_byte, bcrypt.gensalt())
        return hashed_pwd

    def register_user(self, email: str, password: str) -> User:
        if not email or not password:
            return None
        if self._db.find_user_by(email=email):
            raise ValueError(f"User {email} already exists.")
        hashed_pwd = self._hash_password(password)
        new_user = self._db.add_user(email, hashed_pwd)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        user = self._db.find_user_by(email=email)
        if user and bcrypt.checkpw(password.encode(), user.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        user = self._db.find_user_by(email=email)
        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        return None

    def get_user_from_session_id(self, session_id: str):
        user = self._db.find_user_by(session_id=session_id)
        if user:
            return user
        return None

    def destroy_session(self, user_id: int):
        return self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        user = self._db.find_user_by(email=email)
        if user:
            token = _generate_uuid()
            user.reset_token = token
            return token
        raise ValueError




