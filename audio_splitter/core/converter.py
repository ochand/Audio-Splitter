#!/usr/bin/env python3
"""
Audio Format Converter - Conversión entre formatos de audio WAV, MP3, FLAC
Soporta conversión con preservación de metadatos y configuración de calidad
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import argparse

import librosa
import soundfile as sf
from pydub import AudioSegment
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wave import WAVE
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()

class AudioFormatError(Exception):
    """Excepción personalizada para errores de formato de audio"""
    pass

class AudioConverter:
    """Conversor de formatos de audio con soporte para WAV, MP3, FLAC"""
    
    SUPPORTED_FORMATS = {
        '.wav': 'WAV',
        '.mp3': 'MP3', 
        '.flac': 'FLAC'
    }
    
    # Configuraciones de calidad por formato
    QUALITY_PRESETS = {
        'mp3': {
            'low': {'bitrate': '128k'},
            'medium': {'bitrate': '192k'},
            'high': {'bitrate': '320k'},
            'vbr_medium': {'codec': 'libmp3lame', 'audio_bitrate': None, 'parameters': ['-q:a', '2']},
            'vbr_high': {'codec': 'libmp3lame', 'audio_bitrate': None, 'parameters': ['-q:a', '0']}
        },
        'flac': {
            'low': {'compression_level': 0},
            'medium': {'compression_level': 5},
            'high': {'compression_level': 8}
        }
    }
    
    def __init__(self):
        self.supported_input_formats = ['.wav', '.mp3', '.flac', '.m4a', '.ogg']
        self.supported_output_formats = ['.wav', '.mp3', '.flac']
    
    def detect_format(self, file_path: Union[str, Path]) -> str:
        """Detecta el formato de audio del archivo"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        extension = path.suffix.lower()
        if extension not in self.supported_input_formats:
            raise AudioFormatError(f"Formato no soportado: {extension}")
        
        return extension
    
    def get_audio_info(self, file_path: Union[str, Path]) -> Dict:
        """Obtiene información detallada del archivo de audio"""
        try:
            # Cargar con librosa para información técnica
            y, sr = librosa.load(str(file_path), sr=None)
            duration = len(y) / sr
            
            # Cargar con mutagen para metadatos
            audio_file = File(str(file_path))
            
            info = {
                'path': str(file_path),
                'format': self.detect_format(file_path),
                'duration': duration,
                'sample_rate': sr,
                'channels': 1 if len(y.shape) == 1 else y.shape[0],
                'file_size': Path(file_path).stat().st_size,
                'metadata': {}
            }
            
            if audio_file is not None:
                # Extraer metadatos comunes
                info['metadata'] = {
                    'title': self._get_tag(audio_file, ['TIT2', 'TITLE', 'Title']),
                    'artist': self._get_tag(audio_file, ['TPE1', 'ARTIST', 'Artist']),
                    'album': self._get_tag(audio_file, ['TALB', 'ALBUM', 'Album']),
                    'date': self._get_tag(audio_file, ['TDRC', 'DATE', 'Date']),
                    'genre': self._get_tag(audio_file, ['TCON', 'GENRE', 'Genre']),
                    'track': self._get_tag(audio_file, ['TRCK', 'TRACKNUMBER', 'TrackNumber'])
                }
            
            return info
            
        except Exception as e:
            raise AudioFormatError(f"Error al leer archivo {file_path}: {e}")
    
    def _get_tag(self, audio_file, tag_names: List[str]) -> Optional[str]:
        """Extrae un tag de metadatos usando múltiples nombres posibles"""
        for tag_name in tag_names:
            if tag_name in audio_file:
                value = audio_file[tag_name]
                if isinstance(value, list) and value:
                    return str(value[0])
                elif value:
                    return str(value)
        return None
    
    def convert_file(self, 
                    input_path: Union[str, Path],
                    output_path: Union[str, Path],
                    target_format: str,
                    quality: str = 'high',
                    preserve_metadata: bool = True) -> bool:
        """
        Convierte un archivo de audio a otro formato
        
        Args:
            input_path: Ruta del archivo de entrada
            output_path: Ruta del archivo de salida
            target_format: Formato objetivo ('wav', 'mp3', 'flac')
            quality: Nivel de calidad ('low', 'medium', 'high')
            preserve_metadata: Si preservar metadatos originales
        """
        try:
            input_path = Path(input_path)
            output_path = Path(output_path)
            
            # Validaciones
            if not input_path.exists():
                raise FileNotFoundError(f"Archivo de entrada no encontrado: {input_path}")
            
            if target_format not in ['wav', 'mp3', 'flac']:
                raise AudioFormatError(f"Formato objetivo no soportado: {target_format}")
            
            # Crear directorio de salida si no existe
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Obtener información del archivo original
            original_info = self.get_audio_info(input_path)
            
            console.print(f"[blue]Convirtiendo:[/blue] {input_path.name} -> {target_format.upper()}")
            
            # Realizar conversión según el formato objetivo
            if target_format == 'wav':
                success = self._convert_to_wav(input_path, output_path)
            elif target_format == 'mp3':
                success = self._convert_to_mp3(input_path, output_path, quality)
            elif target_format == 'flac':
                success = self._convert_to_flac(input_path, output_path, quality)
            
            # Preservar metadatos si se solicita
            if success and preserve_metadata and original_info['metadata']:
                self._copy_metadata(original_info['metadata'], output_path, target_format)
            
            if success:
                console.print(f"[green]✓ Conversión exitosa:[/green] {output_path}")
                return True
            else:
                console.print("[red]✗ Error en conversión[/red]")
                return False
                
        except Exception as e:
            console.print(f"[red]Error al convertir {input_path}: {e}[/red]")
            return False
    
    def _convert_to_wav(self, input_path: Path, output_path: Path) -> bool:
        """Convierte archivo a formato WAV"""
        try:
            # Cargar audio con librosa (soporta múltiples formatos)
            y, sr = librosa.load(str(input_path), sr=None)
            
            # Guardar como WAV
            sf.write(str(output_path), y, sr, format='WAV')
            return True
            
        except Exception as e:
            console.print(f"[red]Error convirtiendo a WAV: {e}[/red]")
            return False
    
    def _convert_to_mp3(self, input_path: Path, output_path: Path, quality: str) -> bool:
        """Convierte archivo a formato MP3"""
        try:
            # Usar pydub para conversión a MP3
            audio = AudioSegment.from_file(str(input_path))
            
            # Configurar parámetros de calidad
            quality_settings = self.QUALITY_PRESETS['mp3'].get(quality, self.QUALITY_PRESETS['mp3']['high'])
            
            # Exportar a MP3
            if 'bitrate' in quality_settings:
                audio.export(str(output_path), format="mp3", bitrate=quality_settings['bitrate'])
            else:
                # Para VBR, usar parámetros personalizados
                audio.export(str(output_path), format="mp3", parameters=quality_settings.get('parameters', []))
            
            return True
            
        except Exception as e:
            console.print(f"[red]Error convirtiendo a MP3: {e}[/red]")
            return False
    
    def _convert_to_flac(self, input_path: Path, output_path: Path, quality: str) -> bool:
        """Convierte archivo a formato FLAC"""
        try:
            # Cargar con librosa
            y, sr = librosa.load(str(input_path), sr=None)
            
            # Configurar nivel de compresión FLAC
            quality_settings = self.QUALITY_PRESETS['flac'].get(quality, self.QUALITY_PRESETS['flac']['high'])
            compression_level = quality_settings['compression_level']
            
            # Guardar como FLAC
            sf.write(str(output_path), y, sr, format='FLAC', subtype='PCM_16')
            
            return True
            
        except Exception as e:
            console.print(f"[red]Error convirtiendo a FLAC: {e}[/red]")
            return False
    
    def _copy_metadata(self, metadata: Dict, output_path: Path, target_format: str):
        """Copia metadatos al archivo convertido"""
        try:
            audio_file = File(str(output_path))
            if audio_file is None:
                return
            
            if target_format == 'mp3':
                self._copy_id3_metadata(audio_file, metadata)
            elif target_format == 'flac':
                self._copy_vorbis_metadata(audio_file, metadata)
            elif target_format == 'wav':
                # WAV tiene soporte limitado de metadatos
                console.print("[yellow]Info: WAV tiene soporte limitado de metadatos[/yellow]")
                
        except Exception as e:
            console.print(f"[yellow]Advertencia: No se pudieron copiar metadatos: {e}[/yellow]")
    
    def _copy_id3_metadata(self, audio_file, metadata: Dict):
        """Copia metadatos usando tags ID3 para MP3"""
        from mutagen.id3 import TIT2, TPE1, TALB, TDRC, TCON, TRCK
        
        # Asegurar que existan tags ID3
        if audio_file.tags is None:
            audio_file.add_tags()
        
        tags = audio_file.tags
        
        # Mapear y agregar tags ID3
        if metadata.get('title'):
            tags.add(TIT2(encoding=3, text=metadata['title']))
        if metadata.get('artist'):
            tags.add(TPE1(encoding=3, text=metadata['artist']))
        if metadata.get('album'):
            tags.add(TALB(encoding=3, text=metadata['album']))
        if metadata.get('date'):
            tags.add(TDRC(encoding=3, text=metadata['date']))
        if metadata.get('genre'):
            tags.add(TCON(encoding=3, text=metadata['genre']))
        if metadata.get('track'):
            tags.add(TRCK(encoding=3, text=metadata['track']))
        
        audio_file.save()
        console.print("[green]✓ Metadatos copiados exitosamente[/green]")
    
    def _copy_vorbis_metadata(self, audio_file, metadata: Dict):
        """Copia metadatos usando Vorbis Comments para FLAC"""
        # Mapeo directo para FLAC
        tag_mapping = {
            'title': 'TITLE',
            'artist': 'ARTIST',
            'album': 'ALBUM', 
            'date': 'DATE',
            'genre': 'GENRE',
            'track': 'TRACKNUMBER'
        }
        
        for field, value in metadata.items():
            if value and field in tag_mapping:
                audio_file[tag_mapping[field]] = str(value)
        
        audio_file.save()
        console.print("[green]✓ Metadatos copiados exitosamente[/green]")
    
    def batch_convert(self, 
                     input_dir: Union[str, Path],
                     output_dir: Union[str, Path],
                     target_format: str,
                     quality: str = 'high',
                     preserve_metadata: bool = True,
                     recursive: bool = False) -> Tuple[int, int]:
        """
        Conversión por lotes de múltiples archivos
        
        Returns:
            Tuple[int, int]: (archivos_exitosos, archivos_con_error)
        """
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        
        if not input_dir.exists():
            raise FileNotFoundError(f"Directorio de entrada no encontrado: {input_dir}")
        
        # Buscar archivos de audio
        pattern = "**/*" if recursive else "*"
        audio_files = []
        
        for ext in self.supported_input_formats:
            audio_files.extend(input_dir.glob(f"{pattern}{ext}"))
        
        if not audio_files:
            console.print(f"[yellow]No se encontraron archivos de audio en {input_dir}[/yellow]")
            return 0, 0
        
        # Crear directorio de salida
        output_dir.mkdir(parents=True, exist_ok=True)
        
        successful = 0
        failed = 0
        
        # Progreso con rich
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
            console=console
        ) as progress:
            
            task = progress.add_task(f"Convirtiendo a {target_format.upper()}", total=len(audio_files))
            
            for audio_file in audio_files:
                # Generar nombre de archivo de salida
                output_file = output_dir / f"{audio_file.stem}.{target_format}"
                
                # Evitar sobrescribir si el archivo ya existe
                counter = 1
                while output_file.exists():
                    output_file = output_dir / f"{audio_file.stem}_{counter}.{target_format}"
                    counter += 1
                
                # Convertir archivo
                if self.convert_file(audio_file, output_file, target_format, quality, preserve_metadata):
                    successful += 1
                else:
                    failed += 1
                
                progress.advance(task)
        
        # Resumen
        console.print(f"\n[green]Conversión completada:[/green]")
        console.print(f"  ✓ Exitosos: {successful}")
        console.print(f"  ✗ Fallidos: {failed}")
        
        return successful, failed

def interactive_mode():
    """Modo interactivo para conversión de archivos"""
    converter = AudioConverter()
    
    console.print(Panel(
        "[bold blue]Audio Format Converter[/bold blue]\n[dim]Conversión entre WAV, MP3 y FLAC[/dim]", 
        title="🔄 Conversor de Audio"
    ))
    
    while True:
        console.print("\n[cyan]Opciones disponibles:[/cyan]")
        options = [
            "1. Convertir archivo individual",
            "2. Conversión por lotes",
            "3. Información de archivo",
            "4. Salir"
        ]
        
        for option in options:
            console.print(f"  {option}")
        
        choice = Prompt.ask("\nSelecciona una opción", choices=["1", "2", "3", "4"])
        
        if choice == '1':
            _convert_single_file_interactive(converter)
        elif choice == '2':
            _batch_convert_interactive(converter)
        elif choice == '3':
            _show_file_info_interactive(converter)
        elif choice == '4':
            console.print("[yellow]¡Hasta luego![/yellow]")
            break

def _convert_single_file_interactive(converter: AudioConverter):
    """Modo interactivo para conversión de archivo individual"""
    
    input_file = Prompt.ask("\nRuta del archivo de entrada")
    if not input_file:
        console.print("[red]Ruta requerida[/red]")
        return
    
    # Mostrar formatos disponibles
    console.print("\n[cyan]Formatos de salida disponibles:[/cyan] WAV, MP3, FLAC")
    target_format = Prompt.ask("Formato de salida", choices=["wav", "mp3", "flac"])
    
    output_file = Prompt.ask("Archivo de salida (Enter para auto)", default="")
    if not output_file:
        input_path = Path(input_file)
        output_file = f"{input_path.stem}_converted.{target_format}"
    
    # Configurar calidad
    quality = 'high'
    if target_format in ['mp3', 'flac']:
        console.print(f"\n[cyan]Niveles de calidad para {target_format.upper()}:[/cyan]")
        if target_format == 'mp3':
            console.print("low, medium, high, vbr_medium, vbr_high")
            quality = Prompt.ask("Calidad", choices=["low", "medium", "high", "vbr_medium", "vbr_high"], default="high")
        else:
            console.print("low, medium, high")
            quality = Prompt.ask("Calidad", choices=["low", "medium", "high"], default="high")
    
    preserve_metadata = Confirm.ask("¿Preservar metadatos?", default=True)
    
    # Realizar conversión
    converter.convert_file(input_file, output_file, target_format, quality, preserve_metadata)

def _batch_convert_interactive(converter: AudioConverter):
    """Modo interactivo para conversión por lotes"""
    
    input_dir = Prompt.ask("\nDirectorio de entrada")
    if not input_dir:
        console.print("[red]Directorio requerido[/red]")
        return
    
    output_dir = Prompt.ask("Directorio de salida")
    if not output_dir:
        console.print("[red]Directorio de salida requerido[/red]")
        return
    
    console.print("\n[cyan]Formatos disponibles:[/cyan] WAV, MP3, FLAC")
    target_format = Prompt.ask("Formato objetivo", choices=["wav", "mp3", "flac"])
    
    recursive = Confirm.ask("¿Buscar en subdirectorios?", default=False)
    
    # Configurar calidad
    quality = 'high'
    if target_format in ['mp3', 'flac']:
        if target_format == 'mp3':
            quality = Prompt.ask(f"Calidad para {target_format.upper()}", 
                               choices=["low", "medium", "high", "vbr_medium", "vbr_high"], 
                               default="high")
        else:
            quality = Prompt.ask(f"Calidad para {target_format.upper()}", 
                               choices=["low", "medium", "high"], 
                               default="high")
    
    preserve_metadata = Confirm.ask("¿Preservar metadatos?", default=True)
    
    # Realizar conversión por lotes
    try:
        converter.batch_convert(input_dir, output_dir, target_format, quality, preserve_metadata, recursive)
    except Exception as e:
        console.print(f"[red]Error en conversión por lotes: {e}[/red]")

def _show_file_info_interactive(converter: AudioConverter):
    """Mostrar información detallada de un archivo de audio"""
    
    file_path = Prompt.ask("\nRuta del archivo")
    if not file_path:
        console.print("[red]Ruta requerida[/red]")
        return
    
    try:
        info = converter.get_audio_info(file_path)
        
        # Crear tabla con información
        table = Table(title=f"Información de: {Path(file_path).name}")
        table.add_column("Campo", style="cyan")
        table.add_column("Valor", style="white")
        
        table.add_row("Formato", info['format'])
        table.add_row("Duración", f"{info['duration']:.2f} segundos")
        table.add_row("Frecuencia", f"{info['sample_rate']} Hz")
        table.add_row("Canales", str(info['channels']))
        table.add_row("Tamaño", f"{info['file_size'] / 1024 / 1024:.2f} MB")
        
        console.print(table)
        
        # Mostrar metadatos si existen
        if info['metadata']:
            console.print("\n[cyan]Metadatos:[/cyan]")
            for key, value in info['metadata'].items():
                if value:
                    console.print(f"  {key.title()}: {value}")
        
    except Exception as e:
        console.print(f"[red]Error obteniendo información: {e}[/red]")

if __name__ == "__main__":
    interactive_mode()
