# Audio Splitter - Documento de Arquitectura de Software

## 1. Resumen Ejecutivo

### 1.1 Propósito del Documento
Este documento describe la arquitectura de software del sistema Audio Splitter, detallando sus componentes, patrones de diseño, decisiones arquitectónicas y consideraciones técnicas.

### 1.2 Alcance
La arquitectura cubre tres módulos principales: división de audio (audio_splitter.py), inserción de bloques (insertar_bloque_interactivo.py) y sustitución de bloques (sustituir_bloque_interactivo.py).

### 1.3 Audiencia
- Ingenieros de software que mantendrán o extenderán el sistema
- Arquitectos de software evaluando el diseño
- Desarrolladores integrando el sistema en workflows más amplios

## 2. Visión Arquitectónica

### 2.1 Objetivos Arquitectónicos
- **Modularidad**: Componentes independientes y reutilizables
- **Simplicidad**: Arquitectura fácil de entender y mantener
- **Eficiencia**: Procesamiento optimizado de archivos de audio grandes
- **Extensibilidad**: Facilidad para agregar nuevas funcionalidades

### 2.2 Principios de Diseño
- **Separación de Responsabilidades**: Cada módulo tiene una función específica
- **Inversión de Dependencias**: Dependencia de abstracciones, no implementaciones
- **Principio DRY**: Reutilización de funciones comunes de parsing temporal
- **Error Handling**: Manejo robusto de excepciones y validaciones

## 3. Arquitectura del Sistema

### 3.1 Vista de Alto Nivel

```
┌─────────────────────────────────────────────────────────────┐
│                    AUDIO SPLITTER SUITE                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐│
│  │  Audio Splitter │  │ Block Inserter  │  │Block Substitutor││
│  │     Module      │  │     Module      │  │     Module      ││
│  └─────────────────┘  └─────────────────┘  └─────────────────┘│
├─────────────────────────────────────────────────────────────┤
│              SHARED UTILITIES & LIBRARIES                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐│
│  │Time Parsing │  │File Handler │  │   Audio Processing      ││
│  │  Utilities  │  │  Utilities  │  │    (librosa/pydub)     ││
│  └─────────────┘  └─────────────┘  └─────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│                   EXTERNAL DEPENDENCIES                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐│
│  │   librosa   │  │  soundfile  │  │    pydub    │  │  numpy  ││
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘│
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Arquitectura por Capas

#### Capa de Presentación (CLI Layer)
- **Responsabilidad**: Interfaz de usuario de línea de comandos
- **Componentes**: Parsers de argumentos, modos interactivos
- **Tecnologías**: argparse, input() nativo

#### Capa de Lógica de Negocio (Business Logic Layer)
- **Responsabilidad**: Algoritmos de procesamiento de audio
- **Componentes**: Funciones de división, inserción y sustitución
- **Tecnologías**: Python puro, validaciones personalizadas

#### Capa de Procesamiento de Audio (Audio Processing Layer)
- **Responsabilidad**: Manipulación de datos de audio
- **Componentes**: Carga, transformación y exportación de audio
- **Tecnologías**: librosa, soundfile, pydub, numpy

#### Capa de Acceso a Datos (Data Access Layer)
- **Responsabilidad**: Operaciones de E/S de archivos
- **Componentes**: Lectores y escritores de archivos WAV
- **Tecnologías**: File system APIs, path management

## 4. Componentes del Sistema

### 4.1 Audio Splitter Module (audio_splitter.py)

#### 4.1.1 Responsabilidades
- División de archivos de audio en múltiples segmentos
- Soporte para múltiples formatos de tiempo
- Interfaces interactiva y de línea de comandos

#### 4.1.2 Componentes Principales

```python
class AudioSplitter:
    + split_audio(input_file, segments, output_dir)
    + convert_to_ms(time_str)
    + interactive_mode()
    + main()
```

#### 4.1.3 Dependencias
- **librosa**: Carga de archivos de audio con preservación de calidad
- **soundfile**: Exportación eficiente de segmentos
- **numpy**: Manipulación de arrays de audio
- **argparse**: Procesamiento de argumentos de línea de comandos

#### 4.1.4 Flujo de Datos
```
Input WAV File → librosa.load() → NumPy Array → Segment Extraction → soundfile.write() → Output WAV Files
```

### 4.2 Block Inserter Module (insertar_bloque_interactivo.py)

#### 4.2.1 Responsabilidades
- Inserción de bloques de audio en posiciones específicas
- Validación de rangos temporales
- Modo interactivo exclusivo

#### 4.2.2 Componentes Principales

```python
class BlockInserter:
    + parse_time_to_ms(time_str)
    + main()
```

#### 4.2.3 Dependencias
- **pydub.AudioSegment**: Manipulación intuitiva de segmentos de audio
- **Librería nativa de Python**: Para validaciones y E/O

#### 4.2.4 Algoritmo de Inserción
```
Original: [-----AUDIO_ORIGINAL-----]
Block:              [BLOCK]
Insert Point:           ↑
Result:   [-----AUDIO-][BLOCK][AUDIO-----]
```

### 4.3 Block Substitutor Module (sustituir_bloque_interactivo.py)

#### 4.3.1 Responsabilidades
- Sustitución de segmentos manteniendo duración total
- Validación de coherencia temporal
- Preservación de estructura original

#### 4.3.2 Componentes Principales

```python
class BlockSubstitutor:
    + parse_time_to_ms(time_str)
    + main()
```

#### 4.3.3 Algoritmo de Sustitución
```
Original: [--AUDIO--][OLD_BLOCK][--AUDIO--]
New Block:           [NEW_BLOCK]
Result:   [--AUDIO--][NEW_BLOCK][--AUDIO--]
```

## 5. Decisiones Arquitectónicas

### 5.1 Elección de Bibliotecas de Audio

#### 5.1.1 librosa vs PyDub
**Decisión**: Usar librosa como biblioteca principal para audio_splitter.py

**Razones**:
- **Precisión**: librosa mantiene mejor fidelidad de audio
- **Compatibilidad**: Mejor soporte para Python 3.13+
- **Rendimiento**: Más eficiente para archivos grandes
- **Flexibilidad**: Mejor control sobre frecuencias de muestreo

#### 5.1.2 Uso Híbrido
**Decisión**: Mantener PyDub para módulos de inserción y sustitución

**Razones**:
- **Simplicidad**: API más intuitiva para operaciones de segmentación
- **Compatibilidad**: Código existente estable
- **Funcionalidad**: Mejor para operaciones de concatenación

### 5.2 Arquitectura Modular vs Monolítica

**Decisión**: Arquitectura modular con archivos separados

**Razones**:
- **Mantenibilidad**: Cada módulo es independiente
- **Reutilización**: Componentes pueden usarse por separado
- **Testing**: Pruebas unitarias más fáciles
- **Escalabilidad**: Facilita adición de nuevas funcionalidades

### 5.3 Modo Interactivo vs Solo CLI

**Decisión**: Soporte dual (interactivo + línea de comandos)

**Razones**:
- **Usabilidad**: Modo interactivo para usuarios novatos
- **Automatización**: Línea de comandos para scripts y workflows
- **Flexibilidad**: Diferentes casos de uso cubiertos

## 6. Patrones de Diseño Implementados

### 6.1 Command Pattern
**Aplicación**: Estructura de comandos CLI
**Beneficio**: Separación entre invocación y ejecución

### 6.2 Template Method Pattern  
**Aplicación**: Flujo común de procesamiento de audio
**Beneficio**: Reutilización de lógica común

### 6.3 Strategy Pattern
**Aplicación**: Diferentes parsers de formato de tiempo
**Beneficio**: Flexibilidad en formatos soportados

### 6.4 Factory Pattern
**Aplicación**: Creación de objetos AudioSegment
**Beneficio**: Abstracción de complejidad de inicialización

## 7. Consideraciones de Rendimiento

### 7.1 Gestión de Memoria

#### 7.1.1 Streaming vs Loading
**Estrategia Actual**: Carga completa en memoria
**Justificación**: Archivos WAV típicos < 2GB, simplicidad de implementación
**Mejora Futura**: Implementar streaming para archivos > 2GB

#### 7.1.2 Optimización de Arrays NumPy
```python
# Eficiente: Slicing sin copia
segment = audio_array[start_sample:end_sample]

# Evitar: Copia innecesaria
# segment = audio_array[start_sample:end_sample].copy()
```

### 7.2 Operaciones de E/O

#### 7.2.1 Lectura Secuencial
- Uso de librosa con `sr=None` para evitar resampling innecesario
- Validación de archivos antes de carga completa

#### 7.2.2 Escritura Optimizada
- soundfile para escritura directa sin conversiones intermedias
- Creación lazy de directorios de salida

### 7.3 Complejidad Algorítmica

| Operación | Complejidad Temporal | Complejidad Espacial |
|-----------|---------------------|---------------------|
| Audio Loading | O(n) | O(n) |
| Segment Extraction | O(k) | O(k) |
| File Writing | O(k) | O(1) |
| Time Parsing | O(1) | O(1) |

Donde n = tamaño total del archivo, k = tamaño del segmento

## 8. Seguridad y Validación

### 8.1 Validación de Entrada

#### 8.1.1 Validación de Archivos
```python
# Verificación de existencia y permisos
if not os.path.exists(input_file):
    raise FileNotFoundError(f"Archivo no encontrado: {input_file}")

# Verificación de formato WAV
if not input_file.lower().endswith('.wav'):
    raise ValueError("Solo se soportan archivos WAV")
```

#### 8.1.2 Validación Temporal
```python
# Validación de rangos
if start_ms >= end_ms:
    raise ValueError("Tiempo de inicio debe ser menor que tiempo de fin")

if end_ms > audio_duration_ms:
    raise ValueError("Tiempo de fin excede duración del audio")
```

### 8.2 Manejo de Errores

#### 8.2.1 Jerarquía de Excepciones
```python
AudioSplitterError
├── InvalidTimeFormatError
├── AudioProcessingError
├── FileAccessError
└── ValidationError
```

#### 8.2.2 Estrategias de Recuperación
- **Fail Fast**: Validación temprana de parámetros
- **Graceful Degradation**: Mensajes de error informativos
- **Rollback**: Limpieza de archivos parciales en caso de falla

## 9. Escalabilidad y Extensibilidad

### 9.1 Puntos de Extensión

#### 9.1.1 Nuevos Formatos de Audio
```python
# Interface para procesadores de formato
class AudioProcessor:
    def load(self, file_path): pass
    def save(self, audio_data, file_path): pass
    def get_duration(self, audio_data): pass
```

#### 9.1.2 Nuevas Operaciones de Audio
```python
# Base class para operaciones
class AudioOperation:
    def execute(self, audio_data, **params): pass
    def validate_params(self, **params): pass
```

## 10. Conclusión Final

La arquitectura de Audio Splitter representa una solución bien estructurada para el procesamiento de archivos de audio WAV, con un enfoque en la simplicidad, modularidad y extensibilidad. El sistema actual cumple efectivamente con los requisitos establecidos y proporciona una base sólida para futuras mejoras.

### 10.1 Logros Arquitectónicos
- **Modularidad Efectiva**: Separación clara de responsabilidades entre componentes
- **Flexibilidad de Uso**: Soporte tanto para usuarios interactivos como para automatización
- **Robustez**: Manejo adecuado de errores y validaciones
- **Rendimiento**: Procesamiento eficiente para archivos de tamaño típico

### 10.2 Valor Técnico
La arquitectura demuestra buenas prácticas de ingeniería de software, incluyendo principios SOLID, patrones de diseño apropiados y consideraciones de seguridad. La elección de bibliotecas y tecnologías está bien justificada y alineada con los objetivos del sistema.

### 10.3 Preparación para el Futuro
Con las consideraciones de extensibilidad y el roadmap técnico definido, el sistema está bien posicionado para evolucionar y adaptarse a nuevos requisitos sin requerir cambios arquitectónicos fundamentales.

---

**Documento preparado por**: Análisis de Arquitectura de Software  
**Fecha**: Junio 2025  
**Versión**: 1.0  
**Estado**: Aprobado para Implementación