
import cv2
import numpy as np
from ultralytics import YOLO
from datetime import datetime
import torch
import math
import threading


class Flugsteuerung():
      
    def __init__(self, VideoManager) -> None:
        # Drone
        self.drone = None
        self.battery_level = None
        self.temprature = None
        self.tackoff_xyz = {"up": 90, "forward":35, "right":20, "rotate":90} # initial flight input after start
        
        # run Variablen
        self.do_run = False
        self.last_objectdetection = datetime.now() # Initialisierung, sonst gibt es einen Error
        self.last_time_check = datetime.now() # Initialisierung, sonst gibt es einen Error
        self.landingrequest = False # Soll später von Extern beschrieben werden
        self.detected_zone = ""  # wird sonst nicht initiiert
        self.rotations = 0
        self.desired_object = "kicker"  # Initialisiertes Zielobjekt
        self.near_landingpad = False
        self.landpad_detected = False
        self.emergency_land = False
        
        # YOLO
        self.model = YOLO('best.pt') # Pfad zum YOLOv8 Modell
        # CPU nutzen falls GPU nicht verfügbar
        if torch.cuda.is_available():
            self.model.to('cuda')
        else:
            self.model.to('cpu') # Low Performance!
        
        # Video
        self.VideoManager = VideoManager
        self.image_width = self.VideoManager.frame_width_x # Bilddimensionen
        self.image_height = self.VideoManager.frame_width_y
        self.img = None
        self.img_copy = None
        self.delta_t_text = 0
        
        # Dynamische Begrenzungen Raster
        self.h1 = 4/9
        self.h2 = 5/9
        self.v1 = 4/9
        self.v2 = 5/9

        # Positionen der dynamischen Begrenzungen
        self.pos_h1 = self.image_height * self.h1
        self.pos_h2 = self.image_height * self.h2
        self.pos_v1 = self.image_height * self.v1
        self.pos_v2 = self.image_height * self.v2

        # Kommunikation
        self.com = {"foul": False,
                    "second_ball": False,
                    "human_intervention": False,
                    "other": False}

    def set_drone(self, drone):
        self.drone = drone
        self.battery_level = self.drone.get_battery()
        self.temprature = self.drone.get_temperature()
        print(f"Flugcontroller initilized\nBattery:{self.battery_level} | Temperature:{self.temprature}")

    def bounding_box_center(self,x1,x2,y1,y2) -> tuple: # Centerpoint der Boundingbox
        # Berechne die Mitte der Bounding Box
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        return center_x, center_y

    def process_angle(self, center_x, center_y) -> int: 
        # Berechnung des Punktes (center_x, center_y) relativ zur Bildmitte
        dx = center_x - self.image_width / 2
        dy = center_y - self.image_height / 2

        # Berechnung des Winkels im Bogenmaß
        angle_radians = math.atan2(dy, dx)

        # Umrechnung des Winkels in Grad
        angle_degrees = math.degrees(angle_radians)

        # Anpassen des Winkels, sodass 0° mittig rechts ist
        angle_degrees = (angle_degrees -37) % 360
        if angle_degrees > 180:
            angle_degrees -= 360

        # Winkel auf ganze Zahl runden
        angle_degrees = -round(angle_degrees)

        return angle_degrees


    def draw_grid(self) -> None: # Funktion zum Zeichnen des Rasters
        
        grid_color = (0, 255, 0)  # Farbe des Rasters

        # Positionen für horizontale Linien berechnen
        h1_pos = int(self.h1 * self.img.shape[0])
        h2_pos = int(self.h2 * self.img.shape[0])

        # Positionen für vertikale Linien berechnen
        v1_pos = int(self.v1 * self.img.shape[1])
        v2_pos = int(self.v2 * self.img.shape[1])

        # Horizontale Linien zeichnen
        cv2.line(self.img_copy, (0, h1_pos), (self.img_copy.shape[1], h1_pos), grid_color, 1)
        cv2.line(self.img_copy, (0, h2_pos), (self.img_copy.shape[1], h2_pos), grid_color, 1)

        # Vertikale Linien zeichnen
        cv2.line(self.img_copy, (v1_pos, 0), (v1_pos, self.img_copy.shape[0]), grid_color, 1)
        cv2.line(self.img_copy, (v2_pos, 0), (v2_pos, self.img_copy.shape[0]), grid_color, 1)

    def get_zone(self, center_x, center_y) -> str: # Abfrage wo sich etwas im Bild befindet, Orientierung am Raster

        # Positionen der horizontalen und vertikalen Linien berechnen
        self.h1_pos = int(self.h1 * self.image_height)
        self.h2_pos = int(self.h2 * self.image_height)
        self.v1_pos = int(self.v1 * self.image_width)
        self.v2_pos = int(self.v2 * self.image_width)

        # Zone bestimmen
        if center_x < self.v1_pos:
            if center_y < self.h1_pos:
                return "Oben Links"
            elif center_y < self.h2_pos:
                return "Mitte Links"
            else:
                return "Unten Links"
        elif center_x < self.v2_pos:
            if center_y < self.h1_pos:
                return "Mitte Oben"
            elif center_y < self.h2_pos:
                return "Mitte Mitte"
            else:
                return "Mitte Unten"
        else:
            if center_y < self.h1_pos:
                return "Oben Rechts"
            elif center_y < self.h2_pos:
                return "Mitte Rechts"
            else:
                return "Unten Rechts"

    def get_instruction(self, zone, area): # Steuerungsbefehl für Drohne basierend auf get_zone

        up_down = 0
        
        if zone == "Oben Links":
            left_right =  -self.speed_multplier
            forward_backward = -self.speed_multplier

            print("Droneinstruction: Go Forwards and Left")
            
        elif zone == "Mitte Links":
            left_right =  -self.speed_multplier
            forward_backward = 0

            print("Droneinstruction: Go Left")
            
        elif zone == "Unten Links":
            left_right =  -self.speed_multplier
            forward_backward = self.speed_multplier

            print("Droneinstruction: Go Backward and Left")
            
        elif zone == "Mitte Oben":
            left_right = 0
            forward_backward = -self.speed_multplier

            print("Droneinstruction: Go Forwards")
            
        elif zone == "Mitte Mitte":
            left_right =  0
            forward_backward = 0
            
            if area > 100000:
                up_down = -self.speed_multplier
                print("Droneinstruction: Increase height")
        
            elif area < 75000:
                up_down = self.speed_multplier
                print("Droneinstruction: Decrease height")
        
            else:
                up_down = 0
                print("Droneinstruction: Stay at height")  

            print("Droneinstruction: Stay")
            
        elif zone == "Mitte Unten":
            left_right =  0
            forward_backward = self.speed_multplier

            print("Droneinstruction: Go Backwards")
            
        elif zone == "Oben Rechts":
            left_right =  self.speed_multplier
            forward_backward = -self.speed_multplier

            print("Droneinstruction: Go Forwards and Right")
            
        elif zone == "Mitte Rechts":
            left_right =  self.speed_multplier
            forward_backward = 0

            print("Droneinstruction: Go Right")
            
        elif zone == "Unten Rechts":
            left_right =  self.speed_multplier
            forward_backward = self.speed_multplier

            print("Droneinstruction: Go Backwards and Right")
            
        else:
            print("Error: Unknown zone")
        
        return(left_right, forward_backward, up_down)

    def get_landinginstruction(self, zone, area): # Instructions for Drone adjust later with commands

        up_down = 0
        
        if zone == "Oben Links":
            left_right =  -self.speed_multplier
            forward_backward = -self.speed_multplier

            print("Droneinstruction_land: Go Forwards and Left")
            
        elif zone == "Mitte Links":
            left_right =  -self.speed_multplier
            forward_backward = 0

            print("Droneinstruction_land: Go Left")
            
        elif zone == "Unten Links":
            left_right =  -self.speed_multplier
            forward_backward = self.speed_multplier

            print("Droneinstruction_land: Go Backwars and Left")
            
        elif zone == "Mitte Oben":
            left_right = 0
            forward_backward = -self.speed_multplier

            print("Droneinstruction_land: Go Forwards")
            
        elif zone == "Mitte Mitte":
            left_right =  0
            forward_backward = 0

            if area < 100000:                 # Area needs to be adjusted!
                print("Droneinstruction_land: Decrease height")
                up_down = self.speed_multplier*2
        
            elif area > 100000:
                print("Droneinstruction_land: Stay at height")
                up_down = 0

            print("Droneinstruction_land: Stay")
            
        elif zone == "Mitte Unten":
            left_right =  0
            forward_backward = self.speed_multplier

            print("Droneinstruction_land: Go Backward")
            
        elif zone == "Oben Rechts":
            left_right =  self.speed_multplier
            forward_backward = -self.speed_multplier

            print("Droneinstruction_land: Go Forwards and Right")
            
        elif zone == "Mitte Rechts":
            left_right =  self.speed_multplier
            forward_backward = 0

            print("Droneinstruction_land: Go Right")
            
        elif zone == "Unten Rechts":
            left_right =  self.speed_multplier
            forward_backward = self.speed_multplier

            print("Droneinstruction_land: Go Backwards and Rights")
            
        else:
            print("Error: Unknown zone")
            
        
                
        return(left_right, -forward_backward, -up_down)

    def start(self):
        self.drone.takeoff()  # Drohne starten
        print("tello.takeoff ausgeführt")
        print("Starte Drohnenroutine zum Start")
        self.drone.move_up(self.tackoff_xyz["up"])
        self.drone.move_forward(self.tackoff_xyz["forward"])
        self.drone.move_right(self.tackoff_xyz["right"])
        self.drone.rotate_clockwise(self.tackoff_xyz["rotate"])
        self.drone.set_speed(10)

        self.do_run = True # Marker Betriebsmodus für Drohne
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):

        left_right = 0  # default assign
        forward_backward = 0
        up_down = 0

        while self.do_run:

            # Frame von der Tello-Drohne abrufen    
            self.img = self.VideoManager.get_img()              ###### Vielleicht einrücken? -> Erproben
            self.img_copy = self.img#.copy()
            
            self.battery_level = self.drone.get_battery()# Akkustand abfragen
            self.temprature = self.drone.get_temperature()  # Temperatur abfragen
            print("Batterie bei", self.battery_level)
            
            if self.battery_level < 15:  # Landung anfordern bei zu wenig Akku
                print("Battery low! Please land the drone.")
                self.landingrequest = True
            
            # YOLO-Objekterkennung
            results = self.model(self.img, imgsz=self.image_width)  # Verwende 'imgsz' statt 'size'
            
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
                        label = f"{self.model.names[int(cls)]} {conf:.2f} Area: {(area):.1f}"
                        
                        if self.model.names[int(cls)] == self.desired_object: # Für das getrackte Objekt: Kicker normal, z.B. landingpad bei Landung
                            area_desired = area
                            object_detected = True
                            cv2.rectangle(self.img_copy, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)  # Rote Farbe für desired_object
                            cv2.putText(self.img_copy, label, (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                        
                        else:   # Beschriftung für andere zu erkennende Objekte
                            cv2.rectangle(self.img_copy, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)  # Gelbe Farbe für andere Objekte
                            cv2.putText(self.img_copy, label, (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                        
                        if self.model.names[int(cls)] == "landingpad" and not self.landingrequest:    # Daten von objekt landingpad für spätere Ausrichtung
                            angle_landingpad = self.process_angle(self.bounding_box_center(x1, x2, y1, y2))
                            landpad_detected = True


            # Verarbeitung der Objekte und deren Positionen

            if object_detected and not self.landingrequest and self.do_run:
                print(f"{self.desired_object} wurde mit einer Konfidenz von über 0.5 erkannt! Keine Landung erwünscht")
                
                # Verarbeitung
                center_x, center_y = self.bounding_box_center(x1, x2, y1, y2)
                self.detected_zone = self.get_zone(center_x, center_y)
                self.last_objectdetection = datetime.now()     
                left_right, forward_backward, up_down = self.get_instruction(self.detected_zone, area_desired)
                # Debug
                cv2.putText(self.img_copy, f"Center of Object ({self.desired_object}): ({int(np.round(center_x))}, {int(np.round(center_y))}), Area: {(area_desired):.1f} px", (20, self.img.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                cv2.circle(self.img_copy, (int(center_x), int(center_y)), 3, (0, 0, 255), -1)
                cv2.putText(self.img_copy, f"Zone: {self.detected_zone}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            elif object_detected and self.landingrequest and self.do_run:
                print(f"{self.desired_object} wurde mit einer Konfidenz von über 0.5 erkannt! Landung erwünscht")
                
                # Verarbeitung
                center_x, center_y = self.bounding_box_center(x1, x2, y1, y2)
                self.detected_zone = self.get_zone(center_x, center_y)
                self.last_objectdetection = datetime.now()
                left_right, forward_backward, up_down = self.get_landinginstruction(self.detected_zone, area_desired)
                # Debug
                cv2.putText(self.img_copy, f"Zone: {self.detected_zone}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                cv2.putText(self.img_copy, f"Center of Object ({self.desired_object}): ({int(np.round(center_x))}, {int(np.round(center_y))}), Area: {(area_desired):.1f} px", (20, self.img.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                cv2.circle(self.img_copy, (int(center_x), int(center_y)), 3, (0, 0, 255), -1)
                

            elif not object_detected:
                cv2.putText(self.img_copy, f"Center of Object ({self.desired_object}): Object not found!", (20, self.img.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                print(f"Objekt ({self.desired_object}) nicht im Bild oder die Konfidenz ist zu gering")

                if ((current_time_check - self.last_objectdetection).total_seconds() > 3) and not self.landingrequest:        # Drohne rotieren, wenn über 3 Sekunden kein Kicker erkannt wurde
                    if self.rotations <= 8:
                        print("Der Zeitstempel ist älter als 3 Sekunden. Rotiere Drohne")
                        self.rotations += 1
                        self.drone.rotate_clockwise(90)
                
                    elif self.rotations >= 8 and not self.landingrequest:     # Wenn Drohne zwei Rotationen durchgeführt hat ohne Kicker zu erkennen -> Landung anfordern
                        self.rotations = 0
                        self.landingrequest = True
                        
                elif self.do_run and not ((current_time_check - self.last_objectdetection).total_seconds() > 0.3):             # Drohne stoppen, wenn 0.3 Sekunden nichts erkannt
                    print("Nichts gefunden unter 0.3 Sekunden, Drohne soll in der Luft stehenbleiben!")
                    left_right = 0
                    forward_backward = 0
                    up_down = 0

            # Drehen der Drohne, wenn Drohne über Kicker
            if not self.landingrequest and self.do_run and self.detected_zone == "Mitte Mitte" and (angle_landingpad > 15 or angle_landingpad < -15) and landpad_detected == True:
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
                self.drone.send_rc_control(int(left_right), int(forward_backward), int(up_down), 0)
            

            # Auswertung für Landeanflug
            if self.landingrequest and self.desired_object == "landingpad" and area_desired > 100000:
                print("Ich bin nah am Landepad, schalte um auf Pointer!")
                near_landingpad = True

            if self.landingrequest and self.desired_object == "pointer_kicker" and area_desired > 6000 and self.detected_zone == "Mitte Mitte":
                self.drone.rotate_counter_clockwise(90)
                self.drone.land()
                self.do_run = False
                break

            # Ändern des Grid zur Abfrage der Flugbefehle bei Landingrequest
            if self.landingrequest:
                self.h1 = 2/9  
                self.h2 = 3/9  # Rastermitte kleiner und nach oben
                self.v1 = 4/9  # Nicht =< 1 wählen!
                self.v2 = 5/9
                if near_landingpad:
                    print("Changed tracked object to pointer_kicker")
                    self.desired_object = "pointer_kicker"
                else:
                    self.desired_object = "landingpad"


            #Bildausgabe
            text_leftcorner = f"Object being followed: {self.desired_object}; Landing-Request: {self.landingrequest}"
            cv2.putText(self.img_copy, text_leftcorner, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            delta_t_text = (current_time_check - self.last_time_check).total_seconds()
            text = f"Frametime: {delta_t_text * 1000:.2f} ms"
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            cv2.putText(self.img_copy, text, ((self.img.shape[1] - text_size[0] - 20), 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            self.last_time_check = current_time_check # Für Generierung des Zeitunterschiedes von Frame zu Frame
            self.draw_grid(self.img_copy)
            cv2.imshow("Result", self.img_copy)


            # Abbruchbedingungen
                        ## ES FEHLT DIE ABFRAGE FÜR NOTLANDUNG!##
            if (cv2.waitKey(1) & 0xFF == ord('q')) or self.emergency_land:    
                self.drone.land()
                self.do_run = False
                self.drone.streamoff()
                cv2.destroyAllWindows()
                break