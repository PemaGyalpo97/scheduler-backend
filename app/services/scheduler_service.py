import os
from sqlalchemy import text
from app.database.session import DATABASE_URL
from app.models.scheduler_model import Scheduler
from app.models.audit_log_model import AuditLog
from app.schemas.scheduler_schema import SchedulerCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.cron_service import schedule_script_execution
from app.job_runner.run_sql_function import  execute_sql_function
from app.core.scheduler_config import scheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from pprint import pprint
from pathlib import Path

class SchedulerService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_scheduler(self, scheduler_data: SchedulerCreate):
        # Step 1: Save to DB
        scheduler_obj = Scheduler(**scheduler_data.dict())
        self.db.add(scheduler_obj)
        await self.db.commit()
        await self.db.refresh(scheduler_obj)
        
        # Step 2: Create file
        file_path = str(Path(scheduler_obj.file_location) / f"{scheduler_obj.file_name}.{scheduler_obj.content_type}")
        os.makedirs(scheduler_obj.file_location, exist_ok=True)
        with open(file_path, "w") as f:
            f.write(scheduler_obj.content)
        print("File Path : ", file_path)
        print("scheduler status", scheduler_obj.is_active)

        if scheduler_data.content_type == "py":
            arguments = []

            if arguments:
                # Step 3: Schedule if active
                if scheduler_obj.is_active:
                    from datetime import datetime
                    job_time = datetime.strptime(f"{scheduler_obj.date} {scheduler_obj.time}", "%Y-%m-%d %H:%M")

                    scheduler.add_job(
                        run_script,
                        "date",
                        run_date=job_time,
                        args=[file_path] + arguments,  # make sure it's a list arguments
                        id=f"scheduler_{scheduler_obj.id}",
                        replace_existing=True
                    )

                    print(scheduler.get_job(f"scheduler_{scheduler_obj.id}"))

                    print("Scheduled job for:", job_time)
                    
                    pprint([{
                        "id": job.id,
                        "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
                        "trigger": str(job.trigger),
                        "args": job.args,
                        "kwargs": job.kwargs,
                        "name": job.name,
                    } for job in scheduler.get_jobs()])
            else:
                print("No arguments provided")
                return None
        elif scheduler_data.content_type == "sql":
            # Create the function in the database
            try:
                await self.db.execute(text(scheduler_obj.content))  # <-- Create function in DB
                await self.db.commit()
                print("SQL function created in database.")
            except Exception as e:
                print("Error creating SQL function:", e)
                await self.db.rollback()
                raise e

            from datetime import datetime
            job_time = datetime.strptime(f"{scheduler_obj.date} {scheduler_obj.time}", "%Y-%m-%d %H:%M")

            function_name = scheduler_obj.file_name

            async def call_sql_function(fn_name: str):
                async with self.db.begin():
                    await self.db.execute(text(f"SELECT {fn_name}()"))

            scheduler.add_job(
                func=execute_sql_function,
                trigger='date',
                run_date=job_time,
                args=[function_name],
                id=str(scheduler_obj.id),
                replace_existing=True
            )
            print("Scheduled SQL function.")

        # Step 4: Log audit
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
        scheduler = await self.db.get(Scheduler, scheduler_data.id)
        if not scheduler:
            return None

        scheduler.file_name = scheduler_data.file_name
        scheduler.file_location = scheduler_data.file_location
        scheduler.cron_expression = scheduler_data.cron_expression

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