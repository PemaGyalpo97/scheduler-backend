"""Scheduler schema."""
from enum import Enum
from pydantic import BaseModel


class FrequencyEnum(str, Enum):
    """Enum class for frequency."""
    once = "once"
    minute = "minute"
    hour = "hour"
    day = "day"
    month = "month"

class SchedulerCreate(BaseModel):
    name: str
    description: str
    content_type: str
    content: str
    file_name: str
    file_location: str
    date: str
    time: str
    frequency: FrequencyEnum
    frequency_value: int
    created_by: str