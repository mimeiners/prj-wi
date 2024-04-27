"""
This is meant to be used as an imported modules file for the main file 
and is basically listing the auxilary functions (literally) the AuVAReS posesses.
"""
__author__ = "Julian Höpe"
__version__ = "1.0.0"
__status__ = " WIP"
__date__ = "2024-04-27"

'''
NOTE:
videoPlayback: 
    Last statement "cv2.destroyAllWindows() might cause an issue with the video stream received from the drone"
'''


import os
import subprocess
import time
import cv2

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

