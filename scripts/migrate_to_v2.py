#!/usr/bin/env python3
"""
Script de migración y configuración para Audio Splitter Suite 2.0
Reorganiza la estructura del proyecto y configura el entorno
"""

import os
import sys
from pathlib import Path
import shutil

def migrate_project():
    """Migra el proyecto a la nueva estructura 2.0"""
    
    print("🔄 Migrando Audio Splitter Suite a la versión 2.0...")
    print()
    
    # Verificar que estamos en el directorio correcto
    if not Path("audio_splitter").exists():
        print("❌ Error: Ejecuta este script desde el directorio raíz del proyecto")
        return False
    
    # 1. Limpiar archivos temporales
    print("🧹 Limpiando archivos temporales...")
    cleanup_temp_files()
    
    # 2. Verificar estructura de directorios
    print("📁 Verificando estructura de directorios...")
    ensure_directory_structure()
    
    # 3. Actualizar imports si es necesario
    print("🔧 Actualizando configuración...")
    update_configuration()
    
    # 4. Crear archivos de configuración faltantes
    print("⚙️ Creando archivos de configuración...")
    create_config_files()
    
    # 5. Verificar dependencias
    print("📦 Verificando dependencias...")
    check_dependencies()
    
    print()
    print("✅ Migración completada exitosamente!")
    print()
    print("🚀 Para usar el sistema:")
    print("   • Modo interactivo: python main.py")
    print("   • Línea de comandos: python -m audio_splitter.ui.cli --help")
    print("   • Tests: python -m pytest tests/")
    
    return True

def cleanup_temp_files():
    """Limpia archivos temporales y cache"""
    patterns_to_remove = [
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '*.tmp',
        '*.temp',
        '.DS_Store'
    ]
    
    removed_count = 0
    
    # Limpiar directorios __pycache__
    for pycache_dir in Path('.').rglob('__pycache__'):
        if pycache_dir.is_dir():
            shutil.rmtree(pycache_dir)
            print(f"  ✓ Eliminado: {pycache_dir}")
            removed_count += 1
    
    # Limpiar archivos .pyc
    for pyc_file in Path('.').rglob('*.pyc'):
        pyc_file.unlink()
        removed_count += 1
    
    print(f"  📊 {removed_count} elementos temporales eliminados")

def ensure_directory_structure():
    """Asegura que la estructura de directorios esté correcta"""
    required_dirs = [
        "audio_splitter/core",
        "audio_splitter/ui", 
        "audio_splitter/utils",
        "audio_splitter/config",
        "tests",
        "docs",
        "scripts",
        "data/templates",
        "data/output",
        "data/sources",
        "data/metadata"
    ]
    
    for dir_path in required_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Directorio: {dir_path}")

def update_configuration():
    """Actualiza archivos de configuración"""
    
    # Verificar que el archivo settings.py existe
    settings_file = Path("audio_splitter/config/settings.py")
    if settings_file.exists():
        print("  ✓ Configuración principal encontrada")
    else:
        print("  ⚠️ Archivo de configuración principal no encontrado")
    
    # Verificar __init__.py files
    init_files = [
        "audio_splitter/__init__.py",
        "audio_splitter/core/__init__.py",
        "audio_splitter/ui/__init__.py",
        "audio_splitter/utils/__init__.py",
        "audio_splitter/config/__init__.py",
        "tests/__init__.py"
    ]
    
    for init_file in init_files:
        if Path(init_file).exists():
            print(f"  ✓ {init_file}")
        else:
            print(f"  ⚠️ Falta: {init_file}")

def create_config_files():
    """Crea archivos de configuración faltantes"""
    
    # Crear .env template si no existe
    env_template = Path(".env.template")
    if not env_template.exists():
        env_content = """# Audio Splitter Suite - Variables de entorno
# Copiar a .env y personalizar

# Directorios
AUDIO_SPLITTER_OUTPUT_DIR=data/output
AUDIO_SPLITTER_SOURCES_DIR=data/sources
AUDIO_SPLITTER_TEMPLATES_DIR=data/templates

# Configuración de calidad por defecto
AUDIO_SPLITTER_DEFAULT_QUALITY=high
AUDIO_SPLITTER_DEFAULT_FORMAT=mp3

# Configuración de metadatos
AUDIO_SPLITTER_DEFAULT_ENCODING=utf-8
AUDIO_SPLITTER_PRESERVE_METADATA=true
"""
        env_template.write_text(env_content)
        print("  ✓ Creado: .env.template")
    
    # Crear MANIFEST.in para distribución
    manifest_file = Path("MANIFEST.in")
    if not manifest_file.exists():
        manifest_content = """include README.md
include LICENSE
include requirements.txt
recursive-include audio_splitter *.py
recursive-include docs *.md
recursive-include tests *.py
recursive-include scripts *.py *.sh
global-exclude __pycache__
global-exclude *.py[co]
"""
        manifest_file.write_text(manifest_content)
        print("  ✓ Creado: MANIFEST.in")

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    required_packages = [
        'librosa',
        'soundfile', 
        'pydub',
        'mutagen',
        'rich',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package} (no instalado)")
    
    if missing_packages:
        print(f"\n⚠️  Paquetes faltantes: {', '.join(missing_packages)}")
        print("   Ejecuta: pip install -r requirements.txt")
    else:
        print("\n✅ Todas las dependencias están instaladas")

if __name__ == "__main__":
    try:
        success = migrate_project()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Migración cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error durante la migración: {e}")
        sys.exit(1)
