"""
Módulo core - Lógica de negocio central del Audio Splitter
"""

from .splitter import AudioSplitter
from .converter import AudioConverter
from .metadata_manager import MetadataEditor

__all__ = ['AudioSplitter', 'AudioConverter', 'MetadataEditor']
