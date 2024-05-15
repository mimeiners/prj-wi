"""

LEVEL 2
Goal detection via GPIO

"""
__author__ = "Lukas Haberkorn"
__version__ = "1.1.0"
__status__ = "good"

import RPi.GPIO as GPIO
import LVL3_classes as lvl3
import time


def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def goal():
    while True:
        if lvl3.sys_status == "ingame":
            if GPIO.input(13) == GPIO.LOW:
                lvl3.react_goal(1,0)
            if GPIO.input(15) == GPIO.LOW:
                lvl3.react_goal(2,0)
        else:
            time.sleep(0.01)