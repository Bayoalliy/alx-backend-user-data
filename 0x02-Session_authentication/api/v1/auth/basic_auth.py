#!/usr/bin/env python3
"""
class to manage the API Basic authentication.
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """class to manage the API Basic authentication."""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        auth_header = authorization_header
        if (auth_header and type(auth_header) == str and
            auth_header.startswith("Basic ")):
            return auth_header.lstrip("Basic ")
        return None

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        base64_header = base64_authorization_header
        if (base64_header and type(base64_header) == str):
            try:
                return base64.b64decode(base64_header).decode()
            except:
                return None
        return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        decoded_header = decoded_base64_authorization_header
        if (decoded_header and type(decoded_header) == str and
            ":" in decoded_header):
            split_header = decoded_header.replace(":", " ", 1).split()
            return (split_header[0], split_header[1])
        return(None, None)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'): 
        if (user_email and type(user_email) == str and
            user_pwd and type(user_pwd) == str):
            user = User.search({'email': user_email})
            if user and user[0].is_valid_password(user_pwd):
                return user[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
         header = self.authorization_header(request)
         auth_header = self.extract_base64_authorization_header(header)
         base64_header = self.decode_base64_authorization_header(auth_header)
         user_info = self.extract_user_credentials(base64_header)
         user = self.user_object_from_credentials(user_info[0], user_info[1])
         return user
