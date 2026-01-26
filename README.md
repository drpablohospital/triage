# Automatización del Triage en Servicios de Urgencias mediante IA

## 📌 Descripción del Proyecto
Repositorio para la tesis **"Automatización del Triage en Servicios de Urgencias mediante Inteligencia Artificial"** desarrollada en el Hospital General Dr. Manuel Gea González. Contiene:

- Modelos de IA (BERT/T5) para clasificación de pacientes
- Herramientas de procesamiento de datos clínicos
- Interfaces para implementación clínica

## 🚀 Objetivos
- Automatizar la clasificación de:
  - Prioridad clínica (I-IV)
  - Derivación (Alta/Consulta/Ingreso)
  - Especialidad requerida
  - Diagnóstico principal (IDX)
- Evaluar desempeño con métricas clínicas (Kappa, precisión)
- Implementar interfaz usable en entorno hospitalario

## 🛠️ Tecnologías
| Componente | Tecnologías |
|------------|-------------|
| Procesamiento | Python 3.10, Pandas, SpaCy |
| Modelos | BERT (BioClinicalBERT-es), T5 |
| Entrenamiento | PyTorch, Transformers |
| Evaluación | Scikit-learn, Matplotlib |
| Implementación | Hugging Face, Gradio |

## 📂 Estructura del Repositorio

| Dirección | Contenido |
|------------|-------------|
| db | Conjuntos de entrenamiento y validación |
| dep | Interferencias para los modelos (Apps) |
| logs | Salida estandar de terminal de entrenamiento de los modelos |
| tools | Herramientas de formato y análisis de datos |

## 🔧 Instalación

1. **Configurar entorno**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
🚦 Uso
Entrenamiento
bash
python trainers/bert_trainer.py --target PRIORIDAD --epochs 10
Evaluación
bash
python tools/eval_tools/model_evaluator.py --model bert_priority
Implementación clínica
python
from transformers import pipeline
triage_ai = pipeline("text-classification", model="tu_usuario/bert_triage_priority")
```

## 📊 Modelos Disponibles
Modelo	Kappa	Rendimiento	Enlace
BERT-Prioridad	0.82	84% accuracy	HF
T5-IDX	0.71	F1=0.76	HF

## 📝 Metodología
Datos: 2,000+ triages anonimizados

Procesamiento:

Extracción PDF→CSV

Limpieza automatizada

Clasificación manual validada

Entrenamiento: Fine-tuning en Colab Pro

Evaluación: Muestra estadística (n=136+)

## 📈 Resultados
Métrica	Prioridad	IDX
Kappa	0.82	0.71
Precisión	0.85	0.73
Recall	0.83	0.70

## 🤝 Contribución
Para colaboraciones contactar:

Crystian Perez Cruz - Investigador Principal
Jose Pablo Fernandez Magana - Investigador Asociado

drpablo.hospital@gmail.com

Hospital General Dr. Manuel Gea González

## 📜 Licencia
CC BY-NC 4.0 International

text

### Notas importantes:
1. Los datos reales no se incluyen por confidencialidad
2. Los modelos se comparten mediante enlaces por limitaciones de tamaño
3. El entorno virtual debe recrearse localmente
4. Requiere Python 3.10+ y CUDA para entrenamiento local

Para acceder a los modelos finales, consultar el archivo `models_links.txt` en la raíz del repositorio.
