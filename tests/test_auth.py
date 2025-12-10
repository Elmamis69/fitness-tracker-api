"""
Tests for authentication endpoints
"""
import pytest
from httpx import AsyncClient


@pytest.mark.unit
class TestAuthRegister:
    """Tests for user registration"""
    
    async def test_register_success(self, client: AsyncClient):
        """Test successful user registration"""
        user_data = {
            "email": "newuser@example.com",
            "password": "SecurePassword123!",
            "name": "New User"
        }
        
        response = await client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["name"] == user_data["name"]
        assert "_id" in data
        assert "password" not in data
    
    async def test_register_duplicate_email(self, client: AsyncClient, test_user: dict):
        """Test registration with duplicate email fails"""
        user_data = {
            "email": test_user["email"],
            "password": "AnotherPassword123!",
            "name": "Another User"
        }
        
        response = await client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    async def test_register_invalid_email(self, client: AsyncClient):
        """Test registration with invalid email format"""
        user_data = {
            "email": "not-an-email",
            "password": "SecurePassword123!",
            "name": "Test User"
        }
        
        response = await client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == 422
    
    async def test_register_weak_password(self, client: AsyncClient):
        """Test registration with weak password"""
        user_data = {
            "email": "weakpass@example.com",
            "password": "123",
            "name": "Weak Pass User"
        }
        
        response = await client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == 422
    
    async def test_register_missing_fields(self, client: AsyncClient):
        """Test registration with missing required fields"""
        response = await client.post("/api/auth/register", json={})
        
        assert response.status_code == 422


@pytest.mark.unit
class TestAuthLogin:
    """Tests for user login"""
    
    async def test_login_success(self, client: AsyncClient, test_user: dict):
        """Test successful login"""
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        
        response = await client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == test_user["email"]
    
    async def test_login_wrong_password(self, client: AsyncClient, test_user: dict):
        """Test login with incorrect password"""
        login_data = {
            "email": test_user["email"],
            "password": "WrongPassword123!"
        }
        
        response = await client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()
    
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with non-existent email"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "SomePassword123!"
        }
        
        response = await client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == 401
    
    async def test_login_missing_fields(self, client: AsyncClient):
        """Test login with missing fields"""
        response = await client.post("/api/auth/login", json={})
        
        assert response.status_code == 422


@pytest.mark.unit
class TestAuthProtectedRoutes:
    """Tests for protected routes authentication"""
    
    async def test_access_protected_route_with_valid_token(
        self, 
        client: AsyncClient, 
        auth_headers: dict
    ):
        """Test accessing protected route with valid token"""
        response = await client.get("/api/exercises/", headers=auth_headers)
        
        assert response.status_code == 200
    
    async def test_access_protected_route_without_token(self, client: AsyncClient):
        """Test accessing protected route without token"""
        response = await client.get("/api/exercises/")
        
        assert response.status_code == 401
    
    async def test_access_protected_route_with_invalid_token(self, client: AsyncClient):
        """Test accessing protected route with invalid token"""
        headers = {"Authorization": "Bearer invalid_token_here"}
        response = await client.get("/api/exercises/", headers=headers)
        
        assert response.status_code == 401
    
    async def test_access_protected_route_with_malformed_header(self, client: AsyncClient):
        """Test accessing protected route with malformed auth header"""
        headers = {"Authorization": "InvalidFormat token"}
        response = await client.get("/api/exercises/", headers=headers)
        
        assert response.status_code == 401
