"""

LEVEL 1
Initializing the second threading level with sensors and interface

"""
__author__ = "Lukas Haberkorn", "Marvin Otten"
__version__ = "1.0.1"
__status__ = "WIP"


import sockets
from time import sleep
import threading

import LVL2_interface_functions as infu
import LVL2_goal_detection as gode
#import LVL2_foul_detection as fode 


#%%

# Main funtion sensor, definition and management

def sensors():
    main_threadlist = [ threading.Thread( target = goal,
                                          args = [],
                                          kwargs = {}),
                        
                        threading.Thread( target = foul,
                                          args = [],
                                          kwargs = {}) ]


def goal():
    gode.goal()

def foul():
    #fode.foul() ?
    pass


#%%

# Main funtion interface, definition and management

def interface(): # Marvin
    pass
