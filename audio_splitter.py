#!/usr/bin/env python3
"""
Audio Splitter - Corta archivos de audio .wav en segmentos definidos por el usuario.
Uso: Especifica el archivo de entrada y los tiempos de inicio y fin para cada segmento.
"""

from pydub import AudioSegment
import os
import argparse

def split_audio(input_file, segments, output_dir="output"):
    """
    Divide un archivo de audio en segmentos según los tiempos especificados.
    
    Args:
        input_file (str): Ruta al archivo de audio .wav
        segments (list): Lista de tuplas (inicio_ms, fin_ms, nombre)
        output_dir (str): Directorio donde se guardarán los archivos de salida
    """
    try:
        # Cargar el archivo de audio
        print(f"Cargando archivo de audio: {input_file}")
        audio = AudioSegment.from_wav(input_file)
        
        # Crear directorio de salida si no existe
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Directorio de salida creado: {output_dir}")
        
        # Procesar cada segmento
        for i, (start_ms, end_ms, name) in enumerate(segments):
            # Extraer el segmento
            print(f"Cortando segmento {i+1}: {start_ms}ms - {end_ms}ms")
            segment = audio[start_ms:end_ms]
            
            # Definir nombre de salida
            if name:
                output_file = f"{output_dir}/{name}.wav"
            else:
                output_file = f"{output_dir}/segment_{i+1}.wav"
            
            # Exportar el segmento
            segment.export(output_file, format="wav")
            print(f"Segmento guardado como: {output_file}")
    
    except Exception as e:
        print(f"Error al procesar el audio: {e}")
        return False
    
    return True

def convert_to_ms(time_str):
    """
    Convierte una cadena de tiempo (MM:SS o MM:SS.ms) a milisegundos.
    
    Args:
        time_str (str): Tiempo en formato "MM:SS" o "MM:SS.ms"
    
    Returns:
        int: Tiempo en milisegundos
    """
    # Manejar casos como "1:30" (1min 30seg) o "1:30.500" (1min 30.5seg)
    parts = time_str.split(':')
    
    if len(parts) == 2:  # formato MM:SS o MM:SS.ms
        minutes, seconds = parts
        minutes = int(minutes)
        seconds = float(seconds)
        return int((minutes * 60 + seconds) * 1000)
    elif len(parts) == 3:  # formato HH:MM:SS o HH:MM:SS.ms
        hours, minutes, seconds = parts
        hours = int(hours)
        minutes = int(minutes)
        seconds = float(seconds)
        return int((hours * 3600 + minutes * 60 + seconds) * 1000)
    else:
        # Asumimos que es directamente segundos o milisegundos
        try:
            if '.' in time_str:  # Si tiene punto decimal, asumimos segundos
                return int(float(time_str) * 1000)
            else:  # Si no tiene punto decimal, asumimos milisegundos
                return int(time_str)
        except ValueError:
            raise ValueError(f"Formato de tiempo no reconocido: {time_str}")

def interactive_mode():
    """Modo interactivo para solicitar parámetros al usuario"""
    input_file = input("Ingresa la ruta del archivo de audio .wav: ").strip()
    output_dir = input("Ingresa el directorio de salida (predeterminado: 'output'): ").strip() or "output"
    
    segments = []
    while True:
        print("\nDefinir un nuevo segmento (deja en blanco para terminar):")
        start_time = input("Tiempo de inicio (MM:SS o MM:SS.ms): ").strip()
        if not start_time:
            break
            
        end_time = input("Tiempo de fin (MM:SS o MM:SS.ms): ").strip()
        name = input("Nombre del archivo de salida (opcional): ").strip()
        
        try:
            start_ms = convert_to_ms(start_time)
            end_ms = convert_to_ms(end_time)
            segments.append((start_ms, end_ms, name))
            print(f"Segmento añadido: {start_time} - {end_time}")
        except ValueError as e:
            print(f"Error: {e}")
    
    if segments:
        if split_audio(input_file, segments, output_dir):
            print(f"\n¡Proceso completado! Se generaron {len(segments)} segmentos en '{output_dir}'")
        else:
            print("\nEl proceso falló.")
    else:
        print("\nNo se definieron segmentos. Terminando.")

def main():
    parser = argparse.ArgumentParser(description='Divide un archivo de audio .wav en segmentos.')
    parser.add_argument('--input', '-i', help='Archivo de audio de entrada (.wav)')
    parser.add_argument('--output-dir', '-o', default='output', help='Directorio de salida para los segmentos')
    parser.add_argument('--segments', '-s', nargs='+', help='Segmentos en formato "inicio-fin:nombre" (ej: "1:30-2:45:intro")')
    
    args = parser.parse_args()
    
    # Si se proporcionan argumentos, usamos el modo línea de comandos
    if args.input and args.segments:
        segments = []
        for seg in args.segments:
            try:
                # Formato esperado: "inicio-fin:nombre" (ej: "1:30-2:45:intro")
                time_range, *name_parts = seg.split(':')
                name = name_parts[0] if name_parts else ""
                
                start_end = time_range.split('-')
                if len(start_end) == 2:
                    start_ms = convert_to_ms(start_end[0])
                    end_ms = convert_to_ms(start_end[1])
                    segments.append((start_ms, end_ms, name))
            except Exception as e:
                print(f"Error al procesar el segmento '{seg}': {e}")
        
        if segments:
            if split_audio(args.input, segments, args.output_dir):
                print(f"\n¡Proceso completado! Se generaron {len(segments)} segmentos en '{args.output_dir}'")
            else:
                print("\nEl proceso falló.")
        else:
            print("No se pudieron procesar los segmentos. Verifica el formato.")
    else:
        # Si no hay argumentos suficientes, usamos modo interactivo
        interactive_mode()

if __name__ == "__main__":
    main()
