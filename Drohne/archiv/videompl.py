"""
This is meant to be used as an imported modules file for the main file 
and is basically listing the auxiliary functions (literally) the AuVAReS possesses.
"""
__author__ = ("Finn Katenkamp", "Julian Höpe")
__version__ = "1.1.1"
__status__ = "WIP"
__date__ = "2024-05-29"

'''
NOTE: NONE
'''

'''
TODO: NONE
'''

'''
Changes:
1.1.1: (2024-05-29) / fkatenkamp,jhöpe
    - complete remake with threading
    - general optimization
'''

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import pyplot as plt
import os
import time
import threading
import queue
import imageio
from collections import deque
import cv2
from djitellopy import tello
import numpy as np

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
    writer : imageio.get_writer
        The video writer object to save the recorded video.

    Methods:
    --------
    set_drone(drone):
        Sets the drone object for video handling.

    get_img():
        Captures the current frame from the drone, resizes and converts it.

    videoPlayback():
        Plays back the recorded video using matplotlib.

    videoRecord():
        Continuously records video frames while recording is enabled.

    startRecord():
        Starts the video recording in a separate thread.

    stopRecord():
        Stops the video recording and releases the video writer.
    """
    
    def __init__(self, filename : str, centerx : int = 700, centery : int = 400, fps:int = 30, replay_time:int = 10):

        self.drone = None                                                                   # Drone object

        self.filename = filename                                                            # Filename .mp4-file, where tello stream will be recorded

        self.framecenterx = centerx                                                         # 
        self.framecentery = centery
        self.record = False                                                                 # bool for record control
        self.fps = fps                                                                      # in frames per second
        self.replay_time = replay_time                                                      # length of replay in seconds
        
        self.video_buffer = deque(maxlen=self.replay_time*self.fps)                         # buffer for video replays
        self.t1 = None                                                                      # threading object (not initialized at this point)
        self.writer = imageio.get_writer(self.filename, fps=self.fps)                       # imageio writer

    def set_drone(self, drone):
        self.drone = drone
        return
    
    def get_img(self):
        self.img = self.drone.get_frame_read().frame
        np.savetxt("test.txt", self.img)
        self.img = cv2.resize(self.img, (2*self.framecenterx, 2*self.framecentery))
        # self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_YUV2RGB_YV12)
        return self.img

    def videoPlayback(self):
        fig = plt.figure()
        ims = []

        for frame in list(self.video_buffer):
            im = plt.imshow(frame, animated=True)
            ims.append([im])

        ani = animation.ArtistAnimation(fig, ims, interval=1000/self.fps, blit=True, repeat_delay=1000)
        plt.show()

    def videoRecord(self):
        while self.record:
            img = self.get_img()
            if img is not None:
                self.video_buffer.append(img)
                self.writer.append_data(img)             # save frame to video
                time.sleep(1/self.fps)

    def startRecord(self):
        self.record = True
        self.t1 = threading.Thread(target=self.videoRecord)
        self.t1.start()

    def stopRecord(self):
        self.record = False
        self.t1.join()
        self.writer.close()


#############################################################################################


drone = tello.Tello()
drone.connect()

drone.streamon()

VideoManager = VideoHandler("test1.mp4", fps=30, replay_time=10)
VideoManager.set_drone(drone)


def run(VideoManager):
    print("sleep 10 sek")
    time.sleep(10)
    print("videoRecord")
    VideoManager.videoRecord()
    print("run_record")
    VideoManager.startRecord()
    print("sleep 15 sek")
    time.sleep(15)
    print("replayVideo")
    VideoManager.videoPlayback("Playback 1")
    print("sleep 5 sek")
    time.sleep(5)
    print("replayVideo")
    VideoManager.videoPlayback("Playback 2")
    print("stopRecord")
    VideoManager.stopRecord()


main_thread = threading.Thread(target=run, args=(VideoManager, ))
main_thread.start()
main_thread.join()