from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr # Valida que sea un email valido
    password: str = Field(..., min_length = 6, description = "Mínimo 6 caracteres")
    nombre: str = Field(..., min_length = 2, max_length = 100)
    peso_inicial: Optional[float] = Field(None, gt = 0, description = "Peso en kg")
    altura: Optional[float] = Field(None, gt = 0, description = "Altura en cm")

    class UserLogin(BaseModel):
        """Schema para login"""
        email: EmailStr
        password: str

    class UserResponse(BaseModel):
        """Schema para respuestas (sin password)"""
        id: str = Field(..., alias = "_id") # MongoDB usa _id
        email: EmailStr
        nombre: str
        peso_inicial: Optional[float] = None
        altura: Optional[float] = None
        fecha_registro: datetime

        class Config:
            populate_by_name = True # Permite usar _id o id
            json_encoders = {
                datetime: lambda v: v.isoformat()
            }

    class Token(BaseModel):
        """Schema para el token JWT"""
        access_token: str
        token_type: str = "bearer"

    class TokenData(BaseModel):
        """Datos contenidos en el token"""
        user_id: Optional[str] = None