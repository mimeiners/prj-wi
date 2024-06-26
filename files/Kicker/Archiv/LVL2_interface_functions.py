<<<<<<< HEAD
# -*- coding: utf-8 -*-
=======
"""

LEVEL 2
interface stuff

> obsolete
"""

__author__ = "Marvin Otten"
__version__ = "1.1.1"
__status__ = "obsolete"


"""
The following functions are for use in different scripts and will carry the the
transfer of data between the Kicker PC, referenced as Server, and Drone PC,
referenced as Client. This documents serves as a collection of these functions
for the sake of accessibility and organisation.

auther : Marvin Otten

"""

>>>>>>> 6b8d4f194d8dd10a17cb91c97f92bbe4ee994e11
#import globally needed libraries
import socket
import time
import threading
<<<<<<< HEAD
=======
import threading as thr
import LVL3_classes as SIF

    
#%%

### server_interface()
# Serverside main implementation of interface
'''
This function defines the serverside connection. The function is designed to
operate inside a thread and will handle the connection to other devices inside
the local network aswell as receiving messages.

The operation order first initializes some needed variables or objects. The operations
for creating connections and receiving messages is handled in the functions
"server_listen()" and "server_recv()". Both functions are executed in threads to
allow for parallel execution and handling of each individual connection.

While "server_interface" does not contain any loops, the operating functions do.
A continues execution is therefore secured inside the functions and can be changed
individualy.

The dictionary for acknowledgment management is initialised and will be updated
by the "server_recv()" function, based on which acknowledgment message has
been received. The function which send the first message will reset the flag to
None.

'''

def server_interface():
    
    while SIF.use_interface == False:
        time.sleep(1)
    
    ## Interface managment threads
    # List of Threads for continues listen and receive function for all connections
    connect_threadlist = [thr.Thread(target= _server_listen,
                                      args= [SIF.server_interface_obj],
                                      kwargs= { ('Client_IP_Adress as str' , 'Port as int') }),   #FIND IP ADRESS AND PORT!!
                          
                          thr.Thread(target= _server_recv_man,
                                      args= [],
                                      kwargs= {})]
    
    #start threats
    for thread in connect_threadlist:
        thread.start()
    
    #wait for threads to join once programm is finished | thread internal check
    for thread in connect_threadlist:
        thread.join()  
    
    return


>>>>>>> 6b8d4f194d8dd10a17cb91c97f92bbe4ee994e11


#%%


'''
desc
'''
def _recv():
    
    global connection_type_objekt
    
    while True:
    # {start of loop

        data = connection_type_objekt.recv(1024)
        data = data.decode()
        
        _data_interpret( data )
        
    return
    


#%%

'''
desc
'''

def _data_interpret( data ):

    global port_lock

    global ack_dic

    global connection_type_objekt
    
    global connection_status
    
    # check if nothing was send
    if data == '': return

    # check if data was keyword
    for keyword in ack_dic:             #take ack dic from connection attribute ack_dic!!!
    
        #send acknowledgement
        if data == keyword:
            ack = ack_dic[ keyword ].encode('utf-8')
            with port_lock: connection_type_objekt.sendall( ack )
            print('here is keyword : ', data)
            
            _keyword_react( data )
            
            return
            
        # check if data was acknowledgment
        elif data == ack_dic[ keyword ]:
            print('here is ack: ', data)
            
            _ack_react( data )
            
            return
        
            
        else:
            # data has not been recognised as a keyword or acknowledgement
            print('Undetermined message:', data)
            return
                
    # end of loop}
    
    return

                 
def _keyword_react(keyword):
    
    if keyword == 'ping':
        pass
        
    elif keyword == 'notify_drone_connect':
        pass
    
    elif keyword == 'notify_start_permission':
        pass
    
    elif keyword == 'notify_gamestart':
        pass
    
    elif keyword == 'notify_newgoal':
        pass
    
    elif keyword == 'notify_foul':
        pass
    
    elif keyword == 'notify_gameover':
        pass
    
    elif keyword == 'please_wait':
        pass
    
    elif keyword == 'please_resume':
        pass
    
    return



def _ack_react( ack ):
    if ack == 'hi':
        global connection_status
        connection_status = True
        pass
        
    elif ack == 'connection_established':
        pass
    
    elif ack == 'drone_in_position':
        pass
    
    elif ack == 'game_started':
        pass
    
    elif ack == 'received_newgoal':
        pass
    
    elif ack == 'received_foul':
        pass
    
    elif ack == 'received_gameover':
        pass
    
    elif ack == 'waiting':
        pass
    
    elif ack == 'gaming':
        pass
    
    return




#%%

'''
desc
'''

def _ping():
    
    global connection_type_objekt
    
    global ack_dic
    
    global connection_status
    
    global port_lock
    
    
    ping = "ping"
    ping = ping.encode('utf-8')
    
    while True:
        with port_lock: connection_type_objekt.sendall( ping )
        connection_status = False
        time.sleep(1)
        print(connection_status)



    
#%%

'''
desc
'''





## Initialize Interface

# Create acknowledgment dictionary which pairs up keywords with acknowledgment
ack_dic = {'ping' : 'hi',
           'notify_drone_connect' : 'connection_established',
           'notify_start_permission' : 'drone_in_position',
           'notify_gamestart' : 'game_started',
           'notify_newgoal' : 'received_newgoal',
           'notify_foul' : 'received_foul',
           'notify_gameover' : 'received_gameover',
           'please_wait' : 'waiting',
           'please_resume' : 'gaming'}





# Create thread lock for access to port
global port_lock ; port_lock = threading.Lock()

global connection_status ; connection_status = False

# Create Serverside Socket objekt
server_interface_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define IP adress and the used Port number and bind them to the Socket object
server_interface_obj.bind(('localhost' , 10000))


# look for connection
server_interface_obj.listen(0)

        
# create conncetion object
global connection_type_objekt
connection_type_objekt , client_address = server_interface_obj.accept()
connection_status = True


if_threadlist = [threading.Thread(target= _ping,
                                  args= [],
                                  kwargs= {}),
                      
                 threading.Thread(target= _recv,
                                  args= [],
                                  kwargs= {})]

#start threats
for thread in if_threadlist:
    thread.start()
    
#wait for threads to join once programm is finished | thread internal check
for thread in if_threadlist:
    thread.join()
  