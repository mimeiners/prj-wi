# -*- coding: utf-8 -*-
"""
This file is suppose to include system wide used function

Level 3

"""

# game status control - - - - - - - - - - - - - - - - - - - -
'''
desc
'''
global game_running; game_running = False
global game_paused;  game_paused  = False

def set_status(change):
    global game_running
    global game_paused
    match change:
        case "start":
            print("ℹ️ Game has been started")
            game_running = True
        case "end":
            print("ℹ️ Game has been finished")
            game_running = False
        case "pause":
            print("ℹ️ Game has been paused")
            game_paused = True
        case "resume":
            print("ℹ️ Game has been resumed")
            game_paused = False
    

#%%

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
        super().__init__(self.reaktion)




#%%
#import globally needed libraries
import socket
import time
import threading
import threading as thr

# Create thread lock for access to connect_dic
global connect_dic_lock
connect_dic_lock = thr.lock()

# Create thread lock for access to port
global port_lock
port_lock = thr.lock()
    
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
        
        self.server_connection_obj = server_connection_obj
        self.keyword_class_dic = self._keyword_checks( ack_dic )
        self.format_ = format_
        self.ack_dic = ack_dic
        
        #Chat GPT lässt grüßen
        self._connection_status = False
        self._thread = threading.Thread(target=self._ping_check)
        self._thread.daemon = True  # Der Thread wird als Hintergrundthread ausgeführt
        self._thread.start()
    


    #Thread which pings the client each second
    def _ping_check(self):
        while True:
            with port_lock: self.send('ping' , 1)
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
            with port_lock: self.server_connection_obj.sendall( message_encoded )
            
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
    
#%% reaction functions, they modify the While-bools to control tasks

