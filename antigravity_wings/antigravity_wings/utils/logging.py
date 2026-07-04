import logging
import os
import sys

def setup_logging(level=None):
    """
    Configura el logging para todo el sistema Antigravity Wings.
    Permite configuración externa vía variables de entorno.
    """
    if level is None:
        level_str = os.getenv("AGW_LOG_LEVEL", "INFO").upper()
        level = getattr(logging, level_str, logging.INFO)

    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))

    # File Handler (opcional si hay ruta configurada)
    log_file = os.getenv("AGW_LOG_FILE")
    handlers = [console_handler]
    
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(log_format, date_format))
        handlers.append(file_handler)

    logging.basicConfig(
        level=level,
        handlers=handlers,
        force=True # Sobrescribe configuraciones previas
    )
    
    # Silenciar logs ruidosos de librerías externas
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized at level {logging.getLevelName(level)}")
