from fastapi import FastAPI
from app.routes import user_route, scheduler_route, dashboard_route
from app.core.scheduler_config import scheduler

app = FastAPI(title="Scheduler Core")

app.include_router(user_route.router)
app.include_router(scheduler_route.router)
app.include_router(dashboard_route.router)

@app.on_event("startup")
async def start_scheduler():
    scheduler.start()

@app.get("/")
def read_root():
    return {"message": "Scheduler Backend API is running"}
