# -*- coding: utf-8 -*-
"""
The following functions are for use in different scripts and will carry the the
transfer of data between the Kicker PC, referenced as Server, and Drone PC,
referenced as Client. This documents serves as a collection of these functions
for the sake of accessibility and organisation.
"""

#import globally needed libraries
import socket
import threading as thr

#%%

# Serverside main implementation of connection
'''
This function defines the serverside connection. The function is designed to
operate inside a threat and will handle the connection to other devices inside
the local network aswell as receiving messages.

Inner workings:
    
'''

def server_interface():
    
    ## Initialize Socket on Serverside
    # Create Serverside Socket objekt
    server_interface_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define IP adress and the used Port number and bind them to the Socket object
    server_add = ('localhost',10000)  #FIND IP ADRESS AND PORT!!!!!!!
    server_interface_obj.bind(server_add)
    
    
    # Create dictionary of connections
    connect_dic = {'drone' :  None,         # Connection type Objekt for Drone
                   'extern1' : None,        # Connection type Objekt for extern excess or future use
                   'extern2' : None,
                   'dynamic': None}
    
    

    
    return

#%%

# Serverside continues search/"listen" for connections
'''
This function will be used as a thread and constantly searches for new connections.
If a connection is found it is inserted into the connect_dic dictionary as a tuple
of the created connection type object and the address of the client as provided
by the .accept() function.

By providing the kwarg "target_address" it is possible to reserve a connection
slot for critical connections like the connection to the drone.

The connect_dic dictionary includes 3 types of connections in 4 slots
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
                        
    connect_dic   :     Imports the dictionary containing the connection objects
                        and the client address of that connection. It is this
                        dictionary which provides the connection type objects
                        for future use in different parts of the system.
                        
kwargs

    target_address:     Import an important IP adress which re
'''

def server_listen(socket_objekt, connect_dic, target_address = None):
    # Check for some operation determing variable
    some_var = False
    while some_var == True:
    #{start of loop
    
        # look for connection
        socket_objekt.listen(0)
    
        # wait/find connection
        client_address = None
        while client_address == None:
    
            # create conncetion object
            connection, client_address = socket_objekt.accept()
        
        #there is probably a smarter way but this is easy and observable
        # check if client is drone client
        if client_address == target_address:
            connect_dic['drone'] = (connection , client_address)
        
        # check if external connection/ non system critical connection is open
        elif connect_dic['extern1'] == None:
            connect_dic['extern1'] = (connection , client_address)
        
        # check if external connection/ non system critical connection is open
        elif connect_dic['extern2'] == None:
            connect_dic['extern2'] = (connection , client_address)
        
        # dynamic connection if external connections are already used
        else :
            dyn_con = connect_dic['dynamic'][0]
            dyn_con.close()
            connect_dic['dynamic'] = (connection , client_address)

        
    #end of loop}
    
    return