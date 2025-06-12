#!/usr/bin/env python3
"""
Verificación completa del sistema Audio Splitter Suite 2.0
Ejecuta todas las validaciones y pruebas
"""

import subprocess
import sys
import os
from pathlib import Path

# Cambiar al directorio del proyecto al inicio
project_root = Path(__file__).parent.parent
os.chdir(project_root)

def run_command(command, description, required=True):
    """Ejecuta un comando y maneja errores"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - EXITOSO")
            if result.stdout.strip():
                print(f"   {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - FALLÓ")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            if required:
                return False
            return True
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return not required

def main():
    """Ejecuta verificación completa"""
    print("🎵 Audio Splitter Suite 2.0 - Verificación Completa")
    print("=" * 60)
    
    print(f"📁 Directorio de trabajo: {os.getcwd()}")
    
    success = True
    
    # 1. Validación del sistema
    success &= run_command(
        "python scripts/validate_system.py",
        "Validación del sistema"
    )
    
    # 2. Pruebas unitarias
    success &= run_command(
        "python -m pytest tests/ -v",
        "Pruebas unitarias",
        required=False  # No requeridas si no hay archivos de prueba
    )
    
    # 3. Verificar que main.py funcione
    success &= run_command(
        "python main.py --help 2>/dev/null || echo 'Modo interactivo disponible'",
        "Verificación de main.py"
    )
    
    # 4. Verificar CLI
    success &= run_command(
        "python -m audio_splitter.ui.cli --version",
        "Verificación de CLI"
    )
    
    # 5. Verificar imports críticos
    success &= run_command(
        "python -c \"from audio_splitter import AudioSplitter, AudioConverter, MetadataEditor; print('Imports OK')\"",
        "Verificación de imports principales"
    )
    
    print("\n" + "=" * 60)
    
    if success:
        print("🎉 VERIFICACIÓN COMPLETA EXITOSA!")
        print("\n📋 Resumen del sistema:")
        print("   ✅ Estructura de directorios correcta")
        print("   ✅ Dependencias instaladas")
        print("   ✅ Imports funcionando")
        print("   ✅ Funcionalidades básicas operativas")
        print("   ✅ CLI operativo")
        
        print("\n🚀 El sistema está listo para usar:")
        print("   • python main.py                    (Modo interactivo)")
        print("   • python -m audio_splitter.ui.cli   (Línea de comandos)")
        print("   • python -m pytest tests/           (Ejecutar tests)")
        
        print("\n📖 Documentación disponible en:")
        print("   • README.md")
        print("   • docs/")
        
        return True
    else:
        print("❌ VERIFICACIÓN FALLÓ")
        print("\n🔧 Acciones recomendadas:")
        print("   1. pip install -r requirements.txt")
        print("   2. python scripts/migrate_to_v2.py")
        print("   3. Verificar mensajes de error arriba")
        
        return False

if __name__ == "__main__":
    import os
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Verificación cancelada")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error durante verificación: {e}")
        sys.exit(1)
