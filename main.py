"""
KnowNet X Backend — FastAPI main application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.core.config import get_settings
from app.core.deps import limiter
from app.db.session import engine, Base
from app.db import init_db
from app.routers import auth, users, projects, knowledge, scholarships, admin
from app.scheduler.collector import scheduled_collection_job

settings = get_settings()

# Create FastAPI app with rate limiter
app = FastAPI(
    title=settings.app_name,
    version="2.0.0",
    description="AI Knowledge Intelligence + Scholarship Finder Platform",
)
app.state.limiter = limiter

# CORS — configure for your frontend domain in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://knownet-ai-x.vercel.app", "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(knowledge.router, prefix="/api/v1")
app.include_router(scholarships.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")

# Exception handler for rate limits
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please slow down."},
    )

# Startup: init DB and scheduler
@app.on_event("startup")
async def on_startup():
    # Create tables
    init_db()

    # Start background scheduler for scholarship collection
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        scheduled_collection_job,
        trigger=IntervalTrigger(minutes=30),
        id="scholarship_collector",
        name="Scholarship RSS Collector",
        replace_existing=True,
    )
    scheduler.start()
    print("✅ KnowNet X backend started. Scholarship collector runs every 30 minutes.")

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "2.0.0", "environment": settings.environment}
