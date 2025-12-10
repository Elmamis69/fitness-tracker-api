from typing import Optional, List
from datetime import datetime
from bson import ObjectId

from app.core.database import get_database
from app.schemas.workout import WorkoutCreate, WorkoutUpdate

class WorkoutModel:
    """Model for Workout CRUD operations in MongoDB"""

    collection_name = "workouts"

    @staticmethod
    def get_collection():
        """Get workouts collection from database"""
        db = get_database()
        return db[WorkoutModel.collection_name]
    
    @staticmethod
    async def create_workout(workout_data: WorkoutCreate, user_id: str) -> dict:
        """
        Create a new workout in database
        Returns the created workout document
        """
        collection = WorkoutModel.get_collection()

        # Preparar ejercicios (convertir sets a dict)
        ejercicios_list = []
        for ejercicio in workout_data.ejercicios:
            ejercicios_list.append({
                "exercise_id": ejercicio.exercise_id,
                "sets": [{"reps": s.reps, "peso": s.peso} for s in ejercicio.sets],
                "notas": ejercicio.notas
            })
        
        # Preparar el documento
        workout_dict = {
            "nombre": workout_data.nombre,
            "fecha": workout_data.fecha,
            "ejercicios": ejercicios_list,
            "duracion_minutos": workout_data.duracion_minutos,
            "notas": workout_data.notas,
            "user_id": user_id,
            "fecha_creacion": datetime.utcnow()
        }
        
        # Insert into MongoDB
        result = await collection.insert_one(workout_dict)

        # Get the created workout
        created_workout = await collection.find_one({"_id": result.inserted_id})
        return created_workout
    
    @staticmethod
    async def get_workouts_by_user(user_id: str) -> List[dict]:
        """
        Get all workouts created by a user
        """
        collection = WorkoutModel.get_collection()
        cursor = collection.find({"user_id": user_id}).sort("fecha", -1)
        workouts = await cursor.to_list(length = None)
        return workouts
    
    @staticmethod
    async def get_workouts_by_user_paginated(user_id: str, skip: int = 0, limit: int = 10) -> List[dict]:
        """
        Get workouts created by a user with pagination
        """
        collection = WorkoutModel.get_collection()
        cursor = collection.find({"user_id": user_id}).sort("fecha", -1).skip(skip).limit(limit)
        workouts = await cursor.to_list(length = limit)
        return workouts
    
    @staticmethod
    async def count_workouts_by_user(user_id: str) -> int:
        """
        Count total workouts created by a user
        """
        collection = WorkoutModel.get_collection()
        count = await collection.count_documents({"user_id": user_id})
        return count
    
    @staticmethod
    async def get_workout_by_id(workout_id: str, user_id: str) -> Optional[dict]:
        """
        Get a workout by ID
        Validates that the workout belongs to user
        """
        collection = WorkoutModel.get_collection()

        try:
            object_id = ObjectId(workout_id)
        except Exception:
            return None
        
        workout = await collection.find_one({
            "_id": object_id,
            "user_id": user_id
        })
        return workout
    
    @staticmethod
    async def update_workout(
        workout_id: str,
        user_id: str, 
        update_data: WorkoutUpdate
    ) -> Optional[dict]:
        """
        Update a workout
        Only updates fields that are provided
        """
        collection = WorkoutModel.get_collection()

        try:
            object_id = ObjectId(workout_id)
        except Exception:
            return None
        
        # Construir el diccionario de actualización
        update_dict = {}
        if update_data.nombre is not None:
            update_dict["nombre"] = update_data.nombre
        if update_data.fecha is not None:
            update_dict["fecha"] = update_data.fecha
        if update_data.ejercicios is not None:
            ejercicios_list = []
            for ejercicio in update_data.ejercicios:
                ejercicios_list.append({
                    "exercise_id": ejercicio.exercise_id,
                    "sets": [{"reps": s.reps, "peso": s.peso} for s in ejercicio.sets],
                    "notas": ejercicio.notas
                })
            update_dict["ejercicios"] = ejercicios_list
        if update_data.duracion_minutos is not None:
            update_dict["duracion_minutos"] = update_data.duracion_minutos
        if update_data.notas is not None:
            update_dict["notas"] = update_data.notas

        # Si no hay nada que actualizar, retornar None
        if not update_dict:
            return None
        
        # Actualizar en MongoDB
        result = await collection.find_one_and_update(
            {"_id": object_id, "user_id": user_id},
            {"$set": update_dict},
            return_document = True
        )
        
        return result
    
    @staticmethod
    async def delete_workout(workout_id: str, user_id: str) -> bool:
        """
        Delete a workout
        Returns True if deleted, False if not found
        """
        collection = WorkoutModel.get_collection()

        try:
            object_id = ObjectId(workout_id)
        except Exception:
            return False
        
        result = await collection.delete_one({
            "_id": object_id,
            "user_id": user_id
        })

        return result.deleted_count > 0
