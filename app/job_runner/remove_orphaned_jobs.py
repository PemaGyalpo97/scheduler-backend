from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.session import SQLALCHEMY_SYNC_DATABASE_URL
from app.models.scheduler_model import Scheduler

engine = create_engine(SQLALCHEMY_SYNC_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def remove_orphaned_jobs(scheduler: BackgroundScheduler):
    db = SessionLocal()
    try:
        # 1. Get all scheduler IDs from DB and format them as APS job IDs
        db_scheduler_ids = {f"scheduler_{s.id}" for s in db.query(Scheduler).filter(Scheduler.is_active == True).all()}
        print(f"✅ db_scheduler_ids: {db_scheduler_ids}")

        # 2. Get all job IDs currently in APScheduler
        aps_job_ids = {job.id for job in scheduler.get_jobs()}
        print(f"📌 aps_job_ids: {aps_job_ids}")

        # 3. Remove jobs from APScheduler that are not in DB
        orphan_job_ids = aps_job_ids - db_scheduler_ids
        for job_id in orphan_job_ids:
            scheduler.remove_job(job_id)
            print(f"🗑️ Removed orphan APS job: {job_id}")

        print("✅ All APScheduler jobs synced with DB.")

    except Exception as e:
        print(f"❌ Error during orphaned job cleanup: {e}") 
    finally:
        db.close()