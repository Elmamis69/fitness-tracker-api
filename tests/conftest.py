"""
Pytest configuration and fixtures
"""
import pytest
import asyncio
import sys
from pathlib import Path
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app
from app.core.config import settings


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Create an async HTTP client for testing"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_db():
    """Create a test database connection"""
    # Use a test database
    test_settings = settings.copy()
    test_settings.MONGO_DB_NAME = "fitness_tracker_test"
    
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[test_settings.MONGO_DB_NAME]
    
    yield db
    
    # Cleanup: drop all collections after tests
    for collection_name in await db.list_collection_names():
        await db[collection_name].drop()
    
    client.close()


@pytest.fixture
async def test_user(client: AsyncClient) -> dict:
    """Create a test user and return user data with token"""
    user_data = {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "name": "Test User"
    }
    
    # Register user
    response = await client.post("/api/auth/register", json=user_data)
    assert response.status_code == 201
    
    # Login to get token
    login_response = await client.post(
        "/api/auth/login",
        json={"email": user_data["email"], "password": user_data["password"]}
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    
    return {
        "email": user_data["email"],
        "password": user_data["password"],
        "name": user_data["name"],
        "token": token_data["access_token"],
        "user_id": token_data["user"]["_id"]
    }


@pytest.fixture
def auth_headers(test_user: dict) -> dict:
    """Return authorization headers with test user token"""
    return {"Authorization": f"Bearer {test_user['token']}"}


@pytest.fixture
async def test_exercise(client: AsyncClient, auth_headers: dict) -> dict:
    """Create a test exercise"""
    exercise_data = {
        "nombre": "Press de Banca",
        "descripcion": "Ejercicio compuesto de pecho",
        "categoria": "Pecho",
        "tipo": "Fuerza",
        "musculos_principales": ["Pectoral Mayor", "Tríceps"],
        "equipo": "Barra"
    }
    
    response = await client.post(
        "/api/exercises/",
        json=exercise_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
async def test_workout(client: AsyncClient, auth_headers: dict, test_exercise: dict) -> dict:
    """Create a test workout"""
    workout_data = {
        "nombre": "Entrenamiento de Pecho",
        "fecha": "2024-12-10T10:00:00",
        "duracion": 60,
        "notas": "Sesión de prueba",
        "ejercicios": [
            {
                "exercise_id": test_exercise["_id"],
                "sets": [
                    {"reps": 10, "weight": 80.0, "rest_seconds": 90},
                    {"reps": 8, "weight": 85.0, "rest_seconds": 90}
                ]
            }
        ]
    }
    
    response = await client.post(
        "/api/workouts/",
        json=workout_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    return response.json()
