"""
This is meant to be used as an imported modules file for the main file 
and is basically listing the auxilary functions (literally) the AuVAReS posesses.
"""
__author__ = ("Finn Katenkamp", "Julian Höpe")
__version__ = "1.1.1"
__status__ = " WIP"
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
    
    def __init__(self, filename : str, centerx : int = 700, centery : int = 400, fps:int = 30, replay_time:int = 10):

        self.drone = None                                                                   # Drone object

        self.filename = filename                                                            # Filename .mp4-file, where tello stream will be recorded

        self.framecenterx = centerx                                                         # 
        self.framecentery = centery
        self.record = False                                                                 # bool for record control
        self.fps = fps                                                                      # in frames per second
        self.replay_time = replay_time                                                      # length of replay in seconds
        
        self.video_buffer = queue.deque(maxlen=self.replay_time*self.fps)                   # buffer for video replays
        self.t1 = None                                                                      # threading object (not initialized at this point)
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(filename = self.filename,
                                   fourcc = self.fourcc,
                                   fps = self.fps,
                                   frameSize = (2*self.framecenterx, 2*self.framecentery))

    def set_drone(self, drone):
        self.drone = drone
        return
    
    def get_img(self):
        self.img = self.drone.get_frame_read().frame
        # print("type of self.img:",type(self.img))
        if not (isinstance(self.img, ndarray)):
            print("no Frame recieved from ")
            self.img = cv2.imread("/home/jetson/prj-wi/files/Drohne/main/hsb-logo.png")

        self.img = cv2.resize(self.img, (2*self.framecenterx, 2*self.framecentery))
        self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
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
        while self.record:
            img = self.get_img()
            cv2.imshow("DroneVid", img);
            self.video_buffer.append(img)
            self.out.write(img)             # save frame to video
            time.sleep(1.0 / self.fps)
            #time.sleep(0.5);
            

    def startRecord(self):
        self.record = True
        self.t1 = threading.Thread(target=self.videoRecord)
        self.t1.start()

    def stopRecord(self):
        self.record = False
        self.t1.join()
        self.out.release()

######################################################################################################

from djitellopy import tello

drone = tello.Tello()
drone.connect()
print("Battery: ", drone.get_battery())
print("Temp.: ", drone.get_temperature())
drone.streamon()


VideoManager = VideoHandler("test2.mp4", fps=30, replay_time=10)
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
    # VideoManager.videoPlayback("Playback 1")
    print("sleep 5 sek")
    time.sleep(5)
    print("replayVideo")
    # VideoManager.videoPlayback("Playback 2")
    print("stopRecord")
    VideoManager.stopRecord()


main_thread = threading.Thread(target=run, args=(VideoManager, ))
main_thread.start()
main_thread.join()