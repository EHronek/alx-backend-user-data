#!/usr/bin/env python3
"""Module defines a class to manage API Authentication"""
from flask import request
import re
from typing import List, TypeVar
import os


class Auth:
    """Class to manage API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checks if a path requires authentication"""
        if path and excluded_paths:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Retrives authorization header field from request object"""
        if request:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
