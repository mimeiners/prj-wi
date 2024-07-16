import cv2
import queue
import threading
from ultralytics import YOLO
from Tello_M import Tello
from datetime import datetime
import torch
import math
from time import sleep

'''
TO-DOs:
- Eingabe von Extern: Landingrequest; Notlandung
- Winkelauswertung in Funktion anpassen
- Klären wie das Bild ein/Ausgegeben wird!
'''
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

def bounding_box_center(x1,x2,y1,y2): # Centerpoint der Boundingbox

    # Berechne die Mitte der Bounding Box
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    
    return center_x, center_y

def process_angle(center_x, center_y): 
    image_width = 640
    image_height = 480

    # Berechnung des Punktes (center_x, center_y) relativ zur Bildmitte
    dx = center_x - image_width / 2
    dy = center_y - image_height / 2

    angle_radians = math.atan2(dy,dx)

    # Berechnung des Winkels im Bog
    angle_degrees = math.degrees(angle_radians)

    # Anpassen des Winkels, sodass 0° mittig rechts ist
    angle_degrees = (angle_degrees -37) % 360
    if angle_degrees > 180:
        angle_degrees -= 360

    # Winkel auf ganze Zahl runden
    angle_degrees = -round(angle_degrees)

    return angle_degrees            


def draw_grid(img, h1, h2, v1, v2): # Funktion zum Zeichnen des Rasters
    left_right
    grid_color = (0, 255, 0)  # Farbe des Rasters

    # Positionen für horizontale Linien berechnen
    h1_pos = int(h1 * img.shape[0])
    h2_pos = int(h2 * img.shape[0])

    # Positionen für vertikale Linien berechnen
    v1_pos = int(v1 * img.shape[1])
    v2_pos = int(v2 * img.shape[1])

    # Horizontale Linien zeichnen
    cv2.line(img, (0, h1_pos), (img.shape[1], h1_pos), grid_color, 1)
    cv2.line(img, (0, h2_pos), (img.shape[1], h2_pos), grid_color, 1)

    # Vertikale Linien zeichnen
    cv2.line(img, (v1_pos, 0), (v1_pos, img.shape[0]), grid_color, 1)
    cv2.line(img, (v2_pos, 0), (v2_pos, img.shape[0]), grid_color, 1)

    return img


def get_zone(center_x, center_y, h1, h2, v1, v2): # Abfrage wo sich etwas im Bild befindet, Orientierung am Raster
    image_width = 640
    image_height = 480

    # Positionen der horizontalen und vertikalen Linien berechnen
    h1_pos = int(h1 * image_height)
    h2_pos = int(h2 * image_height)
    v1_pos = int(v1 * image_width)
    v2_pos = int(v2 * image_width)

    # Zone bestimmen
    if center_x < v1_pos:
        if center_y < h1_pos:
           return "Oben Links"
        elif center_y < h2_pos:
            return "Mitte Links"
        else:
            return "Unten Links"
    elif center_x < v2_pos:
        if center_y < h1_pos:
            return "Mitte Oben"
        elif center_y < h2_pos:
            return "Mitte Mitte"
        else:
            return "Mitte Unten"
    else:
        if center_y < h1_pos:
            return "Oben Rechts"
        elif center_y < h2_pos:
            return "Mitte Rechts"
        else:
            return "Unten Rechts"

def get_instruction(zone, area): # Steuerungsbefehl für Drohne basierend auf get_zone
    
    speed_multplier = 10
    up_down = 0
    
    if zone == "Oben Links":
        left_right =  -speed_multplier
        forward_backward = -speed_multplier

        print("Droneinstruction: Go Forwards and Left")
        
    elif zone == "Mitte Links":
        left_right =  -speed_multplier
        forward_backward = 0

        print("Droneinstruction: Go Left")
        
    elif zone == "Unten Links":
        left_right =  -speed_multplier
        forward_backward = speed_multplier

        print("Droneinstruction: Go Backward and Left")
        
    elif zone == "Mitte Oben":
        left_right = 0
        forward_backward = -speed_multplier

        print("Droneinstruction: Go Forwards")
        
    elif zone == "Mitte Mitte":
        left_right =  0
        forward_backward = 0
        
        if area > 100000:
            up_down = -speed_multplier
            print("Droneinstruction: Increase height")
    
        elif area < 75000:
            up_down = speed_multplier
            print("Droneinstruction: Decrease height")
    
        else:
            up_down = 0
            print("Droneinstruction: Stay at height")  

        print("Droneinstruction: Stay")
        
    elif zone == "Mitte Unten":
        left_right =  0
        forward_backward = speed_multplier

        print("Droneinstruction: Go Backwards")
        
    elif zone == "Oben Rechts":
        left_right =  speed_multplier
        forward_backward = -speed_multplier

        print("Droneinstruction: Go Forwards and Right")
        
    elif zone == "Mitte Rechts":
        left_right =  speed_multplier
        forward_backward = 0

        print("Droneinstruction: Go Right")
        
    elif zone == "Unten Rechts":
        left_right =  speed_multplier
        forward_backward = speed_multplier

        print("Droneinstruction: Go Backwards and Right")
        
    else:
        print("Error: Unknown zone")
    
    return(left_right, -forward_backward, -up_down)


def get_landinginstruction(zone, area): # Instructions for Drone adjust later with commands
    
    speed_multplier = 10
    up_down = 0
    
    if zone == "Oben Links":
        left_right =  -speed_multplier
        forward_backward = -speed_multplier

        print("Droneinstruction_land: Go Forwards and Left")
        
    elif zone == "Mitte Links":
        left_right =  -speed_multplier
        forward_backward = 0

        print("Droneinstruction_land: Go Left")
        
    elif zone == "Unten Links":
        left_right =  -speed_multplier
        forward_backward = speed_multplier

        print("Droneinstruction_land: Go Backwars and Left")
        
    elif zone == "Mitte Oben":
        left_right = 0
        forward_backward = -speed_multplier

        print("Droneinstruction_land: Go Forwards")
        
    elif zone == "Mitte Mitte":
        left_right =  0
        forward_backward = 0

        if area < 100000:                 # Area needs to be adjusted!
            print("Droneinstruction_land: Decrease height")
            up_down = speed_multplier*3
    
        elif area > 100000:
            print("Droneinstruction_land: Stay at height")
            up_down = 0

        print("Droneinstruction_land: Stay")
        
    elif zone == "Mitte Unten":
        left_right =  0
        forward_backward = speed_multplier

        print("Droneinstruction_land: Go Backward")
        
    elif zone == "Oben Rechts":
        left_right =  speed_multplier
        forward_backward = -speed_multplier

        print("Droneinstruction_land: Go Forwards and Right")
        
    elif zone == "Mitte Rechts":
        left_right =  speed_multplier
        forward_backward = 0

        print("Droneinstruction_land: Go Right")
        
    elif zone == "Unten Rechts":
        left_right =  speed_multplier
        forward_backward = speed_multplier

        print("Droneinstruction_land: Go Backwards and Rights")
        
    else:
        print("Error: Unknown zone")
        
    
            
    return(left_right, -forward_backward, -up_down)

####################

# Variableninitialisierung
delta_t_text = 0
last_objectdetection = datetime.now() # Initialisierung, sonst gibt es einen Error
last_time_check = datetime.now() # Initialisierung, sonst gibt es einen Error
rotations = 0
center_x_landingpad = 0
center_y_landingpad = 0
angle_landingpad = 0
desired_object = "kicker"  # Initialisiertes Zielobjekt
near_landingpad = False
landpad_detected = False
ready = False
takeoff = False
detected_zone = ""  # wird sonst nicht initiiert
landingrequest = False # Soll später von Extern beschrieben werden
image_width = 640 # BilddiCapture
image_height = 480
left_right = 0
forward_backward = 0
up_down = 0
# Dynamische Begrenzungen Raster
h1 = 4/9        
h2 = 5/9        
v1 = 4/9        
v2 = 5/9

# Positionen der dynamischen Begrenzungen
pos_h1 = image_height * h1
pos_h2 = image_height * h2
pos_v1 = image_height * v1
pos_v2 = image_height * v2

cv2.imshow("test", cv2.imread("/home/jetson/prj-wi/files/Drohne/img/lenna.png"))
cv2.waitKey(1)
cv2.destroyAllWindows()

# Tello-Drohne initialisieren und verbinden
# ist an sich schon initiert
tello = Tello()
tello.connect()
tello.streamon()

# Fehlt noch im Jetson
tello.takeoff()  # Drohne starten
print("tello.takeoff ausgeführt")
takeoff = True
print("Starte Drohnenroutine zum Start")
tello.move_up(90)
tello.move_forward(35)
tello.move_right(20)
tello.rotate_clockwise(90)
tello.set_speed(10)
ready = True # Marker Betriebsmodus für Drohne
takeoff = False # Indikator abgeschlossener Takeoff


# YOLO-Modell laden
model = YOLO('best_28_05.pt')  # Pfad zum YOLOv8 Modell

# CPU nutzen falls GPU nicht verfügbar
if torch.cuda.is_available():
    model.to('cuda')
else:
    model.to('cpu') # Low Performance!

cap = VideoGrabber(tello.get_udp_video_address()+"?overrun_nonfatal=1")

cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
# cv2.setWindowProperty("Result", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) # Fullscreen

# Hauptschleife
while True:

    # Frame von der Tello-Drohne abrufen    
    img = cap.read_frame()              ###### Vielleicht einrücken? -> Erproben
    img = cv2.resize(img, (image_width, image_height))
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Konvertiere BGR zu RGB
    img = cv2.flip(img, 0)  # Vertikale Spiegelung
    imgContour = img
    
    battery_level = tello.get_battery()# Akkustand abfragen
    print('\x1b[6;30;42m' + f"Battery: {battery_level} | Temperature: {tello.get_temperature()}" + '\x1b[0m')
    
    if battery_level < 20:  # Landung anfordern bei zu wenig Akku
        print("Battery low! Please land the drone.")
        landingrequest = True
    
    # YOLO-Objekterkennung
    results = model(img, imgsz=image_width)  # Verwende 'imgsz' statt 'size'
    
    # Aktuelle Zeit in Zeitstempel schreiben
    current_time_check = datetime.now()
    area = 0
    area_desired = 0
    center_x = 0
    center_y = 0
    object_detected = False # Abfrage ob desired_object gefunden
    landpad_detected = False
    ########################################
    #landingrequest = ÜBERGABE VON EXTERN
    ########################################
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            area = (x2 - x1) * (y2 - y1)
            conf = box.conf[0]
            cls = box.cls[0]
            if conf > 0.5:  # Mindestkonfidenz für zuverlässige Erkennung
                label = f"{model.names[int(cls)]} {conf:.2f} Area: {(area):.1f}"
                
                if model.names[int(cls)] == desired_object: # Für das getrackte Objekt: Kicker normal, z.B. landingpad bei Landung
                    area_desired = area
                    object_detected = True
                    center_x, center_y = bounding_box_center(x1,x2,y1,y2)
                    cv2.rectangle(imgContour, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)  # Rote Farbe für desired_object
                    cv2.putText(imgContour, label, (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                
                else:   # Beschriftung für andere zu erkennende Objekte
                    cv2.rectangle(imgContour, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)  # Gelbe Farbe für andere Objekte
                    cv2.putText(imgContour, label, (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                
                if model.names[int(cls)] == "landingpad" and not landingrequest:    # Daten von objekt landingpad für spätere Ausrichtung
                    center_x_landingpad, center_y_landingpad = bounding_box_center(x1, x2, y1, y2)
                    angle_landingpad = process_angle(center_x_landingpad, center_y_landingpad)
                    landpad_detected = True


    # Verarbeitung der Objekte und deren Positionen

    if object_detected and not landingrequest and ready:
        print(f"{desired_object} wurde mit einer Konfidenz von über 0.5 erkannt! Keine Landung erwünscht")
        
        # Verarbeitung
        # center_x, center_y = bounding_box_center(x1, x2, y1, y2)
        detected_zone = get_zone(center_x, center_y, h1, h2, v1, v2)
        last_objectdetection = datetime.now()     
        left_right, forward_backward, up_down = get_instruction(detected_zone, area_desired)
        # Debug
        # text_for_box = f"Center of Object ({desired_object}): ({int(np.round(center_x))}, {int(np.round(center_y))}), Area: {(area_desired):.1f} px"
        text_for_box = f"Center of Object ({desired_object}): ({int(center_x)}, {int(center_y)}), Area: {(area_desired):.1f} px"
        cv2.putText(imgContour, text_for_box, (20, img.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.circle(imgContour, (int(center_x), int(center_y)), 3, (0, 0, 255), -1)
        cv2.putText(imgContour, f"Zone: {detected_zone}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    elif object_detected and landingrequest and ready:
        print(f"{desired_object} wurde mit einer Konfidenz von über 0.5 erkannt! Landung erwünscht")
        
        # Verarbeitung
        # center_x, center_y = bounding_box_center(x1, x2, y1, y2)
        detected_zone = get_zone(center_x, center_y, h1, h2, v1, v2)
        last_objectdetection = datetime.now()
        left_right, forward_backward, up_down = get_landinginstruction(detected_zone, area_desired)
        # Debug
        cv2.putText(imgContour, f"Zone: {detected_zone}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(imgContour, f"Center of Object ({desired_object}): ({int(center_x)}, {int(center_y)}), Area: {(area_desired):.1f} px", (20, img.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.circle(imgContour, (int(center_x), int(center_y)), 3, (0, 0, 255), -1)


    elif not object_detected:
        cv2.putText(imgContour, f"Center of Object ({desired_object}): Object not found!", (20, img.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        print(f"Objekt ({desired_object}) nicht im Bild oder die Konfidenz ist zu gering")

        if ((current_time_check - last_objectdetection).total_seconds() > 10) and not landingrequest:        # Drohne rotieren, wenn über 3 Sekunden kein Kicker erkannt wurde
            if rotations <= 12:
                print("Der Zeitstempel ist älter als 10 Sekunden. Rotiere Drohne")
                rotations += 1
                # tello.rotate_clockwise(90)
        
            elif rotations >= 12 and not landingrequest:     # Wenn Drohne zwei Rotationen durchgeführt hat ohne Kicker zu erkennen -> Landung anfordern
                rotations = 0
                landingrequest = True
                
        elif ready and not ((current_time_check - last_objectdetection).total_seconds() > 0.3):             # Drohne stoppen, wenn 0.3 Sekunden nichts erkannt
            print("Nichts gefunden unter 0.3 Sekunden, Drohne soll in der Luft stehenbleiben!")
            left_right = 0
            forward_backward = 0
            up_down = 0

    # Drehen der Drohne, wenn Drohne über Kicker
    if not landingrequest and ready and detected_zone == "Mitte Mitte" and (angle_landingpad > 15 or angle_landingpad < -15) and landpad_detected == True:
        angle = int(angle_landingpad)   # Winkel zu Integer ändern
        print("TESTAUSGABE: Drehung der Drohne:")
        print("Angle:", angle)
        
        ######### Evtl mit Zeitstemepl wenn über 2 Sekunden in "Mitte Mitte"!
        
        # Entscheidung für Drehrichtung
        if angle >= 0:
            print("Clockwise Rotation")
            #tello.rotate_clockwise(angle)          # Erst nutzen, wenn Winkel zuverlässig berechnet wird!
        elif angle < 0:
            print("Counterclockwise Rotation")
            #tello.rotate_counter_clockwise(-angle) # Erst nutzen, wenn Winkel zuverlässig berechnet wird!
            
    # Sonst: Normaler Flugbefehl für Tracking-Steuerung / Landeanflug
    else:
        tello.send_rc_control(int(left_right), int(forward_backward), int(up_down), 0)
    

    # Auswertung für Landeanflug
    if landingrequest and desired_object == "landingpad" and area_desired > 90000:
        print("Ich bin nah am Landepad, schalte um auf Pointer!")
        near_landingpad = True

    if landingrequest and desired_object == "pointer_kicker" and area_desired > 5000 and detected_zone == "Mitte Mitte":
        # tello.rotate_counter_clockwise(90)
        # tello.send_rc_control(10,10,0,0)
        # sleep(1)
        ready = False
        tello.land()
        tello.streamoff()
        break

    # Ändern des Grid zur Abfrage der Flugbefehle bei Landingrequest
    if landingrequest:
        h1 = 1/8  
        h2 = 2/8  # Rastermitte kleiner und nach oben
        v1 = 4/9  # Nicht =< 1 wählen!
        v2 = 5/9
        if near_landingpad:
            print("Changed tracked object to pointer_kicker")
            desired_object = "pointer_kicker"
        else:
            desired_object = "landingpad"


    #Bildausgabe
    text_leftcorner = f"Object being followed: {desired_object}; Landing-Request: {landingrequest}"
    cv2.putText(imgContour, text_leftcorner, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    delta_t_text = (current_time_check - last_time_check).total_seconds()
    text = f"Frametime: {delta_t_text * 1000:.2f} ms"
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
    cv2.putText(imgContour, text, ((img.shape[1] - text_size[0] - 20), 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    last_time_check = current_time_check # Für Generierung des Zeitunterschiedes von Frame zu Frame
    draw_grid(imgContour, h1, h2, v1, v2)
    cv2.imshow("Result", imgContour)

    # Abbruchbedingungen
                ## ES FEHLT DIE ABFRAGE FÜR NOTLANDUNG!##
    if cv2.waitKey(1) & 0xFF == ord('q'):    
        landingrequest = True

    if cv2.waitKey(1) & 0xFF == ord('e'):    
        try:
            tello.land()
        except:
            print("landing command failed")
        break


tello.streamoff()
cv2.destroyAllWindows()
