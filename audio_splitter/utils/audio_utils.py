"""
Utilidades para procesamiento de audio
"""

import librosa
import numpy as np
from pathlib import Path
from typing import Tuple, Union, Optional

def load_audio(file_path: Union[str, Path], 
               sample_rate: Optional[int] = None) -> Tuple[np.ndarray, int]:
    """
    Carga un archivo de audio
    
    Args:
        file_path: Ruta del archivo de audio
        sample_rate: Frecuencia de muestreo deseada (None para mantener original)
        
    Returns:
        Tuple[np.ndarray, int]: (audio_data, sample_rate)
    """
    return librosa.load(str(file_path), sr=sample_rate)

def get_audio_info(file_path: Union[str, Path]) -> dict:
    """
    Obtiene información básica de un archivo de audio
    
    Args:
        file_path: Ruta del archivo de audio
        
    Returns:
        dict: Información del audio
    """
    y, sr = load_audio(file_path)
    
    return {
        'duration': len(y) / sr,
        'sample_rate': sr,
        'channels': 1 if len(y.shape) == 1 else y.shape[0],
        'samples': len(y),
        'format': Path(file_path).suffix.lower()
    }

def ms_to_samples(milliseconds: float, sample_rate: int) -> int:
    """
    Convierte milisegundos a número de muestras
    
    Args:
        milliseconds: Tiempo en milisegundos
        sample_rate: Frecuencia de muestreo
        
    Returns:
        int: Número de muestras
    """
    return int((milliseconds / 1000) * sample_rate)

def samples_to_ms(samples: int, sample_rate: int) -> float:
    """
    Convierte número de muestras a milisegundos
    
    Args:
        samples: Número de muestras
        sample_rate: Frecuencia de muestreo
        
    Returns:
        float: Tiempo en milisegundos
    """
    return (samples / sample_rate) * 1000

def time_to_ms(time_str: str) -> int:
    """
    Convierte una cadena de tiempo a milisegundos
    
    Args:
        time_str: Tiempo en formato "MM:SS" o "HH:MM:SS" o "MM:SS.ms"
        
    Returns:
        int: Tiempo en milisegundos
    """
    parts = time_str.split(':')
    
    if len(parts) == 2:  # MM:SS o MM:SS.ms
        minutes, seconds = parts
        minutes = int(minutes)
        seconds = float(seconds)
        return int((minutes * 60 + seconds) * 1000)
    elif len(parts) == 3:  # HH:MM:SS o HH:MM:SS.ms
        hours, minutes, seconds = parts
        hours = int(hours)
        minutes = int(minutes)
        seconds = float(seconds)
        return int((hours * 3600 + minutes * 60 + seconds) * 1000)
    else:
        # Asumimos que es directamente segundos o milisegundos
        try:
            if '.' in time_str:  # Si tiene punto, asumimos segundos
                return int(float(time_str) * 1000)
            else:  # Si no, asumimos milisegundos
                return int(time_str)
        except ValueError:
            raise ValueError(f"Formato de tiempo no reconocido: {time_str}")

def ms_to_time(milliseconds: int) -> str:
    """
    Convierte milisegundos a formato de tiempo legible
    
    Args:
        milliseconds: Tiempo en milisegundos
        
    Returns:
        str: Tiempo en formato "MM:SS.ms"
    """
    total_seconds = milliseconds / 1000
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    
    return f"{minutes:02d}:{seconds:06.3f}"

def validate_audio_segment(start_ms: int, end_ms: int, duration_ms: int) -> bool:
    """
    Valida que un segmento de audio sea válido
    
    Args:
        start_ms: Tiempo de inicio en milisegundos
        end_ms: Tiempo de fin en milisegundos
        duration_ms: Duración total del audio en milisegundos
        
    Returns:
        bool: True si el segmento es válido
    """
    return (
        0 <= start_ms < end_ms <= duration_ms and
        start_ms >= 0 and
        end_ms > start_ms
    )
