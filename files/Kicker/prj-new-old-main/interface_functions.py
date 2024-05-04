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
import threading as thr

#%%

### server_interface()
# Serverside main implementation of connection
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
    
    ## Initialize Socket on Serverside
    # Create Serverside Socket objekt
    server_interface_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define IP adress and the used Port number and bind them to the Socket object
    server_add = ('localhost',10000)  #FIND IP ADRESS AND PORT!!!!!!!
    server_interface_obj.bind(server_add)
    
    
    # Create dictionary of connections | Reference Dictionary for all Connections !
    global connect_dic
    connect_dic = {'drone' :  None,         # Connection type Objekt for Drone
                   'extern1' : None,        # Connection type Objekt for extern excess or future use
                   'extern2' : None,        # ...
                   'dynamic': None}         # Connection type Objekt for dynamic use. Description in server.listen() Header
    
    
    # Create acknowledgment status dictionary which saves the status of an received acknowledgment
    global ack_status_dic
    ack_status_dic = {'hi' : False,
               'drone_in_position' : False,
               'received_newgoal' : False,
               'received_foul' : False,
               'received_gameover' : False,
               'waiting' : False,
               'gaming' : False}
    
    
    # Create acknowledgment dictionary which pairs up keywords with acknowledgment
    global ack_dic
    ack_dic = {'ping' : ['hi'],
               'notify_gamestart' : ['drone_in_position'],
               'notify_newgoal' : ['received_newgoal'],
               'notify_foul' : ['received_foul'],
               'notify_gameover' : ['received_gameover'],
               'please_wait' : ['waiting'],
               'please_resume' : ['gaming']}
    
    
    # Create thread lock for access to connect_dic
    global connect_dic_lock
    connect_dic_lock = thr.lock()
    
    ## Interface managment threads
    # List of Threads for continues listen and receive function for all connections
    connect_threadlist = [thr.Thread(target= server_listen,
                                      args= [server_interface_obj, connect_dic],
                                      kwargs= { ('Client_IP_Adress as str' , 'Port as int') }),   #FIND IP ADRESS AND PORT!!
                          
                          thr.Thread(target= server_recv_man,
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


ver. 1.0.0

auther : Marvin Otten
'''

def server_listen( socket_objekt , target_address = None ):
    
    global connect_dic
    global connect_dic_lock
    
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
                connect_dic['drone'] = (connection_type_objekt , client_address)
            
            # check if external connection/ non system critical connection is open
            elif connect_dic['extern1'] == None:
                connect_dic['extern1'] = (connection_type_objekt , client_address)
            
            # check if external connection/ non system critical connection is open
            elif connect_dic['extern2'] == None:
                connect_dic['extern2'] = (connection_type_objekt , client_address)
            
            # dynamic connection if external connections are already used
            else :
                dyn_con = connect_dic['dynamic'][0]
                dyn_con.close()
                connect_dic['dynamic'] = (connection_type_objekt , client_address)
        
    # end of loop}
    
    return




#%%

### server_recv()
# Serverside receive function to check for incoming data
'''
This function creates threads for each connection in the "connect_dic" dictionary.
Each thread runs the function "server_recv()" which then handles the execution
of receiving data and interpreting it's content.

This function assigns the keys from the "connect_dic" dictionary to each thread.
The values from these keys are updated inside the threads which also contain the
while loop for continues operation.

ver. 1.1.0
    
auther : Marvin Otten

'''
def server_recv_man():
    
    global connect_dic
    
    # Create list of threads for each connection
    recv_threadlist = []
    for connection_type in connect_dic:
        recv_threadlist.append(thr.Thread(target= server_recv,
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

# Serverside receive function

'''
This function will recieve all messages from a given connection from the "connect_dic".
At first it will check if a connection is present. If that is case, the function
can receive a max 1024 long string which will be decoded bei utf-8 format. After
decoding the data is checked for it's content. First if there was a message at all,
followed up by a check if a keyword was received and lastly if a acknowledgment was
received. After that the funtion will once again check if the connection exists.

There has not been a collision check implemented yet.

ver. 1.0.0
    
auther : Marvin Otten

'''
def server_recv( connection_type ):
    
    global connect_dic
    
    global ack_status_dic
    
    global ack_dic
    
    # Check for some operation determing variable
    some_var = False
    while some_var == True:
    # {start of loop
        
    
        # if Connection exists, receive 1024 sized string
        if type( connect_dic[connection_type] ) == tuple:
            connection_type_objekt = connect_dic[connection_type][0]
            data = connection_type_objekt.recv(1024)
            data = data.decode('utf-8')
        
        # if connection has not been established, continue
        elif connection_type == None: continue
        
        # if weird connection_type_object appears, send Error to cmd, continue
        else :
            print('Error: undetermined Connection type :', type( connect_dic[connection_type] ))
            continue
        
        
        # Data if/else Tree here! Interpret all messages!
        
        # check if nothing was send
        if data == '': continue
        
        # check if data was keyword
        for keyword in ack_dic:
            #send acknowledgement
            if data == keyword:
                connection_type_objekt.sendall( ack_dic[keyword][0])
                
                # Insert reaction function here, call from ack_dic[keyword][1]
                react_to_keyword_function_call = None
                continue
        
        # check if data was acknowledgment
        #could be implemented in keyword check
        for acknowledgment in ack_status_dic:
            
            #set acknowledgment to True
            if data == acknowledgment and ack_status_dic[acknowledgment] == False :
                ack_status_dic[acknowledgment] = True
                continue
        
        # data has not been recognised as a keyword or acknowledgement
        print('Undetermined message:', data)
        continue
                
    # end of loop}
    
    return




#%%

#serverside send function. Might be updated to systemwide send function

def server_sendall( message_str , connection_type_object = connect_dic['drone'][0], timeout = 0):
    
    import ack_status_dic
    
    # connection not established, continue with normal operation
    if connection_type_object == None : return
    
    # send message
    message_str = message_str.encode('utf-8')
    connection_type_object.sendall(message_str)
    
    # set acknowledgment to False, waiting position
    ack_status_dic[message_str] = False
    
    # wait for acknowledgment
    wait_time = 0
    while ack_status_dic[message_str] == False or wait_time < timeout:
        time.sleep(0.1)
        wait_time += 0.1
    
    # reset acknowledgment flag
    ack_status_dic[message_str] = None
    
    #if timeout was reached react
    if wait_time < timeout:
        reaction_to_timeout = None
    
    return
    




#%%

def client_interface():
    
    ## Initialize Socket on Serverside
    # Create clientside Socket objekt
    client_interface_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define IP adress and the used Port number of the target Server
    server_add = ('localhost',10000)  #FIND IP ADRESS AND PORT!!!!!!!
    # Connect to Server
    some_var = False
    while some_var == True:
        try: client_interface_obj.connect(server_add)
        except: continue
    

    # Create acknowledgment status dictionary which saves the status of an received acknowledgment
    global ack_status_dic
    ack_status_dic = {'hi' : False,
                'drone_in_position' : False,
                'received_newgoal' : False,
                'received_foul' : False,
                'received_gameover' : False,
                'waiting' : False,
                'gaming' : False}
    
    
    # Create acknowledgment dictionary which pairs up keywords with acknowledgment
    global ack_dic
    ack_dic = {'ping' : ['hi'],
               'notify_gamestart' : ['drone_in_position'],
               'notify_newgoal' : ['received_newgoal'],
               'notify_foul' : ['received_foul'],
               'notify_gameover' : ['received_gameover'],
               'please_wait' : ['waiting'],
               'please_resume' : ['gaming']}
    
    
    
    ## Interface managment threads
    # List of Threads for continues recieve. Implemented as list to allow for easy expansion
    connect_threadlist = [thr.Thread(target= client_recv,
                                      args= [ client_interface_obj ],
                                      kwargs= {})]
    
    #start threats
    for thread in connect_threadlist:
        thread.start()
    
    #wait for threads to join once programm is finished | thread internal check
    for thread in connect_threadlist:
        thread.join()  
    
    return




#%%%

# Clientside receive function

def client_recv( connection_type_object ):
        
    global connect_dic
    
    global ack_status_dic
    
    global ack_dic
    
    # Check for some operation determing variable
    some_var = False
    while some_var == True:
    # {start of loop
        
        data = connection_type_object.recv(1024)
        data = data.decode('utf-8')
        
        
        # Data if/else Tree here! Interpret all messages!
        
        # check if nothing was send
        if data == '': continue
        
        # check if data was keyword
        for keyword in ack_dic:
            #send acknowledgement
            if data == keyword:
                connection_type_object.sendall( ack_dic[keyword][0] )
                
                # Insert reaction function here, call from ack_dic[keyword][1]
                react_to_keyword_function_call = None
                continue
        
        # check if data was acknowledgment
        #could be implemented in keyword check
        for acknowledgment in ack_status_dic:
            
            #set acknowledgment to True
            if data == acknowledgment and ack_status_dic[acknowledgment] == False :
                ack_status_dic[acknowledgment] = True
                continue
        
        # data has not been recognised as a keyword or acknowledgement
        print('Undetermined message:', data)
        continue
                
    # end of loop}
    
    return