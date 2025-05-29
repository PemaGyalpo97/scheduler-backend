from pydantic import BaseModel
from datetime import datetime

class AuditLogResponse(BaseModel):
    id: int
    scheduler_id: int
    executed_at: datetime
    status: str
    log_file_name: str
    log_file_location: str

    class Config:
        orm_mode = True