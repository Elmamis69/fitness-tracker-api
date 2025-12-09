from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from datetime import datetime

from app.schemas.metric import (
    BodyWeightMetric,
    WorkoutVolumeMetric,
    ExerciseMaxMetric,
    MetricQuery,
    MetricResponse,
    MetricType
)
from app.services.metrics_service import MetricsService
from app.utils.auth import get_current_user

router = APIRouter()

@router.post("/body_weight", status_code = status.HTTP_201_CREATED)
async def add_body_weight_metric(
    metric: BodyWeightMetric,
    current_user: dict = Depends(get_current_user)
):
    """
    Record body weight metric

    - Requires authentication
    - Metric is associated to the user
    """
    await MetricsService.write_body_weight_metric(
        str(current_user["_id"]),
        metric
    )

    return {"message": "Body weight recorded successfully"}

@router.post("/workout_volume", status_code = status.HTTP_201_CREATED)
async def record_workout_volume(
    metric: WorkoutVolumeMetric,
    current_user: dict = Depends(get_current_user)
):
    """
    Record workout volume metric

    - Requires authentication
    - Tracks total weight lifted in a workout
    """
    await MetricsService.write_workout_volume(
        str(current_user["_id"]),
        metric
    )

    return {"message": "Workout volume recorded successfully"}

@router.post("/exercise_max", status_code = status.HTTP_201_CREATED)
async def record_exercise_max(
    metric: ExerciseMaxMetric,
    current_user: dict = Depends(get_current_user)
):
    """
    Record exercise max metric

    - Requires authentication
    - Tracks maximum weight lifted for an exercise
    """
    await MetricsService.write_exercise_max(
        str(current_user["_id"]),
        metric
    )

    return {"message": "Exercise max recorded successfully"}

@router.post("/workout-count", status_code = status.HTTP_201_CREATED)
async def record_workout_count(
    current_user: dict = Depends(get_current_user)
):
    """
    Record workout count metric

    - Requires authentication
    - Increments workout counter for frequency tracking
    """
    await MetricsService.write_workout_count(
        str(current_user["_id"]),
    )

    return {"message": "Workout count incremented successfully"}

@router.post("/query", response_model = List[MetricResponse])
async def query_metrics(
    query: MetricQuery,
    current_user: dict = Depends(get_current_user)
):
    """
    Query metrics from InfluxDB

    - Requires authentication
    - Supports filtering by date range, metric type and IDs
    - Returns time-series data for visualization
    """
    metrics = await MetricsService.query_metrics(
        user_id = str(current_user["_id"]),
        metric_type = query.metric_type,
        start_date = query.start_date,
        end_date = query.end_date,
        exercise_id = query.exercise_id,
        workout_id = query.workout_id
    )

    return metrics