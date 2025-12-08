from typing import Optional
from datetime import datetime
from bson import ObjectId
import bcrypt

from app.core.database import get_database
from app.schemas.user import UserCreate


class UserModel:
    """Model for User CRUD operations in MongoDB"""

    collection_name = "users"

    @staticmethod
    def get_collection():
        """Get users collection from database"""
        db = get_database()
        return db[UserModel.collection_name]
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    
    @staticmethod
    async def create_user(user_data: UserCreate) -> dict:
        """
        Create a new user in database
        Returns the created user document
        """
        collection = UserModel.get_collection()

        #Preparar el documento
        user_dict = {
            "email": user_data.email.lower(), # Guardamos email en minusculas
            "password_hash": UserModel.hash_password(user_data.password),
            "nombre": user_data.nombre,
            "peso_inicial": user_data.peso_inicial,
            "altura": user_data.altura,
            "fecha_registro": datetime.utcnow()
        }

        # Insertar en MongoDB
        result = await collection.insert_one(user_dict)

        # Obtener el usuario creado
        created_user = await collection.find_one({"_id": result.inserted_id})
        return created_user
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[dict]:
        """Find a user by email"""
        collection = UserModel.get_collection()
        user = await collection.find_one({"email": email.lower()})
        return user
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[dict]:
        """Find user by ID"""
        collection = UserModel.get_collection()

        # Convertir string a ObjectId
        try:
            object_id = ObjectId(user_id)
        except Exception:
            return None
        
        user = await collection.find_one({"_id": object_id})
        return user
    
    @staticmethod
    async def email_exists(email: str) -> bool:
        """Check if email exists"""
        user = await UserModel.get_user_by_email(email)
        return user is not None