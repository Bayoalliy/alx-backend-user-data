#!/usr/bin/env python3
"""
In this task you will create a SQLAlchemy model named User
for a database table named users

The model will have the following attributes:
id , the integer primary key
email , a non-nullable string
hashed_password , a non-nullable string
session_id , a nullable string
reset_token , a nullable string
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """ maps mysql table users
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250) ,nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
