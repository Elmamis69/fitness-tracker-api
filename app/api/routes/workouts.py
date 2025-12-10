from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app.schemas.workout import WorkoutCreate, WorkoutUpdate, WorkoutResponse
from app.schemas.filters import WorkoutFilters
from app.models.workout import WorkoutModel
from app.utils.auth import get_current_user
from app.utils.pagination import PaginationParams, PaginatedResponse

router = APIRouter()

@router.post(
    "/",
    response_model=WorkoutResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new workout",
    response_description="Workout successfully created"
)
async def create_workout(
    workout_data: WorkoutCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new workout session with exercises, sets, and reps.
    
    **Authentication Required**
    
    **Example Request:**
    ```json
    {
        "nombre": "Día de Pecho",
        "fecha": "2024-12-10T10:00:00",
        "duracion": 60,
        "notas": "Buen entrenamiento, aumenté peso en press",
        "ejercicios": [
            {
                "exercise_id": "507f1f77bcf86cd799439011",
                "sets": [
                    {"reps": 10, "weight": 80.0, "rest_seconds": 90},
                    {"reps": 8, "weight": 85.0, "rest_seconds": 90},
                    {"reps": 6, "weight": 90.0, "rest_seconds": 120}
                ]
            }
        ]
    }
    ```
    
    **Fields:**
    - `nombre`: Workout name/title
    - `fecha`: Workout date and time (ISO format)
    - `duracion`: Duration in minutes
    - `notas`: Optional notes
    - `ejercicios`: Array of exercises with sets
        - `exercise_id`: Reference to existing exercise
        - `sets`: Array of sets with reps, weight, and rest time
    
    **Automatic Metrics:**
    - Total volume (weight × reps) calculated automatically
    - Progress tracked in InfluxDB
    - Available in Grafana dashboards
    
    **Errors:**
    - `401`: Authentication required
    - `422`: Invalid data format
    """

    # Crear el workout
    created_workout = await WorkoutModel.create_workout(
        workout_data,
        str(current_user["_id"])
    )

    # Convertir ObjectId a string para la respuesta
    created_workout["_id"] = str(created_workout["_id"])

    return created_workout

@router.get(
    "/",
    response_model=PaginatedResponse[WorkoutResponse],
    summary="List user's workouts",
    response_description="Paginated list of workouts"
)
async def get_user_workouts(
    filters: WorkoutFilters = Depends(),
    pagination: PaginationParams = Depends(),
    current_user: dict = Depends(get_current_user)
):
    """
    Get paginated and filtered list of workouts.
    
    **Authentication Required**
    
    **Pagination Parameters:**
    - `page`: Page number (default: 1)
    - `size`: Items per page (default: 10, max: 100)
    
    **Filter Parameters:**
    - `search`: Search in workout name or notes (case-insensitive)
    - `fecha_desde`: Filter from date (YYYY-MM-DD)
    - `fecha_hasta`: Filter to date (YYYY-MM-DD)
    - `duracion_min`: Minimum duration in minutes
    - `duracion_max`: Maximum duration in minutes
    
    **Example Request:**
    ```
    GET /api/workouts/?page=1&size=10&search=Pecho&duracion_min=45
    ```
    
    **Example Response:**
    ```json
    {
        "items": [
            {
                "_id": "507f1f77bcf86cd799439011",
                "nombre": "Día de Pecho",
                "fecha": "2024-12-10T10:00:00",
                "duracion": 60,
                "ejercicios": [...]
            }
        ],
        "total": 25,
        "page": 1,
        "page_size": 10,
        "total_pages": 3,
        "has_next": true,
        "has_prev": false
    }
    ```
    
    **Sorting:** Workouts are returned sorted by date (newest first)
    
    **Errors:**
    - `401`: Authentication required
    """
    # Construir query con filtros
    query = filters.to_mongo_query(str(current_user["_id"]))
    
    # Obtener total de workouts que cumplen con los filtros
    total = await WorkoutModel.count_workouts_by_query(query)
    
    # Obtener workouts paginados y filtrados
    workouts = await WorkoutModel.get_workouts_by_query(
        query,
        skip=pagination.skip,
        limit=pagination.limit
    )

    # Convertir ObjectId a string para la respuesta
    for workout in workouts:
        workout["_id"] = str(workout["_id"])

    return PaginatedResponse.create(workouts, total, pagination)

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
            status_code = status.HTTP_404_NOT_FOUND,
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
        str(current_user["_id"]),
        workout_data
    )

    if not updated_workout:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
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
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Workout not found"
        )
    return None