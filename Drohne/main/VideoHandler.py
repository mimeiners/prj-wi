"""
This is meant to be used as an imported modules file for the main file 
and is basically listing the auxilary functions (literally) the AuVAReS posesses.
"""
__author__ = ("Finn Katenkamp", "Julian Höpe")
__version__ = "1.1.2"
__status__ = " WIP"
__date__ = "2024-06-05"

'''
NOTE: NONE
'''

'''
TODO: NONE
'''

'''
Changes:
1.1.2: (2024-06-05) / fkatenkamp
    - read imf from drone via UDP
    
Changes:
1.1.1: (2024-05-29) / fkatenkamp,jhöpe
    - complete remake with threading
    - general optimisation

'''

import cv2
import os
import time
import threading
import queue
from numpy import ndarray

class VideoHandler():
    """
    A class to handle video recording and playback for a drone stream.

    Attributes:
    -----------
    filename : str
        The filename where the video stream will be saved (in .mp4 format).
    framecenterx : int
        The x-coordinate of the video frame.
    framecentery : int
        The y-coordinate of the video frame.
    record : bool
        A boolean flag to control the recording state.
    fps : int
        The frame rate for recording (frames per second).
    replay_time : int
        The length of the replay in seconds.
    video_buffer : deque
        A buffer to store video frames for replay.
    t1 : threading.Thread
        A threading object to handle the recording process.
    fourcc : cv2.VideoWriter_fourcc
        The four character code for the codec used in video writing.
    out : cv2.VideoWriter
        The video writer object to save the recorded video.

    Methods:
    --------
    set_drone(drone):
        Sets the drone object for video handling.

    get_img():
        Captures the current frame from the drone, resizes and converts it.

    videoPlayback(windowName="Playback"):
        Plays back the recorded video in a named window.

    videoRecord():
        Continuously records video frames while recording is enabled.

    startRecord():
        Starts the video recording in a separate thread.

    stopRecord():
        Stops the video recording and releases the video writer.
    """
    
    def __init__(self, filename : str, width_x : int = 640, width_y : int = 480, fps:int = 30, replay_time:int = 10):

        self.drone = None                                                                   # Drone object

        self.filename = filename                                                            # Filename .mp4-file, where tello stream will be recorded

        self.frame_width_x = width_x                                                         # 
        self.frame_width_y = width_y
        self.record = False                                                                 # bool for record control
        self.fps = fps                                                                      # in frames per second
        self.replay_time = replay_time                                                      # length of replay in seconds
        
        self.video_buffer = queue.deque(maxlen=self.replay_time*self.fps)                   # buffer for video replays
        self.t1 = None                                                                      # threading object (not initialized at this point)
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(filename = self.filename,
                                   fourcc = self.fourcc,
                                   fps = self.fps,
                                   frameSize = (2*self.frame_width_x, 2*self.frame_width_y))
        self.cap = None
        self.ret = False
        self.img = cv2.resize(cv2.imread("/home/jetson/prj-wi/files/Drohne/img/warning_battery.png"), (2*self.frame_width_x, 2*self.frame_width_y))

    def set_drone(self, drone):
        self.drone = drone
        # self.cap = cv2.VideoCapture(self.drone.get_udp_video_address())
        self.cap = cv2.VideoCapture(self.drone.get_udp_video_address()+"?overrun_nonfatal=1", cv2.CAP_FFMPEG)
        return
    
    def get_img(self):
        # try:
        #     ret, self.img = self.cap.read()
        #     self.img = cv2.resize(self.img, (2*self.frame_width_x, 2*self.frame_width_y))
        #     # self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
        #     self.img = cv2.flip(self.img, 0)

        # except:
        #     print("no Frame recieved from ")
        #     # self.img = cv2.imread("/home/jetson/prj-wi/files/Drohne/main/hsb-logo.png")
        #     self.img = cv2.imread("/home/jetson/prj-wi/files/Drohne/img/warning_battery.png")
        #     self.img = cv2.resize(self.img, (2*self.frame_width_x, 2*self.frame_width_y))

        return self.img

    def videoPlayback(self, windowName:str="Playback"):
        # config openCV window
        cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) # Fullscreen
        cv2.setWindowProperty(windowName, cv2.WND_PROP_TOPMOST, 1)  # Keep the window on top
        cv2.moveWindow(windowName, 0, 0)  # Move the window to the primary display
        # play replay
        for frame in list(self.video_buffer):
            cv2.imshow(windowName, frame)
            if cv2.waitKey(int(1000 / self.fps)) & 0xFF == ord('q'):
                break
        cv2.destroyWindow(windowName)

    def videoRecord(self):
        while self.record and self.cap.isOpened():
            self.ret, self.img = self.cap.read()
            self.video_buffer.append(self.img)
            self.out.write(self.img)             # save frame to video

    def startRecord(self):
        self.record = True
        self.t1 = threading.Thread(target=self.videoRecord)
        self.t1.start()
        print("VideoHandler: startRecord")

    def stopRecord(self):
        self.record = False
        self.t1.join()
        self.out.release()
        print("VideoHandler: stopRecord")

