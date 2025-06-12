#!/usr/bin/env python3
from pydub import AudioSegment

def parse_time_to_ms(t):
    """Convierte un string mm:ss o ss a milisegundos."""
    parts = t.split(':')
    if len(parts) == 1:
        seconds = float(parts[0])
        return int(seconds * 1000)
    elif len(parts) == 2:
        minutes = float(parts[0])
        seconds = float(parts[1])
        return int((minutes * 60 + seconds) * 1000)
    else:
        raise ValueError("Formato de tiempo inválido (debe ser ss o mm:ss)")

def main():
    print("=== Inserción de bloque de audio en WAV ===\n")

    entrada = input("Ruta del archivo WAV de entrada: ").strip()
    salida = input("Nombre del archivo WAV de salida: ").strip()

    ini_b = input("Tiempo inicio del bloque (ss o mm:ss): ").strip()
    fin_b = input("Tiempo fin del bloque (ss o mm:ss): ").strip()
    ins_pt = input("Punto de inserción (ss o mm:ss): ").strip()

    try:
        start_ms = parse_time_to_ms(ini_b)
        end_ms   = parse_time_to_ms(fin_b)
        insert_ms= parse_time_to_ms(ins_pt)
    except ValueError as e:
        print(f"Error al parsear tiempos: {e}")
        return

    # Carga y procesamiento
    print("\nCargando audio…")
    audio = AudioSegment.from_wav(entrada)

    # Validar rangos
    if start_ms < 0 or end_ms > len(audio) or start_ms >= end_ms:
        print("Rangos de corte inválidos.")
        return
    if insert_ms < 0 or insert_ms > len(audio):
        print("Punto de inserción fuera de los límites del audio.")
        return

    bloque = audio[start_ms:end_ms]
    inicio = audio[:insert_ms]
    final  = audio[insert_ms:]
    resultado = inicio + bloque + final

    # Exportar
    resultado.export(salida, format="wav")
    print(f"\n✅ Archivo generado: {salida} (duración: {len(resultado)/1000:.2f}s)")

if __name__ == "__main__":
    main()