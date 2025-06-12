"""
Audio Splitter Suite - Sistema completo de procesamiento de audio

Este paquete proporciona herramientas para:
- División de archivos de audio en segmentos
- Conversión entre formatos (WAV, MP3, FLAC)
- Edición profesional de metadatos
- Gestión de carátulas de álbumes
"""

__version__ = "2.0.0"
__author__ = "Audio Splitter Team"
__email__ = "contact@audiosplitter.dev"

# Importaciones principales para facilitar el uso
from .core.splitter import AudioSplitter
from .core.converter import AudioConverter
from .core.metadata_manager import MetadataEditor

__all__ = [
    'AudioSplitter',
    'AudioConverter', 
    'MetadataEditor'
]
