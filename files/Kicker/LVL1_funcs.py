"""

LEVEL 1
Initializing the second threading level with sensors and interface

"""
__author__ = "Lukas Haberkorn", "Marvin Otten"
__version__ = "1.0.2"
__status__ = "WIP"


import sockets
from time import sleep
import threading

import LVL2_interface_functions as infu
import LVL2_goal_detection as gode
import LVL2_pregame as pregame
#import LVL2_foul_detection as fode 


#%%

# Main funtion sensor, definition and management

def sensors():
    gode.init()
    main_threadlist = [ threading.Thread( target = gode.goal(),
                                          args = [],
                                          kwargs = {}),
                        
                        threading.Thread( target = foul,
                                          args = [],
                                          kwargs = {}) ]
    #start threads
    for thread in main_threadlist:
        thread.start()

    #wait for threads to join once programm is finished | thread internal check
    for thread in main_threadlist:
        thread.join()  



# just a Weiterleitung to LVL2
def pregame():
    pregame.pregame()



#%%

# Main funtion interface, definition and management

def interface(): # Marvin
    pass



