#!/usr/bin/env python3
"""Basic authentication module for the API"""
from .auth import Auth
import re
import binascii
import base64
from typing import Tuple, TypeVar


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

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str,
            ) -> str:
        """Decodes a base64-encoded authorization header"""
        if type(base64_authorization_header) == str:
            try:
                res = base64.b64decode(
                        base64_authorization_header,
                        validate=True)
                return res.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None
            
    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """extracts user credentials from a base64-decoded authorization
        header that uses the basic authentication flow"""
        if type(decoded_base64_authorization_header) == str:
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            field_match =re.fullmatch(
                pattern,
                decoded_base64_authorization_header.strip(),
            )
            if field_match is not None:
                user = field_match.group('user')
                password = field_match.group('password')
                return user, password
        return None, None
