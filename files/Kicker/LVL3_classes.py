"""

Level 3
This file includes system wide used functions

> commented out interface stuff in react_goal()
> custom exception not used anymore
"""

__author__ = "Lukas Haberkorn", "Marvin Otten"
__version__ = "1.1.2"
__status__ = "WIP"


import socket
import time
import threading
import threading as thr


def init():
    '''
    Has to be run before all other level 3 functions to initialize global variables
    '''
    
    global use_interface; use_interface = False # ONLY USED FOR TESTING
    
    global goals_player1; goals_player1 = 0 # might become obsolete with usage of the database, but can be left in after testing
    global goals_player2; goals_player2 = 0
    global sys_status; sys_status = "init"
    global status_lock; status_lock = threading.Lock()
    print("Status is: init")
    if use_interface:
        ## Initialize Interface

        # Create Serverside Socket objekt
        server_interface_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Define IP adress and the used Port number and bind them to the Socket object
        server_ip = socket.gethostbyname()
        server_add = ( server_ip , 10000 )  #FIND IP ADRESS AND PORT!!!!!!!
        server_interface_obj.bind(server_add)
        
        
        # Create dictionary of connections | Reference Dictionary for all Connections !
        drone_connection = connection()
        extern_connection_1 = connection()
        extern_connection_2 = connection()
        dynamic_connection = connection()
        
        
        global connect_dic
        connect_dic = {'drone' :  drone_connection,         # Connection type Objekt for Drone
                       'extern1' : extern_connection_1,        # Connection type Objekt for extern excess or future use
                       'extern2' : extern_connection_2,        # ...
                       'dynamic': dynamic_connection}         # Connection type Objekt for dynamic use. Description in server.listen() Header
        
        
        
        # Create acknowledgment dictionary which pairs up keywords with acknowledgment
        global ack_dic
        ack_dic = {'ping' : 'hi',
                   'notify_drone_connect' : 'connection_established',
                   'notify_start_permission' : 'drone_in_position',
                   'notify_gamestart' : 'game_started',
                   'notify_newgoal' : 'received_newgoal',
                   'notify_foul' : 'received_foul',
                   'notify_gameover' : 'received_gameover',
                   'please_wait' : 'waiting',
                   'please_resume' : 'gaming'}
    

    # Create thread lock for access to connect_dic
    global connect_dic_lock
    connect_dic_lock = thr.Lock()
    
    # Create thread lock for access to port
    global port_lock
    port_lock = thr.Lock()
    

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
    


# reaction functions, what to do when specific game events occur - - - - - - - - - - - - - - - - - - - -

def react_goal( player , connection_obj ):
    '''
    called by the exception in the goal sensor thread
    '''
    global goals_player1; global goals_player2
    set_status("wait_ingame")

    if player == 1: # add goal to the correct player
        goals_player1 += 1
        print("player 1 scored")
    
    elif player == 2:
        goals_player2 += 1
        print("player 2 scored")

    if (goals_player1 == 6 or goals_player2 == 6) or (goals_player1 == 5 and goals_player2 == 5): # check win condition
        # >>> UPDATE DATABASE HERE
#         if connection_obj.connection_status == True:
#             connection_obj.send( "notify_gameover", 3) # sending keyword for gameover
#         else:
#             time.sleep(10)
        print("##########\n A GAME HAS BEEN FINISHED with", goals_player1,":", goals_player2,"\n##########\n")
        time.sleep(5)
        set_status("wait_pre")
        goals_player1 = 0; goals_player2 = 0 # Resetting AFTER writing to database!!

    else: # no win condition was met
        # >>> UPDATE DATABASE HERE
#         if connection_obj.connection_status == True:
#             connection_obj.send( "notify_newgoal", 3) # sending keyword for new goal
#         else:
#             time.sleep(10)
        time.sleep(2)
        set_status("ingame")
        print("we continue with ", goals_player1,":", goals_player2)


def react_foul( connection_obj ):
    '''
    called by the exception in the foul sensor thread
    '''
    set_status("wait_ingame")
    if connection_obj.connection_status == True:
        connection_obj.send( "notify_foul", 3) # sending keyword for foul
    else:
        time.sleep(5)
    set_status("ingame")


def react_drone_connected(state):
    '''
    boolean argument
    '''
    global drone_connected; drone_connected = state
    print("Drone connected: ", drone_connected)


def react_drone_wants_gamestart(state):
    '''
    boolean argument
    '''
    global drone_wants_gamestart; drone_wants_gamestart = state
    print("Drone wants the game to start: ", drone_wants_gamestart)


#%%
# generate Exception  - - - - - - - - - - - - - - - - - - - -

"""
!!Initialize Exception class object!!

This class allows any user to create her/his own local Exception and raise it at
will. After importing this class, define your own Exception by setting

my_own_Exception = userdefined_Exception( reaction = my_Exception_function() )

and calling

raise my_own_Exception

anywhere in your programm. Then, inside your Exception handling, for Example an
"except" block, you can access all attributes of this class instance

except userdefine_Exception as e:
    e.reaktion

to call your function. If you don't want to call a function but simply refer to
an object like a varibale, list, array ... you can do so with the other class
attributes (you can use reaction aswell).

my_own_Exception = userdefined_Exception( att1|att2|att3 = my_object )


!!Add to initialized Exception class object!!

If you want to add something to an already established Exception you can do so
by calling the initialized class object and your desired attribute and redifine
at like a variable

my_own_Exception.reaction = my_new_Exception_function()
my_own_Exception.att1|att2|att3 = my_new_object


This Class has been brought to you by ChatGPT
"""
        
            
class userdefined_Exception(Exception):
    def __init__(self, reaction = None , att1 = None , att2 = None , att3 = None):
        self.reaction = reaction
        self.att1 = att1
        self.att2 = att2
        self.att3 = att3
        super().__init__(self.reaction)




#%%
# interface connection classes - - - - - - - - - - - - - - - - - - - -
"""
Desc
"""
# define current status and settings of a keyword
class keyword_class:
    
    def __init__(self, keyword, ack, keyword_func = None , ack_func = None , ack_TOE_func = None):
        
        self.keyword = keyword
        self.ack = ack
        self.ack_status =  None
        self.react = keyword_func
        self.ack_react = ack_func
        self.ack_TOE = ack_TOE_func

        
# automatically run a function in a thread
class Thread(threading.Thread):
    def __init__(self, t , *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()
    

# expand connection object for project
class connection( socket.socket , keyword_class , Thread ):
    
    def __init__(self , server_connection_obj = None , ack_dic = {} , format_ = 'utf-8'):
        
        global port_lock
        global connect_dic_lock
        
        self.server_connection_obj = server_connection_obj
        self.keyword_class_dic = self._keyword_checks( ack_dic )
        self.format_ = format_
        self.ack_dic = ack_dic
        self.port_lock = port_lock
        
        #Chat GPT lässt grüßen
        self._connection_status = False
        self._thread = threading.Thread(target=self._ping_check)
        self._thread.daemon = True  # Der Thread wird als Hintergrundthread ausgeführt
        self._thread.start()
    


    #Thread which pings the client each second
    def _ping_check(self):
        while True:
            with self.port_lock: self.send('ping' , 1)
            time.sleep(1)
    
    #retuen current connection Bool of this connection
    def connection_status(self):
        return self._connection_status



    # But in Thread for less script interference
    def send_thread(self , args ):
        Thread(self.send , args )
    
    # Send to connection patner and handle ACK
    def send(self, message, timeout = -1):
        try:
            message_encoded = message.encode( self.format_ )
            with self.port_lock: self.server_connection_obj.sendall( message_encoded )
            
            # If the message was a keyword -> acknowledgement management
            for keyword in self.ack_dic:
                if message == keyword and timeout != -1:
                    self._ack_check( message , timeout )
            return True
        
        except:
            return False

    # acknowledgement management
    def _ack_check(self, keyword, timeout):
        # set acknowledgment to False, waiting position
        self.keyword_class_dic[ keyword ].ack_status = False
        
        # wait for acknowledgment
        wait_time = 0
        while self.keyword_class_dic[ keyword ].ack_status == False and wait_time < timeout:
            time.sleep(0.1)
            wait_time += 0.1
        
        # react to ACK or NACK
        if wait_time >= timeout:
            self.keyword_class_dic[ keyword ].ack_TOE
            
        if wait_time < timeout:
            self.keyword_class_dic[ keyword ].ack_react
        
        # reset acknowledgment flag
        self.keyword_class_dic[ keyword ].ack_status = None


        
    
    
    #create keyword_class_dic containing the keyword settings classes
    def _keyword_checks(self, keyword_dic):
        keyword_class_dic = {}
        for keyword in keyword_dic:
            keyword_class_dic[ keyword ] = keyword_class( keyword , keyword_dic[keyword] )
            
        #define ping ack and nack reaction function
        keyword_class_dic[ 'ping' ].ack_react = self._ping_ack_react()
        keyword_class_dic[ 'ping' ].ack_TOE = self._ping_nack_react()
        
        return keyword_class_dic
     
    #define ping ack and nack reaction function
    def _ping_ack_react(self):
       self._connection_status = True
    def _ping_nack_react(self):
       self._connection_status = False
       
    
    # inner working recv function for call von server_recv
    def _recv(self, length):
        self.raw_data = self.server_connection_obj.recv( length )
        self.data = self.raw_data.decode( self.format_ )
        return self.data