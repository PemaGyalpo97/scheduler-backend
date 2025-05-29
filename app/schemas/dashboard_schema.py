from pydantic import BaseModel

class DashboardStats(BaseModel):
    total_jobs: int
    active_jobs: int
    scheduled_jobs: int
    failed_jobs: int
    completed_jobs: int
