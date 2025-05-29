from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log_model import AuditLog

class AuditLogService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_logs_for_scheduler(self, scheduler_id: int):
        result = await self.db.execute(
            select(AuditLog).where(AuditLog.scheduler_id == scheduler_id)
        )
        return result.scalars().all()