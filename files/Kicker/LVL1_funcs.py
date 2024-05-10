"""

M O D U L E S bzw. F U N C T I O N S:
Level 1

"""
__author__ = "Lukas Haberkorn", "Marvin Otten"
__version__ = "1.0.0"
__status__ = "WIP"


import sockets
from time import sleep
import threading
#import TASKS



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
    return

def foul():
    return


#%%

# Main funtion interface, definition and management

def interface(): # Marvin

    pass
