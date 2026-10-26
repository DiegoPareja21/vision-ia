#  Asistente visual con IA

Asistente que **reconoce más de 600 objetos en tiempo real** con la webcam y **describe en voz alta** qué ve y dónde está. Pensado como prototipo de ayuda para personas con discapacidad visual.

![Demo](demo.gif)

##  Qué hace
- Detecta objetos en tiempo real con **YOLOv8x** entrenado con **Open Images V7** (601 clases, 1,7 M de imágenes)
- Indica la posición de cada objeto: izquierda, centro o derecha
- Habla en español usando el motor de voz de Windows (SAPI), con las 601 clases traducidas
- Ignora personas, partes del cuerpo y categorías genéricas para describir solo lo útil
- Solo habla cuando la escena cambia (*debounce*), para no repetir información
- Optimizado para tiempo real en GPU: PyTorch + CUDA, precisión FP16, entrada a 960 px y NMS agnóstico

##  Estructura
| Archivo | Qué contiene |
|---|---|
| `asistente_voz.py` | El asistente: cámara, detección y voz |
| `traducciones.py` | Traducción al español de las 601 clases y la lista de clases ignoradas |
| `pasos/` | Los ejercicios previos, en orden de aprendizaje |

##  Tecnologías
Python · OpenCV · Ultralytics YOLOv8 · PyTorch · CUDA · pywin32

##  Instalación
```bash
python -m venv .venv
.venv\Scripts\activate
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
pip install -r requirements.txt
python asistente_voz.py
```

##  Controles
| Tecla | Acción |
|---|---|
| `v` | Describir la escena ahora |
| `m` | Silenciar o activar la voz automática |
| `q` | Salir |

##  Lo que aprendí
La carpeta `pasos/` muestra la evolución del proyecto: desde abrir la webcam hasta la detección de 600 objetos.

##  Créditos
- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
- [Open Images Dataset V7](https://storage.googleapis.com/openimages/web/index.html) (Google)