# 🎵 Audio Splitter Suite 2.0

Sistema completo de procesamiento de audio con arquitectura modular profesional. Divide, convierte y edita metadatos de archivos de audio con facilidad.

## ✨ Características

- **🔄 Audio Converter**: Conversión entre WAV, MP3 y FLAC con preservación de metadatos
- **✂️ Audio Splitter**: División precisa de archivos de audio en segmentos
- **🏷️ Metadata Editor**: Editor profesional de metadatos ID3v2.4, Vorbis y iTunes
- **🖼️ Artwork Manager**: Gestión completa de carátulas de álbumes
- **🎛️ Interfaz dual**: Línea de comandos y menús interactivos
- **📦 Arquitectura modular**: Código organizado y mantenible

## 🚀 Instalación

### Instalación rápida
```bash
git clone https://github.com/yourusername/Audio-Splitter.git
cd Audio-Splitter
pip install -r requirements.txt
```

### Instalación como paquete
```bash
pip install -e .
```

### Scripts de instalación
```bash
# Instalación básica
./scripts/install.sh

# Instalación avanzada con herramientas de desarrollo
./scripts/install_advanced.sh
```

## 📖 Uso

### Modo Interactivo
```bash
python main.py
```

### Línea de Comandos

#### División de audio
```bash
python -m audio_splitter.ui.cli split archivo.wav --segments "0:30-1:45:intro" "1:45-3:20:verso"
```

#### Conversión de formatos
```bash
python -m audio_splitter.ui.cli convert archivo.wav -f mp3 -q high
python -m audio_splitter.ui.cli convert directorio/ -f flac --batch --recursive
```

#### Edición de metadatos
```bash
python -m audio_splitter.ui.cli metadata archivo.mp3 --title "Mi Canción" --artist "Mi Artista"
```

## 🏗️ Arquitectura

```
Audio-Splitter/
├── 📁 audio_splitter/              # Paquete principal
│   ├── 📁 core/                    # Lógica de negocio
│   │   ├── splitter.py             # División de audio
│   │   ├── converter.py            # Conversión de formatos
│   │   └── metadata_manager.py     # Gestión de metadatos
│   ├── 📁 ui/                      # Interfaces de usuario
│   │   ├── cli.py                  # Línea de comandos
│   │   └── interactive.py          # Menús interactivos
│   ├── 📁 utils/                   # Utilidades
│   │   ├── file_utils.py           # Manejo de archivos
│   │   └── audio_utils.py          # Procesamiento de audio
│   └── 📁 config/                  # Configuraciones
│       └── settings.py             # Configuraciones globales
├── 📁 tests/                       # Tests unitarios
├── 📁 docs/                        # Documentación
├── 📁 scripts/                     # Scripts de utilidad
├── 📁 data/                        # Datos del proyecto
│   ├── 📁 templates/               # Plantillas de metadatos
│   ├── 📁 output/                  # Archivos de salida
│   └── 📁 sources/                 # Archivos fuente
├── main.py                         # Punto de entrada
├── setup.py                        # Configuración del paquete
└── requirements.txt                # Dependencias
```

## 🛠️ Desarrollo

### Ejecutar tests
```bash
python -m pytest tests/
```

### Limpiar archivos temporales
```bash
python scripts/cleanup.py
```

### Estructura modular
- **Separación de responsabilidades**: Core, UI, Utils, Config
- **Importaciones limpias**: Cada módulo con responsabilidad específica
- **Tests unitarios**: Cobertura de funcionalidades principales
- **Configuración centralizada**: Settings globales en un solo lugar

## 📋 Formatos Soportados

### Entrada
- WAV (sin compresión)
- MP3 (MPEG Audio Layer III)
- FLAC (Free Lossless Audio Codec)
- M4A (MPEG-4 Audio)
- OGG (Ogg Vorbis)

### Salida
- WAV (sin compresión, máxima calidad)
- MP3 (128k, 192k, 320k, VBR)
- FLAC (niveles de compresión 0-8)

### Metadatos
- **MP3**: ID3v2.4 (TIT2, TPE1, TALB, etc.)
- **FLAC**: Vorbis Comments
- **MP4/M4A**: iTunes tags
- **WAV**: ID3 embebido (soporte limitado)

## 🎯 Casos de Uso

### Para Músicos
- División de sesiones de grabación en pistas individuales
- Conversión de masters a diferentes formatos para distribución
- Organización de metadatos para bibliotecas musicales

### Para Podcasters
- División de episodios largos en segmentos
- Conversión a MP3 optimizado para distribución
- Adición de metadatos y artwork profesional

### Para Archivistas
- Conversión de formatos legacy a estándares modernos
- Preservación con FLAC sin pérdida
- Organización masiva de colecciones

## 🔧 Configuración Avanzada

### Calidades de conversión
```python
# MP3
'low': 128k bitrate
'medium': 192k bitrate  
'high': 320k bitrate
'vbr_medium': Variable Bitrate Q2
'vbr_high': Variable Bitrate Q0

# FLAC
'low': Compresión nivel 0 (más rápido)
'medium': Compresión nivel 5 (balanceado)
'high': Compresión nivel 8 (menor tamaño)
```

### Directorios personalizables
```python
# En audio_splitter/config/settings.py
OUTPUT_DIR = "mi_directorio_salida"
TEMPLATES_DIR = "mis_plantillas"
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Changelog

### v2.0.0
- ✨ **Nueva arquitectura modular**
- ✨ **Interfaz CLI completa**
- ✨ **Sistema de configuración centralizado**
- ✨ **Tests unitarios**
- ✨ **Mejor manejo de errores**
- ✨ **Documentación mejorada**
- 🔧 **Refactoring completo del código**
- 🔧 **Separación de responsabilidades**

### v1.0.0
- 🎉 **Lanzamiento inicial**
- ✨ **Audio Splitter básico**
- ✨ **Audio Converter**
- ✨ **Metadata Editor**

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Reconocimientos

- **librosa**: Procesamiento de audio
- **mutagen**: Manejo de metadatos
- **rich**: Interfaz de terminal mejorada
- **pydub**: Manipulación de audio
- **soundfile**: I/O de archivos de audio

## 📞 Soporte

- 📧 **Email**: contact@audiosplitter.dev
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/Audio-Splitter/issues)
- 📖 **Documentación**: [Docs](docs/)
- 💬 **Discusiones**: [GitHub Discussions](https://github.com/yourusername/Audio-Splitter/discussions)

---

**🎵 Audio Splitter Suite 2.0** - *Procesamiento de audio profesional, simplificado.*
