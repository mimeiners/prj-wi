"""

LEVEL 1 (formerly 0 and 1)
Initializing the first and second threading level. 
Has to be run as sudo for GPIO to work

"""
__author__ = "Lukas Haberkorn", "Marvin Otten"
__version__ = "1.1.4"
__status__ = "good"


import threading
import LVL2_interface as infa
import LVL2_goal_detection as gode
import LVL2_pregame as pre
import LVL2_foul_detection as fode
import LVL3_classes as lvl3



def sensors():
    '''
    This function is called alongside the three main threads and creates two more threads inside its own thread
    '''
    gode.init()
    fode.init()
    main_threadlist = [ threading.Thread( target = gode.goal,
                                          args = [],
                                          kwargs = {}),
                        
                        threading.Thread( target = fode.foul,
                                          args = [],
                                          kwargs = {})
                        ]
    #start threads
    for thread in main_threadlist:
        thread.start()

    #wait for threads to join once programm is finished | thread internal check
    for thread in main_threadlist:
        thread.join()  


'''
main code starts here
'''

lvl3.init() # initialize global variables in level 3

# Thread level one
main_threadlist = [ threading.Thread( target = sensors,
                                      args = [],
                                      kwargs = {}),
                    
                    threading.Thread( target = infa.interface,
                                      args = [],
                                      kwargs = {}),

                    threading.Thread( target = pre.pregame,
                                      args = [],
                                      kwargs = {}) ]

#start threads
for thread in main_threadlist:
    thread.start()

#wait for threads to join once programm is finished | thread internal check
for thread in main_threadlist:
    thread.join()