import pandas as pd
import re
from difflib import SequenceMatcher

class IDXClassifier:
    def __init__(self, archivo_entrenamiento):
        """Carga el archivo con IDX conocido para entrenar el clasificador"""
        self.patrones = self._cargar_patrones(archivo_entrenamiento)
    
    def _cargar_patrones(self, archivo):
        """Extrae patrones de diagnóstico del archivo de entrenamiento"""
        df = pd.read_csv(archivo)
        patrones = {}
        
        for idx, grupo in df.groupby('IDX'):
            textos = grupo['MOTIVO'].str.upper().str.strip().tolist()
            palabras_clave = self._extraer_palabras_clave(textos)
            patrones[idx] = {
                'palabras_clave': palabras_clave,
                'ejemplos': textos[:3]  # Guarda algunos ejemplos para referencia
            }
        return patrones
    
    def _extraer_palabras_clave(self, textos):
        """Identifica palabras recurrentes en los textos de diagnóstico"""
        palabras = []
        for texto in textos:
            # Extrae palabras de 4+ letras (ignora conectores)
            palabras.extend(re.findall(r'\b[A-ZÁÉÍÓÚÜÑ]{4,}\b', texto))
        
        # Frecuencia de palabras
        frecuencias = pd.Series(palabras).value_counts()
        return frecuencias.head(10).index.tolist()  # Top 10 palabras por IDX
    
    def clasificar_texto(self, texto):
        """Asigna un IDX basado en similitud con los patrones de entrenamiento"""
        texto = str(texto).upper().strip()
        mejor_coincidencia = None
        mejor_puntaje = 0
        
        for idx, patron in self.patrones.items():
            # Puntaje por palabras clave coincidentes
            palabras_coincidentes = sum(
                1 for palabra in patron['palabras_clave'] 
                if palabra in texto
            )
            
            # Puntaje por similitud textual con ejemplos
            similitud = max(
                SequenceMatcher(None, texto, ejemplo).ratio()
                for ejemplo in patron['ejemplos']
            )
            
            puntaje_total = 0.7 * palabras_coincidentes + 0.3 * similitud
            
            if puntaje_total > mejor_puntaje:
                mejor_puntaje = puntaje_total
                mejor_coincidencia = idx
        
        return mejor_coincidencia if mejor_puntaje > 0.4 else "NO_CLASIFICADO"

def procesar_archivos():
    print("=== Clasificador Automático de IDX ===")
    
    # Paso 1: Archivo de entrenamiento (con IDX conocido)
    archivo_entrenamiento = input("\nRuta del archivo CSV de entrenamiento (con IDX): ")
    try:
        classifier = IDXClassifier(archivo_entrenamiento)
        print(f"\n✅ Modelo entrenado con {len(classifier.patrones)} patrones de IDX")
    except Exception as e:
        print(f"\n❌ Error al cargar archivo de entrenamiento: {e}")
        return
    
    # Paso 2: Archivo a clasificar
    archivo_clasificar = input("\nRuta del archivo CSV a clasificar: ")
    try:
        df = pd.read_csv(archivo_clasificar)
        if 'MOTIVO' not in df.columns:
            print("\n❌ El archivo debe contener columna 'MOTIVO'")
            return
    except Exception as e:
        print(f"\n❌ Error al leer archivo: {e}")
        return
    
    # Paso 3: Clasificar
    print("\n🔍 Clasificando diagnósticos...")
    df['IDX_PREDICHOS'] = df['MOTIVO'].apply(classifier.clasificar_texto)
    
    # Paso 4: Guardar resultados
    archivo_salida = archivo_clasificar.replace('.csv', '_clasificado.csv')
    df.to_csv(archivo_salida, index=False, encoding='utf-8-sig')
    
    # Resumen
    resumen = df['IDX_PREDICHOS'].value_counts().to_string()
    print(f"\n✅ Clasificación completada. Resultados guardados en:\n{archivo_salida}")
    print(f"\n📊 Resumen de clasificación:\n{resumen}")

if __name__ == "__main__":
    procesar_archivos()
