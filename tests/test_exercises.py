"""
Tests for exercise endpoints
"""
import pytest
from httpx import AsyncClient


@pytest.mark.unit
class TestExerciseCreate:
    """Tests for creating exercises"""
    
    async def test_create_exercise_success(self, client: AsyncClient, auth_headers: dict):
        """Test successful exercise creation"""
        exercise_data = {
            "nombre": "Sentadilla",
            "descripcion": "Ejercicio compuesto de piernas",
            "categoria": "Piernas",
            "tipo": "Fuerza",
            "musculos_principales": ["Cuádriceps", "Glúteos"],
            "equipo": "Barra"
        }
        
        response = await client.post(
            "/api/exercises/",
            json=exercise_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == exercise_data["nombre"]
        assert data["categoria"] == exercise_data["categoria"]
        assert "_id" in data
    
    async def test_create_exercise_without_auth(self, client: AsyncClient):
        """Test creating exercise without authentication fails"""
        exercise_data = {
            "nombre": "Sentadilla",
            "descripcion": "Ejercicio de piernas",
            "categoria": "Piernas",
            "tipo": "Fuerza"
        }
        
        response = await client.post("/api/exercises/", json=exercise_data)
        
        assert response.status_code == 401
    
    async def test_create_exercise_missing_required_fields(
        self, 
        client: AsyncClient, 
        auth_headers: dict
    ):
        """Test creating exercise with missing required fields"""
        exercise_data = {
            "nombre": "Sentadilla"
            # Missing required fields
        }
        
        response = await client.post(
            "/api/exercises/",
            json=exercise_data,
            headers=auth_headers
        )
        
        assert response.status_code == 422


@pytest.mark.unit
class TestExerciseList:
    """Tests for listing exercises"""
    
    async def test_get_exercises_empty_list(self, client: AsyncClient, auth_headers: dict):
        """Test getting exercises when user has none"""
        response = await client.get("/api/exercises/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert data["total"] == 0
        assert len(data["items"]) == 0
    
    async def test_get_exercises_with_data(
        self, 
        client: AsyncClient, 
        auth_headers: dict,
        test_exercise: dict
    ):
        """Test getting exercises returns user's exercises"""
        response = await client.get("/api/exercises/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert len(data["items"]) >= 1
        assert any(ex["_id"] == test_exercise["_id"] for ex in data["items"])
    
    async def test_get_exercises_pagination(
        self, 
        client: AsyncClient, 
        auth_headers: dict,
        test_exercise: dict
    ):
        """Test exercise pagination"""
        response = await client.get(
            "/api/exercises/?page=1&size=5",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "page" in data
        assert "size" in data
        assert "total" in data
        assert "total_pages" in data
        assert data["page"] == 1
        assert data["size"] == 5
    
    async def test_get_exercises_without_auth(self, client: AsyncClient):
        """Test getting exercises without authentication fails"""
        response = await client.get("/api/exercises/")
        
        assert response.status_code == 401


@pytest.mark.unit
class TestExerciseDetail:
    """Tests for getting exercise details"""
    
    async def test_get_exercise_by_id_success(
        self, 
        client: AsyncClient, 
        auth_headers: dict,
        test_exercise: dict
    ):
        """Test getting exercise by ID"""
        response = await client.get(
            f"/api/exercises/{test_exercise['_id']}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["_id"] == test_exercise["_id"]
        assert data["nombre"] == test_exercise["nombre"]
    
    async def test_get_exercise_not_found(self, client: AsyncClient, auth_headers: dict):
        """Test getting non-existent exercise"""
        fake_id = "507f1f77bcf86cd799439011"
        response = await client.get(
            f"/api/exercises/{fake_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 404
    
    async def test_get_exercise_invalid_id(self, client: AsyncClient, auth_headers: dict):
        """Test getting exercise with invalid ID format"""
        response = await client.get(
            "/api/exercises/invalid_id",
            headers=auth_headers
        )
        
        assert response.status_code == 404


@pytest.mark.unit
class TestExerciseUpdate:
    """Tests for updating exercises"""
    
    async def test_update_exercise_success(
        self, 
        client: AsyncClient, 
        auth_headers: dict,
        test_exercise: dict
    ):
        """Test successful exercise update"""
        update_data = {
            "descripcion": "Descripción actualizada",
            "equipo": "Barra Olímpica"
        }
        
        response = await client.put(
            f"/api/exercises/{test_exercise['_id']}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["descripcion"] == update_data["descripcion"]
        assert data["equipo"] == update_data["equipo"]
        assert data["nombre"] == test_exercise["nombre"]  # Unchanged
    
    async def test_update_exercise_not_found(self, client: AsyncClient, auth_headers: dict):
        """Test updating non-existent exercise"""
        fake_id = "507f1f77bcf86cd799439011"
        update_data = {"descripcion": "Nueva descripción"}
        
        response = await client.put(
            f"/api/exercises/{fake_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 404


@pytest.mark.unit
class TestExerciseDelete:
    """Tests for deleting exercises"""
    
    async def test_delete_exercise_success(
        self, 
        client: AsyncClient, 
        auth_headers: dict,
        test_exercise: dict
    ):
        """Test successful exercise deletion"""
        response = await client.delete(
            f"/api/exercises/{test_exercise['_id']}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        
        # Verify exercise is deleted
        get_response = await client.get(
            f"/api/exercises/{test_exercise['_id']}",
            headers=auth_headers
        )
        assert get_response.status_code == 404
    
    async def test_delete_exercise_not_found(self, client: AsyncClient, auth_headers: dict):
        """Test deleting non-existent exercise"""
        fake_id = "507f1f77bcf86cd799439011"
        response = await client.delete(
            f"/api/exercises/{fake_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 404


@pytest.mark.unit
class TestExerciseFilters:
    """Tests for exercise filtering"""
    
    async def test_filter_by_search(
        self, 
        client: AsyncClient, 
        auth_headers: dict,
        test_exercise: dict
    ):
        """Test filtering exercises by search term"""
        response = await client.get(
            "/api/exercises/?search=Press",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert any("Press" in ex["nombre"] for ex in data["items"])
    
    async def test_filter_by_category(
        self, 
        client: AsyncClient, 
        auth_headers: dict,
        test_exercise: dict
    ):
        """Test filtering exercises by category"""
        response = await client.get(
            f"/api/exercises/?categoria={test_exercise['categoria']}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(ex["categoria"] == test_exercise["categoria"] for ex in data["items"])
    
    async def test_filter_by_type(
        self, 
        client: AsyncClient, 
        auth_headers: dict,
        test_exercise: dict
    ):
        """Test filtering exercises by type"""
        response = await client.get(
            f"/api/exercises/?tipo={test_exercise['tipo']}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(ex["tipo"] == test_exercise["tipo"] for ex in data["items"])
