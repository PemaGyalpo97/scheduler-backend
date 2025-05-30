"""Scheduler Service"""
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.scheduler_model import Scheduler
from app.models.audit_log_model import AuditLog
from app.schemas.scheduler_schema import SchedulerCreate
from app.job_runner.run_sql_function import  execute_sql_function
from app.job_runner.run_script import run_script  # type: ignore
from app.core.scheduler_config import scheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from pathlib import Path
from datetime import datetime

class SchedulerService:
    """Scheduler Service"""
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_scheduler(self, scheduler_data: SchedulerCreate):
        """Create a scheduler in the database."""

        data = scheduler_data.dict()

        # Step 1: Save to DB
        scheduler_obj = Scheduler(**data)
        self.db.add(scheduler_obj)
        await self.db.commit()
        await self.db.refresh(scheduler_obj)


        # Step 2: Create file (cross-platform-safe)
        script_dir = Path(scheduler_obj.file_location)  # type: ignore
        script_dir.mkdir(parents=True, exist_ok=True)
        file_path = script_dir / f"{scheduler_obj.file_name}.{scheduler_obj.content_type}"

        with open(file_path, "w") as f: 
            f.write(scheduler_obj.content)  # type: ignore

        print(f"File Path: {file_path}")
        print(f"Scheduler Active: {scheduler_obj.is_active}")

        # Step 3: Determine trigger
        job_time = datetime.strptime(f"{scheduler_obj.date} {scheduler_obj.time}", "%Y-%m-%d %H:%M")

        def get_trigger(frequency: str, start_time: datetime, freq_val: int):
            if frequency == "once":
                return DateTrigger(run_date=start_time)

            elif frequency == "minute":
                # Every freq_val minutes
                return CronTrigger(minute=f"*/{freq_val}")

            elif frequency == "hour":
                # Every freq_val hours at the specified minute
                return CronTrigger(hour=f"*/{freq_val}", minute=start_time.minute)

            elif frequency == "day":
                # Every freq_val days at the specified hour and minute
                return CronTrigger(day=f"*/{freq_val}", hour=start_time.hour, minute=start_time.minute)

            elif frequency == "month":
                # Every freq_val months on the specified day, hour, and minute
                return CronTrigger(month=f"*/{freq_val}", day=start_time.day, hour=start_time.hour, minute=start_time.minute)

            else:
                raise ValueError(f"Unsupported frequency: {frequency}")
            
        trigger = get_trigger(scheduler_data.frequency, job_time, scheduler_data.frequency_value)

        # Step 4: Schedule the job
        if scheduler_obj.is_active:  # type: ignore
            job_id = f"scheduler_{scheduler_obj.id}"
            
            if scheduler_data.content_type == "py":
                arguments = "gyalpococ@gmail.com"
                
                if arguments:
                        
                    scheduler.add_job( # type: ignore
                        run_script,
                        trigger=trigger,
                        args=[str(file_path), arguments],
                        id=job_id,
                        replace_existing=True
                    )
                    print("Scheduled Python script.")
                else:
                    print("No arguments provided.")
                    return None
            elif scheduler_data.content_type == "sql":
                try:
                    await self.db.execute(text(scheduler_obj.content))  # type: ignore # Create SQL function
                    await self.db.commit()
                    print("SQL function created in database.")
                except Exception as e:
                    print("Error creating SQL function:", e)
                    await self.db.rollback()
                    raise e

                scheduler.add_job(  # type: ignore
                    func=execute_sql_function,
                    trigger=trigger,
                    args=[scheduler_obj.file_name],  # function name = file_name
                    id=job_id,
                    replace_existing=True
                )
                print("Scheduled SQL function.")

        # Step 5: Log audit
        audit = AuditLog(
            scheduler_id=scheduler_obj.id,
            executed_at=scheduler_obj.created_at,
            status="Created",
            log_file_name=f"{scheduler_obj.file_name}.log",
            log_file_location=scheduler_obj.file_location,
        )

        self.db.add(audit)
        await self.db.commit()

        return scheduler_obj
    
    async def update_scheduler(self, scheduler_data: SchedulerCreate):
        """Update a scheduler in the database."""
        scheduler = await self.db.get(Scheduler, scheduler_data.id)  # type: ignore
        if not scheduler:
            return None

        scheduler.file_name = scheduler_data.file_name  # type: ignore
        scheduler.file_location = scheduler_data.file_location  # type: ignore
        scheduler.cron_expression = scheduler_data.cron_expression  # type: ignore

        await self.db.commit()
        await self.db.refresh(scheduler)

        audit = AuditLog(
            scheduler_id=scheduler.id,
            executed_at=scheduler.updated_at,
            status="Updated",
            log_file_name=f"{scheduler.file_name}.log",
            log_file_location=scheduler.file_location,
        )
        self.db.add(audit)
        await self.db.commit()

        return scheduler

    async def get_scheduler_by_id(self, id: int):
        return await self.db.get(Scheduler, id)

    async def get_all_schedulers(self):
        return await self.db.scalars(select(Scheduler)).all()

    async def delete_scheduler(self, id: int):
        scheduler = await self.db.get(Scheduler, id)
        if not scheduler:
            return None

        await self.db.delete(scheduler)
        await self.db.commit()
        return scheduler