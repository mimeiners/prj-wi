"""
@date       2024.04.19
@version:   V1.03
@author:    Finn Katenkmap
"""

"""
Hinweis: Für die Fehlersuche kann Zeile 42,44-45 einkommentiert werden,
um den Log in einer Datei zu speichern.
Das Loglevel kann in zeile 38 angepasst werden.

Flugsteuerung:

    links/rechts/vorwärts/rückwärts -> "Pfeiltasten"
    hoch -> "w"
    runter -> "s"
    rechts-/linksdrehen -> "d"/"a"

    starten -> "q"
    landen -> "e"
    Programm beenden -> "ESCAPE"

    Screenshot -> "p"
"""

#%% Imports

from djitellopy import tello
import cv2
import KeyPressModule as kp
import logging
import os


#%% Settings

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s : \"%(message)s\"",
    datefmt="%Y-%m-%d %H:%M:%S",
    # uncomment the following line to save log in a file
    filename="{filename}.log".format(filename = __file__.replace(".py","_py"))
    )
with open(next((handler for handler in logging.getLogger().handlers if isinstance(handler, logging.FileHandler)), None).baseFilename, "a") as file:
    print("\nStart of Skript:", file=file)

kp.init()
tello = tello.Tello()
tello.connect()
tello.LOGGER.setLevel(logging.WARNING)
logging.warning(f"battery: {tello.get_battery()} | temperature: {tello.get_temperature}")

tello.streamon()

landed = True
save = False

# Stellt sicher, dass ein Pfad zum speichern von Screenshots verfpgbar ist
# bei bedarf die Variable directory ändern
directory = "screenshots"
os.makedirs(directory, exist_ok=True)

#%% functions

def getKeyboardInput():
    lr,fb,ud,yv = 0,0,0,0
    speed = 50
    esc = False
    global save
    global landed

    if kp.getKey("LEFT"): lr    = -speed
    elif kp.getKey("RIGHT"): lr = speed 

    if kp.getKey("UP"): fb     = speed
    elif kp.getKey("DOWN"): fb = -speed 

    if kp.getKey("s"): ud   = -speed
    elif kp.getKey("w"): ud = speed

    if kp.getKey("d"): yv   =   speed
    elif kp.getKey("a"): yv =   -speed

    if kp.getKey("e"):
        if not landed:
            tello.land()
            landed = True

    if kp.getKey("q"):
        if landed:
            tello.takeoff()
            landed = False

    if kp.getKey("ESCAPE"):
        esc = True

    if kp.getKey("p"):
        save = True

    return[lr,fb,ud,yv,esc,save]

def get_file_list(path):
    file_list = []
    highest_number = 0
    for file_name in os.listdir(path):
        if file_name.startswith("img_") and file_name.endswith(".png"):
            file_list.append(file_name)
            number = int(file_name[4:-4])  # Extrahiere die Nummer aus dem Dateinamen
            if number > highest_number:
                highest_number = number

    return file_list, highest_number


#%% main

running = True
battery = tello.get_battery()
temperature = tello.get_temperature()
path = os.path.dirname(__file__)

# img_nr = get_file_list(os.path.join(path, directory))[1]
img_nr = 0000
logging.info(f"next img number: {img_nr:04d}")

while running:
    direc = getKeyboardInput()

    # stop programm
    if direc[4]:
        running = False
        if not landed:
            tello.land()
            landed = True
        break

    # battery
    if not (battery == tello.get_battery()):
        battery = tello.get_battery()
        logging.warning(f"battery: {battery}")
    # temperature
    if not (temperature == tello.get_temperature()):
        temperature = tello.get_temperature()
        logging.warning(f"temperature: {temperature}")

    print(f"battery: {battery} | temperature: {temperature}")

    # rc controll
    tello.send_rc_control(direc[0],direc[1],direc[2],direc[3])

    ### camera control
    img = tello.get_frame_read().frame
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # save frame as image
    if direc[5]:
        img_nr +=1
        save = False
        img_path = os.path.join(os.path.join(path, directory), "img_{img_nr:04d}.png".format(img_nr=img_nr))
        if cv2.imwrite(img_path, img):
            logging.info(f"image saved : \"{img_path}\"")
        else:
            logging.error(f"saving picture failed -- path: \"{img_path}\"")
    # video stream
    if img is not None:
        img = cv2.resize(img, (360,240))
        cv2.imshow("Image", img)
        cv2.waitKey(1)
    else:
        logging.warning("empty frame")

