# Audio Splitter

Una herramienta en Python para cortar archivos de audio .wav en segmentos más pequeños según tiempos específicos.

## Características

- Corta archivos .wav en múltiples segmentos
- Permite especificar tiempos de inicio y fin en varios formatos
- Soporta modo interactivo y modo línea de comandos
- Nombra los archivos de salida automáticamente o con nombres personalizados

## Requisitos previos

1. Python 3.6 o superior
2. Biblioteca `pydub`:
   ```
   pip install pydub
   ```
3. FFmpeg instalado en tu sistema (necesario para que pydub funcione)

   - **En macOS** (usando Homebrew):
     ```
     brew install ffmpeg
     ```
   - **En Ubuntu/Debian**:
     ```
     sudo apt-get install ffmpeg
     ```
   - **En Windows**: Descarga desde [ffmpeg.org](https://ffmpeg.org/download.html) y añade a PATH

## Instalación

1. Clona o descarga este repositorio
2. Asegúrate de tener instaladas las dependencias mencionadas anteriormente

## Uso

### Modo interactivo

Ejecuta el script sin argumentos para usar el modo interactivo, que te guiará paso a paso:

```
python audio_splitter.py
```

El programa te pedirá:
1. La ruta del archivo de audio .wav
2. El directorio donde guardar los segmentos (opcional)
3. Para cada segmento:
   - Tiempo de inicio
   - Tiempo de fin
   - Nombre del archivo de salida (opcional)

### Modo línea de comandos

Para automatizar el proceso o usarlo en scripts:

```
python audio_splitter.py --input ARCHIVO.WAV --segments "INICIO-FIN:NOMBRE" "INICIO-FIN:NOMBRE" ...
```

Parámetros:
- `--input` o `-i`: Ruta al archivo de audio .wav
- `--output-dir` o `-o`: Directorio donde guardar los segmentos (por defecto: "output")
- `--segments` o `-s`: Lista de segmentos en formato "inicio-fin:nombre"

## Formatos de tiempo aceptados

El programa acepta varios formatos de tiempo:

- `MM:SS` (minutos:segundos) - Ejemplo: "1:30" (1 minuto y 30 segundos)
- `MM:SS.ms` (minutos:segundos.milisegundos) - Ejemplo: "1:30.500" (1 minuto, 30 segundos y 500 milisegundos)
- `HH:MM:SS` (horas:minutos:segundos) - Ejemplo: "1:30:45" (1 hora, 30 minutos y 45 segundos)
- Segundos - Ejemplo: "90.5" (90 segundos y medio)
- Milisegundos - Ejemplo: "90500" (90.5 segundos en milisegundos)

## Ejemplos

### Ejemplo 1: Cortar una canción en partes

```
python audio_splitter.py --input cancion.wav --segments "0:00-0:30:intro" "0:30-2:15:estrofa1" "2:15-2:45:coro" "2:45-4:30:estrofa2" "4:30-5:00:outro"
```

### Ejemplo 2: Extraer segmentos de una entrevista

```
python audio_splitter.py --input entrevista.wav --segments "1:20-3:45:pregunta1" "5:30-8:15:pregunta2" "10:20-15:00:pregunta3"
```

### Ejemplo 3: Guardar en un directorio específico

```
python audio_splitter.py --input podcast.wav --output-dir segmentos_podcast --segments "0:00-5:00:introduccion" "5:00-25:00:tema_principal" "25:00-30:00:conclusion"
```

## Solución de problemas

### Error al cargar el archivo de audio
- Asegúrate de que la ruta al archivo es correcta
- Verifica que el archivo esté en formato .wav
- Comprueba que FFmpeg esté instalado correctamente

### Error al procesar los segmentos
- Verifica que los tiempos de inicio sean menores que los tiempos de fin
- Asegúrate de usar los formatos de tiempo correctos
- Comprueba que tienes permisos de escritura en el directorio de salida

## Licencia

Este proyecto está disponible como código abierto bajo los términos de la licencia MIT.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, siente libre de mejorar este código o reportar problemas.
