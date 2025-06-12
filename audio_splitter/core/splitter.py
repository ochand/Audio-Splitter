#!/usr/bin/env python3
"""
Audio Splitter Core - Corta archivos de audio .wav en segmentos definidos por el usuario.
Uso: Especifica el archivo de entrada y los tiempos de inicio y fin para cada segmento.
"""

# Alternativa usando librosa y soundfile que son más compatibles con Python 3.13
import librosa
import soundfile as sf
import numpy as np
import os
import argparse
from pathlib import Path
from typing import List, Tuple, Union, Optional

# Imports relativos para la nueva arquitectura
try:
    from ..utils.audio_utils import time_to_ms
    from ..config.settings import OUTPUT_DIR
except ImportError:
    # Fallback para ejecución directa
    def time_to_ms(time_str: str) -> int:
        parts = time_str.split(':')
        if len(parts) == 2:
            minutes, seconds = parts
            minutes = int(minutes)
            seconds = float(seconds)
            return int((minutes * 60 + seconds) * 1000)
        elif len(parts) == 3:
            hours, minutes, seconds = parts
            hours = int(hours)
            minutes = int(minutes)
            seconds = float(seconds)
            return int((hours * 3600 + minutes * 60 + seconds) * 1000)
        else:
            try:
                if '.' in time_str:
                    return int(float(time_str) * 1000)
                else:
                    return int(time_str)
            except ValueError:
                raise ValueError(f"Formato de tiempo no reconocido: {time_str}")
    
    OUTPUT_DIR = "output"

class AudioSplitter:
    """Clase principal para dividir archivos de audio en segmentos"""
    
    def __init__(self):
        self.supported_formats = ['.wav', '.mp3', '.flac', '.m4a', '.ogg']
    
    def split_audio(self, input_file: Union[str, Path], 
                   segments: List[Tuple[int, int, str]], 
                   output_dir: Union[str, Path] = "output") -> bool:
        """
        Divide un archivo de audio en segmentos según los tiempos especificados.
        
        Args:
            input_file: Ruta al archivo de audio
            segments: Lista de tuplas (inicio_ms, fin_ms, nombre)
            output_dir: Directorio donde se guardarán los archivos de salida
        
        Returns:
            bool: True si la operación fue exitosa
        """
        try:
            # Cargar el archivo de audio usando librosa
            print(f"Cargando archivo de audio: {input_file}")
            y, sr = librosa.load(str(input_file), sr=None)  # sr=None conserva la frecuencia de muestreo original
            
            # Crear directorio de salida si no existe
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            print(f"Directorio de salida: {output_path}")
            
            # Procesar cada segmento
            for i, (start_ms, end_ms, name) in enumerate(segments):
                # Convertir milisegundos a muestras
                start_sample = int((start_ms / 1000) * sr)
                end_sample = int((end_ms / 1000) * sr)
                
                # Extraer el segmento
                print(f"Cortando segmento {i+1}: {start_ms}ms - {end_ms}ms")
                segment = y[start_sample:end_sample]
                
                # Definir nombre de salida
                if name:
                    output_file = output_path / f"{name}.wav"
                else:
                    output_file = output_path / f"segment_{i+1}.wav"
                
                # Exportar el segmento usando soundfile
                sf.write(str(output_file), segment, sr)
                print(f"Segmento guardado como: {output_file}")
        
        except Exception as e:
            print(f"Error al procesar el audio: {e}")
            return False
        
        return True
    
    def convert_to_ms(self, time_str: str) -> int:
        """
        Convierte una cadena de tiempo (MM:SS o MM:SS.ms) a milisegundos.
        
        Args:
            time_str: Tiempo en formato "MM:SS" o "MM:SS.ms"
        
        Returns:
            int: Tiempo en milisegundos
        """
        return convert_to_ms(time_str)
    
    def interactive_mode(self):
        """Modo interactivo para solicitar parámetros al usuario"""
        input_file = input("Ingresa la ruta del archivo de audio: ").strip()
        output_dir = input("Ingresa el directorio de salida (predeterminado: 'data/output'): ").strip() or "data/output"
        
        segments = []
        while True:
            print("\nDefinir un nuevo segmento (deja en blanco para terminar):")
            start_time = input("Tiempo de inicio (MM:SS o MM:SS.ms): ").strip()
            if not start_time:
                break
                
            end_time = input("Tiempo de fin (MM:SS o MM:SS.ms): ").strip()
            name = input("Nombre del archivo de salida (opcional): ").strip()
            
            try:
                start_ms = self.convert_to_ms(start_time)
                end_ms = self.convert_to_ms(end_time)
                segments.append((start_ms, end_ms, name))
                print(f"Segmento añadido: {start_time} - {end_time}")
            except ValueError as e:
                print(f"Error: {e}")
        
        if segments:
            if self.split_audio(input_file, segments, output_dir):
                print(f"\n¡Proceso completado! Se generaron {len(segments)} segmentos en '{output_dir}'")
            else:
                print("\nEl proceso falló.")
        else:
            print("\nNo se definieron segmentos. Terminando.")

# Funciones de compatibilidad para mantener la API anterior
def split_audio(input_file, segments, output_dir="output"):
    """Función de compatibilidad - usa AudioSplitter internamente"""
    splitter = AudioSplitter()
    return splitter.split_audio(input_file, segments, output_dir)

def convert_to_ms(time_str):
    """
    Convierte una cadena de tiempo (MM:SS o MM:SS.ms) a milisegundos.
    
    Args:
        time_str (str): Tiempo en formato "MM:SS" o "MM:SS.ms"
    
    Returns:
        int: Tiempo en milisegundos
    """
    # Manejar casos como "1:30" (1min 30seg) o "1:30.500" (1min 30.5seg)
    parts = time_str.split(':')
    
    if len(parts) == 2:  # formato MM:SS o MM:SS.ms
        minutes, seconds = parts
        minutes = int(minutes)
        seconds = float(seconds)
        return int((minutes * 60 + seconds) * 1000)
    elif len(parts) == 3:  # formato HH:MM:SS o HH:MM:SS.ms
        hours, minutes, seconds = parts
        hours = int(hours)
        minutes = int(minutes)
        seconds = float(seconds)
        return int((hours * 3600 + minutes * 60 + seconds) * 1000)
    else:
        # Asumimos que es directamente segundos o milisegundos
        try:
            if '.' in time_str:  # Si tiene punto decimal, asumimos segundos
                return int(float(time_str) * 1000)
            else:  # Si no tiene punto decimal, asumimos milisegundos
                return int(time_str)
        except ValueError:
            raise ValueError(f"Formato de tiempo no reconocido: {time_str}")

def interactive_mode():
    """Función de compatibilidad - usa AudioSplitter internamente"""
    splitter = AudioSplitter()
    splitter.interactive_mode()
