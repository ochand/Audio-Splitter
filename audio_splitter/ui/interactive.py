"""
Interfaz interactiva principal del Audio Splitter Suite
"""

import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def interactive_menu():
    """Menú principal interactivo del sistema Audio Splitter Suite"""
    
    console.print(Panel(
        "[bold blue]🎵 Audio Splitter Suite 2.0[/bold blue]\n" +
        "[dim]Sistema completo de procesamiento de audio[/dim]",
        title="Audio Processing Suite"
    ))
    
    while True:
        console.print("\n[cyan]🎛️ Módulos disponibles:[/cyan]")
        options = [
            "1. 🔄 Audio Converter - Conversión entre formatos (WAV/MP3/FLAC)",
            "2. ✂️  Audio Splitter - División en segmentos con metadatos",
            "3. 🏷️  Metadata Editor - Editor profesional de metadatos",
            "4. 🖼️  Artwork Manager - Gestión de carátulas",
            "5. 📄 Documentación y ayuda",
            "6. 🚪 Salir"
        ]
        
        for option in options:
            console.print(f"  {option}")
        
        choice = Prompt.ask("\nSelecciona un módulo", choices=["1", "2", "3", "4", "5", "6"])
        
        if choice == "1":
            run_audio_converter()
        elif choice == "2":
            run_audio_splitter()
        elif choice == "3":
            run_metadata_editor()
        elif choice == "4":
            run_artwork_manager()
        elif choice == "5":
            show_documentation()
        elif choice == "6":
            console.print("\n[yellow]👋 ¡Gracias por usar Audio Splitter Suite![/yellow]")
            break

def run_audio_converter():
    """Ejecuta el módulo de conversión de audio"""
    try:
        from ..core.converter import interactive_mode
        console.print("\n[blue]🔄 Iniciando Audio Converter...[/blue]")
        interactive_mode()
    except ImportError as e:
        console.print(f"[red]❌ Error importando Audio Converter: {e}[/red]")
    except Exception as e:
        console.print(f"[red]❌ Error ejecutando Audio Converter: {e}[/red]")

def run_audio_splitter():
    """Ejecuta el módulo de división de audio"""
    try:
        from ..core.splitter import interactive_mode
        console.print("\n[blue]✂️ Iniciando Audio Splitter...[/blue]")
        interactive_mode()
    except ImportError as e:
        console.print(f"[red]❌ Error importando Audio Splitter: {e}[/red]")
    except Exception as e:
        console.print(f"[red]❌ Error ejecutando Audio Splitter: {e}[/red]")

def run_metadata_editor():
    """Ejecuta el editor de metadatos"""
    try:
        from ..core.metadata_manager import interactive_mode
        console.print("\n[blue]🏷️ Iniciando Metadata Editor...[/blue]")
        interactive_mode()
    except ImportError as e:
        console.print(f"[red]❌ Error importando Metadata Editor: {e}[/red]")
    except Exception as e:
        console.print(f"[red]❌ Error ejecutando Metadata Editor: {e}[/red]")

def run_artwork_manager():
    """Ejecuta el gestor de carátulas"""
    console.print("\n[yellow]🖼️ Artwork Manager integrado en Metadata Editor[/yellow]")
    console.print("[dim]Usa el Metadata Editor para gestionar carátulas[/dim]")
    run_metadata_editor()

def show_documentation():
    """Muestra documentación y ayuda"""
    console.print("\n[cyan]📄 Documentación Audio Splitter Suite 2.0[/cyan]")
    
    docs = {
        "🔄 Audio Converter": [
            "• Convierte entre formatos WAV, MP3, FLAC",
            "• Preserva metadatos automáticamente", 
            "• Configuración de calidad personalizable",
            "• Conversión por lotes con progreso visual"
        ],
        "✂️ Audio Splitter": [
            "• División precisa con milisegundos",
            "• Soporte múltiples formatos de entrada",
            "• Preservación de metadatos en segmentos",
            "• Modo interactivo y línea de comandos"
        ],
        "🏷️ Metadata Editor": [
            "• Editor profesional ID3v2.4, Vorbis, iTunes",
            "• Plantillas de metadatos guardables",
            "• Edición por lotes",
            "• Gestión completa de carátulas"
        ],
        "🖼️ Artwork Manager": [
            "• Embedding en MP3, FLAC, M4A",
            "• Redimensionado automático",
            "• Extracción de carátulas existentes",
            "• Soporte JPEG, PNG"
        ]
    }
    
    for module, features in docs.items():
        console.print(f"\n[bold]{module}[/bold]")
        for feature in features:
            console.print(f"  {feature}")
    
    console.print(f"\n[cyan]📁 Archivos de documentación:[/cyan]")
    console.print("  • docs/README.md - Guía de uso")
    console.print("  • docs/architecture.md - Documentación técnica")
    console.print("  • docs/product_requirements.md - Especificaciones")
    console.print("  • docs/implementation.md - Detalles de implementación")
    
    console.print(f"\n[cyan]🛠️ Línea de comandos:[/cyan]")
    console.print("  • python -m audio_splitter.ui.cli split <archivo> --segments '1:30-2:45:intro'")
    console.print("  • python -m audio_splitter.ui.cli convert <archivo> -f mp3 -q high")
    console.print("  • python -m audio_splitter.ui.cli metadata <archivo> --title 'Mi Canción'")

if __name__ == "__main__":
    interactive_menu()
