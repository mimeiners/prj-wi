"""

LEVEL 2
Goal detection via GPIO

"""
__author__ = "Lukas Haberkorn"
__version__ = "1.0.0"
__status__ = "WIP"

import RPi.GPIO as GPIO
import LVL3_classes as lvl3
import time

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(13, GPIO.IN)
    GPIO.setup(15, GPIO.IN)
    global player_1_scored_goal; player_1_scored_goal = lvl3.userdefined_Exception( reaction = lvl3.react_goal(1) )
    global player_2_scored_goal; player_2_scored_goal = lvl3.userdefined_Exception( reaction = lvl3.react_goal(2) )

def goal():
    global player_1_scored_goal
    global player_2_scored_goal
    while True:
        try:
            if lvl3.sys_status == "ingame":
                if GPIO.input(13) == GPIO.LOW:
                    raise player_1_scored_goal
                if GPIO.input(15) == GPIO.LOW:
                    raise player_2_scored_goal
            else:
                time.sleep(0.01)
        except lvl3.userdefined_Exception as e:
            e.reaction