#!/usr/bin/env python3
"""
class to manage the API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """class to manage the API authentication."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        if not path or not excluded_paths:
            return True

        for p in excluded_paths:
            if p.endswith("*"):
                if path.startswith(p.rstrip("*")):
                    return False
            if path.rstrip("/") == p.rstrip("/"):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        if not request:
            return None
        return request.headers.get("Authorization") 

    def current_user(self, request=None) -> TypeVar('User'):
        return None
