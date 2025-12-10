"""User authentication routes"""
from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId

from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.models.user import UserModel
from app.utils.auth import create_access_token, get_current_user

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    response_description="User successfully created"
)
async def register_user(user_data: UserCreate):
    """
    Register a new user in the system.
    
    **Process:**
    - Validates email format
    - Checks email doesn't already exist
    - Hashes password securely with bcrypt
    - Creates user document in MongoDB
    - Returns user data (password excluded)
    
    **Example Request:**
    ```json
    {
        "email": "user@example.com",
        "password": "SecurePass123!",
        "name": "John Doe"
    }
    ```
    
    **Example Response:**
    ```json
    {
        "_id": "507f1f77bcf86cd799439011",
        "email": "user@example.com",
        "name": "John Doe",
        "created_at": "2024-12-10T10:00:00"
    }
    ```
    
    **Errors:**
    - `400`: Email already registered
    - `422`: Invalid input data (weak password, invalid email)
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


@router.post(
    "/login",
    response_model=Token,
    summary="Login and get access token",
    response_description="JWT access token"
)
async def login_user(user_credentials: UserLogin):
    """
    Authenticate user and return JWT access token.
    
    **Process:**
    - Validates email exists
    - Verifies password with bcrypt
    - Generates JWT token (valid for 7 days)
    - Returns token and user info
    
    **Example Request:**
    ```json
    {
        "email": "user@example.com",
        "password": "SecurePass123!"
    }
    ```
    
    **Example Response:**
    ```json
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer",
        "user": {
            "_id": "507f1f77bcf86cd799439011",
            "email": "user@example.com",
            "name": "John Doe"
        }
    }
    ```
    
    **Usage:**
    Include the token in subsequent requests:
    ```
    Authorization: Bearer <access_token>
    ```
    
    **Errors:**
    - `401`: Invalid credentials
    - `422`: Invalid input format
    """
    # Buscar usuario por email
    user = await UserModel.get_user_by_email(user_credentials.email)
    
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar password
    if not UserModel.verify_password(user_credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token JWT
    access_token = create_access_token(data={"sub": str(user["_id"])})
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    response_description="Current user information"
)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get authenticated user's profile information.
    
    **Authentication Required:**
    Include JWT token in Authorization header:
    ```
    Authorization: Bearer <your_access_token>
    ```
    
    **Example Response:**
    ```json
    {
        "_id": "507f1f77bcf86cd799439011",
        "email": "user@example.com",
        "name": "John Doe",
        "created_at": "2024-12-10T10:00:00"
    }
    ```
    
    **Errors:**
    - `401`: Missing or invalid token
    """
    # Convertir ObjectId a string
    current_user["_id"] = str(current_user["_id"])
    
    return current_user