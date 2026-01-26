import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    archivo = filedialog.askopenfilename(
        title="Selecciona el archivo CSV",
        filetypes=[("Archivos CSV", "*.csv")]
    )
    return archivo

def generar_muestra_estratificada(df):
    # Definir el tamaño de muestra por estrato (prioridad)
    tamanos_muestra = {
        'I': 20,
        'II': 30,
        'III': 75,
        'IV': 25
    }

    # Verificar que hay suficientes casos para cada estrato
    for prioridad, tamano in tamanos_muestra.items():
        disponibles = len(df[df['PRIORIDAD'] == prioridad])
        if disponibles < tamano:
            print(f"⚠️ Advertencia: Solo hay {disponibles} casos de prioridad {prioridad} (se solicitaban {tamano})")
            tamanos_muestra[prioridad] = disponibles

    # Seleccionar muestras aleatorias para cada estrato
    muestras = []
    indices_muestra = []
    for prioridad, tamano in tamanos_muestra.items():
        estrato = df[df['PRIORIDAD'] == prioridad]
        muestra = estrato.sample(n=tamano, random_state=42)
        muestras.append(muestra)
        indices_muestra.extend(muestra.index.tolist())

    # Combinar todas las muestras y mezclar
    muestra_final = pd.concat(muestras).sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Crear base remanente (excluyendo los índices usados)
    base_remanente = df.drop(indices_muestra).reset_index(drop=True)
    
    return muestra_final, base_remanente

def guardar_archivos(df_muestra, df_remanente, archivo_original):
    directorio = os.path.dirname(archivo_original)
    nombre_base = os.path.basename(archivo_original)
    
    # Generar nombres para los nuevos archivos
    ruta_muestra = os.path.join(directorio, f"muestra_estratificada_{nombre_base}")
    ruta_remanente = os.path.join(directorio, f"base_remanente_{nombre_base}")
    
    # Guardar ambos archivos
    df_muestra.to_csv(ruta_muestra, index=False, encoding='utf-8-sig')
    df_remanente.to_csv(ruta_remanente, index=False, encoding='utf-8-sig')
    
    return ruta_muestra, ruta_remanente

if __name__ == "__main__":
    print("📊 Generador de Muestra Estratificada + Base Remanente")
    print("------------------------------------------------------")

    csv_file = seleccionar_archivo()

    if csv_file:
        try:
            df = pd.read_csv(csv_file, encoding='utf-8')

            if 'PRIORIDAD' not in df.columns:
                raise ValueError("El archivo CSV no contiene la columna 'PRIORIDAD'")

            muestra, remanente = generar_muestra_estratificada(df)

            print("\n📝 Resumen de la muestra generada:")
            print(muestra['PRIORIDAD'].value_counts().sort_index())
            
            print("\n📝 Resumen de la base remanente:")
            print(remanente['PRIORIDAD'].value_counts().sort_index())

            ruta_muestra, ruta_remanente = guardar_archivos(muestra, remanente, csv_file)
            print(f"\n✅ Muestra guardada en: {ruta_muestra}")
            print(f"✅ Base remanente guardada en: {ruta_remanente}")
            print(f"📊 Total original: {len(df)} | Muestra: {len(muestra)} | Remanente: {len(remanente)}")

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
    else:
        print("\n❌ No se seleccionó ningún archivo CSV")