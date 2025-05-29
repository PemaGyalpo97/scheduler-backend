from sqlalchemy import select, func
from sqlalchemy.orm import aliased
from sqlalchemy.sql import label
from app.models.scheduler_model import Scheduler
from app.models.audit_log_model import AuditLog

class DashboardService:
    def __init__(self, db):
        self.db = db

    async def get_dashboard_stats(self):
        # Total and active jobs
        total_jobs_query = await self.db.execute(select(func.count()).select_from(Scheduler))
        total_jobs = total_jobs_query.scalar()

        active_jobs_query = await self.db.execute(select(func.count()).select_from(Scheduler).where(Scheduler.is_active == True))
        active_jobs = active_jobs_query.scalar()

        # Latest status per scheduler
        latest_audit = aliased(AuditLog)
        subq = (
            select(
                AuditLog.scheduler_id,
                func.max(AuditLog.executed_at).label("latest")
            ).group_by(AuditLog.scheduler_id).subquery()
        )

        joined = select(AuditLog.status, func.count()).join(
            subq,
            (AuditLog.scheduler_id == subq.c.scheduler_id) & (AuditLog.executed_at == subq.c.latest)
        ).group_by(AuditLog.status)

        result = await self.db.execute(joined)
        status_counts = {row[0]: row[1] for row in result.all()}

        return {
            "total_jobs": total_jobs,
            "active_jobs": active_jobs,
            "scheduled_jobs": status_counts.get("scheduled", 0),
            "failed_jobs": status_counts.get("failed", 0),
            "completed_jobs": status_counts.get("completed", 0),
        }
