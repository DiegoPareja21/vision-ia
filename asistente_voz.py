import cv2
import time
import queue
import threading
import pythoncom
import win32com.client
from ultralytics import YOLO
from traducciones import TRADUCCION, IGNORAR

# ───────────── 1. LA VOZ (en un hilo aparte) ─────────────
cola_voz = queue.Queue()

def trabajador_voz():
    pythoncom.CoInitialize()                         # Necesario para usar la voz desde un hilo
    voz = win32com.client.Dispatch("SAPI.SpVoice")   # Voz de Windows (Helena, en español)
    while True:
        texto = cola_voz.get()                       # Espera a que llegue un mensaje
        voz.Speak(texto)

threading.Thread(target=trabajador_voz, daemon=True).start()

def decir(texto):
    print("🔊", texto)
    if cola_voz.empty():           # Si todavía está hablando, no acumulamos mensajes viejos
        cola_voz.put(texto)



def posicion(x_centro, ancho):
    if x_centro < ancho / 3:
        return "a la izquierda"
    if x_centro > 2 * ancho / 3:
        return "a la derecha"
    return "en el centro"

def describir(r):
    """Convierte las detecciones de YOLO en un diccionario {objeto: posición}."""
    ancho = r.orig_shape[1]
    vistos = {}
    for box in r.boxes:
        nombre = r.names[int(box.cls)]
        if nombre in IGNORAR:
            continue
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        texto = TRADUCCION.get(nombre, nombre)   # Si no está traducido, lo dice en inglés
        vistos[texto] = posicion((x1 + x2) / 2, ancho)
    return vistos

def frase(vistos):
    if not vistos:
        return "No veo ningún objeto."
    partes = [f"{obj} {pos}" for obj, pos in vistos.items()]
    if len(partes) == 1:
        return f"Veo {partes[0]}."
    return "Veo " + ", ".join(partes[:-1]) + " y " + partes[-1] + "."

# ───────────── 3. EL PROGRAMA PRINCIPAL ─────────────
model = YOLO("yolov8x-oiv7.pt")   # x = extra large, el más preciso
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
tiempo_anterior = time.time()

candidato = set()      # Lo que se está viendo ahora
frames_estable = 0     # Cuántos frames seguidos lleva igual
ultimo_dicho = set()   # Lo último que se anunció en voz alta
silencio = False

decir("Asistente activado.")

while True:
    ok, frame = cap.read()
    if not ok:
        print("No pude leer la cámara")
        break

    r = model(frame, conf=0.3, imgsz=960, quantize=16, agnostic_nms=True, verbose=False)[0]
    vistos = describir(r)
    actual = set(vistos)

    # Debounce: solo hablamos si la escena se mantiene igual 15 frames seguidos
    if actual == candidato:
        frames_estable += 1
    else:
        candidato = actual
        frames_estable = 0

    if frames_estable == 15 and actual != ultimo_dicho:
        if actual and not silencio:
            decir(frase(vistos))
        ultimo_dicho = actual

    imagen = r.plot()
    ahora = time.time()
    fps = 1 / (ahora - tiempo_anterior)
    tiempo_anterior = ahora
    cv2.putText(imagen, f"FPS: {fps:.0f}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    estado = "SILENCIO" if silencio else "voz activa"
    cv2.putText(imagen, f"{estado}  [v] describir  [m] silencio  [q] salir", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.imshow("Asistente visual", imagen)

    tecla = cv2.waitKey(1) & 0xFF
    if tecla == ord("q"):
        break
    if tecla == ord("v"):          
        decir(frase(vistos))
    if tecla == ord("m"):
        silencio = not silencio

cap.release()
cv2.destroyAllWindows()