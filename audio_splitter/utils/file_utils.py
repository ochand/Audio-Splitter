"""
Utilidades para manejo de archivos
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Union

def ensure_directory(path: Union[str, Path]) -> Path:
    """
    Asegura que un directorio exista, lo crea si no existe
    
    Args:
        path: Ruta del directorio
        
    Returns:
        Path: Objeto Path del directorio
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_files_by_extension(directory: Union[str, Path], 
                          extensions: List[str], 
                          recursive: bool = False) -> List[Path]:
    """
    Obtiene archivos por extensión en un directorio
    
    Args:
        directory: Directorio a buscar
        extensions: Lista de extensiones (ej: ['.mp3', '.wav'])
        recursive: Si buscar en subdirectorios
        
    Returns:
        List[Path]: Lista de archivos encontrados
    """
    directory = Path(directory)
    pattern = "**/*" if recursive else "*"
    
    files = []
    for ext in extensions:
        files.extend(directory.glob(f"{pattern}{ext}"))
    
    return files

def safe_filename(filename: str) -> str:
    """
    Convierte un filename a un nombre seguro para el sistema de archivos
    
    Args:
        filename: Nombre original
        
    Returns:
        str: Nombre seguro
    """
    # Caracteres no permitidos en nombres de archivo
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Eliminar espacios extra y puntos al final
    filename = filename.strip().rstrip('.')
    
    return filename

def get_unique_filename(directory: Union[str, Path], 
                       base_name: str, 
                       extension: str) -> Path:
    """
    Genera un nombre de archivo único en un directorio
    
    Args:
        directory: Directorio destino
        base_name: Nombre base del archivo
        extension: Extensión del archivo
        
    Returns:
        Path: Ruta única para el archivo
    """
    directory = Path(directory)
    extension = extension if extension.startswith('.') else f'.{extension}'
    
    # Limpiar nombre base
    base_name = safe_filename(base_name)
    
    # Generar nombre único
    counter = 1
    filename = f"{base_name}{extension}"
    file_path = directory / filename
    
    while file_path.exists():
        filename = f"{base_name}_{counter}{extension}"
        file_path = directory / filename
        counter += 1
    
    return file_path

def get_file_size_mb(file_path: Union[str, Path]) -> float:
    """
    Obtiene el tamaño de un archivo en MB
    
    Args:
        file_path: Ruta del archivo
        
    Returns:
        float: Tamaño en MB
    """
    return Path(file_path).stat().st_size / (1024 * 1024)

def copy_file_with_metadata(source: Union[str, Path], 
                           destination: Union[str, Path]) -> bool:
    """
    Copia un archivo preservando metadatos del sistema
    
    Args:
        source: Archivo fuente
        destination: Archivo destino
        
    Returns:
        bool: True si la copia fue exitosa
    """
    try:
        shutil.copy2(str(source), str(destination))
        return True
    except Exception:
        return False
