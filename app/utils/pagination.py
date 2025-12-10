from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field
from math import ceil

T = TypeVar('T')

class PaginationParams(BaseModel):
    """Parámetros de paginación"""
    page: int = Field(default = 1, ge = 1, description = "Número de página (inicia en 1)")
    size: int = Field(default = 10, ge = 1, le = 100, description = "Items por página (maximo 100)")

    @property
    def skip(self) -> int:
        """Calcular cuántos items saltar"""
        return (self.page - 1) * self.size
    
    @property
    def limit(self) -> int:
        """Límite de items a retornar"""
        return self.size
    
class PaginatedResponse(BaseModel, Generic[T]):
    """Respuesta paginada genérica"""
    items: List[T] 
    total: int = Field(..., description = "Total de items en la base de datos")
    page: int = Field(..., description = "Página actual")
    page_size: int = Field(..., description = "Items por páginas")
    total_pages: int = Field(..., description = "Total de páginas")
    has_next: bool = Field(..., description = "Si hay una página siguiente")
    has_prev: bool = Field(..., description = "Si hay una página anterior")

    @classmethod
    def create(cls, items: List[T], total: int, params: PaginationParams):
        """Factory method para crear la respuesta paginada"""
        total_pages = ceil(total / params.page_size) if total > 0 else 0

        return cls(
            items = items,
            total = total,
            page = params.page,
            page_size = params.page_size,
            total_pages = total_pages,
            has_next = params.page < total_pages,
            has_prev = params.page > 1,
        )