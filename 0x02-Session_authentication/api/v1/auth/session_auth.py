#!/usr/bin/env python3
"""
class to manage the API authentication.
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """class to manage the API Session authentication."""
    user_id_by_session_id = {}
    
    def create_session(self, user_id: str = None) -> str:
        if user_id and type(user_id) == str:
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        if session_id and type(session_id) == str:
            return self.user_id_by_session_id.get(session_id)
        return None
