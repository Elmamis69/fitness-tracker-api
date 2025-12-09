"""FastAPI application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.database import connect_to_mongo, close_mongo_connection
from app.core.influxdb import connect_to_influxdb, close_influxdb_connection
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup and shutdown"""
    # Startup
    await connect_to_mongo()
    connect_to_influxdb()
    yield
    # Shutdown
    await close_mongo_connection()
    close_influxdb_connection()


app = FastAPI(
    title="Fitness Tracker API",
    description="API for fitness and workout tracking with MongoDB, InfluxDB, and Grafana",
    version="1.0.0",
    lifespan=lifespan
)

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
