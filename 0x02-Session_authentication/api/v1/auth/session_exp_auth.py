#!/usr/bin/env python3
"""Module defines a class with session authentication
with expiration for an for that Session"""
from .session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session authentication with expiration"""
    def __init__(self):
        """initializes the class object"""
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id = None):
        """Overoads create_session by calling super()"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id = None):
        """Overloaded method to retrieve the user_id of user
        linked to the given session_id"""
        if session_id in self.user_id_by_session_id:
            session_dictionary = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dictionary['user_id']
            if 'created_at' not in session_dictionary:
                return None
            now = datetime.now()
            time_span = timedelta(seconds=self.session_duration)
            expiry = session_dictionary['created_at'] + time_span
            if expiry < now:
                return None
            return session_dictionary['user_id']
