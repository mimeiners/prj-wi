import cv2

def videoPlayback(filename: str, startframe: int, numberOfFrames: int, timedelay:int = 50):
    """Ausgabe Video von Frame A bis Frame B

    Args:
        filename (str): Dateiname mp4-file
        startframe (int): frameNumber Frame A
        numberOfFrames (int): frameNumber Frame B
        timedelay (int, optional): Parameter, welcher die Ausgabegeschwindigkeit steuert Defaults to 50.
    """    
    # Create a VideoCapture object to read the video file
    cap = cv2.VideoCapture(filename)

    # Get the video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps, width,height)

    # Create a VideoWriter object with the output file name and parameters
    #fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4 video
    #out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

    # Set the position of the video file to the starting frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, startframe)

    # Create a window and specify the HDMI output
    cv2.namedWindow('Video Playback', cv2.WINDOW_NORMAL)
    #cv2.setWindowProperty('Video Playback', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
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
    #out.release()
    cv2.destroyAllWindows()

videoPlayback('tello_stream.mp4', 40, 100)