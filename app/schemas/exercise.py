from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class ExerciseCategory(str, Enum):
    """Categorías de ejercicios"""
    PECHO = "pecho"
    ESPALDA = "espalda"
    PIERNAS = "piernas"
    BRAZOS = "brazos"
    HOMBROS = "hombros"
    CARDIO = "cardio"
    CORE = "core"

class ExerciseType(str, Enum):
    """Tipos de ejercicios"""
    FUERZA = "fuerza"
    CARDIO = "cardio"
    FLEXIBILIDAD = "flexibilidad"

class ExerciseCreate(BaseModel):
    """Schema para crear ejercicio"""
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    categoria: ExerciseCategory
    tipo: ExerciseType

class ExerciseUpdate(BaseModel):
    """Schema para actualizar ejercicio (todos los campos opcionales)"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    categoria: Optional[ExerciseCategory] = None
    tipo: Optional[ExerciseType] = None

class ExcerciseResponse(BaseModel):
    """Schema para respuestas de ejercicio"""
    id: str = Field(..., alias="_id")
    nombre: str
    descripcion: Optional[str]
    categoria: ExerciseCategory
    tipo: ExerciseType
    fecha_creacion: datetime

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
