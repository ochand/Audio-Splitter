"""
Sistema de logging para Audio Splitter Suite
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from ..config.environment import LOG_LEVEL, LOG_FILE, DEBUG

def setup_logging(
    level: Optional[str] = None,
    log_file: Optional[str] = None,
    console_output: bool = True
) -> logging.Logger:
    """
    Configura el sistema de logging
    
    Args:
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR)
        log_file: Archivo de log (opcional)
        console_output: Si mostrar logs en consola
    
    Returns:
        Logger configurado
    """
    
    # Usar configuración por defecto si no se especifica
    level = level or LOG_LEVEL
    log_file = log_file or str(LOG_FILE)
    
    # Crear logger
    logger = logging.getLogger('audio_splitter')
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Limpiar handlers existentes
    logger.handlers.clear()
    
    # Formato de logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para consola
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Handler para archivo (si se especifica)
    if log_file:
        try:
            # Crear directorio de logs si no existe
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"No se pudo configurar logging a archivo: {e}")
    
    return logger

def get_logger(name: str = 'audio_splitter') -> logging.Logger:
    """Obtiene un logger configurado"""
    return logging.getLogger(name)

# Logger por defecto
default_logger = setup_logging()
