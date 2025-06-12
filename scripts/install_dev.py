#!/usr/bin/env python3
"""
Script de instalación rápida para Audio Splitter Suite 2.0
Instala el paquete en modo desarrollo para resolver imports
"""

import subprocess
import sys
import os
from pathlib import Path

def run_install():
    """Instala el paquete en modo desarrollo"""
    print("🔧 Instalando Audio Splitter Suite 2.0 en modo desarrollo...")
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    try:
        # Instalar en modo desarrollo
        print("📦 Ejecutando: pip install -e .")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Instalación exitosa!")
            print(result.stdout)
            
            # Verificar que funciona
            print("\n🔍 Verificando instalación...")
            try:
                import audio_splitter
                print("✅ audio_splitter importado correctamente")
                print(f"📍 Ubicación: {audio_splitter.__file__}")
                return True
            except ImportError as e:
                print(f"❌ Error importando: {e}")
                return False
        else:
            print("❌ Error durante la instalación:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando instalación: {e}")
        return False

def main():
    """Función principal"""
    print("🎵 Audio Splitter Suite 2.0 - Instalación de Desarrollo")
    print("=" * 60)
    
    success = run_install()
    
    if success:
        print("\n🎉 ¡Instalación completada!")
        print("\n🚀 Ahora puedes usar:")
        print("   • python main.py")
        print("   • python -m audio_splitter.ui.cli --help")
        print("   • python scripts/validate_system.py")
        print("   • python scripts/check_system.py")
        
    else:
        print("\n❌ Instalación falló")
        print("\n🔧 Prueba manualmente:")
        print("   • pip install -e .")
        print("   • pip install -r requirements.txt")
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Instalación cancelada")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
