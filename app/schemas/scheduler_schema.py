from pydantic import BaseModel
from typing import Optional

class SchedulerCreate(BaseModel):
    name: str
    description: str
    content_type: str
    content: str
    file_name: str
    file_location: str
    date: str
    time: str
    created_by: str