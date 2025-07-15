#!/usr/bin/env python3
"""
class to manage the API session authentication.
"""
from typing import List, TypeVar
import os
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """class to manage the API authentication."""
    def __init__(self):
        super().__init__()
        if os.getenv('SESSION_DURATION'):
            try:
                self.session_duration = int(os.getenv('SESSION_DURATION'))
            except:
                self.session_duration = 0
        else:
            self.session_duration = 0

    def create_session(self, user_id=None):
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {}
            self.user_id_by_session_id[session_id]['user_id'] =  user_id
            self.user_id_by_session_id[session_id]['created_at'] = datetime.now()
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        if (session_id not in self.user_id_by_session_id or
            'created_at' not in self.user_id_by_session_id[session_id]):
            return None
        u_session = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return u_session.get('user_id')
        if (u_session.get('created_at') +
            timedelta(seconds=self.session_duration) <= datetime.now()):
            return None
        return u_session.get('user_id')
