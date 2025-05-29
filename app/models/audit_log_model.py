from sqlalchemy import Column, Integer, String, DateTime
from app.models.user_model import Base
import datetime

class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(Integer, primary_key=True)
    scheduler_id = Column(Integer)
    executed_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String)
    log_file_name = Column(String)
    log_file_location = Column(String)