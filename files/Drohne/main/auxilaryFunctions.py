"""
This is meant to be used as an imported modules file for the main file 
and is basically listing the auxilary functions (literally) the AuVAReS posesses.
"""
__author__ = "Julian Höpe"
__version__ = "1.0.2"
__status__ = " WIP"
__date__ = "2024-04-28"

'''
NOTE:
videoPlayback: 
    Last statement "cv2.destroyAllWindows() might cause an issue with the video stream received from the drone"

network_function:
    Error handling has to be implemented, which ensures that the connection is closed correctly in case of an error
'''

'''
Changes:

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


def connect_wifi(ssids : list[str]):

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

    # Turn on Wi-Fi
    os.system(f"nmcli radio wifi on")

    # Wait for Wi-Fi to be ready
    time.sleep(5)

    # Scan for Wi-Fi networks
    try:
        networks = subprocess.check_output(["nmcli", "dev", "wifi"], universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print(f"Error scanning for Wi-Fi networks: {e}")
        return False

    # Check if any of the specified Wi-Fi networks are available
    for ssid in ssids:
        if ssid in networks:
            # Join the Wi-Fi network
            try:
                subprocess.check_call(["nmcli", "dev", "wifi", "connect", ssid])
            except subprocess.CalledProcessError as e:
                print(f"Error connecting to Wi-Fi network: {e}")
                continue

            # Wait for Wi-Fi to connect
            time.sleep(5)

            # Check if the Wi-Fi is connected
            connected = False
            while not connected:
                try:
                    output = subprocess.check_output(["nmcli", "dev", "status"], universal_newlines=True)
                    if interface_name in output and "connected" in output:
                        connected = True
                except subprocess.CalledProcessError as e:
                    print(f"Error checking Wi-Fi connection status: {e}")
                    return False
                time.sleep(1)

            return connected

    # If none of the specified networks are available, return False
    return False


def videoPlayback(filename: str, startframe: int, numberOfFrames: int, timedelay:int = 50):

    """
    This function plays a specified portion of a video file and displays it on the screen.

    Args:
        filename (str): The name of the video file to play.
        startframe (int): The number of the frame at which to start playing the video.
        numberOfFrames (int): The number of frames to play.
        timedelay (int, optional): A parameter that controls the playback speed. A higher value will result in slower playback.

    Returns:
        None
    """    

    # Create a VideoCapture object to read the video file
    cap = cv2.VideoCapture(filename)

    # Get the video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps, width,height)

    # Set the position of the video file to the starting frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, startframe)

    # Create a window and specify the HDMI output
    cv2.namedWindow('Video Playback', cv2.WINDOW_NORMAL)
    #cv2.setWindowProperty('Video Playback', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) # Fullscreen
    #cv2.setWindowProperty('Video Playback', cv2.WND_PROP_TOPMOST, 1)  # Keep the window on top
    cv2.moveWindow('Video Playback', 0, 0)  # Move the window to the primary display

    # Read and display frames until the desired number of frames is reached
    for i in range(numberOfFrames):
        # Read the next frame
        ret, frame = cap.read()

        # Check if the frame was successfully read
        if not ret:
            break

        # Write the frame to the output video file
        #out.write(frame)

        # Display the frame in the window
        cv2.imshow('Video Playback', frame)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(timedelay) & 0xFF == ord('q'):
            break

    # Release the video file and destroy the window
    cap.release()
    cv2.destroyAllWindows()
    return


def network_connection(s : socket, main_task_thread, connection_established):

    """
    Establishes a network connection and handles incoming messages.

    Args:
        s (object): A socket object representing the network connection.
        main_task_thread (MainTaskThread): A thread object representing the main task.
        connection_established (Event): An object representing the established connection.

    Returns:
        None
    """
    
    #while True:
    try:
        #s.connect((host, port))
        connection_established.set()
        s.sendall(b"HELLO SERVER FROM network_connection")
        print('Doing network connection')
        #break
    #except BlockingIOError:
        # Connection not established yet, wait and try again        
    #    time.sleep(0.1)
    except Exception as e:
        print(f"Error connecting: {e}")
        #break

    # Set the last keep-alive time
    last_keep_alive = time.time()
    while True:
        try:
            data = s.recv(1024)
            if data:
                print("Received:", data.decode())
                # Check if the received message is a special message
                decdata = data.decode().strip() # decode received message

                if decdata == "SPECIAL_MESSAGE":
                    # Interrupt the main task and run the special function
                    main_task_thread.do_run = False
                    print("interrupted main task")
                    special_message_function(s)
                    main_task_thread.do_run = True
                    print("continued main task")
        
                # Check if the received message is a special message
                elif decdata == "GAMEPHASE_eventType_PLAYER":
                    # Interrupt the main task and run the special function
                    main_task_thread.do_run = False
                    print("interrupted main task")
                    special_message_function()
                    main_task_thread.do_run = True
                    print("continued main task")
                
                # Check if the received message is a special message
                elif decdata == "GAMEPHASE_eventType_PLAYER":
                    # Interrupt the main task and run the special function
                    main_task_thread.do_run = False
                    print("interrupted main task")
                    special_message_function()
                    main_task_thread.do_run = True
                    print("continued main task")

                # Check if the received message is a special message
                elif decdata == "GAMEPHASE_eventType_PLAYER":
                    # Interrupt the main task and run the special function
                    main_task_thread.do_run = False
                    print("interrupted main task")
                    special_message_function()
                    main_task_thread.do_run = True
                    print("continued main task")

                # Check if the received message is a special message  
                elif decdata == "GAMEPHASE_eventType_PLAYER":
                    # Interrupt the main task and run the special function
                    main_task_thread.do_run = False
                    print("interrupted main task")
                    special_message_function()
                    main_task_thread.do_run = True
                    print("continued main task")

        except KeyboardInterrupt:
            s.close()


class MainTaskThread(threading.Thread):
    """
    This class defines a thread that runs the main task of the application.

    Attributes:
        connection_established (object): An object representing the established connection.
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
        self.do_run = True
        self.s = s

    def run(self):
        """
        Runs the main task in a loop while the do_run flag is True.
        """
        while self.do_run:
            main_task(self.connection_established, self.s)


def main_task(connection_established, s : socket):
    # main task function - planned content: AI video processign
    # function called in threat

    # Logic to be implemented
    #global s    # network connection
    # When connection established (optional):
    while connection_established.is_set():
        print("Doing main task...")
        s.sendall(b"HELLO SERVER from main_task")
        time.sleep(5)


def special_message_function(s : socket):
    # This function is called when the server sends a special message

    #global s    # network connection
    print("Special message received! Running special function...")
    s.sendall(b"HELLO SERVER FROM special_message_function")

    # Logic to be implemented
    return

