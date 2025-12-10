from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WorkoutFilters(BaseModel):
    """Filtros para búsqueda de workouts"""
    search: Optional[str] = Field(None, description = "Buscar por nombre del workout")
    fecha_desde: Optional[datetime] = Field(None, description = "Filtrar workouts desde esta fecha")
    fecha_hasta: Optional[datetime] = Field(None, description = "Filtrar workouts hasta esta fecha")
    duracion_min: Optional[int] = Field(None, ge = 0, description = "Duración mínima en minutos")
    duracion_max: Optional[int] = Field(None, ge = 0, description = "Duración máxima en minutos")

    def to_mongo_query(self, user_id: str) -> dict:
        """Convertir filtros a query de MongoDB"""
        query = {"user_id": user_id}

        # Búsqueda por nombre (case-insensitive)
        if self.search:
            query["nombre"] = {"$regex": self.search, "$options": "i"}

        # Filtro por rango de fechas
        if self.fecha_desde or self.fecha_hasta:
            query["fecha"] = {}
            if self.fecha_desde:
                query["fecha"]["$gte"] = self.fecha_desde
            if self.fecha_hasta:
                query["fecha"]["$lte"] = self.fecha_hasta
        
        # Filtro por duración
        if self.duracion_min or self.duracion_max:
            query["duracion_minutos"] = {}
            if self.duracion_min is not None:
                query["duracion_minutos"]["$gte"] = self.duracion_min
            if self.duracion_max is not None:
                query["duracion_minutos"]["$lte"] = self.duracion_max

        return query

class ExerciseFilters(BaseModel):
    """Filtros para búsqueda de ejercicios"""
    search: Optional[str] = Field(None, description="Buscar por nombre del ejercicio")
    categoria: Optional[str] = Field(None, description="Filtrar por categoría")
    tipo: Optional[str] = Field(None, description="Filtrar por tipo")

    def to_mongo_query(self, user_id: str) -> dict:
        """Convertir filtros a query de MongoDB"""
        query = {"user_id": user_id}

        # Búsqueda por nombre
        if self.search:
            query["nombre"] = {"$regex": self.search, "$options": "i"}

        # Filtro por categoría
        if self.categoria:
            query["categoria"] = self.categoria

        # Filtro por tipo
        if self.tipo:
            query["tipo"] = self.tipo

        return query