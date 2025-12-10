from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.logger import logger

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handler para excepciones HTTP"""
    logger.error(f"FTTP {exc.status_code}: {exc.detail} - {request.method} {request.url}")
    return JSONResponse(
        status_code = exc.status_code,
        content = {
            "error": True,
            "status_code": exc.status_code,
            "message": exc.detail,
            "path": str(request.url)
            },
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler para errores de validacion de Pydantic"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": "->".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(f"Validation Error: {errors} - {request.method} {request.url}")

    return JSONResponse(
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
        content = {
            "error": True,
            "status_code": 422,
            "message": "Validation Error",
            "details": errors,
            "path": str(request.url)
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handler para excepciones generales no capturadas"""
    logger.exception(f"Unhandled exception: {(exc)} - {request.method} {request.url}")
    return JSONResponse(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        content = {
            "error": True,
            "status_code": 500,
            "message": "Internal Server Error",
            "detail": str(exc) if isinstance(exc, Exception) else "An unexpected error occurred",
            "path": str(request.url)
        }
    )