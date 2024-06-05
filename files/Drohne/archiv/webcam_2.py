
import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from ultralytics import YOLO
import math

model = YOLO("/home/jetson/auvares/prj-wi/files/Drohne/Drohne_YOLO_test/best.pt")
# object classes
classNames = model.names

def grab_frame(cap):
    ret, img = cap.read()
    results = model(img, stream=True)
    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)

            # class name
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

cap1 = cv2.VideoCapture(0)

ax1 = plt.subplot(1,1,1)

im1 = ax1.imshow(grab_frame(cap1))

def update(i):
    im1.set_data(grab_frame(cap1))

ani = FuncAnimation(plt.gcf(), update, interval=33)

plt.show()