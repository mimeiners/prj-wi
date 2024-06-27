"""

LEVEL 1 (formerly 0 and 1)
Initializing the first and second threading level. Also includes emergency stop
Has to be run as sudo for GPIO to work; "rpi-lgpio" library required!!

"""
__author__ = "Lukas Haberkorn", "Marvin Otten"
__version__ = "1.2.2"
__status__ = "good"



import RPi.GPIO as GPIO
import threading
import LVL2_interface as infa
import LVL2_goal_detection as gode
import LVL2_pregame as pre
import LVL2_foul_detection as fode
import LVL3_classes as lvl3


def stop(channel):
    '''
    Interrup routine, emergency stop
    argument is bodge
    '''
    lvl3.server_send("STOP")


def emergency_stop():
    '''
    Thread for emergency stop button
    '''
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(36, GPIO.FALLING, callback=stop, bouncetime=200)
    while True:
        pass


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
                                          kwargs = {}),
                        threading.Thread( target = emergency_stop,
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