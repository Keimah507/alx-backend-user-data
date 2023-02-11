#!/usr/env/python3
"""Contains the class SessionAuth"""
from auth import Auth
import uuid

class SessionAuth(Auth):
    """Empty class"""
    def __init__(self) -> None:
        super().__init__(Auth)
        self.user_id_by_session_id = {}

    
    def create_session(self, user_id: str = None) -> str:
        """Creates a session id for user_id"""
        if user_id is None and user_id is not str:
            return None
        self.session_id = str(uuid.uuid4())
        self.user_id_by_session_id = {self.session_id: user_id}
        return self.session_id
