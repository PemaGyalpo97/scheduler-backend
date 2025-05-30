from fastapi import FastAPI
from app.routes import user_route, scheduler_route, dashboard_route
from app.core.scheduler_config import scheduler
from app.job_runner.remove_orphaned_jobs import remove_orphaned_jobs

app = FastAPI(title="Scheduler Core")

app.include_router(user_route.router)
app.include_router(scheduler_route.router)
app.include_router(dashboard_route.router)

@app.on_event("startup")
def start_scheduler():
    scheduler.start()
    remove_orphaned_jobs(scheduler)
    print("✅ All APScheduler jobs synced with DB.")

@app.get("/")
def read_root():
    return {"message": "Scheduler Backend API is running"}
