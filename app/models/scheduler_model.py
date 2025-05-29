from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from app.models.user_model import Base
import datetime

class Scheduler(Base):
    __tablename__ = "scheduler"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    content_type = Column(String)
    content = Column(Text)
    file_name = Column(String)
    file_location = Column(String)
    date = Column(String)
    time = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(String)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(String, nullable=True)