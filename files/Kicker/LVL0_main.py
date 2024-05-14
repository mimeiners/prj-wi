"""

LEVEL 0
Initializing the first threading level

"""
__author__ = "Lukas Haberkorn", "Marvin Otten"
__version__ = "1.0.2"
__status__ = "WIP"


from time import sleep
import threading
import LVL1_funcs as lvl1
import LVL3_classes as lvl3

lvl3.init()

# Thread level one
main_threadlist = [ threading.Thread( target = lvl1.sensors,
                                      args = [],
                                      kwargs = {}),
                    
                    threading.Thread( target = lvl1.interface,
                                      args = [],
                                      kwargs = {}),

                    threading.Thread( target = PREGAME WIP,
                                      args = [],
                                      kwargs = {}) ]


#start threats
for thread in main_threadlist:
    thread.start()

#wait for threads to join once programm is finished | thread internal check
for thread in main_threadlist:
    thread.join()  
