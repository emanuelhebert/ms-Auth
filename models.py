from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    doc_number = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False)
    full_name = Column(String)
    loggedin = Column(Boolean, default=False)
    created_at = Column(Date, server_default=func.now())
    updated_at = Column(Date, onupdate=func.now())

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, nullable=False)
    created_at = Column(Date, server_default=func.now())
