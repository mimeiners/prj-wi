"""
_author_ = "Ben Mariem, Achraf", "Haberkorn, Lukas"
_contact_ = ""
_date_ = "2023/01/10"
_deprecated_ = false
_status_ = "WIP"
_version_ = "1.1.6"

Dieses Skript läuft auf einer Maschine und lässt die Drohne nach einem bestimmten Objekt ausrichten. "Q" landet die Drohne sofort. 
pyPID.py und yolov8n.pt müssen im gleichen Verzeichnis vorhanden sein.
Eine Suchfunktion bei fehlendem Ziel ist noch nicht getestet. Das Hinfliegen zu einem Ziel ist in Arbeit.
"""

""" Zukünftige mögliche Features:
- Die Search-Funktion muss noch weiter ausgebaut werden [Lukas]
- Die Ausrichtung muss noch vor/zurück berücksichtigen [Achraf]
- evtl Anpassung einzelner Parameter (framecenter, rc_scale, are_we_close)
- Smarte Suchfunktion (an welchem Rand war das Objekt zuletzt)
- Anleitung für Anpassung von Parametern
- weitere Ausgaben über print()
"""

from djitellopy import Tello
from ultralytics import YOLO
from pynput import keyboard
import cv2
import time
import pyPID as PID
import numpy as np


# - - - PARAMETER, pid_yaw kann noch weiter optimiert werden - - -
model = YOLO("yolov8n.pt")
pid_yaw = PID.pyPID(0.5, 60, 0.75, 1, 0.01) #PID-Parameter Drehung
pid_dtof = PID.pyPID(0.1, 110, 1,0,0)       #PID-Parameter Höhe
framecenterx = 700     #Zielkoordinaten im Bild (Sollwert)
framecentery = 400
rc_scale_dtof = 0.5     #Vorfaktor des Regelwerts der an rc_control() gegeben wird          
rc_scale_yaw = 0.5
target_id = 0           #YOLO IDs: 0: person, 67: cell phone, 39: bottle
enable_search_mode = True #Ob die Drohne ohne Zielobjekt in den Suchmodus wechselt
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

me = Tello()
me.connect()
me.streamon()
Tello.FPS_30
#me.set_video_direction(Tello.CAMERA_DOWNWARD)
me.speed = 50 #beeinflusst nur Tastatursteuerung, nicht PID

# Create an OpenCV window to display the live stream
#cv2.namedWindow('Tello Stream', cv2.WINDOW_NORMAL)

# Define the codec and create a VideoWriter object to save the stream as a video file
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('tello_stream.mp4', fourcc, 10.0, (2*framecenterx, 2*framecentery))


difference_list = []
emergency_landing = False
search_active = False


def on_key_release(key):
    global emergency_landing
    try:
        # Check for 'q' keypress to initiate landing
        if key.char == 'q':
            #cv2.destroyAllWindows()
            print("Emergency landing initiated.")
            me.end()
            emergency_landing = True
    except AttributeError:
        pass


# Funktion beendet Pendeln von yaw
def are_we_close(new):
    global difference_list
    difference_list.append(new)
    if len(difference_list) < 20:
        print("a")
        return new
    elif abs(np.mean(difference_list)) < 15:
        difference_list.pop(0)
        print("b")
        return 0
    else:
        difference_list.pop(0)
        print("c")
        return new


# Ohne Zielobjekt sucht die Drohne
def search(search_active):
    global difference_list
    difference_list = []
    yaw_inc = 0 # Wird bei aktiviertem Suchmodus überschrieben
    dtof_inc = 0
    if enable_search_mode == True:
        if search_active == False: # nur bei Beginn einer Suche
            global search_yaw_start
            search_yaw_start = me.get_yaw() # Startausrichtung speichern
            search_active = True # dann passiert diese if nur einmal
        else:
            if search_yaw_start <= me.get_yaw(): # irgendwann ist YAW wieder kleiner, sorgt für randomness
                print("hier passiert noch nix")
        yaw_inc = 50
        dtof_inc = 0 # Die Drohne würde immer weiter aufsteigen wenn man einen positiven Wert eingibt
    return yaw_inc, dtof_inc


listener = keyboard.Listener(on_release=on_key_release)
listener.start()
print("Temp:", me.get_temperature(),"°C","Charge:", me.get_battery(),"%")
me.takeoff()
try:
    while not emergency_landing:
        # Empfangen des Bildes vom Videostreamwe
        print("Temp:", me.get_temperature(),"°C","Charge:", me.get_battery(),"%")
        img = me.get_frame_read().frame
        img = cv2.resize(img, (2*framecenterx, 2*framecentery))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        #cv2.imshow('Tello Stream', img) # show in Video stream
        

        result = model.predict(source=img, show=True, conf=0.5)
        #out.write(img) # save frame to video
        # Falls das Zielobjekt erkannt wurde, mit PID darauf ausrichten
        if target_id in result[0].boxes.cls and me.get_flight_time() != 0:
            n = 0
            for i in result[0].boxes.cls:
                if i == target_id:
                    break
                n += 1
            boxcenterx = int(result[0].boxes.xywh[n][0])
            boxcentery = int(result[0].boxes.xywh[n][1])
            # if result[0].boxes.conf[n] >= 0.6:
            yaw_inc = - pid_yaw.run(framecenterx, boxcenterx)
            #qyaw_inc = are_we_close(yaw_inc) #if close to center for long time, do 0
            dtof_inc = pid_dtof.run(framecentery, boxcentery)
        elif me.get_flight_time() != 0:
            yaw_inc, dtof_inc = search(search_active)
            #me.send_rc_control(0,0,0,0)
        me.send_rc_control(0,0,int(dtof_inc*rc_scale_dtof),int(yaw_inc*rc_scale_yaw))
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    print("Program terminated.")
    out.release()   # beende Video
    cv2.destroyAllWindows()
    me.end()
    listener.stop()
    listener.join()
