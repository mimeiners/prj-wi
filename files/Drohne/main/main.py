"""
This is the main file for the project.
"""
__author__ = "Julian Höpe"
__version__ = "1.0.1"
__status__ = " WIP"
__date__ = "2024-04-28"

'''
NOTE:
Error Handling has to be implemented in the most functions

NOTE:
This is the first approach of the main code
'''

'''
Changes:

1.0.1: (2024-04-28) / JH
    - fixed socket connection
'''

##### Imports #####
from auxilaryFunctions import *         # auxilary functions for AuVAReS

##### Variables #####
ssids = ["TELLO-303446", "TELLO-E9BB29", "TELLO-E9C3AE"]    # SSIDs of the drones

### NETWORK Variables
kickerIP = "192.168.xxx.xxx"                                # IP-Address of the WohnInvest4.0 kicker
kickerPORT = "1234"                                         # Port of the WohnInvest4.0 kicker

### VIDEO record/playback Variables
filename = 'tello_stream.mp4'                               # Filename .mp4-file, where tello stream will be recorded
framecenterx = 700     
framecentery = 400


##### Main #####

'''
# TO-DO: establish connection with drone
# TO-DO: code should follow main_flowchart (tbd)   
# TO-DO: [optional] write class for establishing socket connection
# TO-DO: customize network_connection function
# TO-DO: implement error handling
# TO-DO: implement functions for event handling
# TO-DO: implement drone connection, PID, stream
'''

### INIT for recording
# Define the codec and create a VideoWriter object to save the stream as a video file
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(filename=filename, fourcc=fourcc, fps=10.0, frameSize=(2*framecenterx, 2*framecentery))

### Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

### INIT the network connection and main task in separate threads
connection_established = threading.Event()
main_task_thread = MainTaskThread(connection_established, s)
network_connection_thread = threading.Thread(target=network_connection, args=(s, main_task_thread, connection_established,))


# Get local machine name
host = socket.gethostname()
#host = kickerIP

port = 12345
#port = kickerPORT

# connect to Server
s.connect((host, port))
connection_established.set()


### Start the threads
network_connection_thread.start()
main_task_thread.start()

# Wait for the threads to finish
network_connection_thread.join()
main_task_thread.join()

# Clean up the connection
s.close()