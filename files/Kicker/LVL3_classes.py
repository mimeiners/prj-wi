"""

LEVEL 3
This file includes system wide used functions and variables

> currently we do not differentiate who made a foul
> initialize Server connection in init() has to be adapted for no connection / timeouts
> we never check DB connection with client.health(), this is stupid!

"""

__author__ = "Lukas Haberkorn", "Marvin Otten", "Torge Plate"
__version__ = "2.3.1"
__status__ = "WIP"


import time
import threading
import socket
import json

#imports for database
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.query_api import QueryApi


def init():
    '''
    !! Has to be run before all other level 3 functions to initialize global variables
    '''
    global goals_player1; goals_player1 = 0
    global goals_player2; goals_player2 = 0
    global player1_name; player1_name = "DEFAULT_player1"
    global player2_name; player2_name = "DEFAULT_player2"
    global drone_connected; drone_connected = False
    global drone_wants_gamestart; drone_wants_gamestart = False
    global gameID; gameID = 0

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


    # init database connection
    host = '192.168.26.98' # TO BE CHANGED
    port = 8086
    token = 'Xady8ZXGEKBuRbEHaBMicR5Qcqmsdw7o9G8mu8q6gx4vsrvWiR9mV1-LLWoo26s8FaMfyZ0BVV1Hr8INrSPBCA=='
    global bucket; bucket = 'kicker'
    org = 'Hochschule Bremen'
    url = "http://192.168.26.98:8086"

    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    global write_api; write_api = client.write_api(write_options=SYNCHRONOUS)
    global query_api; query_api = client.query_api()

    # Clear player names in json
    data = json_read()
    data["name1"] = ""; data["name2"] = ""
    json_write(data)



# connection functions - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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

def server_send( keyword , delay = 10**-3 ):
    '''
    global function for sending data with the interface.

    "keyword" should be str type keyword.
    '''

    global port_lock
    global connection_type_object
    
    if connection_status == True:
        data = keyword.encode('utf-8')
        with port_lock :
            connection_type_object.sendall(keyword)
            time.sleep(delay)

def set_connection_status( set_status ):
    '''
    boolean set_status
    '''
    global connection_status
    connection_status = set_status



# game status control - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def set_status( arg_ , delay = 0):
    '''
    sys_status should be string: "init"|"wait_pre"|"ingame"|"wait_ingame"
    '''
    time.sleep( delay )
    global sys_status; global status_lock
    with status_lock:
        print("Status is:", arg_)
        sys_status = arg_
    


# reaction functions, what to do when specific game events occur - - - - - - - - - - - - - - - - - - 

def react_goal( player , connection_obj ): # reaction to event in goal_detection thread
    '''
    called by the exception in the goal sensor thread
    '''
    global goals_player1; global goals_player2
    global connection_status
    global port_lock
    global player1_name
    global player2_name
    global gameID
    
    set_status("wait_ingame")

    if player == 1: # add goal to the correct player
        goals_player1 += 1
        print("player 1 scored")
        database_write( gameID, player1_name, goals_player1)
    
    elif player == 2:
        goals_player2 += 1
        print("player 2 scored")
        database_write( gameID, player2_name, goals_player2)

    if (goals_player1 == 6 or goals_player2 == 6) or (goals_player1 == 5 and goals_player2 == 5): # check win condition
        
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
        

    else: # no win condition was met

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



# Database & Website functions - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def database_write( gameid, playername, goalcount ):
    '''
    string gameid = timestamp of first "ingame" in lvl2.pregame()
    string playername
    int goalcount
    '''
    point = (
    Point( gameid ) # gameid = timestamp
    .tag("Spieler", playername )
    .field("Tore", goalcount)
    )
    # Schreibe Daten in die InfluxDB
    write_api.write(bucket=bucket, org="Hochschule Bremen", record=point)


def json_read():
    with open('data.json', 'r') as file:
        return json.load(file)


def json_write(input):
    with open("data.json", "r") as file:
        json.dump(input, file, indent=4)