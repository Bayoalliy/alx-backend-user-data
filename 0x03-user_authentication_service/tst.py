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
user = my_db.add_user(email, hashed_password)
print(user.id)
try:
    my_db.update_user(user.id, session_id="fff")
    print(user.session_id)
    print("Password updated")
except ValueError:
    print("Error")
