"""

LEVEL 2
Pregame stuff

> drone_on_button and start_button need to be polled from website seperately
> sending messages for changing infos on website are still missing
> Step 1 and 3 website GET methods should be replaced with flask

"""

__author__ = "Lukas Haberkorn", "Martin Schwarz", "Torge Plate"
__version__ = "1.3.0"
__status__ = "WIP"


import LVL3_classes as lvl3
import time


# PREGAME Function  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def pregame():
    '''
    This function is running as a thread in LVL1; handles all the pregame tasks 
    '''
    while True:
        if lvl3.sys_status == "init": # only directly after poweron
            time.sleep(1) # wait for init to be done, how long?? (WAP, Website)
            lvl3.set_status("wait_pre")

        if lvl3.sys_status == "wait_pre": # after init or gameover

        # 1.    
            # get USER names from website
            player_names = lvl3.load_player_names()
            lvl3.player1_name = player_names.get('name1')
            lvl3.player2_name = player_names.get('name2')

            # # # # # # # # # # # # # # # # # # # # # # # # # #
            # wait for USER button press, drone is turned on  #
            # # # # # # # # # # # # # # # # # # # # # # # # # #
            
            # try to notify AuVAReS
            for i in range(5):
                if lvl3.connection_status == True:
                    data = "notify_drone_powered"
                    lvl3.server_send( data )
                    break
                time.sleep(0.33)
            else:
                print("tja es ist kein auvares da oder was") #?? was machen wir dann?
        
        # 2.   
            for i in range(5): # try 5 times
                if lvl3.connection_status == True: # check connection
                    while not lvl3.drone_connected:
                        time.sleep(0.01) # wait here for "notify_drone_connected"
                    break
                time.sleep(0.33)
            else:
                print("tja es ist kein auvares da oder was") #?? was machen wir dann?

        # 3.    

            # # # # # # # # # # # # # # # # # # # # # # # # #
            # wait for USER has pressed drone start button  #
            # # # # # # # # # # # # # # # # # # # # # # # # #

            for i in range(5):
                if lvl3.connection_status == True:
                    data = "notify_start_permission"
                    lvl3.server_send( data )
                    break
                time.sleep(0.33)
            else:
                print("tja es ist kein auvares da oder was") #?? was machen wir dann?

        # 4.
            for i in range(5): # try 5 times
                if lvl3.connection_status == True: # check connection
                    while not lvl3.drone_wants_gamestart:
                        time.sleep(0.01) # wait here for "notify_gamestart"
                    break
                time.sleep(0.33)
            else:
                print("tja es ist kein auvares da oder was") #?? was machen wir dann?

            lvl3.gameID = str( time.time()//1 )
            print("Game ID is", lvl3.gameID)
            lvl3.goals_player1 = 0; lvl3.goals_player2 = 0
            lvl3.set_status("ingame")
            lvl3.react_drone_connected(False)
            lvl3.react_drone_wants_gamestart(False)
        
        else: # while "ingame" or "wait_ingame"
            time.sleep(0.01)