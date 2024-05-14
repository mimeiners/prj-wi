"""

LEVEL 2
Pregame stuff

"""
__author__ = "Lukas Haberkorn"
__version__ = "1.0.0"
__status__ = "WIP"


import LVL3_classes as lvl3
import time

def pregame():
    lvl3.drone_connection.keyword_class_dic["notify_gamestart"].ack_react = lvl3.react_drone_in_position()
    while True:
        if lvl3.sys_status == "init": # only directly after poweron
            # >>> wait for init to be done??
            time.sleep(5) # ???
            lvl3.set_status("wait_pre")

        if lvl3.sys_status == "wait_pre": # after init or gameover
            start_button = True # DEBUG, should be polled from Website
            if start_button and lvl3.drone_in_position: # wait for start button & drone in position ACK
                lvl3.set_status("ingame")
                lvl3.drone_in_position = False
            