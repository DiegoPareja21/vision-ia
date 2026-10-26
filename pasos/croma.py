import cv2
import numpy as np
from ultralytics import YOLO

# 🆕 1) Modelo "small" en vez de "nano": más preciso, y tu GPU lo aguanta
model = YOLO("yolo11s-seg.pt")

cap = cv2.VideoCapture(0)

COLOR_CROMA = (0, 255, 0)
usar_croma = True

while True:
    ok, frame = cap.read()
    if not ok:
        print("No pude leer la cámara")
        break

    #  2) retina_masks=True → máscaras en ALTA resolución (bordes más finos)
    #  3) conf=0.15 → acepta objetos aunque YOLO esté menos seguro
    r = model(frame, conf=0.15, retina_masks=True, verbose=False)[0]

    mascara = np.zeros(frame.shape[:2], dtype=np.uint8)
    if r.masks is not None:
        for contorno in r.masks.xy:
            cv2.fillPoly(mascara, [contorno.astype(np.int32)], 255)

    # 4) Arreglar los bordes de la máscara
    # dilate: "engorda" la máscara unos píxeles para no cortar los bordes del objeto
    mascara = cv2.dilate(mascara, np.ones((15, 15), np.uint8))
    # GaussianBlur: difumina el borde para que la transición sea suave
    alpha = cv2.GaussianBlur(mascara, (21, 21), 0).astype(np.float32) / 255.0
    alpha = alpha[:, :, None]

    if usar_croma:
        fondo = np.full_like(frame, COLOR_CROMA)
        # Mezcla suave: 1 = 100% cámara, 0 = 100% croma, 0.5 = mitad y mitad
        imagen = (frame * alpha + fondo * (1 - alpha)).astype(np.uint8)
    else:
        imagen = frame

    imagen = r.plot(img=imagen, masks=False)

    cv2.imshow("Croma IA", imagen)
    cv2.imshow("Mascara", mascara)

    tecla = cv2.waitKey(1) & 0xFF
    if tecla == ord("q"):
        break
    if tecla == ord("c"):
        usar_croma = not usar_croma

cap.release()
cv2.destroyAllWindows()