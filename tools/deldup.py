import os
import re
from pathlib import Path

def seleccionar_carpeta_terminal():
    print("\n📂 Carpetas disponibles en el directorio actual:")
    contenido = [f for f in os.listdir() if os.path.isdir(f)]
    
    if not contenido:
        print("No hay subcarpetas aquí.")
        return None
        
    for i, carpeta in enumerate(contenido, 1):
        print(f"{i}. {carpeta}")
    
    try:
        seleccion = int(input("\nIngresa el número de la carpeta: ")) - 1
        return contenido[seleccion]
    except (ValueError, IndexError):
        return None

def eliminar_duplicados(directorio):
    patron_duplicado = re.compile(r'^(.*?)\s+\(\d+\)(\..+)?$')
    eliminados = 0
    
    for nombre_archivo in os.listdir(directorio):
        ruta_archivo = os.path.join(directorio, nombre_archivo)
        
        if not os.path.isfile(ruta_archivo):
            continue
            
        coincidencia = patron_duplicado.match(nombre_archivo)
        if coincidencia:
            nombre_base = coincidencia.group(1)
            extension = coincidencia.group(2) or ""
            nombre_original = f"{nombre_base}{extension}"
            ruta_original = os.path.join(directorio, nombre_original)
            
            if os.path.exists(ruta_original):
                print(f"🗑️ Eliminando duplicado: {nombre_archivo}")
                os.remove(ruta_archivo)
                eliminados += 1

    return eliminados

if __name__ == "__main__":
    print("=== Modo Terminal ===")
    print(f"Ubicación actual: {os.getcwd()}")
    
    opcion = input("\n¿Quieres: \n1. Usar esta carpeta \n2. Navegar a subcarpetas\nOpción: ")
    
    if opcion == "1":
        carpeta = os.getcwd()
    elif opcion == "2":
        carpeta = seleccionar_carpeta_terminal()
    else:
        print("❌ Opción inválida")
        exit()

    if carpeta:
        total = eliminar_duplicados(carpeta)
        print(f"\n✅ Listo! Se eliminaron {total} archivos duplicados en: {carpeta}")
    else:
        print("❌ No se seleccionó carpeta válida")