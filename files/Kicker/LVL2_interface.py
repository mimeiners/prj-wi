"""

LEVEL 2
interface for sending keywords/receiving ACKs

"""

__author__ = "Marvin Otten"
__version__ = "1.0.7"
__status__ = "WIP"

#import globally needed libraries
import time
import threading
import LVL3_classes as lvl3


#%%

'''
_recv()

Desc:   This function is called in the excuting function interface()
        and should only be called there. After a connection is established
        this function runs as a Thread parallel to _ping()

Func:   This function allows for continuous receiving of messages.
        The received data is decoded (utf-8) and given as an argument
        to the function _data_interpret which interprets the data based
        on systemwide keywords. Afterwards the function receives a new message.

        The included while loop for continues operation does not include
        a condition but loops indefintly (v. 1.0.4). There is no return.
'''


def _recv():

    while True:
    # {start of loop
        try:
            data = lvl3.connection_type_object.recv(1024)
            data = data.decode('utf-8')
            _data_interpret( data )
        except:pass
    


#%%

'''
_data_interpret( data )

Desc:   This function is called in _recv(). While excuting, _recv() is blocked.

Func:   The argumente is chaecked for content anf then compared to entries inside
        the ack_dic, which serves as a databse for all keywords and acknowledgemenets.
        If an keyword or a acknowledgement is detected the appropiate rection is called
        from the function _keyword_react() or _ack_react().

        Additionally, if a keyword is detected, an acknowledment is automatically send.

Argument:

data : str type object. Provided by _recv(). Needs to be decoded.
'''

def _data_interpret( data ):

    global ack_dic
    
    # check if nothing was send
    if data == '': return

    # check if data was keyword/ack
    for keyword in ack_dic:             #take ack dic from connection attribute ack_dic!!!
    
        # check if data is keyword
        if data == keyword:
            ack = ack_dic[ keyword ]
            #send acknowledgement
            lvl3.server_send( ack )

            # call react to keyword
            _keyword_react( str(data) )
            return
            
        # check if data was acknowledgment
        elif data == ack_dic[ keyword ]:
            # call react to acknowledgement
            _ack_react( data )
            return
                
    # end of loop}
    
    return


'''
_keyword_react( keyword )

Desc :  This function is called in _data_interpret and habours the reactions
        of a received keyword.

Func :  Based on the provided keyword, an if-based reaction is called.
        This function is only called if a keyword has been detected in _recv(),
        an else-condition is therfore not necessary but could help for debugging.

Arguments : 

keyword : str type object. Provided by _recv() if keyword is detected.
'''

def _keyword_react( keyword ):
    
    if keyword == 'ping':
        return

    elif keyword == "notify_drone_powered":
        return

    elif keyword == 'notify_drone_connected':
        lvl3.react_drone_connected(True)
        return
    
    elif keyword == 'notify_start_permission':
        return
    
    elif keyword == 'notify_gamestart':
        lvl3.react_drone_wants_gamestart(True)
        return
    
    elif keyword == 'notify_newgoal':
        return
    
    elif keyword == 'notify_foul':
        return
    
    elif keyword == 'notify_gameover':
        return
    
    elif keyword == 'please_wait':
        lvl3.react_drone_pleasewait()
        return
    
    elif keyword == 'please_resume':
        lvl3.react_drone_pleaseresume()
        return


'''
_ack_react( ack )

Desc :  This function is called in _data_interpret and habours the reactions
        of a received acknowledgement.

Func :  Based on the provided acknowledgement, an if-based reaction is called.
        This function is only called if a acknowledgement has been detected in _recv(),
        an else-condition is therfore not necessary but could help for debugging.

Arguments : 

keyword : str type object. Provided by _recv() if acknowledgement is detected.
'''

def _ack_react( ack ):

    if ack == 'hi':
        lvl3.ping_ack_flag = True
        lvl3.set_connection_status(True)
        return
        
    elif ack == 'connecting_drone':
        return
    
    elif ack == 'waiting_for_startbutton':
        return
    
    elif ack == 'positioning_drone':
        return
    
    elif ack == 'game_started':
        return
    
    elif ack == 'received_newgoal':
        return
    
    elif ack == 'received_foul':
        return
    
    elif ack == 'received_gamover':
        return
    
    elif ack == 'waiting':
        return
    
    elif ack == 'gaming':
        return

    return



#%%

'''
_ping()

Desc :  This function is called in the excuting function interface()
        and should only be called there. After a connection is established
        this function runs as a Thread parallel to _recv()

Func :  To check for an uninterrupted connection, a ping-keyword is send 
        every second. As long as the corresponding acknowledgement has not
        received, the global connection status is set to False. If the
        acknowledgement has been reeceived, it's corresponding
        reaction in _ack_react() will set the connection status to True.

        This function might change to only set the connection status to
        False once a NACK has been recieved.
'''

def _ping():
    
    ping = "ping"
    ping = ping.encode('utf-8')

    while True:
        try:
            with lvl3.port_lock:
                lvl3.connection_type_object.sendall( ping )
                lvl3.ping_ack_flag = False
                time.sleep(10**-3)
            time.sleep(0.999)
            #if ack not received, set connection_status to False
            if lvl3.ping_ack_flag == False: lvl3.set_connection_status(False)

        #if ping could not be sended, close connection, find new connection
        except Exception as e:
            print('ping not sended because %s \nconnection status is : %s' % ( e , lvl3.connection_status))
            lvl3.set_connection_status(False)
            lvl3.connection_type_object.close()
            lvl3._find_connection()


    
#%%

'''
desc
'''



def interface():

    # wait for connection
    while lvl3.connection_type_object == None:
        time.sleep(0.1)

    ## Initialize Interface

    # Create acknowledgment dictionary which pairs up keywords with acknowledgment
    global ack_dic
    ack_dic = {'ping' : 'hi',
               'notify_drone_powered' : 'connection_drone',
            'notify_drone_connected' : 'waiting_for_startbutton',
            'notify_start_permission' : 'positioning_drone',
            'notify_gamestart' : 'game_started',
            'notify_newgoal' : 'received_newgoal',
            'notify_foul' : 'received_foul',
            'notify_gameover' : 'received_gameover',
            'please_wait' : 'waiting',
            'please_resume' : 'gaming'}



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