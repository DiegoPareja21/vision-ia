import cv2
import os
import time

CARPETA = "dataset/imagenes"
os.makedirs(CARPETA, exist_ok=True)   # Crea la carpeta si no existe

cap = cv2.VideoCapture(0)

# Continuamos la numeración si ya hay fotos guardadas
contador = len(os.listdir(CARPETA))
modo_auto = False
ultima_foto = 0

def guardar(frame):
    global contador
    nombre = os.path.join(CARPETA, f"img_{contador:04d}.jpg")
    cv2.imwrite(nombre, frame)
    contador += 1

while True:
    ok, frame = cap.read()
    if not ok:
        print("No pude leer la cámara")
        break

    # Modo automático: guarda una foto cada 0.5 segundos
    if modo_auto and time.time() - ultima_foto > 0.5:
        guardar(frame)
        ultima_foto = time.time()

    # Dibujamos la info en una COPIA, no en el frame original
    vista = frame.copy()
    estado = "AUTO ON" if modo_auto else "manual"
    cv2.putText(vista, f"Fotos: {contador}  ({estado})", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(vista, "[espacio] foto  [a] auto  [q] salir", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.imshow("Captura de dataset", vista)

    tecla = cv2.waitKey(1) & 0xFF
    if tecla == ord("q"):
        break
    if tecla == ord(" "):
        guardar(frame)
    if tecla == ord("a"):
        modo_auto = not modo_auto

cap.release()
cv2.destroyAllWindows()