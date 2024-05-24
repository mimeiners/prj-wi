"""

LEVEL 2
Foul detection via GPIO

"""
__author__ = "Lukas Haberkorn"
__version__ = "1.0.2"
__status__ = "untested"

import RPi.GPIO as GPIO
import LVL3_classes as lvl3
import time


def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def foul():
    while True:
        if lvl3.sys_status == "ingame":
            if GPIO.input(38) == GPIO.HIGH:
                lvl3.react_foul(1)
            if GPIO.input(40) == GPIO.HIGH:
                lvl3.react_foul(2)
        else:
            time.sleep(0.01)