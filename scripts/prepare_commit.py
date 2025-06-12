#!/usr/bin/env python3
"""
Preparación final para commit - Audio Splitter Suite 2.0
Consolida archivos, limpia proyecto y prepara para commit
"""

import os
import shutil
import sys
from pathlib import Path

def consolidate_scripts():
    """Consolida y organiza scripts eliminando duplicados"""
    print("📁 Consolidando scripts...")
    
    project_root = Path(__file__).parent.parent
    scripts_dir = project_root / "scripts"
    
    # Scripts a mantener (finales)
    keep_scripts = {
        "install_dev.py": "Instalación en modo desarrollo",
        "validate_system.py": "Validación completa del sistema", 
        "check_system.py": "Verificación automática",
        "clean_project.py": "Limpieza del proyecto",
        "migrate_to_v2.py": "Migración a v2.0",
        "install.sh": "Instalación básica",
        "install_advanced.sh": "Instalación avanzada",
        "example_usage.sh": "Ejemplos de uso"
    }
    
    # Scripts a eliminar (duplicados/legacy)
    remove_scripts = [
        "cleanup.py",  # Duplicado de clean_project.py
        "demo.py",     # Movido a scripts de ejemplo
        "legacy_insertar_bloque.py",  # Legacy
        "legacy_sustituir_bloque.py"  # Legacy
    ]
    
    removed_count = 0
    
    for script in remove_scripts:
        script_path = scripts_dir / script
        if script_path.exists():
            script_path.unlink()
            print(f"  ✓ Eliminado: {script}")
            removed_count += 1
    
    print(f"  📊 {removed_count} scripts duplicados/legacy eliminados")
    
    # Mostrar scripts finales
    print("\n📋 Scripts finales:")
    for script, description in keep_scripts.items():
        if (scripts_dir / script).exists():
            print(f"  ✓ {script} - {description}")
        else:
            print(f"  ⚠️ {script} - {description} [FALTANTE]")
    
    return removed_count

def clean_empty_data_dirs():
    """Limpia directorios de datos vacíos innecesarios"""
    print("\n📂 Verificando directorios de datos...")
    
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    
    if not data_dir.exists():
        print("  ℹ️ Directorio data/ no existe")
        return 0
    
    # Verificar subdirectorios
    subdirs = ["sources", "output", "templates", "metadata"]
    cleaned = 0
    
    for subdir_name in subdirs:
        subdir = data_dir / subdir_name
        if subdir.exists():
            # Eliminar .DS_Store si existe
            ds_store = subdir / ".DS_Store"
            if ds_store.exists():
                ds_store.unlink()
                print(f"  ✓ Eliminado: data/{subdir_name}/.DS_Store")
                cleaned += 1
            
            # Verificar si está vacío (excepto .gitkeep)
            contents = list(subdir.iterdir())
            gitkeep_only = len(contents) == 1 and contents[0].name == ".gitkeep"
            empty = len(contents) == 0
            
            if empty:
                # Crear .gitkeep para mantener el directorio en git
                gitkeep_file = subdir / ".gitkeep"
                gitkeep_file.touch()
                print(f"  ✓ Creado: data/{subdir_name}/.gitkeep")
                cleaned += 1
            elif gitkeep_only:
                print(f"  ✓ data/{subdir_name}/ ya tiene .gitkeep")
            else:
                print(f"  ℹ️ data/{subdir_name}/ contiene archivos")
    
    return cleaned

def verify_essential_files():
    """Verifica que todos los archivos esenciales estén presentes"""
    print("\n🔍 Verificando archivos esenciales...")
    
    project_root = Path(__file__).parent.parent
    
    essential_files = {
        "main.py": "Punto de entrada principal",
        "setup.py": "Configuración del paquete",
        "requirements.txt": "Dependencias",
        "README.md": "Documentación principal",
        ".gitignore": "Archivos ignorados por git",
        "pytest.ini": "Configuración de tests",
        "MANIFEST.in": "Archivos para distribución"
    }
    
    missing_files = []
    
    for file_name, description in essential_files.items():
        file_path = project_root / file_name
        if file_path.exists():
            print(f"  ✓ {file_name} - {description}")
        else:
            print(f"  ❌ {file_name} - {description} [FALTANTE]")
            missing_files.append(file_name)
    
    return missing_files

def run_final_cleanup():
    """Ejecuta limpieza final usando el script de limpieza"""
    print("\n🧹 Ejecutando limpieza final...")
    
    project_root = Path(__file__).parent.parent
    cleanup_script = project_root / "scripts" / "clean_project.py"
    
    if cleanup_script.exists():
        # Importar y ejecutar la función de limpieza
        import subprocess
        result = subprocess.run([sys.executable, str(cleanup_script)], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  ✅ Limpieza ejecutada exitosamente")
            return True
        else:
            print(f"  ❌ Error en limpieza: {result.stderr}")
            return False
    else:
        print("  ⚠️ Script de limpieza no encontrado")
        return False

def create_commit_message():
    """Crea mensaje de commit sugerido"""
    commit_message = """feat: Audio Splitter Suite 2.0 - Arquitectura modular completa

🎵 Nuevas características:
- ✨ Arquitectura modular profesional reorganizada
- 🔄 Audio Converter con preservación de metadatos
- ✂️ Audio Splitter mejorado con soporte multi-formato
- 🏷️ Metadata Editor profesional (ID3v2.4, Vorbis, iTunes)
- 🎛️ CLI completo con subcomandos
- 🖥️ Interfaz interactiva mejorada

🏗️ Mejoras técnicas:
- 📦 Estructura de paquete Python estándar
- 🧪 Sistema de testing con pytest
- 📚 Documentación completa
- ⚙️ Configuración centralizada
- 🔧 Scripts de utilidad y validación

🔧 Formatos soportados:
- 📥 Entrada: WAV, MP3, FLAC, M4A, OGG
- 📤 Salida: WAV, MP3, FLAC
- 🏷️ Metadatos: ID3v2.4, Vorbis Comments, iTunes tags

💻 Interfaces disponibles:
- 🖥️ Modo interactivo: python main.py
- ⌨️ CLI: python -m audio_splitter.ui.cli
- 📦 Paquete instalable: pip install -e .

🎯 Casos de uso:
- 🎤 División de sesiones de grabación
- 🎧 Conversión para distribución
- 📁 Organización de bibliotecas musicales
- 🎙️ Procesamiento de podcasts"""
    
    return commit_message

def main():
    """Preparación final para commit"""
    print("🎵 Audio Splitter Suite 2.0 - Preparación Final para Commit")
    print("=" * 70)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print(f"📁 Directorio: {project_root}")
    
    total_changes = 0
    issues = []
    
    # 1. Consolidar scripts
    total_changes += consolidate_scripts()
    
    # 2. Limpiar directorios de datos
    total_changes += clean_empty_data_dirs()
    
    # 3. Verificar archivos esenciales
    missing_files = verify_essential_files()
    if missing_files:
        issues.extend(missing_files)
    
    # 4. Ejecutar limpieza final
    cleanup_success = run_final_cleanup()
    if not cleanup_success:
        issues.append("Limpieza final falló")
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📋 PREPARACIÓN PARA COMMIT COMPLETADA")
    print("=" * 70)
    
    if issues:
        print("⚠️ PROBLEMAS ENCONTRADOS:")
        for issue in issues:
            print(f"   • {issue}")
        print("\n🔧 Resuelve estos problemas antes del commit")
        return False
    else:
        print("✅ PROYECTO LISTO PARA COMMIT")
        print(f"\n📊 Cambios realizados: {total_changes}")
        
        # Mostrar mensaje de commit sugerido
        print("\n💬 MENSAJE DE COMMIT SUGERIDO:")
        print("-" * 50)
        print(create_commit_message())
        print("-" * 50)
        
        print("\n🚀 COMANDOS PARA COMMIT:")
        print("   git add .")
        print("   git commit")
        print("   git push")
        
        return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Preparación cancelada")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error durante preparación: {e}")
        sys.exit(1)
