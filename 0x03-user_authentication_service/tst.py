#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User
from auth import Auth
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
my_db = DB()
my_auth = Auth()
email = 'test@test.com'
hashed_password = "hashedPwd"
user = my_auth.register_user(email, hashed_password)
print(f"user created with id of {user.id}")
try:
    session_id = my_auth.create_session(user.email)
    reset_token = my_auth.get_reset_password_token(user.email)
    print("user.hashed_password:", user.hashed_password)
    print("user.reset_token:", user.reset_token)
    my_auth.update_password(reset_token, "abcd")
    print("user.hashed_pass:", user.hashed_password)
    print("user.reset_token:", user.reset_token)
except ValueError:
    print("Error")

