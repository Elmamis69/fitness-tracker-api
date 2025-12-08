from typing import Optional
from datetime import datetime
from bson import ObjectId
from passlib.context import CryptContext

from app.core.database import get_database
from app.schemas.user import UserCreate

# Configuracion para hashear passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
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