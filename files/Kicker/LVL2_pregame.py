"""

LEVEL 2
Pregame stuff

> drone_on_button and start_button need to be polled from website seperately
> sending messages for changing infos on website are still missing

"""

__author__ = "Lukas Haberkorn", "Martin Schwarz"
__version__ = "1.2.0"
__status__ = "WIP"


import LVL3_classes as lvl3
import time
import os


# functions for getting website's USER input - - - - - - - - - - - - - - - - - - -

def monitor_names():
    if os.path.exists("/var/www/html/PlayerNames.txt"):
        with open("/var/www/html/PlayerNames.txt", "r") as names_file:
            names = names_file.read().strip()
        if names:
            name1, name2 = names.split(",")
            return name1, name2
        else:
            return "wait"
    else:
        return "emptypath"

	
def monitor_drone():
    if os.path.exists("/var/www/html/DroneCheck.txt"):
        with open("/var/www/html/DroneCheck.txt", "r") as Dcheck_file:
            check = Dcheck_file.read().strip()
        if check:
            check == "success"
            print("drone start")
            return True
        else:
            print("wait for drone")
            time.sleep(1)
            return False
    else:
        print("no drone")
        time.sleep(1)
        return "emptypath"


def reset_check():
    if os.path.exists("/var/www/html/PlayerNames.txt"):
        with open("/var/www/html/PlayerNames.txt", "r") as names_file:
            names = names_file.read().strip()

    if os.path.exists("/var/www/html/DroneCheck.txt"):
        with open("/var/www/html/DroneCheck.txt", "r") as Dcheck_file:
            check = Dcheck_file.read().strip()
                    
    if names == "" or check == "":
        return True
    return False



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
            while monitor_names() == "emptypath" or monitor_names() == "wait":
                match monitor_names():
                    case "emptypath":
                        lvl3.player1_name = "_Player 1"
                        lvl3.player2_name = "_Player 2"
                        break
                    case "wait":
                        time.sleep(0.1)
                        continue
                    case _:
                        Names = monitor_names()
                        lvl3.player1_name = Names[0]
                        lvl3.player2_name = Names[1]
                        break
            
            # wait for USER button press, drone is turned on
            while monitor_drone() == False:
                time.sleep(0.1)
            if monitor_drone == "emptypath":
                print("quasi 404") #was machen wir dann??
            
            # try to notify AuVAReS
            for i in range(5):
                if lvl3.connection_status == True:
                    data = "notify_drone_powered"
                    data.encode('utf-8')
                    lvl3.server_send( data )
                    break
                time.sleep(0.33)
            else:
                print("tja es ist kein auvares da oder was") #?? was machen wir dann?
        
        # 2.    
            # wait for "notify_drone_connected"
            while not lvl3.drone_connected:
                time.sleep(0.01)

        # 3.    
            # wait for USER has pressed drone start button, tell auvares
            while monitor_drone() == False:
                time.sleep(0.1)
            if monitor_drone == "emptypath":
                print("quasi 404") #was machen wir dann??

            for i in range(5):
                if lvl3.connection_status == True:
                    data = "notify_start_permission"
                    data.encode('utf-8')
                    lvl3.server_send( data )
                    break
                time.sleep(0.33)
            else:
                print("tja es ist kein auvares da oder was") #?? was machen wir dann?

        # 4.
            # wait for "notify_gamestart"
            while not lvl3.drone_wants_gamestart:
                time.sleep(0.01)

            lvl3.gameID = str( time.time()//1 )
            print("Game ID is", lvl3.gameID)
            lvl3.goals_player1 = 0; lvl3.goals_player2 = 0
            lvl3.set_status("ingame")
            lvl3.react_drone_connected(False)
            lvl3.react_drone_wants_gamestart(False)
        else: # while "ingame" or "wait_ingame"
            time.sleep(0.05)
            if reset_check():
                lvl3.set_status("wait_pre")