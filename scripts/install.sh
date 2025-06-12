#!/bin/bash
# Script para instalar las dependencias requeridas

echo "Instalando dependencias..."

# Para entorno conda
if command -v conda &> /dev/null; then
    echo "Detectado entorno Conda. Instalando con conda..."
    conda install -y -c conda-forge librosa soundfile numpy
else
    # Instalación con pip
    echo "Instalando con pip..."
    pip install librosa soundfile numpy
fi

echo "Instalación completa. Ahora puedes ejecutar audio_splitter.py"
