from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class MetricType(str, Enum):
    """Tipos de métricas disponibles"""
    BODY_WEIGHT = "body_weight"
    WORKOUT_VOLUME = "workout_volume"
    EXERCISE_MAX = "exercise_max"
    WORKOUT_COUNT = "workout_count"

class BodyWeightMetric(BaseModel):
    """Schema para métrica de peso corporal"""
    peso: float = Field(..., ge = 1, le = 500, description="Peso en kg")
    timestamp: Optional[datetime] = Field(default_factory = datetime.utcnow)

class WorkoutVolumeMetric(BaseModel):
    """Schema para métrica de volumen de entrenamiento"""
    workout_id: str = Field(..., description = "ID del entrenamiento")
    volumen_total: float = Field(..., ge = 0, description = "Volumen total levantado en kg")
    timestamp: Optional[datetime] = Field(default_factory = datetime.utcnow)

class ExerciseMaxMetric(BaseModel):
    """Schema para peso máximo de un ejercicio"""
    exercise_id: str = Field(..., description = "ID del ejercicio")
    peso_maximo: float = Field(..., ge = 0, description = "Peso máximo levantado en kg")
    reps: int = Field(..., ge = 1, description = "Repeticiones con ese peso")
    timestamp: Optional[datetime] = Field(default_factory = datetime.utcnow)

class MetricQuery(BaseModel):
    """Schema para consultas de métricas"""
    metric_type: MetricType
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    exercise_id: Optional[str] = None
    workout_id: Optional[str] = None

class MetricResponse(BaseModel):
    """Schema para respuesta de métricas"""
    timestamp: datetime
    value: float
    metadata: Optional[dict] = None