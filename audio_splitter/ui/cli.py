"""
Interfaz de línea de comandos principal del Audio Splitter Suite
"""

import argparse
import sys
from pathlib import Path

# Imports relativos limpios
from ..core.splitter import split_audio, convert_to_ms
from ..core.converter import AudioConverter
from ..core.metadata_manager import MetadataEditor, AudioMetadata
from rich.console import Console

console = Console()

def create_parser():
    """Crea el parser principal de argumentos"""
    parser = argparse.ArgumentParser(
        description='Audio Splitter Suite - Sistema completo de procesamiento de audio',
        prog='audio-splitter'
    )
    
    parser.add_argument('--version', '-v', action='version', version='Audio Splitter Suite 2.0.0')
    
    # Subcomandos
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Comando split
    split_parser = subparsers.add_parser('split', help='Dividir archivos de audio')
    split_parser.add_argument('input_file', help='Archivo de audio de entrada')
    split_parser.add_argument('--output-dir', '-o', default='data/output', help='Directorio de salida')
    split_parser.add_argument('--segments', '-s', nargs='+', 
                             help='Segmentos en formato "inicio-fin:nombre"')
    
    # Comando convert
    convert_parser = subparsers.add_parser('convert', help='Convertir formatos de audio')
    convert_parser.add_argument('input', help='Archivo o directorio de entrada')
    convert_parser.add_argument('--output', '-o', required=True, help='Archivo o directorio de salida')
    convert_parser.add_argument('--format', '-f', required=True, choices=['wav', 'mp3', 'flac'], 
                               help='Formato de salida')
    convert_parser.add_argument('--quality', '-q', default='high', 
                               help='Calidad de conversión')
    convert_parser.add_argument('--batch', action='store_true', 
                               help='Conversión por lotes')
    convert_parser.add_argument('--recursive', '-r', action='store_true',
                               help='Buscar recursivamente')
    
    # Comando metadata
    metadata_parser = subparsers.add_parser('metadata', help='Editar metadatos')
    metadata_parser.add_argument('file_path', help='Archivo de audio')
    metadata_parser.add_argument('--title', help='Título')
    metadata_parser.add_argument('--artist', help='Artista')
    metadata_parser.add_argument('--album', help='Álbum')
    metadata_parser.add_argument('--genre', help='Género')
    metadata_parser.add_argument('--year', help='Año')
    
    return parser

def handle_split_command(args):
    """Maneja el comando split"""
    try:
        if not args.segments:
            console.print("[red]Error: Se requieren segmentos para dividir[/red]")
            return False
        
        # Procesar segmentos
        segments = []
        for seg in args.segments:
            try:
                # Formato: "inicio-fin:nombre"
                time_range, name = seg.split(':', 1) if ':' in seg else (seg, "")
                start_str, end_str = time_range.split('-')
                
                start_ms = convert_to_ms(start_str)
                end_ms = convert_to_ms(end_str)
                segments.append((start_ms, end_ms, name))
            except Exception as e:
                console.print(f"[red]Error procesando segmento '{seg}': {e}[/red]")
                return False
        
        # Ejecutar división
        success = split_audio(args.input_file, segments, args.output_dir)
        if success:
            console.print(f"[green]✓ División completada en '{args.output_dir}'[/green]")
        else:
            console.print("[red]✗ Error en la división[/red]")
        
        return success
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return False

def handle_convert_command(args):
    """Maneja el comando convert"""
    try:
        converter = AudioConverter()
        
        if args.batch:
            # Conversión por lotes
            successful, failed = converter.batch_convert(
                args.input, args.output, args.format, 
                args.quality, True, args.recursive
            )
            console.print(f"[green]Conversión completada: {successful} exitosos, {failed} fallidos[/green]")
            return failed == 0
        else:
            # Conversión individual
            success = converter.convert_file(
                args.input, args.output, args.format, args.quality, True
            )
            if success:
                console.print("[green]✓ Conversión exitosa[/green]")
            else:
                console.print("[red]✗ Error en conversión[/red]")
            return success
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return False

def handle_metadata_command(args):
    """Maneja el comando metadata"""
    try:
        editor = MetadataEditor()
        
        # Leer metadatos existentes
        existing_metadata = editor.read_metadata(args.file_path)
        if existing_metadata is None:
            console.print("[red]Error leyendo metadatos[/red]")
            return False
        
        # Crear nueva estructura con cambios
        new_metadata = AudioMetadata()
        
        # Copiar valores existentes
        for field in ['title', 'artist', 'album', 'genre', 'date', 'track', 'comment']:
            setattr(new_metadata, field, getattr(existing_metadata, field, None))
        
        # Aplicar cambios desde argumentos
        if args.title:
            new_metadata.title = args.title
        if args.artist:
            new_metadata.artist = args.artist
        if args.album:
            new_metadata.album = args.album
        if args.genre:
            new_metadata.genre = args.genre
        if args.year:
            new_metadata.date = args.year
        
        # Guardar cambios
        success = editor.write_metadata(args.file_path, new_metadata)
        if success:
            console.print("[green]✓ Metadatos actualizados[/green]")
        else:
            console.print("[red]✗ Error actualizando metadatos[/red]")
        
        return success
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return False

def main_cli(args=None):
    """Función principal del CLI"""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    if not parsed_args.command:
        parser.print_help()
        return False
    
    # Ejecutar comando correspondiente
    if parsed_args.command == 'split':
        return handle_split_command(parsed_args)
    elif parsed_args.command == 'convert':
        return handle_convert_command(parsed_args)
    elif parsed_args.command == 'metadata':
        return handle_metadata_command(parsed_args)
    else:
        console.print(f"[red]Comando no reconocido: {parsed_args.command}[/red]")
        return False

if __name__ == "__main__":
    success = main_cli()
    sys.exit(0 if success else 1)
