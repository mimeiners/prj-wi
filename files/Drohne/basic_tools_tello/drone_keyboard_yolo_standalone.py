import cv2
import queue
import threading
from ultralytics import YOLO
from Tello_M import Tello
import torch
import KeyPressModule as kp
from time import sleep
"""
Flugsteuerung:

    links/rechts/vorwärts/rückwärts -> "Pfeiltasten"
    hoch -> "w"
    runter -> "s"
    rechts-/linksdrehen -> "d"/"a"

    starten -> "q"
    landen -> "e"
    Programm beenden -> "ESCAPE"
"""
###### VideoCapture ######

class VideoGrabber:
    def __init__(self, soucrce) -> None:
        self.cap = cv2.VideoCapture(soucrce)
        self.q = queue.Queue()
        self.t = threading.Thread(target=self._reader)
        self.t.daemon = True
        self.t.start()

    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read_frame(self):
        return self.q.get()
        
#### Funktionen ####
def getKeyboardInput():
    lr,fb,ud,yv = 0,0,0,0
    speed = 50
    esc = False
    global save
    global landed

    if kp.getKey("LEFT"): lr    = -speed
    elif kp.getKey("RIGHT"): lr = speed 

    if kp.getKey("UP"): fb     = speed
    elif kp.getKey("DOWN"): fb = -speed 

    if kp.getKey("s"): ud   = -speed
    elif kp.getKey("w"): ud = speed

    if kp.getKey("d"): yv   =   speed
    elif kp.getKey("a"): yv =   -speed

    if kp.getKey("e"):
        if not landed:
            tello.land()
            landed = True

    if kp.getKey("q"):
        if landed:
            tello.takeoff()
            landed = False
            sleep(3)

    if kp.getKey("ESCAPE"):
        esc = True

    return[lr,fb,ud,yv,esc]
####################
# CV init
cv2.imshow("test", cv2.imread("/home/jetson/prj-wi/files/Drohne/img/lenna.png"))
cv2.waitKey(1)
cv2.destroyAllWindows()

# Tello-Drohne initialisieren und verbinden
kp.init()
tello = Tello()
tello.connect()
tello.streamon()
# Variableninitialisierung
landed = True
running = True
image_width = 640 # Bilddimensionen
image_height = 480
battery = tello.get_battery()
temperature = tello.get_temperature()

# YOLO-Modell laden
model = YOLO('best.pt')  # Pfad zum YOLOv8 Modell

# CPU nutzen falls GPU nicht verfügbar
if torch.cuda.is_available():
    model.to('cuda')
else:
    model.to('cpu') # Low Performance!

# cap des Streams 
cap = VideoGrabber(tello.get_udp_video_address()+"?overrun_nonfatal=1")
cv2.namedWindow("Result", cv2.WINDOW_NORMAL)

# Hauptschleife
while running:
    direc = getKeyboardInput()
    
    # stop programm
    if direc[4]:
        running = False
        if not landed:
            tello.land()
            landed = True
        break

    # rc controll
    tello.send_rc_control(direc[0],direc[1],direc[2],direc[3])

    # Frame von der Tello-Drohne abrufen    
    img = cap.read_frame()     
    img = cv2.resize(img, (image_width, image_height))
    img = cv2.flip(img, 0)  # Vertikale Spiegelung
    imgContour = img
    
    if battery < 20:  # Landung anfordern bei zu wenig Akku
        print("Battery low! Please land the drone.")
        cv2.putText(imgContour,"Battery low! Please land the drone.", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    # YOLO-Objekterkennung
    results = model(img, imgsz=image_width)  # Verwende 'imgsz' statt 'size'
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            area = (x2 - x1) * (y2 - y1)
            conf = box.conf[0]
            cls = box.cls[0]
            if conf > 0.5:  # Mindestkonfidenz für zuverlässige Erkennung
                label = f"{model.names[int(cls)]} {conf:.2f} Area: {(area):.1f}"
                cv2.rectangle(img,(int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 255), 2)
                cv2.putText(imgContour, label, (int(x1),int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
    #Bildausgabe
    cv2.imshow("Result", imgContour)

cv2.destroyAllWindows()
