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

ver. 1.0.0
    
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
    
    
    # List of Threads for continues listen and receive function for all connections
    connect_threadlist = [thr.Thread(target= server_listen,
                                      args= [server_interface_obj, connect_dic],
                                      kwargs= { ('Client_IP_Adress as str' , 'Port as int') }),   #FIND IP ADRESS AND PORT!!
                          
                          thr.Thread(target= server_recv,
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
Each thread runs the function "server_connect_man()" which then handles the execution
of receiving data and interpreting it's content.

So this function serves as a place holder for these threads in the function
"server_interface()", which represents the main function for the interface. It
also assigns the keys from the "connect_dic" dictionary to each thread. The values
from these keys are updated inside the threads which also contain the while loop
for continues operation.

ver. 1.0.0
    
auther : Marvin Otten

'''
def server_recv():
    
    global connect_dic
    
    # Create list of threads for each connection
    recv_threadlist = []
    for connection_type in connect_dic:
        recv_threadlist.append(thr.Thread(target= server_connect_man,
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
# Not yet finished!!!!!!!!!!!
def server_connect_man( connection_type ):
    
    global connect_dic
    
    # Check for some operation determing variable
    some_var = False
    while some_var == True:
    # {start of loop

        if type( connect_dic[connection_type] ) == tuple:
            connection_type_objekt = connect_dic[connection_type][0]
            data = connection_type_objekt.recv(1024)
            data.decode('utf-8')
            
        elif connection_type == None: return
        
        else : print('Error: undetermined Connection')
        
        #Data if/else Tree here!
    
    
    return
