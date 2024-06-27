"""
This is the main file for the project.
"""
__author__ = ("Julian Höpe", "Finn Katenkamp")
__version__ = "1.0.4"
__status__ = " WIP"
__date__ = "2024-06-05"

'''
NOTE:
Error Handling has to be implemented in the most functions

NOTE:
This is the first approach of the main code
'''

'''
Changes:
1.0.4: (2024-06-05) / JH
    - added new thread for displaying kicker website

1.0.3: (2024-05-29) / jHöpe, fKatenkamp
    - updated objecthandling of VideoHandler object

1.0.2: (2024-05-04) / JH
    - added imports
    - adjusted class-inits and function calls  

    
1.0.1: (2024-04-28) / JH
    - fixed socket connection
'''

##### Imports #####
import auxiliaryFunctions as aux        # auxilary functions for AuVAReS
import os                               # Connect Wifi
import subprocess                       # Connect Wifi
import time                             # Timeloop
import cv2                              # Video Stream / Record
import socket                           # Socket connection WohnInvest4.0
import threading                        # Parallel Tasks
# from Tello_M import Tello            # Drone Package
import VideoHandler as VH               # VideoHandling AuVAReS
import Flugsteuerung as FS              # Flight Controller and AI AuVAReS
import Website_start_fullscreen as wsf  # Display Kicker Game Information

##### Variables #####
ssids = ["TELLO-303446", "TELLO-E9BB29", "TELLO-E9C3AE"]    # SSIDs of the drones

### NETWORK Variables
kickerIP = "192.168.xxx.xxx"                                # IP-Address of the WohnInvest4.0 kicker
kickerPORT = "1234"                                         # Port of the WohnInvest4.0 kicker

filename = 'file.mp4'                                       # Filename, where to store the Video

gameURL = "www.google.de"                                   # Website of Kicker displaying game information and instructions

##### Main #####

'''
# TODO: establish connection with drone - DONE in notify_drone_connect
# TODO: customize network_connection function
# TODO: implement error handling
# TODO: implement functions for event handling
# TODO: implement drone connection, PID, stream
'''

### INIT for recording
videoManager = VH.VideoHandler(filename=filename)
Flugcontroller = FS.Flugsteuerung(videoManager)


### Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

### INIT the network connection and main task in separate threads
connection_established = threading.Event()
main_task_thread = aux.MainTaskThread(connection_established, s)
network_connection_thread = threading.Thread(target=aux.network_connection, args=(s, connection_established, videoManager, Flugcontroller, ))
# website_thread = threading.Thread(target=wsf.display_website_fullscreen(), args=(gameURL, ))

# Get local machine name
host = aux.socket.gethostname()
#host = kickerIP

port = 8765
#port = kickerPORT

# connect to Server
s.connect((host, port))
connection_established.set()


### Start the threads
network_connection_thread.start()
main_task_thread.start()
# website_thread.start()

# Wait for the threads to finish
network_connection_thread.join()
main_task_thread.join()
# website_thread.join()

# Clean up the connection
s.close()