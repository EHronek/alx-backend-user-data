#!/usr/bin/env python3
"""Basic authentication module for the API"""
from .auth import Auth
import re


class BasicAuth(Auth):
    """BasicAuth class for basic authentication"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """extracts base64 part of the authorization header
        for basic authentication"""
        if type(authorization_header) == str:
            pattern = r'Basic (?P<token>.+)'
            field_match = re.fullmatch(pattern, authorization_header.strip())
            if field_match is not None:
                return field_match.group('token')
        return None
