"""
Configuraciones globales del Audio Splitter Suite
"""

import os
from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).parent.parent.parent

# Directorios de datos
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = DATA_DIR / "output"
SOURCES_DIR = DATA_DIR / "sources"
TEMPLATES_DIR = DATA_DIR / "templates"
METADATA_DIR = DATA_DIR / "metadata"

# Formatos soportados
SUPPORTED_INPUT_FORMATS = ['.wav', '.mp3', '.flac', '.m4a', '.ogg']
SUPPORTED_OUTPUT_FORMATS = ['.wav', '.mp3', '.flac']

# Configuraciones de calidad
QUALITY_PRESETS = {
    'mp3': {
        'low': {'bitrate': '128k'},
        'medium': {'bitrate': '192k'},
        'high': {'bitrate': '320k'},
        'vbr_medium': {'codec': 'libmp3lame', 'parameters': ['-q:a', '2']},
        'vbr_high': {'codec': 'libmp3lame', 'parameters': ['-q:a', '0']}
    },
    'flac': {
        'low': {'compression_level': 0},
        'medium': {'compression_level': 5},
        'high': {'compression_level': 8}
    }
}

# Configuraciones de metadatos
DEFAULT_ENCODING = 3  # UTF-8 para ID3
SUPPORTED_ARTWORK_FORMATS = ['.jpg', '.jpeg', '.png']
MAX_ARTWORK_SIZE = 10 * 1024 * 1024  # 10MB

# Configuraciones de la interfaz
DEFAULT_OUTPUT_DIR = str(OUTPUT_DIR)
DEFAULT_PRESERVE_METADATA = True

# Crear directorios si no existen
def ensure_directories():
    """Crea los directorios necesarios si no existen"""
    for directory in [OUTPUT_DIR, SOURCES_DIR, TEMPLATES_DIR, METADATA_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

# Ejecutar al importar
ensure_directories()
