import os
from PyPDF2 import PdfMerger
import tkinter as tk
from tkinter import filedialog

def seleccionar_carpeta():
    """Muestra un diálogo para seleccionar una carpeta y retorna su ruta"""
    root = tk.Tk()
    root.withdraw()
    try:
        carpeta = filedialog.askdirectory(
            title="Selecciona la carpeta con los PDFs",
            initialdir=os.getcwd()  # Comienza en el directorio actual
        )
        return carpeta
    except Exception as e:
        print(f"Error al seleccionar carpeta: {e}")
        return None

def unificar_pdfs(carpeta_origen, archivo_salida="pdf_unificado.pdf"):
    """
    Une todos los PDFs de una carpeta en un único archivo de forma optimizada.
    
    Args:
        carpeta_origen (str): Ruta de la carpeta con PDFs.
        archivo_salida (str): Nombre del archivo resultante.
    """
    if not os.path.isdir(carpeta_origen):
        print(f"❌ La carpeta no existe: {carpeta_origen}")
        return

    merger = PdfMerger()
    pdfs = sorted([
        archivo for archivo in os.listdir(carpeta_origen) 
        if archivo.lower().endswith('.pdf')
    ])

    if not pdfs:
        print("⚠️ No se encontraron archivos PDF en la carpeta")
        return

    print(f"\n📂 Procesando {len(pdfs)} PDFs en: {carpeta_origen}")

    # Procesar cada PDF con manejo de recursos
    for pdf in pdfs:
        try:
            with open(os.path.join(carpeta_origen, pdf), 'rb') as f:
                merger.append(f)
            print(f"  ✓ {pdf}")
        except Exception as e:
            print(f"  ✗ Error con {pdf}: {str(e)}")
            continue

    # Guardar el resultado con manejo de errores
    ruta_salida = os.path.join(carpeta_origen, archivo_salida)
    
    try:
        with open(ruta_salida, 'wb') as salida:
            merger.write(salida)
        print(f"\n✅ PDF unificado guardado en:\n{ruta_salida}")
        print(f"📄 Total de páginas: {len(merger.pages)}")
    except Exception as e:
        print(f"\n❌ Error al guardar: {e}")
    finally:
        merger.close()

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🔄 UNIFICADOR DE PDFs OPTIMIZADO".center(50))
    print("="*50 + "\n")
    
    carpeta = seleccionar_carpeta()
    if carpeta:
        unificar_pdfs(carpeta)
    else:
        print("Operación cancelada por el usuario.")