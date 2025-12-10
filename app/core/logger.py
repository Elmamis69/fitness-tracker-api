from loguru import logger
import sys
from app.core.config import settings

# Configurar formato del logger
log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# Remover handler por defecto
logger.remove()

# Agregar handler para consola
logger.add(
    sys.stdout,
    format = log_format,
    level = "DEBUG" if settings.ENVIRONMENT == "development" else "INFO",
    colorize = True
)

# Agregar handler para archivo (solo en producción)
if settings.ENVIRONMENT == "production":
    logger.add(
        "logs/app_{time:YYYY-MM-DD}.log",
        format = log_format,
        level = "INFO",
        rotation = "00:00", # Nuevo archivo cada día
        retention = "30 days", # Mantener logs por 30 días
        compression = "zip" # Comprimir logs antiguos
    )

# Exportar logger configurado
__all__ = ["logger"]