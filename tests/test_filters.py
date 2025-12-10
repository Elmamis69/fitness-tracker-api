"""
Tests for filter utilities
"""
import pytest
from app.schemas.filters import WorkoutFilters, ExerciseFilters


@pytest.mark.unit
class TestWorkoutFilters:
    """Tests for WorkoutFilters"""
    
    def test_empty_filters(self):
        """Test filters with no values"""
        filters = WorkoutFilters()
        query = filters.to_mongo_query("user123")
        
        assert query == {"user_id": "user123"}
    
    def test_search_filter(self):
        """Test search filter"""
        filters = WorkoutFilters(search="Pecho")
        query = filters.to_mongo_query("user123")
        
        assert "user_id" in query
        assert "nombre" in query
        assert "$regex" in query["nombre"]
    
    def test_date_range_filter(self):
        """Test date range filters"""
        filters = WorkoutFilters(
            fecha_desde="2024-01-01",
            fecha_hasta="2024-12-31"
        )
        query = filters.to_mongo_query("user123")
        
        assert "fecha" in query
        assert "$gte" in query["fecha"]
        assert "$lte" in query["fecha"]
    
    def test_duration_filter(self):
        """Test duration filters"""
        filters = WorkoutFilters(
            duracion_min=30,
            duracion_max=90
        )
        query = filters.to_mongo_query("user123")
        
        assert "duracion_minutos" in query
        assert "$gte" in query["duracion_minutos"]
        assert "$lte" in query["duracion_minutos"]
    
    def test_combined_filters(self):
        """Test combining multiple filters"""
        filters = WorkoutFilters(
            search="Pierna",
            fecha_desde="2024-01-01",
            duracion_min=45
        )
        query = filters.to_mongo_query("user123")
        
        assert "user_id" in query
        assert "nombre" in query
        assert "fecha" in query
        assert "duracion_minutos" in query
    
    def test_only_min_duration(self):
        """Test filter with only minimum duration"""
        filters = WorkoutFilters(duracion_min=30)
        query = filters.to_mongo_query("user123")
        
        assert "duracion_minutos" in query
        assert "$gte" in query["duracion_minutos"]
        assert "$lte" not in query["duracion_minutos"]
    
    def test_only_max_duration(self):
        """Test filter with only maximum duration"""
        filters = WorkoutFilters(duracion_max=60)
        query = filters.to_mongo_query("user123")
        
        assert "duracion_minutos" in query
        assert "$lte" in query["duracion_minutos"]
        assert "$gte" not in query["duracion_minutos"]


@pytest.mark.unit
class TestExerciseFilters:
    """Tests for ExerciseFilters"""
    
    def test_empty_filters(self):
        """Test filters with no values"""
        filters = ExerciseFilters()
        query = filters.to_mongo_query("user123")
        
        assert query == {"user_id": "user123"}
    
    def test_search_filter(self):
        """Test search filter"""
        filters = ExerciseFilters(search="Press")
        query = filters.to_mongo_query("user123")
        
        assert "user_id" in query
        assert "nombre" in query
        assert "$regex" in query["nombre"]
    
    def test_category_filter(self):
        """Test category filter"""
        filters = ExerciseFilters(categoria="Pecho")
        query = filters.to_mongo_query("user123")
        
        assert "categoria" in query
        assert query["categoria"] == "Pecho"
    
    def test_type_filter(self):
        """Test type filter"""
        filters = ExerciseFilters(tipo="Fuerza")
        query = filters.to_mongo_query("user123")
        
        assert "tipo" in query
        assert query["tipo"] == "Fuerza"
    
    def test_combined_filters(self):
        """Test combining multiple filters"""
        filters = ExerciseFilters(
            search="Press",
            categoria="Pecho",
            tipo="Fuerza"
        )
        query = filters.to_mongo_query("user123")
        
        assert "user_id" in query
        assert "nombre" in query
        assert "categoria" in query
        assert "tipo" in query
    
    def test_case_insensitive_search(self):
        """Test that search is case insensitive"""
        filters = ExerciseFilters(search="PRESS")
        query = filters.to_mongo_query("user123")
        
        # Check that $options: "i" is set for case-insensitive search
        assert "nombre" in query
        assert "$regex" in query["nombre"]
        assert query["nombre"]["$options"] == "i"
