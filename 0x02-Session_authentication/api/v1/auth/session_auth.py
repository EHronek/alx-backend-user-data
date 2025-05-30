#!/usr/bin/env python3
"""Defines a class that authenticates a Session"""
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """Session authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id:str = None) -> str:
        """creates a session id for user_id"""
        if user_id is None:
            return None
        if type(user_id) is str:
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        
