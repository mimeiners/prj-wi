# -*- coding: utf-8 -*-
"""
Created on Wed May 15 06:57:01 2024

@author: User
"""

import time
import socket as st
import threading


#%%

def _recv():
    
    end = 0
    while True:
    # {start of loop
        try :
            data = client.recv(1024)
            data = data.decode('utf-8')
            print('data received: ', data)
            _data_interpret( data )
        except: 
            if end > 10:break
            else:
                end +=1 
                time.sleep(0.33)
                continue
        

#%%

def _data_interpret( data ):

    global port_lock

    global ack_dic

    global client
    
    # check if nothing was send
    if data == '': return

    # check if data was keyword
    for keyword in ack_dic:
    
        #send acknowledgement
        if data == keyword:
            ack = ack_dic[keyword]
            ack = ack.encode('utf-8')
            client_send(ack)

            _keyword_react( data )
            return
            
        # check if data was acknowledgment
        elif data == ack_dic[keyword]:

            _ack_react(data)
            return
            
    # data has not been recognised as a keyword or acknowledgement
    print('Undetermined message:', data)
                
    # end of loop}
    
    return

#%%

def _keyword_react( keyword ):
    
    if keyword == 'ping':
        pass

    elif keyword == "notify_drone_powered":
        pass

    elif keyword == 'notify_drone_connected':
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


'''
_ack_react( ack )

'''

def _ack_react( ack ):

    import LVL3_classes as lvl3

    if ack == 'hi':
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

def client_send( keyword , delay = 10**-3 ):
    '''
    global function for sending data with the interface.

    "keyword" should be str type keyword.
    '''

    global port_lock
    global client
    

    with port_lock :
        client.sendall(keyword)
        time.sleep(delay)

#%%


# MAIN Routine

###Initiliazing
#Create Socket object
client = st.socket(st.AF_INET, st.SOCK_STREAM)

ack_dic = {'ping' : 'hi',
           'notify_drone_connect' : 'connection_established',
           'notify_start_permission' : 'drone_in_position',
           'notify_gamestart' : 'game_started',
           'notify_newgoal' : 'received_newgoal',
           'notify_foul' : 'received_foul',
           'notify_gameover' : 'received_gameover',
           'please_wait' : 'waiting',
           'please_resume' : 'gaming'}

###Connection
#give target address
server_address = ('localhost', 10000)
print ('connecting to %s port %s' % server_address)
#connect to address
while True:
    try:
        client.connect(server_address)
        break
    except: continue


global port_lock ; port_lock = threading.Lock()

#%%

if_threadlist = [threading.Thread(target= _recv,
                                  args= [],
                                  kwargs= {})]
#start threats
for thread in if_threadlist:
    thread.start()
    
#wait for threads to join once programm is finished | thread internal check
for thread in if_threadlist:
    thread.join()



client.close()




