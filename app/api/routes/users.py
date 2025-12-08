from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId

from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.models.user import UserModel
from app.utils.auth import create_access_token, get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    """
    Register a new user

    - Validates email doesn't exist
    - Hashes password
    - Creates user in MongoDB
    - Returns user data (without password)
    """
    # Verificar si el email ya existe
    if await UserModel.email_exists(user_data.email):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Email already registered" 
        )
    
    # Crear el usuario
    created_user = await UserModel.create_user(user_data)

    # Convertir ObjectId a string para la respuesta
    created_user["_id"] = str(created_user["_id"])

    return created_user

@router.post("/login", response_model=Token)
async def login_user(user_data: UserLogin):
    """
    Login user and return JWT token

    - Validates email and password
    - Returns access token
    """
    # Buscar el usuario por email
    user = await UserModel.get_user_by_email(user_data.email)

    if user is None or not UserModel.verify_password(user_data.password, user["password_hash"]):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or password",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    
    # Crear token JWT
    access_token = create_access_token(data={"sub": str(user["_id"])})

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user information

    Requires authentication (Bearer token in header)
    """
    # Convertir ObjectId a string
    current_user["_id"] = str(current_user["_id"])
    return current_user