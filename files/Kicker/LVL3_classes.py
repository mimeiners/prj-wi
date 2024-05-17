"""

LEVEL 3
This file includes system wide used functions and variables

> currently we do not differentiate who made a foul
> initialize Server connection in init() has to be adapted for no connection

"""

__author__ = "Lukas Haberkorn", "Marvin Otten"
__version__ = "2.1.3"
__status__ = "WIP"


import time
import threading
import socket

def init():
    '''
    !! Has to be run before all other level 3 functions to initialize global variables
    '''
    global goals_player1; goals_player1 = 0
    global goals_player2; goals_player2 = 0
    global drone_connected; drone_connected = False
    global drone_wants_gamestart; drone_wants_gamestart = False

    global sys_status; sys_status = "init"
    global status_lock; status_lock = threading.Lock()          # Lock for changing system status
    global port_lock ; port_lock = threading.Lock()             # Lock for sending
    
    global connection_status; connection_status = False
    print("Status is: init")


    ## initialize Server connection
    global ping_ack_flag ; ping_ack_flag = False
    global connection_type_object ; connection_type_object = None
    find_thread = threading.Thread( target = _find_connection(), args = [], kwargs = [])
    find_thread.daemon = True
    find_thread.start()



def _find_connection():
    server_interface_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_interface_obj.bind(('localhost' , 10000))

    # look for connection
    server_interface_obj.listen(0)
    
    # create conncetion object
    global connection_type_object
    connection_type_object , client_address = server_interface_obj.accept()

    set_connection_status( True )
    return

# game status control - - - - - - - - - - - - - - - - - - - -

def set_status( arg_ , delay = 0):
    '''
    sys_status should be string: "init"|"wait_pre"|"ingame"|"wait_ingame"
    '''
    time.sleep( delay )
    global sys_status; global status_lock
    with status_lock:
        print("Status is:", arg_)
        sys_status = arg_
    

def set_connection_status( set_status ):
    '''
    boolean set_status
    '''
    global connection_status
    connection_status = set_status


# reaction functions, what to do when specific game events occur - - - - - - - - - - - - - - - - - - - -

def react_goal( player , connection_obj ): # reaction to event in goal_detection thread
    '''
    called by the exception in the goal sensor thread
    '''
    global goals_player1; global goals_player2
    global connection_status
    global port_lock
    
    set_status("wait_ingame")

    if player == 1: # add goal to the correct player
        goals_player1 += 1
        print("player 1 scored")
    
    elif player == 2:
        goals_player2 += 1
        print("player 2 scored")

    if (goals_player1 == 6 or goals_player2 == 6) or (goals_player1 == 5 and goals_player2 == 5): # check win condition
        # >>> UPDATE DATABASE HERE
        if connection_status == True:
            data = "notify_gameover"
            data.encode('utf-8')
            with port_lock :
                connection_obj.sendall( data ) # sending keyword for foul
                time.sleep(0.1)
        else:
            time.sleep(10)
        print("##########\n A GAME HAS BEEN FINISHED with", goals_player1,":", goals_player2,"\n##########\n")
        time.sleep(5)
        set_status("wait_pre")
        goals_player1 = 0; goals_player2 = 0 # Resetting AFTER writing to database!!

    else: # no win condition was met
        # >>> UPDATE DATABASE HERE
        if connection_status == True:
            data = "notify_newgoal"
            data.encode('utf-8')
            with port_lock :
                connection_obj.sendall( data ) # sending keyword for foul
                time.sleep(0.1)
        else:
            time.sleep(10)
        time.sleep(2)
        set_status("ingame")
        print("we continue with ", goals_player1,":", goals_player2)


def react_foul( connection_obj ): # reaction to event in foul_detection thread
    '''
    called by the exception in the foul sensor thread
    '''
    global connection_status
    global port_lock

    set_status("wait_ingame")
    if connection_status == True:
        data = "notify_foul"
        data.encode('utf-8')
        with port_lock : connection_obj.sendall( data ) # sending keyword for foul
    else:
        time.sleep(5)
    set_status("ingame")


def react_drone_connected( state ): # reaction to keyword
    '''
    boolean argument
    '''
    global drone_connected; drone_connected = state
    print("Drone connected: ", drone_connected)


def react_drone_wants_gamestart( state ): # reaction to keyword
    '''
    boolean argument
    '''
    global drone_wants_gamestart; drone_wants_gamestart = state
    print("Drone wants the game to start: ", drone_wants_gamestart)


def react_drone_pleasewait(): # reaction to keyword
    set_status("wait_ingame")
    print(" ### GAME PAUSED by AuVAReS ### ")


def react_drone_pleaseresume(): # reaction to keyword
    set_status("ingame")
    print(" ### GAME RESUMED by AuVAReS ### ")