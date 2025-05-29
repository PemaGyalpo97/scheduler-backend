from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from app.database.session import SQLALCHEMY_SYNC_DATABASE_URL

# Create a sync engine for APScheduler
jobstores = {
    'default': SQLAlchemyJobStore(url=SQLALCHEMY_SYNC_DATABASE_URL)
}

scheduler = AsyncIOScheduler(jobstores=jobstores)