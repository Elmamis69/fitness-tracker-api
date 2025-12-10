"""FastAPI application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager

from app.core.database import connect_to_mongo, close_mongo_connection
from app.core.influxdb import connect_to_influxdb, close_influxdb_connection
from app.core.config import settings
from app.core.logger import logger
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup and shutdown"""
    # Startup
    logger.info("🚀 Starting Fitness Tracker API...")
    await connect_to_mongo()
    connect_to_influxdb()
    logger.success("✅ Application started successfully")
    yield
    # Shutdown
    logger.info("🛑 Shutting down Fitness Tracker API...")
    await close_mongo_connection()
    close_influxdb_connection()
    logger.success("👋 Application shutdown complete")


app = FastAPI(
    title="Fitness Tracker API",
    description="API for fitness and workout tracking with MongoDB, InfluxDB, and Grafana",
    version="1.0.0",
    lifespan=lifespan
)

# Exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Fitness Tracker API Running",
        "environment": settings.ENVIRONMENT
    }


# Import and include routers
from app.api.routes import users, exercises, workouts, metrics

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(exercises.router, prefix="/api/exercises", tags=["exercises"])
app.include_router(workouts.router, prefix="/api/workouts", tags=["workouts"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host = settings.HOST,
        port = settings.PORT,
        reload=True if settings.ENVIRONMENT == "development" else False
    )
