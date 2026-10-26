import cv2
from ultralytics import YOLO

# YOLO entrenado con Open Images V7 (600 objetos). Se descarga solo la primera vez.
# "m" = medium: más preciso que nano/small, y tu GPU lo mueve bien.
model = YOLO("yolov8m-oiv7.pt")

# Los objetos que nos interesan (escritos tal como los nombra el dataset)
QUIERO = ["Pen", "Tablet computer", "Mobile phone"]

# Buscamos el número de cada clase dentro de las 600
ids = [i for i, nombre in model.names.items() if nombre in QUIERO]
print("Clases elegidas:", {i: model.names[i] for i in ids})

solo_mis_objetos = True   # Con la tecla 't' cambias entre "mis 3 objetos" y "los 600"

cap = cv2.VideoCapture(0)

while True:
    ok, frame = cap.read()
    if not ok:
        print("No pude leer la cámara")
        break

    filtro = ids if solo_mis_objetos else None
    r = model(frame, classes=filtro, conf=0.2, verbose=False)[0]

    imagen = r.plot()
    modo = "Mis objetos" if solo_mis_objetos else "TODOS (600)"
    cv2.putText(imagen, f"Modo: {modo}  [t] cambiar  [q] salir", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.imshow("Detector 600 objetos", imagen)

    tecla = cv2.waitKey(1) & 0xFF
    if tecla == ord("q"):
        break
    if tecla == ord("t"):
        solo_mis_objetos = not solo_mis_objetos

cap.release()
cv2.destroyAllWindows()