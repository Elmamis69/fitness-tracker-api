"""
Tests for pagination utility
"""
import pytest
from app.utils.pagination import PaginationParams, PaginatedResponse


@pytest.mark.unit
class TestPaginationParams:
    """Tests for PaginationParams"""
    
    def test_default_values(self):
        """Test default pagination parameters"""
        params = PaginationParams()
        assert params.page == 1
        assert params.size == 10
    
    def test_custom_values(self):
        """Test custom pagination parameters"""
        params = PaginationParams(page=2, size=20)
        assert params.page == 2
        assert params.size == 20
    
    def test_skip_calculation(self):
        """Test skip offset calculation"""
        params = PaginationParams(page=1, size=10)
        assert params.skip == 0
        
        params = PaginationParams(page=2, size=10)
        assert params.skip == 10
        
        params = PaginationParams(page=3, size=25)
        assert params.skip == 50
    
    def test_limit_property(self):
        """Test limit property"""
        params = PaginationParams(page=1, size=15)
        assert params.limit == 15
    
    def test_max_size_validation(self):
        """Test maximum size validation"""
        with pytest.raises(Exception):  # Pydantic validation error
            params = PaginationParams(page=1, size=150)
    
    def test_minimum_values(self):
        """Test minimum values validation"""
        params = PaginationParams(page=1, size=1)
        assert params.page >= 1
        assert params.size >= 1


@pytest.mark.unit
class TestPaginatedResponse:
    """Tests for PaginatedResponse"""
    
    def test_create_paginated_response(self):
        """Test creating paginated response"""
        items = [{"id": 1}, {"id": 2}, {"id": 3}]
        total = 10
        params = PaginationParams(page=1, size=3)
        
        response = PaginatedResponse.create(items, total, params)
        
        assert response.items == items
        assert response.total == total
        assert response.page == 1
        assert response.page_size == 3
        assert response.total_pages == 4  # ceil(10/3)
    
    def test_has_next_page(self):
        """Test has_next property"""
        params = PaginationParams(page=1, size=5)
        response = PaginatedResponse.create([1, 2, 3, 4, 5], 10, params)
        assert response.has_next is True
        
        params = PaginationParams(page=2, size=5)
        response = PaginatedResponse.create([6, 7, 8, 9, 10], 10, params)
        assert response.has_next is False
    
    def test_has_previous_page(self):
        """Test has_prev property"""
        params = PaginationParams(page=1, size=5)
        response = PaginatedResponse.create([1, 2, 3, 4, 5], 10, params)
        assert response.has_prev is False
        
        params = PaginationParams(page=2, size=5)
        response = PaginatedResponse.create([6, 7, 8, 9, 10], 10, params)
        assert response.has_prev is True
    
    def test_total_pages_calculation(self):
        """Test total pages calculation"""
        params = PaginationParams(page=1, size=10)
        
        # Exact division
        response = PaginatedResponse.create([], 30, params)
        assert response.total_pages == 3
        
        # With remainder
        response = PaginatedResponse.create([], 35, params)
        assert response.total_pages == 4
        
        # Empty result
        response = PaginatedResponse.create([], 0, params)
        assert response.total_pages == 0
    
    def test_empty_result(self):
        """Test paginated response with empty results"""
        params = PaginationParams(page=1, size=10)
        response = PaginatedResponse.create([], 0, params)
        
        assert response.items == []
        assert response.total == 0
        assert response.total_pages == 0
        assert response.has_next is False
        assert response.has_prev is False
