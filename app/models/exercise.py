from typing import Optional, List
from datetime import datetime
from bson import ObjectId

from app.core.database import get_database
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate

class ExerciseModel:
    """Model for Exercise CRUD operations in MongoDB"""

    collection_name = "exercises"

    @staticmethod
    def get_collection():
        """Get exercises collection from database"""
        db = get_database()
        return db[ExerciseModel.collection_name]

    @staticmethod
    async def create_exercise(exercise_data: ExerciseCreate, user_id: str) -> dict:
        """
        Create a new exercise in database
        Returns the created exercise document
        """
        collection = ExerciseModel.get_collection()

        # Preparar el documento
        exercise_dict = {
            "nombre": exercise_data.nombre,
            "descripcion": exercise_data.descripcion,
            "categoria": exercise_data.categoria.value, # Enum to string
            "tipo": exercise_data.tipo.value,
            "user_id": user_id,
            "fecha_creacion": datetime.utcnow()
        }

        # Insert into MongoDB
        result = await collection.insert_one(exercise_dict)

        # Get the created exercise
        created_exercise = await collection.find_one({"_id": result.inserted_id})
        return created_exercise
    
    @staticmethod
    async def get_exercise_by_user(user_id: str) -> List[dict]:
        """
        Get all exercises created by a user
        """
        collection = ExerciseModel.get_collection()
        cursor = collection.find({"user_id": user_id})
        exercises = await cursor.to_list(length = None)
        return exercises
    
    @staticmethod
    async def get_exercise_by_id(exercise_id: str, user_id: str) -> Optional[dict]:
        """
        Get an exercise by ID
        Validates that the exercise belongs to user
        """
        collection = ExerciseModel.get_collection()

        try:
            object_id = ObjectId(exercise_id)
        except Exception:
            return None
        exercise = await collection.find_one({
            "_id": object_id,
            "user_id": user_id
        })
        return exercise
    
    @staticmethod
    async def update_exercise(
        exercise_id: str, 
        user_id: str, 
        update_data: ExerciseUpdate
    ) -> Optional[dict]:
        """
        Update an exercise
        Only updates fields that are provided
        """
        collection = ExerciseModel.get_collection()

        try:
            object_id = ObjectId(exercise_id)
        except Exception:
            return None
        
        # Construir el diccionario de actualización solo con campos provistos
        update_dict = {}
        if update_data.nombre is not None:
            update_dict["nombre"] = update_data.nombre
        if update_data.descripcion is not None:
            update_dict["descripcion"] = update_data.descripcion
        if update_data.categoria is not None:
            update_dict["categoria"] = update_data.categoria.value
        if update_data.tipo is not None:
            update_dict["tipo"] = update_data.tipo.value
        
        # Si no hay nada que actualizar, retornar None
        if not update_dict:
            return None
        
        # Actualiar en MongoDB
        result = await collection.find_one_and_update(
            {"_id": object_id, "user_id": user_id},
            {"$set": update_dict},
            return_document=True # Retorna el documento actualizado
        )

        return result

    @staticmethod
    async def delete_exercise(exercise_id: str, user_id: str) -> bool:
        """
        Delete an exercise
        Returns True if deleted, False if not found
        """
        collection = ExerciseModel.get_collection()

        try:
            object_id = ObjectId(exercise_id)
        except Exception:
            return False
        
        result = await collection.delete_one({
            "_id": object_id,
            "user_id": user_id
        })

        return result.deleted_count > 0