"""
This is meant to be used as an imported modules file for the main file 
and is basically listing the auxilary functions (literally) the AuVAReS posesses.
"""
__author__ = "Julian Höpe"
__version__ = "1.0.7"
__status__ = " WIP"
__date__ = "2024-05-29"

'''
NOTE:
videoPlayback: 
    Last statement "cv2.destroyAllWindows() might cause an issue with the video stream received from the drone"

network_function:
    Error handling has to be implemented, which ensures that the connection is closed correctly in case of an error
'''

'''
TODO: fill all  notify_... functions with routines
TODO: fill function main_task (AI)
TODO: gameover_routines - Drone landing
'''

'''
Changes:

1.0.7_ (2024-05-29) / jHöpe, fKatenkamp
    - removed class VideoHandler
    - updated objecthandling of VideoHandler object

1.0.6: (2024-05-27) / Samland
    - added defs for object detections
    - added YOLO import and the loop for object detections in main_task/ while connection_established.is_set()

1.0.5: (2024-05-25) / JH
    - added method clearFile to class VideoHandler
    - implemented showing messages on screens, when drone is too hot or battery too low when initializing (function: notify_drone_powered)
    - updated function notify_gameover

1.0.4: (2024-05-17) / JH
    - renamed function notify_drone_connect to notify_drone_powered
    - added function notify_drone_connected
    - updated function notify_drone_powered
    - added methods get_img, set_drone, inc_FrameNumber to class VideoHandler
    - updated method videoRecord of class VideoHandler
    - updated function notify_newgoal
    - updated function notify_foul
    - updated function notify_gameover
    - updated function network_connection
    - updated function main_task
    - updated function notify_gamestart
    - updated function notify_start_permission


1.0.3: (2024-05-04) / JH
    - added class VideoHandler  (incomplete)
    - moved function videoPlayback into class VideoHandler
    - added function notify_drone_connect   (incomplete)
    - added function notify_start_permission    (incomplete)
    - added function notify_gamestart (complete)  
    - added function please_resume  (complete)
    - added function please_wait    (complete)
    - added function notify_newgoal (incomplete)
    - added function notify_foul    (incomplete)
    - added function notify_gameover    (incomplete)
    - added new attribute 'output' to class MainTas kThread
    - updated function network_connection, added function calls depending on received message


1.0.2: (2024-04-28) / JH
    - Fixed function network_function   (socket)
    - Fixed class MainTaskThread        (socket)
    - Fixed function main_task          (socket)
    - Fixed function special_function   (socket)

    
1.0.1: (2024-04-28) / JH
    - Added function network_function
    - Added class MainTaskThread
    - Added function main_task
    - Added function special_function
    
'''


import os
import subprocess
import time
import cv2
import socket
import threading
from djitellopy import Tello            # Drone Package
from ultralytics import YOLO            # YoloAI Package
import torch                            # check for device (main_task)
import numpy as np                      # Yolo/Drone
from datetime import datetime           # Yolo/Drone
import math                             # Yolo/Drone

def connect_wifi_osx(ssid : str):
    """Establishing Wifi-Connection to a Wi-Fi network on MacOS via en0 interface

    Args:
        ssid (str): network SSIDs to connect to

    Returns:
        bool: True, when connection established
              False, when connection failed
    """ 
 

    # Get the interface name
    interface_name = "en0"

    # Turn on Wi-Fi
    os.system(f"networksetup -setairportpower {interface_name} on")

    # Wait for Wi-Fi to be ready
    time.sleep(5)

    # Scan for Wi-Fi networks
    networks = os.popen(f"/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport scan").read()

    # Check if the specified Wi-Fi network is available
    if ssid in networks:
        # Join the Wi-Fi network
        os.system(f"networksetup -setairportnetwork {interface_name} {ssid}")

        # Wait for Wi-Fi to connect
        time.sleep(5)

        # Check if the Wi-Fi is connected
        connected = False
        while not connected:
            output = subprocess.check_output(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"], universal_newlines=True)
            if " SSID: " + ssid in output:
                connected = True
            time.sleep(1)

        return connected

    return False

def connect_wifi(ssids):

    """
    Establish a Wi-Fi connection to a Wi-Fi network on Linux via the wlan0 interface.

    This function attempts to connect to one of the specified Wi-Fi networks by scanning for available networks,
    checking if any of the specified networks are available, and then attempting to connect to the first available
    network. If the connection is successful, the function returns True. If the connection fails, the function returns
    False.

    Args:
        ssids (list[str]): A list of network SSIDs to connect to.

    Returns:
        bool: True if the connection is established, False otherwise.
    """

    # Get the interface name
    interface_name = "wlan0"
    wifi_on = False     # wifi is not enabled
    
    while not wifi_on:
        # Turn on Wi-Fi
        os.system(f"nmcli radio wifi on")

        # Wait for Wi-Fi to be ready
        time.sleep(5)
        check_wifi = subprocess.check_output(["nmcli", "dev", "status"], universal_newlines=True)
    
        if interface_name in check_wifi and "disconnected" in check_wifi:
            wifi_on = True
            print("STATUS-WIFI: enabled")
        else: 
            print("STATUS-WIFI: not enabled")
        


    # Scan for Wi-Fi networks
    try:
        networks = subprocess.check_output(["nmcli", "dev", "wifi"], universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print(f"Error scanning for Wi-Fi networks: {e}")
        return False

    # Check if any of the specified Wi-Fi networks are available
    connected = False           # connection not established
    while not connected:
        print("STATUS-DRONE-CONNECT: trying to connect")
        for ssid in ssids:
            if ssid in networks:
                # Join the Wi-Fi network
                try:
                    subprocess.check_call(["nmcli", "dev", "wifi", "connect", ssid])
                except subprocess.CalledProcessError as e:
                    print(f"Error connecting to Wi-Fi network: {e}")

                # Wait for Wi-Fi to connect
                time.sleep(5)

                # Check if the Wi-Fi is connected
                #connected = False
                #while not connected:
                try:
                    output = subprocess.check_output(["nmcli", "dev", "status"], universal_newlines=True)
                    if interface_name in output and "connected" in output:
                        connected = True
                    else:
                        print("STATUS-DRONE-CONNECT: re-trying connection")
                except subprocess.CalledProcessError as e:
                    print(f"Error checking Wi-Fi connection status: {e}")
                    #return False
                time.sleep(1)

            #return connected

    # If none of the specified networks are available, return False
    return connected

def network_connection(s : socket, main_task_thread, connection_established, videoManager : object, Flugcontroller : object):

    """
    Establishes a network connection and handles incoming messages.

    Args:
        s (object): A socket object representing the network connection.
        main_task_thread (MainTaskThread): A thread object representing the main task.
        connection_established (Event): An object representing the established connection.
        videoManager (object) : An object which handles the video recording and playback

    Returns:
        None
    """
    
    #while True:
    try:
        connection_established.set()
        s.sendall(b'HELLO SERVER FROM network_connection')
        print('Doing network connection')

    except Exception as e:
        print(f"Error connecting: {e}")

    while True:
        try:
            data = s.recv(1024)
            if data:
                print("Received:", data.decode())
                # Check if the received message is a special message
                decdata = data.decode().strip() # decode received message

                ### INIT GAME ###
                # Keyword "ping" received
                if decdata == "ping":
              
                    print(f"RECV:{decdata} ")
                    main_task_thread.do_run = False     # Main_AI_Loop inactive
                    s.sendall(b"hi")                    # SEND ACK-Message "hi"                    
                    print("SEND: hi")

                ### PRE-GAME ROUTINE ###
                # Keyword "notify_drone_powered" received   
                elif decdata == "notify_drone_powered":
                     
                    print(f"RECV: {decdata} ")
                    main_task_thread.do_run = False        # Main_AI_Loop inactive
                    drone = notify_drone_powered(s=s)
                    if drone == False:
                        print("Drone not connected")
                    else: 
                        videoManager.set_drone(drone)       # init drone in videoManager-Object
                        print(f"Drone connected and initialized")
                        
                        Flugcontroller.set_drone(drone)

                        videoManager.startRecord()          # start video recording
                        print("Video recording started")
                        
                        notify_drone_connected(s=s)         # Send Keyword to kicker, wait for start_permission
                     

                # Keyword "notify_start_permission" received
                elif decdata == "notify_start_permission":

                    main_task_thread.do_run = True      # Main_AI_Loop active
                    main_task_thread.output = False     # AI_results disabled
                    print(f"RECV: {decdata} ")
                    DroneInPosition = notify_start_permission(s, drone)
                    if DroneInPosition:
                        print('Starting Game')
                        # Send "notify_gamestart" and wait for ACK
                        notify_gamestart(s=s)  
                        main_task_thread.do_run = True      # Main_AI_Loop active
                        main_task_thread.output = True      # AI_results enabled
                    else:
                        pass
                    
                
                ### IN-GAME ###
                # Keyword "notify_newgoal" received
                elif decdata == "notify_newgoal":

                    print(f"RECV:{decdata} ")

                    # Set Attributes for MainTask and VideoManager
                    main_task_thread.do_run = True      # Main_AI_Loop active
                    main_task_thread.output = False     # AI_results disabled

                    # Routine 
                    notify_newgoal(s=s, videoManager=videoManager)

                    # Resume to game
                    please_resume(s=s, videoManager=videoManager)

                    # Set Attributes for MainTask and VideoManager
                    main_task_thread.do_run = True      # Main_AI_Loop active
                    main_task_thread.output = True      # AI_results enabled


                # Keyword "notify_foul" received
                elif decdata == "notify_foul":

                    print(f"RECV:{decdata} ")
                    # Set Attributes for MainTask and VideoManager
                    main_task_thread.do_run = True      # Main_AI_Loop active
                    main_task_thread.output = False     # AI_results disabled

                    notify_foul(s, videoManager, Flugcontroller)

                    # Set Attributes for MainTask and VideoManager
                    main_task_thread.do_run = True      # Main_AI_Loop active
                    main_task_thread.output = True      # AI_results enabled


                ### END OF GAME ###
                # Keyword "notify_gameover" received
                elif decdata == "notify_gameover":

                    print(f"RECV:{decdata} ")
                    # Set Attributes for MainTask and VideoManager
                    main_task_thread.do_run = False      # Main_AI_Loop active
                    main_task_thread.output = False     # AI_results disabled
                    notify_gameover(s=s, drone=drone, videoManager=videoManager)



        except KeyboardInterrupt:
            s.close()

class MainTaskThread(threading.Thread):
    """
    This class defines a thread that runs the main task of the application.

    Attributes:
        connection_established (object): An object representing the established connection to kicker.
        do_run (bool): A flag indicating whether the thread should continue running.
        s (object): An object representing some additional data.

    Methods:
        __init__(self, connection_established, s): Initializes the thread with the given connection and additional data.
        run(self): Runs the main task in a loop while the do_run flag is True.
    """

    def __init__(self, connection_established, s : socket):
        """
        Initializes the thread with the given connection and additional data.

        Args:
            connection_established (object): An object representing the established connection.
            s (object): An object representing some additional data.
        """
        super().__init__()
        self.connection_established = connection_established
        self.do_run = False     # main_task: main_AI_loop default disabled
        self.s = s
        self.output = False     # Output default disabled

    def run(self):
        """
        Runs the main task in a loop while the do_run flag is True.
        """
        while self.do_run:
            main_task(self.connection_established, self.s, self.output)

######################################################################################
#### Functions for YOLO/Drone ####

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


def draw_grid(img, h1, h2, v1, v2): # Funktion zum Zeichnen des Rasters
    
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
    
    return(left_right, forward_backward, up_down)


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
            up_down = speed_multplier*2
    
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
######################################################################################

def main_task(connection_established, s : socket, output : bool, videoManager : object):

    # main task function - planned content: AI video processign
    # function called in threat
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
    image_width = 640 # Bilddimensionen
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
    # Logic to be implemented
    #global s    # network connection
    # When connection established (optional):
    # YOLO-Modell laden
    model = YOLO('best.pt')  # Pfad zum YOLOv8 Modell

    # CPU nutzen falls GPU nicht verfügbar
    if torch.cuda.is_available():
        model.to('cuda')
    else:
        model.to('cpu') # Low Performance!

    while connection_established.is_set():
        img  = videoManager.get_img()   # get Frame from Drone
        # INIT AI
        img = cv2.resize(img, (image_width, image_height))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Konvertiere BGR zu RGB
        img = cv2.flip(img, 0)  # Vertikale Spiegelung
        imgContour = img.copy()
        
        battery_level = drone.get_battery()# Akkustand abfragen
        print("Batterie bei", battery_level)
        
        if battery_level < 15:  # Landung anfordern bei zu wenig Akku
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
            center_x, center_y = bounding_box_center(x1, x2, y1, y2)
            detected_zone = get_zone(center_x, center_y, h1, h2, v1, v2)
            last_objectdetection = datetime.now()     
            left_right, forward_backward, up_down = get_instruction(detected_zone, area_desired)
            # Debug
            cv2.putText(imgContour, f"Center of Object ({desired_object}): ({int(np.round(center_x))}, {int(np.round(center_y))}), Area: {(area_desired):.1f} px", (20, img.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.circle(imgContour, (int(center_x), int(center_y)), 3, (0, 0, 255), -1)
            cv2.putText(imgContour, f"Zone: {detected_zone}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        elif object_detected and landingrequest and ready:
            print(f"{desired_object} wurde mit einer Konfidenz von über 0.5 erkannt! Landung erwünscht")
            
            # Verarbeitung
            center_x, center_y = bounding_box_center(x1, x2, y1, y2)
            detected_zone = get_zone(center_x, center_y, h1, h2, v1, v2)
            last_objectdetection = datetime.now()
            left_right, forward_backward, up_down = get_landinginstruction(detected_zone, area_desired)
            # Debug
            cv2.putText(imgContour, f"Zone: {detected_zone}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.putText(imgContour, f"Center of Object ({desired_object}): ({int(np.round(center_x))}, {int(np.round(center_y))}), Area: {(area_desired):.1f} px", (20, img.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.circle(imgContour, (int(center_x), int(center_y)), 3, (0, 0, 255), -1)
            

        elif not object_detected:
            cv2.putText(imgContour, f"Center of Object ({desired_object}): Object not found!", (20, img.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            print(f"Objekt ({desired_object}) nicht im Bild oder die Konfidenz ist zu gering")

            if ((current_time_check - last_objectdetection).total_seconds() > 3) and not landingrequest:        # Drohne rotieren, wenn über 3 Sekunden kein Kicker erkannt wurde
                if rotations <= 8:
                    print("Der Zeitstempel ist älter als 3 Sekunden. Rotiere Drohne")
                    rotations += 1
                    drone.rotate_clockwise(90)
            
                elif rotations >= 8 and not landingrequest:     # Wenn Drohne zwei Rotationen durchgeführt hat ohne Kicker zu erkennen -> Landung anfordern
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
            drone.send_rc_control(int(left_right), int(forward_backward), int(up_down), 0)
        

        # Auswertung für Landeanflug
        if landingrequest and desired_object == "landingpad" and area_desired > 100000:
            print("Ich bin nah am Landepad, schalte um auf Pointer!")
            near_landingpad = True

        if landingrequest and desired_object == "pointer_kicker" and area_desired > 6000 and detected_zone == "Mitte Mitte":
            drone.rotate_counter_clockwise(90)
            ready = False
            drone.land()

        # Ändern des Grid zur Abfrage der Flugbefehle bei Landingrequest
        if landingrequest:
            h1 = 2/9  
            h2 = 3/9  # Rastermitte kleiner und nach oben
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
            drone.land()
            break
        ### Video Ref is not active
        if not output:
            pass


        ### Video Ref is active
        else:
            
            # Second Ball detected
            if second_ball:
                
                # interrupt game
                please_wait(s=s)

                #TODO ROUTINE when second Ball detected

                # resume game
                please_resume(s=s)

            # Arms in Playfield
            elif forbidden_intervention:

                # interrupt game
                please_wait(s=s)

                #TODO ROUTINE when detected arm in playfield

                # resume game
                please_resume(s=s)

            # Other intervention
            elif other_intervention:
                                
                # interrupt game                
                please_wait(s=s)

                #TODO ROUTINE when other interverntion

                # resume game
                please_resume(s=s)

def notify_drone_powered(s : socket):
    global ssids
    ssids = ["TELLO-303446", "TELLO-E9BB29", "TELLO-E9C3AE"]    # SSIDs of the drones
    waitTime = 7    # Showing Battery Warning and Temperature Warning for 7 seconds
    maxTmp = 70     # parameter for Temperature Warning of drone-init: Temp must lower than this value
    minBat = 50     # parameter for Battery Warning of drone-init: Battery must be higher than value

    s.sendall(b'connecting_drone')  # send ACK to wi4.0
    print("SEND: connecting_drone")
    drone_connected = connect_wifi(ssids=ssids)

    if drone_connected:
        print("Drone connected to wifi")
        drone = Tello()     # INIT drone Objekt
        drone.connect()     # Connect to drone
        drone.streamon()    # Start Video Stream

        battery = drone.get_battery()           # Read in drone_battery
        temperature = drone.get_temperature()   # Read in drone_temp  

        print(f'Battery: {battery}%')
        print(f'Temperature: {temperature}°C')

        # If Drone to hot or battery to low:
        if (battery <= minBat or temperature >= maxTmp):
            # s.sendall(b"Drone to Hot or Battery to Low")
            print('Drone to Hot or Battery to Low')
            if temperature >= maxTmp:   # Drone temp hits 70°C (default of maxTmp)

                temp_img = cv2.imread("files/Drohne/img/warning_temp.png")  # read img in
                print(f"Drohne ist {temperature}°C warm - zu heiß!")
                # cv2.imshow("WARNING:TEMPERATURE", temp_img )                # display img

                # time.sleep(waitTime)       # sleep for 7 seconds (default)
                # cv2.destroyWindow("WARNING:TEMPERATURE")    # close window


            elif battery <= minBat:     # Drone battery lower than 50% (default of minBat)

                batt_img = cv2.imread("files/Drohne/img/warning_battery.png")   # read img in
                print(f"Drohne ist zu {battery}% geladen - Spielzeit eingeschränkt!") 
                # cv2.imshow("WARNING:BATTERY", batt_img)                         # display img

                # time.sleep(waitTime)        # sleep for 7 seconds (default)
                # cv2.destroyWindow("WARNING:BATTERY")    # close window

            # return None #TODO determine return
            return drone
        else:
            return drone

    else:
        print("Drone is NOT connected")
        return False

def notify_drone_connected(s : socket) -> None:
    s.sendall(b'notify_drone_connected')        # Send Keyword

    # Waiting for ACK
    while True:
        msg = s.recv(1024).decode().strip()
        if msg == "waiting_for_startbutton":
            print("Waiting for Start Permission")
            break
        else:
            time.sleep(0.5) # wait 0.5s
            s.sendall(b'notify_drone_connected')    # Repeat Keyword

def notify_start_permission(s : socket, drone):
    s.sendall(b'positioning_drone')
    # TODO get drone in position
    # TODO: If-Anweisung vorsehen, und senden, wenn Drohne in Position
    drone.takeoff()  # Drohne starten
    print("tello.takeoff ausgeführt")
    takeoff = True
    print("Starte Drohnenroutine zum Start")
    drone.move_up(20)
    drone.move_forward(20)
    drone.rotate_clockwise(90)
    drone.set_speed(10)
    ready = True # Marker Betriebsmodus für Drohne
    takeoff = False # Indikator abgeschlossener Takeoff
    drone.takeoff()
    time.sleep(5)
    drone.land()
    print("Drohne in Position")     # Debug Output
    return True

def notify_gamestart(s : socket) -> None:

    """
    Notifies the server that the game has started.

    Args:
        s (socket): A socket object representing the network connection.

    Returns:
        None
    """

    s.sendall(b'notify_gamestart')

    while True:
        msg = s.recv(1024).decode().strip()
        if msg == "game_started":
            print("Game started")
            return
        else:
            time.sleep(0.5)     # wait 0.5s
            s.sendall(b'notify_gamestart')

def please_resume(s : socket) -> None:

    """
    Notifies the server that AuVAReS is ready to continue the game and waits for ACK.
    Enables Frame Counting and VideoCapturing

    Args:
        s (socket): A socket object representing the network connection.

    Returns:
        None
    """

    s.sendall(b'please_resume')

    while True:
        msg = s.recv(1024).decode().strip()
        if msg == "gaming":
            print("Continue Game")
            return
        else:
            time.sleep(0.5) # wait 0.5s
            s.sendall(b'please_resume')

def please_wait(s : socket) -> None:

    """
    Notifies the server to pause the game and waits for ACK.
    Disables Frame Counting and VideoCapturing

    Args:
        s (socket): A socket object representing the network connection.

    Returns:
        None
    """

    s.sendall(b'please_wait')

    while True:
        msg = s.recv(1024).decode().strip()
        if msg == "waiting":
            print("Game paused")
            break
        else:
            time.sleep(0.5) # wait 0.5s
            s.sendall(b'please_wait')

def notify_newgoal(s: socket, videoManager : object) -> None:
    # Send ACK "received_newgoal"
    s.sendall(b"received_newgoal")

    # NEWGOAl ROUTINE
    # Playback of previous 10 sec. (300 Frames)
    videoManager.videoPlayback(windowName = 'Replay Goal')

    return

def notify_foul(s: socket, videoManager : object, Flugconteoller : object) -> None:
    # Send ACK "received_foul"
    s.sendall(b"received_foul")

    # FOUL ROUTINE
    # Playback of previous 10 sec. (300 Frames)
    Flugconteoller.emergency_land = True
    videoManager.videoPlayback(windowName = 'Replay Foul')

    return
    
def notify_gameover(s: socket, drone, videoManager : object):
    # Send ACK "received_gameover"
    s.sendall(b"received_gameover")

    # GAME OVER ROUTINE
    
    # Landing drone
    # TODO init landung
    # TODO check for landing success

    # Re-init videoManager-object
    videoManager.stopRecord()                       # Stop recording
    cv2.destroyAllWindows()                         # destroy all cv2 windows opened
    filename = getattr(videoManager, "filename")    # Read current filename in
    videoManager.__init__(filename=filename)        # reset all variables     

    # delete drone-object
    del drone

