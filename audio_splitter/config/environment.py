"""
Configuración de entorno para Audio Splitter Suite
"""

import os
from pathlib import Path

# Variables de entorno con valores por defecto
def get_env_path(env_var: str, default_path: str) -> Path:
    """Obtiene ruta desde variable de entorno o usa default"""
    return Path(os.getenv(env_var, default_path))

def get_env_bool(env_var: str, default: bool) -> bool:
    """Obtiene booleano desde variable de entorno"""
    value = os.getenv(env_var, str(default)).lower()
    return value in ('true', '1', 'yes', 'on')

# Rutas configurables por entorno
BASE_DIR = Path(__file__).parent.parent.parent
OUTPUT_DIR = get_env_path('AUDIO_SPLITTER_OUTPUT_DIR', str(BASE_DIR / 'data' / 'output'))
SOURCES_DIR = get_env_path('AUDIO_SPLITTER_SOURCES_DIR', str(BASE_DIR / 'data' / 'sources'))
TEMPLATES_DIR = get_env_path('AUDIO_SPLITTER_TEMPLATES_DIR', str(BASE_DIR / 'data' / 'templates'))

# Configuraciones por entorno
DEFAULT_QUALITY = os.getenv('AUDIO_SPLITTER_DEFAULT_QUALITY', 'high')
DEFAULT_FORMAT = os.getenv('AUDIO_SPLITTER_DEFAULT_FORMAT', 'mp3')
PRESERVE_METADATA = get_env_bool('AUDIO_SPLITTER_PRESERVE_METADATA', True)

# Configuración de logging
LOG_LEVEL = os.getenv('AUDIO_SPLITTER_LOG_LEVEL', 'INFO')
LOG_FILE = get_env_path('AUDIO_SPLITTER_LOG_FILE', str(BASE_DIR / 'logs' / 'audio_splitter.log'))

# Configuración de desarrollo
DEBUG = get_env_bool('AUDIO_SPLITTER_DEBUG', False)
VERBOSE = get_env_bool('AUDIO_SPLITTER_VERBOSE', False)
