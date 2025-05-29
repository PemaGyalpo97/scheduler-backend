from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class UserRegistration(Base):
    __tablename__ = "user_registration"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    middle_name = Column(String, nullable=True)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(String)

class PersonalDetail(Base):
    __tablename__ = "personal_details"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    middle_name = Column(String, nullable=True)
    last_name = Column(String)
    role = Column(String)
    email = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(String)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(String, nullable=True)

class UserDetail(Base):
    __tablename__ = "user_details"
    id = Column(Integer, primary_key=True)
    login_id = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(String)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(String, nullable=True)