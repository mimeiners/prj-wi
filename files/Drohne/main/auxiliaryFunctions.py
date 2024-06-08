"""
This is meant to be used as an imported modules file for the main file 
and is basically listing the auxilary functions (literally) the AuVAReS posesses.
"""
__author__ = "Julian Höpe"
__version__ = "1.0.8"
__status__ = " WIP"
__date__ = "2024-06-05"

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

1.0.8.: (2024-06-05) / sSamland, jHöpe, fKatenkamp
    - changed structure in terms of flight control
    - adjusted functions to new class Flugsteuerung

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
from Tello_M import Tello               # Drone Package
from ultralytics import YOLO            # YoloAI Package
import torch                            # check for device (main_task)


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
        networks = subprocess.check_output(["nmcli", "dev", "wifi"], universal_newlines=True)
        # print("STATUS-DRONE-CONNECT: trying to connect")
        for ssid in ssids:
            time.sleep(1)
            print(f"trying to connect to {ssid}")
            if ssid in networks:
                print("SSID LINE 198")
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

def network_connection(s : socket, connection_established, videoManager : object, Flugcontroller : object):

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
                    s.sendall(b"hi")                    # SEND ACK-Message "hi"                    
                    print("SEND: hi")

                ### PRE-GAME ROUTINE ###
                # Keyword "notify_drone_powered" received   
                elif decdata == "notify_drone_powered":
                     
                    print(f"RECV: {decdata} ")
                    drone = notify_drone_powered(s=s)
                    if drone == False:
                        print("Drone not connected")
                    else: 
                        videoManager.set_drone(drone)       # init drone in videoManager-Object
                        Flugcontroller.set_drone(drone)     # init drone in Flugcontroller-Object
                        print(f"Drone connected and initialized")
                        
                        videoManager.startRecord()          # start video recording
                        print("Video recording started")
                        
                        notify_drone_connected(s=s)         # Send Keyword to kicker, wait for start_permission
                     

                # Keyword "notify_start_permission" received
                elif decdata == "notify_start_permission":

                    print(f"RECV: {decdata} ")
                    DroneInPosition = notify_start_permission(s, Flugcontroller)
                    if DroneInPosition:
                        print('Starting Game')
                        # Send "notify_gamestart" and wait for ACK
                        notify_gamestart(s=s)  
                    else:
                        pass
                    
                
                ### IN-GAME ###
                # Keyword "notify_newgoal" received
                elif decdata == "notify_newgoal":

                    print(f"RECV:{decdata} ")

                    # Set Attributes for MainTask and VideoManager

                    # Routine 
                    notify_newgoal(s=s, videoManager=videoManager)

                    # Resume to game
                    please_resume(s=s, videoManager=videoManager)

                    # Set Attributes for MainTask and VideoManager

                # Keyword "notify_foul" received
                elif decdata == "notify_foul":

                    print(f"RECV:{decdata} ")
                    # Set Attributes for MainTask and VideoManager

                    notify_foul(s=s, videoManager=videoManager)

                    # Set Attributes for MainTask and VideoManager

                ### END OF GAME ###
                # Keyword "notify_gameover" received
                elif decdata == "notify_gameover":

                    print(f"RECV:{decdata} ")
                    # Set Attributes for MainTask and VideoManager
                    notify_gameover(s=s, drone=drone, videoManager=videoManager, Flugcontroller=Flugcontroller)

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
            

def main_task(connection_established, s : socket, output : bool, videoManager : object):

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

                temp_img = cv2.imread("/home/jetson/prj-wi/files/Drohne/img/hsb-logo.png")  # read img in
                print(f"Drohne ist {temperature}°C warm - zu heiß!")
                cv2.imshow("WARNING:TEMPERATURE", temp_img )                # display img
                cv2.waitKey(waitTime * 1000)                                # wait for 7 seconds
                cv2.destroyWindow("WARNING:TEMPERATURE")    # close window


            elif battery <= minBat:     # Drone battery lower than 50% (default of minBat)

                batt_img = cv2.imread("/home/jetson/prj-wi/files/Drohne/img/warning_battery.png")   # read img in
                print(f"Drohne ist zu {battery}% geladen - Spielzeit eingeschränkt!") 
                cv2.imshow("WARNING:BATTERY", batt_img)                         # display img
                cv2.waitKey(waitTime * 1000)                                # wait for 7 seconds
                cv2.destroyWindow("WARNING:BATTERY")    # close window

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

def notify_start_permission(s : socket, Flugsteuerung):
    s.sendall(b'positioning_drone')
    # TODO get drone in position
    # TODO: If-Anweisung vorsehen, und senden, wenn Drohne in Position

    print("Starte Drone")
    Flugsteuerung.start()
    
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

def notify_foul(s: socket, videoManager : object) -> None:
    # Send ACK "received_foul"
    s.sendall(b"received_foul")

    # FOUL ROUTINE
    # Playback of previous 10 sec. (300 Frames)
    videoManager.videoPlayback(windowName = 'Replay Foul')

    return
    
def notify_gameover(s: socket, drone, videoManager : object, Flugcontroller : object):
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

