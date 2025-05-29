from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.dashboard_service import DashboardService
from app.schemas.dashboard_schema import DashboardStats
from app.database.session import get_db

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    service = DashboardService(db)
    return await service.get_dashboard_stats()
