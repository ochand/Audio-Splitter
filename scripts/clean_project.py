#!/usr/bin/env python3
"""
Script de limpieza pre-commit para Audio Splitter Suite 2.0
Limpia archivos temporales, cache y otros elementos no deseados antes del commit
"""

import os
import shutil
import sys
from pathlib import Path
import fnmatch

def clean_pycache_directories():
    """Elimina todos los directorios __pycache__"""
    print("🧹 Limpiando directorios __pycache__...")
    
    project_root = Path(__file__).parent.parent
    removed_count = 0
    
    # Solo limpiar __pycache__ del código fuente (no del venv)
    source_dirs = [
        "audio_splitter",
        "tests",
        "scripts"
    ]
    
    for source_dir in source_dirs:
        source_path = project_root / source_dir
        if source_path.exists():
            for pycache_dir in source_path.rglob('__pycache__'):
                if pycache_dir.is_dir():
                    shutil.rmtree(pycache_dir)
                    print(f"  ✓ Eliminado: {pycache_dir.relative_to(project_root)}")
                    removed_count += 1
    
    print(f"  📊 {removed_count} directorios __pycache__ eliminados")
    return removed_count

def clean_pyc_files():
    """Elimina archivos .pyc individuales"""
    print("\n🗑️ Limpiando archivos .pyc...")
    
    project_root = Path(__file__).parent.parent
    removed_count = 0
    
    # Solo limpiar del código fuente
    source_dirs = ["audio_splitter", "tests", "scripts"]
    
    for source_dir in source_dirs:
        source_path = project_root / source_dir
        if source_path.exists():
            for pyc_file in source_path.rglob('*.pyc'):
                pyc_file.unlink()
                print(f"  ✓ Eliminado: {pyc_file.relative_to(project_root)}")
                removed_count += 1
    
    print(f"  📊 {removed_count} archivos .pyc eliminados")
    return removed_count

def clean_ds_store():
    """Elimina archivos .DS_Store de macOS"""
    print("\n🍎 Limpiando archivos .DS_Store...")
    
    project_root = Path(__file__).parent.parent
    removed_count = 0
    
    for ds_file in project_root.rglob('.DS_Store'):
        ds_file.unlink()
        print(f"  ✓ Eliminado: {ds_file.relative_to(project_root)}")
        removed_count += 1
    
    print(f"  📊 {removed_count} archivos .DS_Store eliminados")
    return removed_count

def clean_pytest_cache():
    """Elimina cache de pytest"""
    print("\n🧪 Limpiando cache de pytest...")
    
    project_root = Path(__file__).parent.parent
    pytest_cache_dir = project_root / ".pytest_cache"
    
    if pytest_cache_dir.exists():
        shutil.rmtree(pytest_cache_dir)
        print("  ✓ Eliminado: .pytest_cache")
        return 1
    else:
        print("  ℹ️ No hay cache de pytest para eliminar")
        return 0

def clean_egg_info():
    """Limpia directorios egg-info de desarrollo"""
    print("\n🥚 Limpiando directorios egg-info...")
    
    project_root = Path(__file__).parent.parent
    removed_count = 0
    
    for egg_dir in project_root.glob("*.egg-info"):
        if egg_dir.is_dir():
            shutil.rmtree(egg_dir)
            print(f"  ✓ Eliminado: {egg_dir.name}")
            removed_count += 1
    
    print(f"  📊 {removed_count} directorios egg-info eliminados")
    return removed_count

def clean_build_dirs():
    """Limpia directorios de build"""
    print("\n🏗️ Limpiando directorios de build...")
    
    project_root = Path(__file__).parent.parent
    build_dirs = ["build", "dist"]
    removed_count = 0
    
    for build_dir_name in build_dirs:
        build_dir = project_root / build_dir_name
        if build_dir.exists():
            shutil.rmtree(build_dir)
            print(f"  ✓ Eliminado: {build_dir_name}")
            removed_count += 1
    
    print(f"  📊 {removed_count} directorios de build eliminados")
    return removed_count

def clean_log_files():
    """Limpia archivos de log"""
    print("\n📝 Limpiando archivos de log...")
    
    project_root = Path(__file__).parent.parent
    removed_count = 0
    
    # Limpiar logs del directorio principal
    for log_file in project_root.glob("*.log"):
        log_file.unlink()
        print(f"  ✓ Eliminado: {log_file.name}")
        removed_count += 1
    
    # Limpiar directorio logs si existe
    logs_dir = project_root / "logs"
    if logs_dir.exists():
        for log_file in logs_dir.rglob("*.log"):
            log_file.unlink()
            print(f"  ✓ Eliminado: logs/{log_file.name}")
            removed_count += 1
    
    print(f"  📊 {removed_count} archivos de log eliminados")
    return removed_count

def clean_temp_files():
    """Limpia archivos temporales"""
    print("\n⏳ Limpiando archivos temporales...")
    
    project_root = Path(__file__).parent.parent
    removed_count = 0
    
    temp_patterns = ["*.tmp", "*.temp", "*.swp", "*.swo", "*~", "*.bak", "*.backup"]
    
    for pattern in temp_patterns:
        for temp_file in project_root.rglob(pattern):
            # Solo eliminar si no está en venv
            if "venv" not in str(temp_file):
                temp_file.unlink()
                print(f"  ✓ Eliminado: {temp_file.relative_to(project_root)}")
                removed_count += 1
    
    print(f"  📊 {removed_count} archivos temporales eliminados")
    return removed_count

def clean_coverage_files():
    """Limpia archivos de coverage"""
    print("\n📊 Limpiando archivos de coverage...")
    
    project_root = Path(__file__).parent.parent
    removed_count = 0
    
    # Archivo .coverage
    coverage_file = project_root / ".coverage"
    if coverage_file.exists():
        coverage_file.unlink()
        print("  ✓ Eliminado: .coverage")
        removed_count += 1
    
    # Directorio htmlcov
    htmlcov_dir = project_root / "htmlcov"
    if htmlcov_dir.exists():
        shutil.rmtree(htmlcov_dir)
        print("  ✓ Eliminado: htmlcov/")
        removed_count += 1
    
    print(f"  📊 {removed_count} elementos de coverage eliminados")
    return removed_count

def verify_gitignore():
    """Verifica que .gitignore tenga las entradas necesarias"""
    print("\n🔍 Verificando .gitignore...")
    
    project_root = Path(__file__).parent.parent
    gitignore_path = project_root / ".gitignore"
    
    if not gitignore_path.exists():
        print("  ⚠️ .gitignore no existe")
        return False
    
    gitignore_content = gitignore_path.read_text()
    
    required_entries = [
        "__pycache__/",
        "*.py[cod]",
        "*.egg-info/",
        ".DS_Store",
        ".pytest_cache/",
        ".coverage",
        "htmlcov/",
        "venv/",
        "*.log"
    ]
    
    missing_entries = []
    for entry in required_entries:
        if entry not in gitignore_content:
            missing_entries.append(entry)
    
    if missing_entries:
        print(f"  ⚠️ Faltan entradas en .gitignore: {missing_entries}")
        return False
    else:
        print("  ✓ .gitignore está actualizado")
        return True

def show_summary(results):
    """Muestra resumen de la limpieza"""
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE LIMPIEZA")
    print("=" * 60)
    
    total_removed = sum(results.values())
    
    for category, count in results.items():
        status = "✅" if count > 0 else "ℹ️"
        print(f"{status} {category}: {count} elementos")
    
    print(f"\n📊 Total de elementos eliminados: {total_removed}")
    
    if total_removed > 0:
        print("\n✅ LIMPIEZA COMPLETADA - Proyecto listo para commit")
    else:
        print("\n✨ PROYECTO YA ESTÁ LIMPIO - No hay elementos para eliminar")
    
    print("\n🚀 Siguientes pasos:")
    print("   1. git add .")
    print("   2. git commit -m 'feat: Audio Splitter Suite 2.0 - Arquitectura modular completa'")
    print("   3. git push")

def main():
    """Ejecuta limpieza completa"""
    print("🧹 Audio Splitter Suite 2.0 - Limpieza Pre-Commit")
    print("=" * 60)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print(f"📁 Directorio: {project_root}")
    
    # Ejecutar todas las limpiezas
    results = {
        "Directorios __pycache__": clean_pycache_directories(),
        "Archivos .pyc": clean_pyc_files(),
        "Archivos .DS_Store": clean_ds_store(),
        "Cache de pytest": clean_pytest_cache(),
        "Directorios egg-info": clean_egg_info(),
        "Directorios de build": clean_build_dirs(),
        "Archivos de log": clean_log_files(),
        "Archivos temporales": clean_temp_files(),
        "Archivos de coverage": clean_coverage_files()
    }
    
    # Verificar .gitignore
    gitignore_ok = verify_gitignore()
    
    # Mostrar resumen
    show_summary(results)
    
    return sum(results.values()) > 0 or not gitignore_ok

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n❌ Limpieza cancelada")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error durante limpieza: {e}")
        sys.exit(1)
