#!/bin/bash
# Ejemplo de uso del divisor de audio

# Asegúrate de tener instalado lo necesario
echo "Verificando que pydub esté instalado..."
pip install pydub

# Crea un ejemplo de uso
echo "=====================================
EJEMPLO DE USO DE AUDIO SPLITTER
=====================================

Para dividir un archivo de audio podcast.wav en tres partes:
- Introducción (0:00 - 2:30)
- Contenido principal (2:30 - 18:45)
- Conclusión (18:45 - 22:10)

Ejecuta el siguiente comando:

python audio_splitter.py --input podcast.wav --segments \"0:00-2:30:introduccion\" \"2:30-18:45:contenido_principal\" \"18:45-22:10:conclusion\"

O si prefieres el modo interactivo, simplemente ejecuta:

python audio_splitter.py

Y sigue las instrucciones en pantalla.
"

# Dar permisos de ejecución al script principal
chmod +x audio_splitter.py

echo "Script de ejemplo creado. Para ejecutarlo: sh ejemplo_uso.sh"
