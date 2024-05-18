from ultralytics import YOLO
import cv2
import math
import torch

# Überprüfen, ob CUDA verfügbar ist und das Gerät einstellen
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Webcam starten
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Setze die Breite der Webcam-Auflösung
cap.set(4, 480)  # Setze die Höhe der Webcam-Auflösung

# Modell laden, aus /unix/bigdata/belehmann/PRJ_Flight_of_AI/YOLOv8/Tests_AuVAReS
model = YOLO("best.pt")
model.to(device)

# Objektklassen
classNames = model.names

while True:
    success, img = cap.read()
    if not success:
        print("Fehler beim Lesen des Bildes von der Webcam")
        break

    results = model.track(img, stream=True, conf=0.5)

    # Koordinaten und Boxen verarbeiten
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # Begrenzungsrahmen-Koordinaten
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Konvertiere in Ganzzahlen

            # Begrenzungsrahmen zeichnen
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # Konfidenzwert
            confidence = math.ceil((box.conf[0] * 100)) / 100
            print("Confidence --->", confidence)

            # Klassenname
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            # Objektdetails auf das Bild schreiben
            org = (x1, y1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, f'{classNames[cls]} {confidence}', org, font, fontScale, color, thickness)
            
    # Bild anzeigen
    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):  # Drücke 'q', um das Programm zu beenden
        break

# Ressourcen freigeben
cap.release()
cv2.destroyAllWindows()
