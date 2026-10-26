import cv2  # OpenCV

# Abrimos la cámara número 0 (la webcam por defecto)
cap = cv2.VideoCapture(0)

while True:
    ok, frame = cap.read()   # Leemos un frame
    print(frame.shape) 
    if not ok:
        print("No pude leer la cámara")
        break
        print(frame.shape) 
    # Le escribimos un texto encima al frame
    cv2.putText(frame, "Mi primera vision IA", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Webcam", frame)   # Mostramos el frame en una ventana

    # Si apretas la tecla 'q', salimos
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
