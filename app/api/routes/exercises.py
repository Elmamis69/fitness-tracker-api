from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app.schemas.exercise import ExerciseCreate, ExerciseUpdate, ExerciseResponse
from app.schemas.filters import ExerciseFilters
from app.models.exercise import ExerciseModel
from app.utils.auth import get_current_user
from app.utils.pagination import PaginationParams, PaginatedResponse

router = APIRouter()

@router.post(
    "/",
    response_model=ExerciseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new exercise",
    response_description="Exercise successfully created"
)
async def create_exercise(
    exercise_data: ExerciseCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new exercise definition.
    
    **Authentication Required**
    
    **Example Request:**
    ```json
    {
        "nombre": "Press de Banca",
        "descripcion": "Ejercicio compuesto para pecho",
        "categoria": "Pecho",
        "tipo": "Fuerza",
        "musculos_principales": ["Pectoral Mayor", "Tríceps", "Deltoides Anterior"],
        "musculos_secundarios": ["Core"],
        "equipo": "Barra",
        "dificultad": "Intermedio",
        "instrucciones": "1. Acuéstate en el banco\n2. Agarra la barra..."
    }
    ```
    
    **Fields:**
    - `nombre`: Exercise name (required)
    - `descripcion`: Brief description
    - `categoria`: Category (e.g., "Pecho", "Piernas", "Espalda")
    - `tipo`: Type (e.g., "Fuerza", "Cardio", "Flexibilidad")
    - `musculos_principales`: Main muscles worked
    - `musculos_secundarios`: Secondary muscles (optional)
    - `equipo`: Required equipment (optional)
    - `dificultad`: Difficulty level (optional)
    - `instrucciones`: Step-by-step instructions (optional)
    
    **Usage:**
    Create exercises once, then reference them in workouts by their `_id`.
    
    **Errors:**
    - `401`: Authentication required
    - `422`: Invalid data format
    """
    # Crear el ejercicio
    created_exercise = await ExerciseModel.create_exercise(
        exercise_data,
        str(current_user["_id"])
    )

    # Convertir ObjectId a string para la respuesta
    created_exercise["_id"] = str(created_exercise["_id"])

    return created_exercise

@router.get(
    "/",
    response_model=PaginatedResponse[ExerciseResponse],
    summary="List user's exercises",
    response_description="Paginated list of exercises"
)
async def get_user_exercises(
    filters: ExerciseFilters = Depends(),
    pagination: PaginationParams = Depends(),
    current_user: dict = Depends(get_current_user)
):
    """
    Get paginated and filtered list of exercises.
    
    **Authentication Required**
    
    **Pagination Parameters:**
    - `page`: Page number (default: 1)
    - `size`: Items per page (default: 10, max: 100)
    
    **Filter Parameters:**
    - `search`: Search in name, description, or muscles (case-insensitive)
    - `categoria`: Filter by category (exact match)
    - `tipo`: Filter by type (exact match)
    
    **Example Requests:**
    ```
    GET /api/exercises/?page=1&size=20
    GET /api/exercises/?search=Press&categoria=Pecho
    GET /api/exercises/?tipo=Fuerza&page=2
    ```
    
    **Example Response:**
    ```json
    {
        "items": [
            {
                "_id": "507f1f77bcf86cd799439011",
                "nombre": "Press de Banca",
                "categoria": "Pecho",
                "tipo": "Fuerza",
                "musculos_principales": ["Pectoral Mayor", "Tríceps"]
            }
        ],
        "total": 15,
        "page": 1,
        "page_size": 20,
        "total_pages": 1,
        "has_next": false,
        "has_prev": false
    }
    ```
    
    **Errors:**
    - `401`: Authentication required
    """
    # Construir query con filtros
    query = filters.to_mongo_query(str(current_user["_id"]))
    
    # Obtener total de exercises que cumplen con los filtros
    total = await ExerciseModel.count_exercises_by_query(query)
    
    # Obtener exercises paginados y filtrados
    exercises = await ExerciseModel.get_exercises_by_query(
        query,
        skip=pagination.skip,
        limit=pagination.limit
    )

    # Convertir ObjectId a string para la respuesta
    for exercise in exercises:
        exercise["_id"] = str(exercise["_id"])

    return PaginatedResponse.create(exercises, total, pagination)

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