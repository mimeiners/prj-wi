from djitellopy import Tello
import cv2
import time
import numpy as np
import torch

# Variables for Requests and Flight instructions
drone_request = False           # Request Drone by Kicker
drone_start_mode = False        # Request to start Flightmode of Drone
drone_flight_mode = False       # Start flight of Drone
drone_exit_request = False      # Request to end use of Drone
show_video = True               # Display video stream if True

drone_status = "Initialisierung"
drone_battery = -1              # Batterylevel, -1 as unplausible Value for init.

object = ["kicker", "red_ball", "angled_kicker", "landingpad", "landing_pointer"]

# Variables Drone
drone = Tello()

# Load YOLOv8 model
model = torch.hub.load('ultralytics/yolov8', 'yolov8', pretrained=True)

def detect_objects(frame):
    results = model(frame)
    return results

while True:
    if drone_request == True:               # if Statement as Placeholder for already used routine
        drone.connect()             
        drone.command()
        drone_battery = drone.get_battery()

        if drone_battery > 70:
            drone_start_mode = True
            drone_status = f"Drohne verfügbar zur Unterstützung des VAR.\nAkku bei {drone_battery}%"
        elif 0 < drone_battery <= 70:
            drone_start_mode = False
            drone_status = f"Drohne steht nicht zur Verfügung.\nAkku bei {drone_battery}%"
            drone_request = False
        else:
            drone_start_mode = False
            drone_status = "Drohne nicht erreichbar"
            drone_request = False
    
    print(drone_status)

    if drone_start_mode and drone_request == True:
        drone.takeoff()
        time.sleep(3)
        drone_start_mode = False
        drone_flight_mode = True
        drone.send_rc_control(0, 0, 50, 0)  # Ascend to safe height
        time.sleep(3)
        drone.send_rc_control(0, 50, 0, 0)  # Move forward to search for kicker
        time.sleep(3)

    if drone_flight_mode == True:
        frame_read = drone.get_frame_read()
        while drone_flight_mode:
            frame = frame_read.frame
            results = detect_objects(frame)

            for obj in results.pred[0]:         # Detect angled_kicker
                
                if obj[5] == 'angled_kicker':
                    angle = obj[4]              # Placeholder for actual angle calculation
                    if angle != 0:
                        drone.send_rc_control(0, 0, 0, int(angle))
                        time.sleep(1)
                        drone.send_rc_control(0, 0, 0, 0)

            if drone_battery < 15:
                landing_pointer_detected = False

                for obj in results.pred[0]:
                    if obj[5] == 'landing_pointer':
                        angle = obj[4]          # Placeholder for actual angle calculation
                        if angle != 0:
                            drone.send_rc_control(0, 0, 0, int(angle))
                            time.sleep(1)
                            drone.send_rc_control(0, 20, 0, 0)  # Fly towards the landing pointer
                            time.sleep(2)
                            drone.send_rc_control(0, 0, 0, 0)
                            landing_pointer_detected = True
                            break

                if landing_pointer_detected == True:
                    frame = frame_read.frame
                    results = detect_objects(frame)
                    for obj in results.pred[0]:
                        if obj[5] == 'landingpad':
                            angle = obj[4]       # Placeholder for actual angle calculation
                            if angle > 10:
                                drone.send_rc_control(0, 0, 0, int(angle))
                                time.sleep(1)
                                drone.send_rc_control(0, 0, 0, 0)
                            drone.land()
                            drone_flight_mode = False
                            break

            if show_video == True:
                cv2.imshow("Drone Camera", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    drone_exit_request = True
                    break

        if drone_exit_request == True:              # Combine in overall landing Routine
            drone.land()
            drone_flight_mode = False
            if show_video == True:
                cv2.destroyAllWindows()





#%% Aus Video:


from djitellopy import Tello
import cv2

#############################################
width = 320 # WIDTH OF THE IMAGE
height = 240 # HEIGHT OF THE IMAGE
startCounter =0 # 0 FOR FIGHT 1 FOR TESTING
#############################################




# CONNECT TO TELLO
me = Tello()
me. connect()
me.for_back_velocity = 0
me.left_right_velocity = 0
me.up_down_velocity =0
me.yaw_velocity = 0
me.speed = 0

print(me.get_battery())

me. streamoff()
me. streamon()

while True:

    # GET THE IMAGE FROM TELLO
    frame_read = me.get_frame_read()
    myFrame = frame_read.frame
    img= cv2.resize(myFrame, (width, height))|

    # TO GO UP IN THE BEGINNING
    if startCounter == 0:
    me. takeoff()
    me.move_left(20)
    me.rotate_clockwise(90)
    startCounter = 1

    # TO GO UP IN THE BEGINNING
    if startCounter == 0:
        me. takeoff()
        time.sleep(8)
        me.rotate_clockwise(90)
        time.sleep(3)
        me.move_left(35)
        time.sleep(3)
        me.land()
        startCounter = 1

    # # SEND VELOCITY VALUES TO TELLO
    # if me.send_rc_control:
    # me.send_rc_control(me.left_right_velocity, me.for_back_velocity, me.up_down_velocity, me.yaw_velocity)

    # DISPLAY IMAGE
    cv2.imshow("MyResult", img)

    # WAIT FOR THE 'Q' BUTTON TO STOP
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break
    
#%% Object Tracking

import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(1)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

deadZone=100
global imgContour

def empty(a):
    pass

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV",640,240)
cv2.createTrackbar("HUE Min","HSV",19,179,empty)
cv2.createTrackbar("HUE Max","HSV",35,179,empty)
cv2.createTrackbar("SAT Min","HSV",107,255,empty)
cv2.createTrackbar("SAT Max","HSV",255,255,empty)
cv2.createTrackbar("VALUE Min","HSV",89,255,empty)
cv2.createTrackbar("VALUE Max","HSV",255,255,empty)

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",166,255,empty)
cv2.createTrackbar("Threshold2","Parameters",171,255,empty)
cv2.createTrackbar("Area","Parameters",3750,30000,empty)


def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img,imgContour):

    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("Area", "Parameters")
        if area > areaMin:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            print(len(approx))
            x , y , w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x , y ), (x + w , y + h ), (0, 255, 0), 5)

            cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)
            cv2.putText(imgContour, " " + str(int(x))+ " "+str(int(y)), (x - 20, y- 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)

            cx = int(x + (w / 2))
            cy = int(y + (h / 2))

            if (cx <int(frameWidth/2)-deadZone):
                cv2.putText(imgContour, " GO LEFT " , (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(0,int(frameHeight/2-deadZone)),(int(frameWidth/2)-deadZone,int(frameHeight/2)+deadZone),(0,0,255),cv2.FILLED)
            elif (cx > int(frameWidth / 2) + deadZone):
                cv2.putText(imgContour, " GO RIGHT ", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(int(frameWidth/2+deadZone),int(frameHeight/2-deadZone)),(frameWidth,int(frameHeight/2)+deadZone),(0,0,255),cv2.FILLED)
            elif (cy < int(frameHeight / 2) - deadZone):
                cv2.putText(imgContour, " GO UP ", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(int(frameWidth/2-deadZone),0),(int(frameWidth/2+deadZone),int(frameHeight/2)-deadZone),(0,0,255),cv2.FILLED)
            elif (cy > int(frameHeight / 2) + deadZone):
                cv2.putText(imgContour, " GO DOWN ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(int(frameWidth/2-deadZone),int(frameHeight/2)+deadZone),(int(frameWidth/2+deadZone),frameHeight),(0,0,255),cv2.FILLED)


            cv2.line(imgContour, (int(frameWidth/2),int(frameHeight/2)), (cx,cy),
                     (0, 0, 255), 3)

def display(img):
    cv2.line(img,(int(frameWidth/2)-deadZone,0),(int(frameWidth/2)-deadZone,frameHeight),(255,255,0),3)
    cv2.line(img,(int(frameWidth/2)+deadZone,0),(int(frameWidth/2)+deadZone,frameHeight),(255,255,0),3)

    cv2.circle(img,(int(frameWidth/2),int(frameHeight/2)),5,(0,0,255),5)
    cv2.line(img, (0,int(frameHeight / 2) - deadZone), (frameWidth,int(frameHeight / 2) - deadZone), (255, 255, 0), 3)
    cv2.line(img, (0, int(frameHeight / 2) + deadZone), (frameWidth, int(frameHeight / 2) + deadZone), (255, 255, 0), 3)

while True:

    _, img = cap.read()
    imgContour = img.copy()
    imgHsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("HUE Min","HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")
    print(h_min)

    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHsv,lower,upper)
    result = cv2.bitwise_and(img,img, mask = mask)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    imgBlur = cv2.GaussianBlur(result, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    getContours(imgDil, imgContour)
    display(imgContour)

    stack = stackImages(0.7,([img,result],[imgDil,imgContour]))

    cv2.imshow('Horizontal Stacking', stack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()