#!/usr/bin/env python3
"""
Authentication module
"""
import bcrypt
from db import DB
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """takes in a password string arguments and returns bytes.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Return a string representation of a new UUID
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user into the db
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            password = hash_password(password)
            user = self._db.add_user(email, password)
            return user
        else:
            raise ValueError('User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """validates a user login
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        else:
            return bcrypt.checkpw(password=password.encode('utf-8'),
                    hashed_password=user.hashed_password)

    def create_session(self, email: str) -> str:
        """Create session to allow user to log in
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            session_id = generate_id()
            self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> str:
        """Locates user by using session id
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        else:
            return user

    def destroy_session(self, user_id: int) -> None:
        """updates corresponding user's session Id to None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        else:
            token = generate_id()
            self._db.update_user(reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """Enables a user to update their password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        else:
            hashed_pw = _hash_password(password)
            self._db.update_user(user.id, password=hashed_pw, reset_token=None)
