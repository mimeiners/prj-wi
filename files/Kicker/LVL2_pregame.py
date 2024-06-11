"""

LEVEL 2
Pregame stuff

> button_stop has to be tested

"""

__author__ = "Lukas Haberkorn", "Martin Schwarz", "Torge Plate"
__version__ = "1.5.3"
__status__ = "good"


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
            
            print("Waiting for playernames...")
            while True:
                data = lvl3.json_read()
                if data["player_1"]["name"] != "":
                    break
                time.sleep(0.5)
            lvl3.player1_name = data["player_1"]["name"]
            lvl3.player2_name = data["player_2"]["name"]
            print("Received playernames!")
            
            # wait for USER button press, drone is turned on
            while True:
                data = lvl3.json_read()
                if data["button_power"] is True:
                    break
                time.sleep(0.5)
            print("USER Button 1 pressed!")

            # try to notify AuVAReS
            lvl3.server_send( "notify_drone_powered" )

        # 2.   
            for i in range(5): # try 5 times
                if lvl3.connection_status == True: # check connection
                    while not lvl3.drone_connected:
                        time.sleep(0.01) # wait here for "notify_drone_connected"
                    break
                time.sleep(0.33)
            else:
                print("ERROR: AuVAReS not found!")
            
        # 3.    
            # wait for USER has pressed drone start button
            while True:
                data = lvl3.json_read()
                if data["button_start"] is True:
                    break
                time.sleep(0.5)
            print("USER Button 2 pressed!")

            # try to notify AuVAReS
            lvl3.server_send( "notify_start_permission" )

        # 4.
            for i in range(5): # try 5 times
                if lvl3.connection_status == True: # check connection
                    while not lvl3.drone_wants_gamestart:
                        time.sleep(0.01) # wait here for "notify_gamestart"
                    break
                time.sleep(0.33)
            else:
                print("ERROR: AuVAReS not found!")

            # setting game id (=timestamp)
            lvl3.gameID = str( time.time()//1 )
            print("Game ID is", lvl3.gameID)

            # write game ID and reset Website Buttons
            data = lvl3.json_read()
            data["game_id"] = lvl3.gameID; data["button_start"] = False; data["button_power"] = False
            lvl3.json_write(data)

            lvl3.goals_player1 = 0; lvl3.goals_player2 = 0
            lvl3.database_write( lvl3.gameID, lvl3.player1_name, 0)
            lvl3.database_write( lvl3.gameID, lvl3.player2_name, 0)
            lvl3.set_status("ingame")
            lvl3.react_drone_connected(False)
            lvl3.react_drone_wants_gamestart(False)
        
        else: # while "ingame" or "wait_ingame"
            time.sleep(0.9)
            data = lvl3.json_read()
            try:
                if data["button_stop"] is True:
                    lvl3.set_status("wait_ingame")
                    
                    if lvl3.connection_status == True:
                        lvl3.server_send( "notify_gameover" )
                    print("##########\n A GAME HAS BEEN CANCELED with", lvl3.goals_player1,":", lvl3.goals_player2,"\n##########\n")
                    
                    # Clear player names in json
                    data = lvl3.json_read()
                    data["player_1"]["name"] = ""; data["player_2"]["name"] = ""; data["button_stop"] = False
                    data["last_completed_game"] = lvl3.gameID
                    lvl3.json_write(data)

                    time.sleep(1)
                    lvl3.set_status("wait_pre")
            except:
                print("button_stop error")