#!/usr/bin/env python3
"""
Script de validación final para Audio Splitter Suite 2.0
Verifica que todo esté funcionando correctamente
"""

import sys
import os
from pathlib import Path
import importlib.util

# Agregar el directorio raíz del proyecto al PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Cambiar al directorio del proyecto
os.chdir(project_root)

def test_imports():
    """Prueba todos los imports críticos"""
    print("🔍 Verificando imports críticos...")
    
    tests = [
        ("audio_splitter", "Paquete principal"),
        ("audio_splitter.core.splitter", "AudioSplitter"),
        ("audio_splitter.core.converter", "AudioConverter"), 
        ("audio_splitter.core.metadata_manager", "MetadataEditor"),
        ("audio_splitter.ui.cli", "CLI"),
        ("audio_splitter.ui.interactive", "Interfaz interactiva"),
        ("audio_splitter.utils.audio_utils", "Utilidades de audio"),
        ("audio_splitter.utils.file_utils", "Utilidades de archivos"),
        ("audio_splitter.config.settings", "Configuraciones")
    ]
    
    failed = []
    
    for module_path, description in tests:
        try:
            __import__(module_path)
            print(f"  ✓ {description}")
        except ImportError as e:
            print(f"  ❌ {description}: {e}")
            failed.append((module_path, str(e)))
    
    return failed

def test_dependencies():
    """Verifica dependencias externas"""
    print("\n📦 Verificando dependencias...")
    
    deps = [
        ("librosa", "Procesamiento de audio"), 
        ("soundfile", "I/O de audio"),
        ("mutagen", "Metadatos de audio"),
        ("rich", "Interfaz de terminal"),
        ("numpy", "Computación numérica"),
        ("pydub", "Manipulación de audio")
    ]
    
    failed = []
    
    for dep, description in deps:
        try:
            __import__(dep)
            print(f"  ✓ {description}")
        except ImportError as e:
            print(f"  ❌ {description}: {e}")
            failed.append((dep, str(e)))
    
    return failed

def test_directory_structure():
    """Verifica estructura de directorios"""
    print("\n📁 Verificando estructura de directorios...")
    
    required_dirs = [
        "audio_splitter",
        "audio_splitter/core",
        "audio_splitter/ui", 
        "audio_splitter/utils",
        "audio_splitter/config",
        "tests",
        "docs",
        "scripts",
        "data",
        "data/output",
        "data/templates"
    ]
    
    missing = []
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"  ✓ {dir_path}")
        else:
            print(f"  ❌ {dir_path} (faltante)")
            missing.append(dir_path)
    
    return missing

def test_files():
    """Verifica archivos importantes"""
    print("\n📄 Verificando archivos importantes...")
    
    required_files = [
        "main.py",
        "setup.py", 
        "requirements.txt",
        "README.md",
        "audio_splitter/__init__.py",
        "audio_splitter/core/__init__.py",
        "audio_splitter/core/splitter.py",
        "audio_splitter/core/converter.py",
        "audio_splitter/core/metadata_manager.py",
        "audio_splitter/ui/cli.py",
        "audio_splitter/ui/interactive.py"
    ]
    
    missing = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ❌ {file_path} (faltante)")
            missing.append(file_path)
    
    return missing

def test_functionality():
    """Prueba funcionalidades básicas"""
    print("\n⚙️ Probando funcionalidades básicas...")
    
    try:
        # Test AudioSplitter
        from audio_splitter.core.splitter import AudioSplitter, convert_to_ms
        splitter = AudioSplitter()
        result = convert_to_ms("1:30")
        assert result == 90000, f"convert_to_ms falló: esperado 90000, obtuvo {result}"
        print("  ✓ AudioSplitter - conversión de tiempo")
        
        # Test AudioConverter
        from audio_splitter.core.converter import AudioConverter
        converter = AudioConverter()
        assert len(converter.supported_input_formats) > 0, "No hay formatos de entrada"
        print("  ✓ AudioConverter - inicialización")
        
        # Test MetadataEditor
        from audio_splitter.core.metadata_manager import MetadataEditor, AudioMetadata
        editor = MetadataEditor()
        metadata = AudioMetadata(title="Test", artist="Test Artist")
        assert metadata.title == "Test", "AudioMetadata falló"
        print("  ✓ MetadataEditor - creación de metadatos")
        
        return []
        
    except Exception as e:
        print(f"  ❌ Error en funcionalidades: {e}")
        return [str(e)]

def run_validation():
    """Ejecuta validación completa"""
    print("🎵 Audio Splitter Suite 2.0 - Validación Final")
    print("=" * 60)
    
    all_errors = []
    
    # Ejecutar todas las pruebas
    import_errors = test_imports()
    dep_errors = test_dependencies()
    dir_errors = test_directory_structure()
    file_errors = test_files()
    func_errors = test_functionality()
    
    all_errors.extend(import_errors)
    all_errors.extend(dep_errors)
    all_errors.extend(dir_errors)
    all_errors.extend(file_errors)
    all_errors.extend(func_errors)
    
    print("\n" + "=" * 60)
    
    if not all_errors:
        print("✅ VALIDACIÓN EXITOSA - Todo funcionando correctamente!")
        print("\n🚀 Sistema listo para usar:")
        print("   • python main.py")
        print("   • python -m audio_splitter.ui.cli --help")
        print("   • python -m pytest tests/")
        return True
    else:
        print("❌ ERRORES ENCONTRADOS:")
        for i, error in enumerate(all_errors, 1):
            if isinstance(error, tuple):
                print(f"   {i}. {error[0]}: {error[1]}")
            else:
                print(f"   {i}. {error}")
        
        print(f"\n📋 Total de errores: {len(all_errors)}")
        print("\n🔧 Recomendaciones:")
        print("   • Ejecuta: pip install -r requirements.txt")
        print("   • Verifica que todos los archivos estén en su lugar")
        print("   • Contacta soporte si persisten los problemas")
        return False

if __name__ == "__main__":
    try:
        success = run_validation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Validación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error durante la validación: {e}")
        sys.exit(1)
