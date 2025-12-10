"""
Tests for workout endpoints
"""
import pytest
from httpx import AsyncClient


@pytest.mark.unit
class TestWorkoutCreate:
    """Tests for creating workouts"""
    
    async def test_create_workout_success(
        self, 
        client: AsyncClient, 
        auth_headers: dict,
        test_exercise: dict
    ):
        """Test successful workout creation"""
        workout_data = {
            "nombre": "Día de Pecho",
            "fecha": "2024-12-10T10:00:00",
            "duracion": 45,
            "notas": "Buen entrenamiento",
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
        data = response.json()
        assert data["nombre"] == workout_data["nombre"]
        assert data["duracion"] == workout_data["duracion"]
        assert len(data["ejercicios"]) == 1
        assert "_id" in data
    
    async def test_create_workout_without_auth(self, client: AsyncClient, test_exercise: dict):
        """Test creating workout without authentication fails"""
        workout_data = {
            "nombre": "Test Workout",
            "fecha": "2024-12-10T10:00:00",
            "ejercicios": []
        }
        
        response = await client.post("/api/workouts/", json=workout_data)
        
        assert response.status_code == 401
    
    async def test_create_workout_missing_required_fields(
        self, 
        client: AsyncClient, 
        auth_headers: dict
    ):
        """Test creating workout with missing required fields"""
        workout_data = {
            "nombre": "Test Workout"
            # Missing required fields
        }
        
        response = await client.post(
            "/api/workouts/",
            json=workout_data,
            headers=auth_headers
        )
        
        assert response.status_code == 422


@pytest.mark.unit
class TestWorkoutList:
    """Tests for listing workouts"""
    
    async def test_get_workouts_empty_list(self, client: AsyncClient, auth_headers: dict):
        """Test getting workouts when user has none"""
        response = await client.get("/api/workouts/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert data["total"] == 0
        assert len(data["items"]) == 0
    
    async def test_get_workouts_with_data(
        self, 
        client: AsyncClient, 
        auth_headers: dict,
        test_workout: dict
    ):
        """Test getting workouts returns user's workouts"""
        response = await client.get("/api/workouts/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert len(data["items"]) >= 1
        assert any(w["_id"] == test_workout["_id"] for w in data["items"])
    
    async def test_get_workouts_pagination(
        self, 
        client: AsyncClient, 
        auth_headers: dict,
        test_workout: dict
    ):
        """Test workout pagination"""
        response = await client.get(
            "/api/workouts/?page=1&size=5",
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
    
    async def test_get_workouts_without_auth(self, client: AsyncClient):
        """Test getting workouts without authentication fails"""
        response = await client.get("/api/workouts/")
        
        assert response.status_code == 401


@pytest.mark.unit
class TestWorkoutDetail:
    """Tests for getting workout details"""
    
    async def test_get_workout_by_id_success(
        self, 
        client: AsyncClient, 
        auth_headers: dict,
        test_workout: dict
    ):
        """Test getting workout by ID"""
        response = await client.get(
            f"/api/workouts/{test_workout['_id']}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["_id"] == test_workout["_id"]
        assert data["nombre"] == test_workout["nombre"]
    
    async def test_get_workout_not_found(self, client: AsyncClient, auth_headers: dict):
        """Test getting non-existent workout"""
        fake_id = "507f1f77bcf86cd799439011"
        response = await client.get(
            f"/api/workouts/{fake_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 404
    
    async def test_get_workout_invalid_id(self, client: AsyncClient, auth_headers: dict):
        """Test getting workout with invalid ID format"""
        response = await client.get(
            "/api/workouts/invalid_id",
            headers=auth_headers
        )
        
        assert response.status_code == 404


@pytest.mark.unit
class TestWorkoutUpdate:
    """Tests for updating workouts"""
    
    async def test_update_workout_success(
        self, 
        client: AsyncClient, 
        auth_headers: dict,
        test_workout: dict
    ):
        """Test successful workout update"""
        update_data = {
            "nombre": "Entrenamiento Actualizado",
            "duracion": 75,
            "notas": "Notas actualizadas"
        }
        
        response = await client.put(
            f"/api/workouts/{test_workout['_id']}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == update_data["nombre"]
        assert data["duracion"] == update_data["duracion"]
        assert data["notas"] == update_data["notas"]
    
    async def test_update_workout_not_found(self, client: AsyncClient, auth_headers: dict):
        """Test updating non-existent workout"""
        fake_id = "507f1f77bcf86cd799439011"
        update_data = {"nombre": "Nuevo Nombre"}
        
        response = await client.put(
            f"/api/workouts/{fake_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 404


@pytest.mark.unit
class TestWorkoutDelete:
    """Tests for deleting workouts"""
    
    async def test_delete_workout_success(
        self, 
        client: AsyncClient, 
        auth_headers: dict,
        test_workout: dict
    ):
        """Test successful workout deletion"""
        response = await client.delete(
            f"/api/workouts/{test_workout['_id']}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        
        # Verify workout is deleted
        get_response = await client.get(
            f"/api/workouts/{test_workout['_id']}",
            headers=auth_headers
        )
        assert get_response.status_code == 404
    
    async def test_delete_workout_not_found(self, client: AsyncClient, auth_headers: dict):
        """Test deleting non-existent workout"""
        fake_id = "507f1f77bcf86cd799439011"
        response = await client.delete(
            f"/api/workouts/{fake_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 404


@pytest.mark.unit
class TestWorkoutFilters:
    """Tests for workout filtering"""
    
    async def test_filter_by_search(
        self, 
        client: AsyncClient, 
        auth_headers: dict,
        test_workout: dict
    ):
        """Test filtering workouts by search term"""
        response = await client.get(
            "/api/workouts/?search=Pecho",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        if data["total"] > 0:
            assert any("Pecho" in w["nombre"] or "Pecho" in w.get("notas", "") 
                      for w in data["items"])
    
    async def test_filter_by_date_range(
        self, 
        client: AsyncClient, 
        auth_headers: dict,
        test_workout: dict
    ):
        """Test filtering workouts by date range"""
        response = await client.get(
            "/api/workouts/?fecha_desde=2024-12-01&fecha_hasta=2024-12-31",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
    
    async def test_filter_by_duration(
        self, 
        client: AsyncClient, 
        auth_headers: dict,
        test_workout: dict
    ):
        """Test filtering workouts by duration"""
        response = await client.get(
            "/api/workouts/?duracion_min=30&duracion_max=90",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        if data["total"] > 0:
            assert all(30 <= w["duracion"] <= 90 for w in data["items"])
    
    async def test_filter_combined(
        self, 
        client: AsyncClient, 
        auth_headers: dict,
        test_workout: dict
    ):
        """Test combining multiple filters"""
        response = await client.get(
            "/api/workouts/?search=Pecho&duracion_min=30&page=1&size=5",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
