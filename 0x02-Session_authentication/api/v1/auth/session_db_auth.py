#!/usr/bin/env python3
"""
class to manage the API authentication.
"""
from typing import List, TypeVar
from api.v1.auth.session_exp_auth import SessionExpAuth
import uuid
from models.user_session import UserSession
from datetime import datetime, timedelta
from models.base import DATA


class SessionDBAuth(SessionExpAuth):
    """class to manage the API Session authentication. with database"""
    #super().__init__()
    user_id_by_session_id = DATA['UserSession']
    def create_session(self, user_id=None):
        if user_id:
            new_session = UserSession(user_id=user_id)
            new_session.save()
            return new_session.id
        return None

    def user_id_for_session_id(self, session_id=None):
        u_session = UserSession.get(session_id)
        if not u_session or not getattr(u_session, 'created_at'):
            return None
        if self.session_duration <= 0:
            return u_session.user_id
        if (getattr(u_session, 'created_at') +
            timedelta(seconds=self.session_duration) <= datetime.utcnow()):
            print("Session ended")
            u_session.remove()
            u_session.save()
            return None
        print(getattr(u_session, 'created_at'))
        print(timedelta(seconds=self.session_duration))
        print(datetime.now())
        return u_session.user_id

    def destroy_session(self, request=None):
        session_id = self.session_cookie(request)
        if request and self.user_id_for_session_id(session_id):
            u_session = UserSession.get(session_id)
            u_session.remove()
            return True
        return False
