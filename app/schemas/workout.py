from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class WorkoutExerciseSet(BaseModel):
    """Schema para un set individual de un ejercicio"""
    reps: int = Field(..., ge = 1, description = "Número de repeticiones")
    peso: float = Field(..., ge = 0, description = "Peso en kg")

class WorkoutExercise(BaseModel):
    """Schema para un ejercicio dentro del workout"""
    exercise_id: str = Field(..., description = "ID del ejercicio")
    sets: List[WorkoutExerciseSet] = Field(..., min_length = 1, description = "Lista de sets realizados")
    notas: Optional[str] = Field(None, max_length = 200, description = "Notas del ejercicio")

class WorkoutCreate(BaseModel):
    """Schema para crear un workout"""
    nombre: str = Field(..., min_length = 2, max_length = 100, description = "Nombre del entrenamiento")
    fecha: datetime = Field(default_factory = datetime.utcnow, description = "Fecha del entrenamiento")
    ejercicios: List[WorkoutExercise] = Field(..., min_length = 1, description = "Ejercicios realizados")
    duracion_minutos: int = Field(..., ge = 1, description = "Duración en minutos")
    notas: Optional[str] = Field(None, max_length = 500, description = "Notas generales del entrenamiento")

class WorkoutUpdate(BaseModel):
    """Schema para actualizar workout (todods opcionales)"""
    nombre: Optional[str] = Field(None, min_length = 2, max_length = 100)
    fecha: Optional[datetime] = None
    ejercicios: Optional[List[WorkoutExercise]] = None
    duracion_minutos: Optional[int] = Field(None, ge = 1)
    notas: Optional[str] = Field(None, max_length = 500)

class WorkoutResponse(BaseModel):
    """Schema para respuestas de workout"""
    id: str = Field(..., alias = "_id")
    nombre: str
    fecha: datetime
    ejercicios: List[WorkoutExercise]
    duracion_minutos: int
    notas: Optional[str]
    fecha_creacion: datetime

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }