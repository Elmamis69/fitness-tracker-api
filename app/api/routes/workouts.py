from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app.schemas.workout import WorkoutCreate, WorkoutUpdate, WorkoutResponse
from app.models.workout import WorkoutModel
from app.utils.auth import get_current_user

router = APIRouter()

@router.post("/", response_model = WorkoutResponse, status_code = status.HTTP_201_CREATED)
async def create_workout(
    workout_data: WorkoutCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new workout for the authenticated user

    - Requires authentication
    - Workout is associated to the user
    """

    # Crear el workout
    created_workout = await WorkoutModel.create_workout(
        workout_data,
        str(current_user["_id"])
    )

    # Convertir ObjectId a string para la respuesta
    created_workout["_id"] = str(created_workout["_id"])

    return created_workout

@router.get("/", response_model = List[WorkoutResponse])
async def get_user_workouts(current_user: dict = Depends(get_current_user)):
    """
    Get all workouts created by the authenticated user

    - Requires authentication
    - Returns workouts sorted by date (newest first)
    """
    workouts = await WorkoutModel.get_workouts_by_user(str(current_user["_id"]))

    # Convertir ObjectId a string para la respuesta
    for workout in workouts:
        workout["_id"] = str(workout["_id"])

    return workouts

@router.get("/{workout_id}", response_model = WorkoutResponse)
async def get_workout(
    workout_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific workout by ID

    - Requires authentication
    - User can only access their own workouts
    """
    workout = await WorkoutModel.get_workout_by_id(
        workout_id,
        str(current_user["_id"])
    )

    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Workout not found"
        )

    # Convertir ObjectId a string para la respuesta
    workout["_id"] = str(workout["_id"])

    return workout

@router.put("/{workout_id}", response_model = WorkoutResponse)
async def update_workout(
    workout_id: str,
    workout_data: WorkoutUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update a specific workout by ID

    - Requires authentication
    - User can only update their own workouts
    - Only provided fields will be updated
    """
    updated_workout = await WorkoutModel.update_workout(
        workout_id,
        workout_data,
        str(current_user["_id"])
    )

    if not updated_workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Workout not found or no changes made"
        )

    # Convertir ObjectId a string para la respuesta
    updated_workout["_id"] = str(updated_workout["_id"])

    return updated_workout

@router.delete("/{workout_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_workout(
    workout_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a specific workout

    - Requires authentication
    - User can only delete their own workouts
    """
    deleted = await WorkoutModel.delete_workout(
        workout_id,
        str(current_user["_id"])
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Workout not found"
        )
    return None