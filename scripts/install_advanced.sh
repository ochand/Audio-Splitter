#!/bin/bash
# Script de instalación para Audio Splitter Suite Avanzado

echo "======================================"
echo "🎵 Audio Splitter Suite - Instalación"
echo "======================================"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instala Python 3.6+ primero."
    exit 1
fi

echo "✅ Python 3 encontrado: $(python3 --version)"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Error creando entorno virtual"
        exit 1
    fi
    echo "✅ Entorno virtual creado"
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Error activando entorno virtual"
    exit 1
fi

# Actualizar pip
echo "📦 Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📦 Instalando dependencias..."

# Dependencias básicas de audio
echo "  - Instalando bibliotecas de audio..."
pip install librosa>=0.10.0
pip install soundfile>=0.12.0
pip install pydub>=0.25.0
pip install numpy>=1.21.0

# Dependencias para metadatos
echo "  - Instalando bibliotecas de metadatos..."
pip install mutagen>=1.47.0
pip install eyed3>=0.9.7
pip install tinytag>=1.10.0

# Dependencias para imágenes
echo "  - Instalando bibliotecas de imágenes..."
pip install Pillow>=10.0.0

# Dependencias para UI
echo "  - Instalando bibliotecas de interfaz..."
pip install rich>=13.0.0
pip install click>=8.1.0
pip install tabulate>=0.9.0

# Dependencias adicionales
echo "  - Instalando utilidades..."
pip install tqdm>=4.64.0
pip install colorama>=0.4.6
pip install requests>=2.28.0

# Verificar instalación
echo ""
echo "🔍 Verificando instalación..."

python3 -c "
import librosa
import soundfile
import mutagen
import rich
from PIL import Image
print('✅ Todas las dependencias principales están instaladas')
" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Verificación exitosa"
else
    echo "⚠️  Algunas dependencias pueden tener problemas"
fi

# Crear directorio de plantillas
echo "📁 Creando directorios..."
mkdir -p metadata_templates
mkdir -p output
mkdir -p sources

# Hacer ejecutables los scripts principales
echo "🔧 Configurando permisos..."
chmod +x main.py
chmod +x audio_splitter.py
chmod +x audio_converter.py
chmod +x metadata_editor.py

echo ""
echo "🎉 ¡Instalación completada!"
echo ""
echo "📖 Para usar el sistema:"
echo "   1. Activa el entorno virtual: source venv/bin/activate"
echo "   2. Ejecuta el menú principal: python3 main.py"
echo ""
echo "🚀 Módulos disponibles:"
echo "   • Audio Converter - Conversión WAV/MP3/FLAC"
echo "   • Audio Splitter - División en segmentos"
echo "   • Metadata Editor - Editor profesional"
echo "   • Artwork Manager - Gestión de carátulas"
echo ""
echo "📚 Documentación:"
echo "   • README.md - Guía de usuario"
echo "   • PRD_Audio_Splitter.md - Especificaciones"
echo "   • Arquitectura_Audio_Splitter.md - Documentación técnica"
echo ""
