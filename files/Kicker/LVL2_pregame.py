"""

LEVEL 2
Pregame stuff

> connection_obj has to be passed here somehow
> drone_on_button and start_button need to be polled from website
> sending messages for changing infos on website are still missing

"""

__author__ = "Lukas Haberkorn"
__version__ = "1.1.7"
__status__ = "WIP"


import LVL3_classes as lvl3
import time


def pregame():
    '''
    This function is running as a thread in LVL1; handles all the pregame tasks 
    '''
    while True:
        if lvl3.sys_status == "init": # only directly after poweron
            time.sleep(3) # wait for init to be done, how long?? (WAP, Website)
            lvl3.set_status("wait_pre")

        if lvl3.sys_status == "wait_pre": # after init or gameover
        # 1.    
            # check USER has turned on Drone/entered names, then notify auvares
            drone_on_button = True # DEBUG, should be polled from Website
            while not drone_on_button:
                time.sleep(0.01)
            
            for i in range(5):
                if lvl3.connection_status == True:
                    data = "notify_drone_powered"
                    data.encode('utf-8')
                    with lvl3.port_lock :
                        lvl3.connection_type_object.sendall( data ) # sending keyword for foul
                        time.sleep(0.1)
                    break
                time.sleep(0.33)
            else:
                print("tja es ist kein auvares da oder was") #?? was machen wir dann?
        
        # 2.    
            # wait for "notify_drone_connected"
            while not lvl3.drone_connected:
                time.sleep(0.01)

        # 3.    
            # check user hat pressed start button, tell auvares
            start_button = True # DEBUG, should be polled from Website
            while not start_button:
                time.sleep(0.01)

            for i in range(5):
                if lvl3.connection_status == True:
                    data = "notify_start_permission"
                    data.encode('utf-8')
                    with lvl3.port_lock :
                        lvl3.connection_type_object.sendall( data ) # sending keyword for foul
                        time.sleep(0.1)
                    break
                time.sleep(0.33)
            else:
                print("tja es ist kein auvares da oder was") #?? was machen wir dann?

        # 4.
            # wait for "notify_gamestart"
            while not lvl3.drone_wants_gamestart:
                time.sleep(0.01)


            lvl3.set_status("ingame")
            lvl3.react_drone_connected(False)
            lvl3.react_drone_wants_gamestart(False)
        else:
            time.sleep(0.01)
            