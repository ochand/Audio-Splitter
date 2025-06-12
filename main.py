#!/usr/bin/env python3
"""
Audio Splitter Suite 2.0 - Punto de entrada principal
Sistema completo de procesamiento de audio con arquitectura modular
"""

import sys
import argparse
from pathlib import Path

# Asegurar que el paquete esté en el path
sys.path.insert(0, str(Path(__file__).parent))

from audio_splitter.ui.interactive import interactive_menu
from audio_splitter.ui.cli import main_cli
from rich.console import Console

console = Console()

def main():
    """Función principal que decide entre modo CLI o interactivo"""
    
    # Si hay argumentos de línea de comandos, usar CLI
    if len(sys.argv) > 1:
        # Modo línea de comandos
        return main_cli()
    else:
        # Modo interactivo
        try:
            interactive_menu()
            return True
        except KeyboardInterrupt:
            console.print("\n[yellow]👋 ¡Hasta luego![/yellow]")
            return True
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
