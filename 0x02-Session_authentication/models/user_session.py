#!/usr/bin/env python3
""" User module
"""
from models.base import Base


class UserSession(Base):
    """ User class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User instance
        """
        super().__init__()
        self.user_id = kwargs.get('user_id')
