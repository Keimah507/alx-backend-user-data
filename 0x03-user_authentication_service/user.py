#!/usr/bin/env python3
"""
creates an SQLAlchemy model User for a database table named users
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    """
    Contains database table named users
    """
    __tablename__ = 'users'

    id = Column(Integer, Primary_key=True)
    email = Column(String, Nullable=False)
    hashed_password = Column(String, Nullable=False)
    session_id = Column(String)
    reset_token = Column(String)

