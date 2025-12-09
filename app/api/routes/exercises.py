from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app.schemas.exercise import ExerciseCreate, ExerciseUpdate, ExerciseResponse
from app.models.exercise import ExerciseModel
from app.utils.auth import get_current_user

router = APIRouter()

@router.post("/", response_model = ExerciseResponse, status_code = status.HTTP_201_CREATED)
async def create_exercise(
    exercise_data: ExerciseCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new exercise for the authenticated user

    - Requires authentication
    - Exercise is associated to the user
    """
    # Crear el ejercicio
    created_exercise = await ExerciseModel.create_exercise(
        exercise_data,
        str(current_user["_id"])
    )

    # Convertir ObjectId a string para la respuesta
    created_exercise["_id"] = str(created_exercise["_id"])

    return created_exercise

@router.get("/", response_model = List[ExerciseResponse])
async def get_user_exercises(current_user: dict = Depends(get_current_user)):
    """
    Get all exercises created by the authenticated user

    - Requires authentication
    - Return only user's exercises
    """
    exercises = await ExerciseModel.get_exercise_by_user(str(current_user["_id"]))

    # Convertir ObjectId a string para la respuesta
    for exercise in exercises:
        exercise["_id"] = str(exercise["_id"])

    return exercises

@router.get("/{exercise_id}", response_model = ExerciseResponse)
async def get_exercise(
    exercise_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific exercise by ID

    - Requires authentication
    - User can only access their own exercises
    """
    exercise = await ExerciseModel.get_exercise_by_id(
        exercise_id,
        str(current_user["_id"])
    )

    if not exercise:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Exercise not found"
        )

    # Convertir ObjectId a string para la respuesta
    exercise["_id"] = str(exercise["_id"])

    return exercise

@router.put("/{exercise_id}", response_model = ExerciseResponse)
async def update_exercise(
    exercise_id: str,
    exercise_data: ExerciseUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update an exercise

    - Requires authentication
    - Only updates provided fields
    - User can only update their own exercises
    """
    updated_exercise = await ExerciseModel.update_exercise(
        exercise_id,
        str(current_user["_id"]),
        exercise_data
    )

    if not updated_exercise:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Exercise not found or no fields to update"
        )

    # Convertir ObjectId a string para la respuesta
    updated_exercise["_id"] = str(updated_exercise["_id"])

    return updated_exercise

@router.delete("/{exercise_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_exercise(
    exercise_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete an exercise

    - Requires authentication
    - User can only delete their own exercises
    """
    deleted = await ExerciseModel.delete_exercise(
        exercise_id,
        str(current_user["_id"])
    )

    if not deleted:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Exercise not found"
        )

    return None # 204 No content no retorna body