# -*- coding: utf-8 -*-
"""
The following functions are for use in different scripts and will carry the the
transfer of data between the Kicker PC, referenced as Server, and Drone PC,
referenced as Client. This documents serves as a collection of these functions
for the sake of accessibility and organisation.

auther : Marvin Otten

"""

#import globally needed libraries
import socket
import time
import threading
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

ver. 1.1.0
    
auther : Marvin Otten

'''

def server_interface():
    
    ## Initialize Interface
    
    # Create Serverside Socket objekt
    server_interface_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define IP adress and the used Port number and bind them to the Socket object
    server_add = ('localhost',10000)  #FIND IP ADRESS AND PORT!!!!!!!
    server_interface_obj.bind(server_add)
    
    
    # Create dictionary of connections | Reference Dictionary for all Connections !
    drone_connection = SIF.connection()
    extern_connection_1 = SIF.connection()
    extern_connection_2 = SIF.connection()
    dynamic_connection = SIF.connection()
    
    
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
    connect_dic_lock = thr.lock()
    
    # Create thread lock for access to port
    global port_lock
    port_lock = thr.lock()
    
    ## Interface managment threads
    # List of Threads for continues listen and receive function for all connections
    connect_threadlist = [thr.Thread(target= _server_listen,
                                      args= [server_interface_obj],
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




#%%

### server_listen( )
# Serverside continues search/"listen" for connections
'''
This function will be used as a thread and constantly searches for new connections.
If a connection is found it is inserted into the "connect_dic" dictionary as a tuple
of the created connection type object and the (address , Port) of the client as
provided by the .accept() function.

By providing the kwarg "target_address" it is possible to reserve a connection
slot for critical connections like the connection to the Drone Client.

The "connect_dic" dictionary includes 3 types of connections in 4 slots.
 - The first slot contains the reserved connection with the provided client address
 - The second and third slot contains external connections with undefined IPs
 - The fourth slot contains a dynamic connection. The dynamic connection is the
   last connection which was connected and not filled into the previous slots.
   If a new connection is detected, the current connection is closed and replaced
   by the new connection.

The main body of the function is a while loop which will be bound to some critical
variable which determines the operating status of the entire system. That way
an active search for new connections is always happening and allows for dynamic
changes of connection status.

arguments

    socket_objekt :     Imports the locally used socket object which is bounded
                        to the server.
                        
kwargs

    target_address:     Import an important IP adress which requires a reserved
                        connection slot


ver. 1.1.0

auther : Marvin Otten
'''

def _server_listen( socket_objekt , target_address = None ):
    
    global connect_dic
    global connect_dic_lock
    global ack_dic
    
    # Check for some operation determing variable
    some_var = False
    while some_var == True:
    # {start of loop
    
        # look for connection
        socket_objekt.listen(0)
    
        # wait/find connection
        client_address = None
        while client_address == None:
            # this loop might be useless as the .accept() function waits until
            # it found a conncetion. It might be handy for future operations and
            # should not impact the programm, so it stays for now.
            
            # create conncetion object
            connection_type_objekt , client_address = socket_objekt.accept()
        
        # with connect_dic_loc access to connect_dic is granted
        with connect_dic_lock:
            # check if client is drone client
            if client_address == target_address:
                drone_connection = SIF.connection( connection_type_objekt , ack_dic )
                connect_dic['drone'] = drone_connection
            
            # check if external connection/ non system critical connection is open
            elif connect_dic['extern1'].server_connection_obj == None:
                extern_connection_1 = SIF.connection( connection_type_objekt , ack_dic )
                connect_dic['extern1'] = extern_connection_1
            
            # check if external connection/ non system critical connection is open
            elif connect_dic['extern2'].server_connection_obj == None:
                extern_connection_2 = SIF.connection( connection_type_objekt , ack_dic )
                connect_dic['extern2'] = extern_connection_2
            
            # dynamic connection if external connections are already used
            else :
                if connect_dic['dynamic'].server_connection_obj != None:
                    connect_dic['dynamic'].close()
                dynamic_connection = SIF.connection( connection_type_objekt , ack_dic )
                connect_dic['dynamic'] = dynamic_connection
                
            
        
    # end of loop}
    
    return




#%%

### server_recv_man()
# Serverside receive function to check for incoming data
'''
This function creates threads for each connection in the "connect_dic" dictionary.
Each thread runs the function "server_recv()" which then handles the execution
of receiving data and interpreting it's content.

This function assigns the keys from the "connect_dic" dictionary to each thread.
The values from these keys are updated inside the threads which also contain the
while loop for continues operation.

ver. 1.2.0
    
auther : Marvin Otten

'''
def _server_recv_man():
    
    global connect_dic
    
    # Create list of threads for each connection
    recv_threadlist = []
    for connection_type in connect_dic:
        recv_threadlist.append(thr.Thread(target= _server_recv,
                                              args= [ connection_type ],
                                              kwargs= {}))
    
    #start threats
    for thread in recv_threadlist:
        thread.start()
        
    #wait for threads to join once programm is finished | thread internal check
    for thread in recv_threadlist:
        thread.join()
            
    return




#%%

### server_recv()
# Serverside receive function

'''
This function will recieve all messages from a given connection from the "connect_dic".
At first it will check if a connection is present. If that is case, the function
can receive a max 1024 long string which will be decoded bei utf-8 format. After
decoding the data is checked for it's content. First if there was a message at all,
followed up by a check if a keyword was received and lastly if a acknowledgment was
received. After that the funtion will once again check if the connection exists.

There has not been a collision check implemented yet.

arguments

    connection_type:    Provides the key for the connection_type_object from
                        "connect_dic" from which a message is suppose to be
                        received from.
                        

ver. 1.0.1
    
auther : Marvin Otten

'''
def _server_recv( connection_type ):
    
    global connect_dic
    
    global ack_dic
    
    # Check for some operation determing variable
    some_var = False
    while some_var == True:
    # {start of loop
        
        # if connection has not been established, continue
        if connect_dic[ connection_type ]._connection_status() == False:
            time.sleep(1)
            continue
    
        # if Connection exists, receive 1024 sized string
        elif connect_dic[ connection_type ]._connection_status() == True:
             data = connect_dic[ connection_type ]._recv(1024)
        
        
        # if weird connection_type_object appears, send Error to cmd, continue
        else :
            print('Error: undetermined Connection :', connect_dic[ connection_type ] )
            continue
        
        _data_interpret( data , connection_type )
        
        return
    


#%%
def _data_interpret( data , connection_type ):
    
    connection_ph = connect_dic[ connection_type ]
    keyword_ph = connection_ph.keyword_class_dic
    
    # check if nothing was send
    if data == '': return

    # check if data was keyword
    for keyword in ack_dic:             #take ack dic from connection attribute ack_dic!!!
        #send acknowledgement
        if data == keyword:
            with port_lock: connection_ph.send_thread( ack_dic[ keyword ] )
            
            # Call reaction function
            keyword_ph[keyword].react
            return
            
        # check if data was acknowledgment
        elif data == ack_dic[keyword]:             #take ack dic from connection attribute ack_dic!!!
            # if timeout in send function was -1 then keyword_ph[keyword].ack_status = None and no reaction is triggered!
            if keyword_ph[keyword].ack_status == False :
                keyword_ph[keyword].ack_status = True
                return
            
        else:
            # data has not been recognised as a keyword or acknowledgement
            print('Undetermined message:', data)
            continue
                
    # end of loop}
    
    return


    

