from fastapi import APIRouter, Depends
from app.database.session import get_db
from app.schemas.scheduler_schema import SchedulerCreate
from app.services.scheduler_service import SchedulerService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/schedulers", tags=["Schedulers"])

@router.post("/")
async def create_scheduler(scheduler: SchedulerCreate, db: AsyncSession = Depends(get_db)):
    service = SchedulerService(db)
    return await service.create_scheduler(scheduler)

@router.post("/update")
async def update_scheduler(scheduler: SchedulerCreate, db: AsyncSession = Depends(get_db)):
    service = SchedulerService(db)
    return await service.update_scheduler(scheduler)

@router.get("/")
async def get_scheduler_by_id(id: int, db: AsyncSession = Depends(get_db)):
    service = SchedulerService(db)
    return await service.get_scheduler_by_id(id)

@router.get("/all")
async def get_all_schedulers(db: AsyncSession = Depends(get_db)):
    service = SchedulerService(db)
    return await service.get_all_schedulers()

@router.delete("/")
async def delete_scheduler(id: int, db: AsyncSession = Depends(get_db)):
    service = SchedulerService(db)
    return await service.delete_scheduler(id)