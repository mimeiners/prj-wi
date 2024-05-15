"""

Level 3
This file includes system wide used functions and variables

"""

__author__ = "Lukas Haberkorn", "Marvin Otten"
__version__ = "2.0.0"
__status__ = "WIP"


import time
import threading


def init():
    '''
    Has to be run before all other level 3 functions to initialize global variables
    '''
    global goals_player1; goals_player1 = 0
    global goals_player2; goals_player2 = 0
    global sys_status; sys_status = "init"
    global status_lock; status_lock = threading.Lock()
    print("Status is: init")
 


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

def react_goal( player , connection_obj ): # reaction to event in goal_detection thread
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


def react_foul( connection_obj ): # reaction to event in foul_detection thread
    '''
    called by the exception in the foul sensor thread
    '''
    set_status("wait_ingame")
    if connection_obj.connection_status == True:
        connection_obj.send( "notify_foul", 3) # sending keyword for foul
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