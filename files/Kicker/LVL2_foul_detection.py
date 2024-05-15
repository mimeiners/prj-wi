"""

LEVEL 2
Foul detection via GPIO

> TBD: do we care who caused a foul? do we need to differantiate between the two sides?

"""
__author__ = "Lukas Haberkorn"
__version__ = "1.0.0"
__status__ = "untested"

import RPi.GPIO as GPIO
import LVL3_classes as lvl3
import time


def init():
    GPIO.setmode(GPIO.BOARD) # does this cause problems? There are two Threads doing this!! (&goaldetection)
    GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def foul():
    while True:
        if lvl3.sys_status == "ingame":
            if GPIO.input(38) == GPIO.LOW:
                lvl3.react_foul()
            if GPIO.input(40) == GPIO.LOW:
                lvl3.react_foul()
        else:
            time.sleep(0.01)