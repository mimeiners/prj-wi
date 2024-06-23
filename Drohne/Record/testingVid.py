import cv2

class VideoHandler():

    def __init__(self, filename : str, centerx : int = 700, centery : int = 400):

        self.CountFrames = False                # FrameCounting disabled
        self.FrameNumber = 0                    # FrameNumber for Playback
        self.numberOfFrames = 300               # Playback 300 Frames := 10s @ 30 FPS
        self.filename = filename                # Filename .mp4-file, where tello stream will be recorded
        #self.clearFile()                        # Delete existing file with filename, if exists
        self.framecenterx = centerx     
        self.framecentery = centery
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(filename = f'out_{self.filename}', fourcc=self.fourcc, fps=30, frameSize=(2*self.framecenterx, 2*self.framecentery))
        # filename=self.filename+"_out"
        self.drone = None                       # Drone object

    # def __del__(self):
    #     print("deleted")

    def clearFile(self):

        """
        Check if the .mp4 file with the name stored in the `filename` attribute exists in the current working directory and delete it.
        If the file does not exist, print a message indicating that the file does not exist.

        Returns:
            None
        """

        if os.path.isfile(self.filename):
            os.remove(self.filename)        # remove VideoFile, if exists
            print(f"Deleted {self.filename}")  
        else:
            print(f"{self.filename} does not exist and will be created")    # INFO-Output


    def videoPlayback(self, windowName : str, timedelay:int = 50):

        """
        This function plays a specified portion of a video file and displays it on the screen.

        Args:
            windowName (str): The name of the window to display the video in.
            timedelay (int, optional): A parameter that controls the playback speed. A higher value will result in slower playback.

        Returns:
            None
        """    

        # Create a VideoCapture object to read the video file
        cap = cv2.VideoCapture("out_"+self.filename)

        # Get the video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(fps, width,height)

        startframe = self.FrameNumber - self.numberOfFrames     # Number of startframe, current Frame Number - frames to playback

        # Set the position of the video file to the starting frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, startframe)

        # Create a window and specify the HDMI output
        cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
        # cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) # Fullscreen
        # cv2.setWindowProperty(windowName, cv2.WND_PROP_TOPMOST, 1)  # Keep the window on top
        cv2.moveWindow(windowName, 0, 0)  # Move the window to the primary display

        # Read and display frames until the desired number of frames is reached
        for i in range(self.numberOfFrames):
            # Read the next frame
            ret, frame = cap.read()

            # Check if the frame was successfully read
            if not ret:
                break

            # Write the frame to the output video file
            #out.write(frame)

            # Display the frame in the window
            cv2.imshow(windowName, frame)

            # Break the loop if the 'q' key is pressed
            if cv2.waitKey(timedelay) & 0xFF == ord('q'):
                break

        # Release the video file and destroy the window
        cap.release()
        cv2.destroyAllWindows()
        return

    def videoRecord(self):
        camera = cv2.VideoCapture(0)
        for i in range (100) :
            ret, img = camera.read()
            print(ret)
            img = cv2.resize(img, (2*self.framecenterx, 2*self.framecentery))
            cv2.imshow("track", img)
            self.out.write(img)     # save frame to video
            self.inc_FrameNumber()  # Increment Frame +1
        self.out.release()
        return

    def set_drone(self, drone):
        self.drone = drone
        return
    
    def get_img(self, drone):
        self.img = drone.get_frame_read().frame
        self.img = cv2.resize(self.img, (2*self.framecenterx, 2*self.framecentery))
        self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
        return self.img
    
    def inc_FrameNumber(self):
        self.FrameNumber +=1
        return
    

videoManager = VideoHandler(filename="tello_stream.mp4")

# videoManager.videoPlayback("test")
videoManager.CountFrames = True
videoManager.videoRecord()
videoManager.CountFrames = False
videoManager.videoPlayback('test')

    