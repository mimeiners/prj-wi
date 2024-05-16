"""

Level 2
interface for sending keywords/receiving ACKs

"""

__author__ = "Marvin Otten"
__version__ = "1.0.3.2"
__status__ = "WIP"

#import globally needed libraries
import socket
import time
import threading
import LVL3_classes as lvl3


#%%

'''

Desc:

This function is called in the excuting function interface()
and should only be called there. After a connection is established
this function runs as a Thread parallel to _ping()

Func:

This function allows for continuous receiving of messages.
The received data is decoded (utf-8) and given as an argument
to the function _data_interpret which interprets the data based
on systemwide keywords. Afterwards the function receives a new message.

The included while loop for continues operation does not include
a condition but loops indefintly (v. 1.0.3.1). Ther is no return.
'''


def _recv():

    
    global connection_type_objekt
    
    while True:
    # {start of loop

        data = connection_type_objekt.recv(1024)
        data = data.decode('utf-8')
        
        _data_interpret( data )
    


#%%

'''
Desc:

This function is called in _recv(). While excuting, _recv() is blocked.

Func:

The argumented
'''

def _data_interpret( data ):

    global port_lock

    global ack_dic

    global connection_type_objekt
    
    
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

                 
def _keyword_react( keyword ):
    
    if keyword == 'ping':
        pass

    elif keyword == "notify_drone_powered":
        pass

    elif keyword == 'notify_drone_connected':
        lvl3.react_drone_connected()
        pass
    
    elif keyword == 'notify_start_permission':
        pass
    
    elif keyword == 'notify_gamestart':
        lvl3.react_drone_wants_gamestart()
        pass
    
    elif keyword == 'notify_newgoal':
        pass
    
    elif keyword == 'notify_foul':
        pass
    
    elif keyword == 'notify_gameover':
        pass
    
    elif keyword == 'please_wait':
        lvl3.react_drone_pleasewait()
        pass
    
    elif keyword == 'please_resume':
        lvl3.react_drone_pleaseresume()
        pass


def _ack_react( ack ):

    import LVL3_classes as lvl3

    if ack == 'hi':
        
        lvl3.set_connection_status(True)

        pass
        
    elif ack == 'connecting_drone':
        pass
    
    elif ack == 'waiting_for_startbutton':
        pass
    
    elif ack == 'positioning_drone':
        pass
    
    elif ack == 'game_started':
        pass
    
    elif ack == 'received_newgoal':
        pass
    
    elif ack == 'received_foul':
        pass
    
    elif ack == 'received_gamover':
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
    
    import LVL3_classes as lvl3

    global connection_type_objekt
    
    global port_lock
    
    
    ping = "ping"
    ping = ping.encode('utf-8')
    
    while True:
        with port_lock: connection_type_objekt.sendall( ping )
        lvl3.set_connection_status(False)
        time.sleep(1)



    
#%%

'''
desc
'''



def interface():

    import LVL3_classes as lvl3

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

    lvl3.set_connection_status( False )

    # Create Serverside Socket objekt
    server_interface_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define IP adress and the used Port number and bind them to the Socket object
    server_interface_obj.bind(('localhost' , 10000))


    # look for connection
    server_interface_obj.listen(0)

            
    # create conncetion object
    global connection_type_objekt
    connection_type_objekt , client_address = server_interface_obj.accept()
    lvl3.set_connection_status( True )


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
    return

