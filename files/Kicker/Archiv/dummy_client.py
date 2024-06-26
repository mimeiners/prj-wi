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
    
    while True:
    # {start of loop
        try :
            data = client.recv(1024)
            data = data.decode('utf-8')
            print('data received in _recv: ', data)
            _data_interpret( data )
        except: 
            continue
    # end of loop}
        

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
            client_send(ack)
            print('sended ack : ', ack)
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
        print('RECEIVED : notify_drone_powered')
        time.sleep(0)
        client_send('notify_drone_connected')
        print('SEND : notify_drone_connected')
        pass

    elif keyword == 'notify_drone_connected':
        pass
    
    elif keyword == 'notify_start_permission':
        print('RECEIVED : notify_start_permission')
        time.sleep(0)
        client_send('notify_gamestart')
        print('SEND : notify_gamestart')
        pass
    
    elif keyword == 'notify_gamestart':
        pass
    
    elif keyword == 'notify_newgoal':
        #print('RECEIVED : notify_newgoal (LETS GO)')
        #client_send('please_wait')
        #print('SEND : please_wait (kicker goal)')
        pass
    
    elif keyword == 'notify_foul':
        #print('RECEIVED : notify_foul (MAAAAAANNNN)')
        #client_send('please_wait')
        #print('SEND : please_wait (kicker foul)')
        pass
    
    elif keyword == 'notify_gameover':
        print('RECEIVED : notify_gameover :(')
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
        print('ping gamin')
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
        print('RECEIVED : waiting')
        time.sleep(0)
        client_send('please_resume')
        print('SEND : please_resume')
        pass
    
    elif ack == 'gaming':
        print('RECEIVED : gaming (Engineer Gaming)')
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
        keyword = keyword.encode('utf-8')
        client.sendall(keyword)
        time.sleep(delay)

#%%

#%%

# -*- coding: utf-8 -*-
"""
Created on Tue May 21 13:40:27 2024

@author: Achraf Ben Mariem
"""

import subprocess

def display_website_fullscreen():
    # URL der Webseite
    url = "https://www.example.com"  # Ersetze dies durch die URL der Webseite, die du anzeigen möchtest

    # Öffnen der URL im Webbrowser im Vollbildmodus
    try:
        browser_path = "/usr/bin/firefox"  # Pfad zu Firefox-Exe-Datei
        subprocess.Popen([browser_path, "--kiosk", url])
    except Exception as e:
        print(f"Fehler beim Öffnen des Browsers: {e}")


def filler():
    # Aufrufen der Funktion
    display_website_fullscreen()
    return


# MAIN Routine

###Initiliazing
#Create Socket object
client = st.socket(st.AF_INET, st.SOCK_STREAM)

ack_dic = {'ping' : 'hi',
           'notify_drone_powered' : 'connection_drone',
           'notify_drone_connected' : 'waiting_for_startbutton',
           'notify_start_permission':'positioning_drone',
           'notify_gamestart' : 'game_started',
           'notify_newgoal' : 'received_newgoal',
           'notify_foul' : 'received_foul',
           'notify_gameover' : 'received_gameover',
           'please_wait' : 'waiting',
           'please_resume' : 'gaming'}

###Connection
#give target address
server_address = ('10.0.0.1', 10000)            # server address for dummy testing
print ('connecting to %s port %s' % server_address)
#connect to address
while True:
    try:
        print('cook connection')
        client.connect(('10.0.0.1', 10000))
        print('connected')
        break
    except:
        print('no connection found')
        time.sleep(0.5)
        continue


global port_lock ; port_lock = threading.Lock()

#%%

if_threadlist = [threading.Thread(target= _recv,
                                  args= [],
                                  kwargs= {}),

                 threading.Thread(target= filler,
                                  args= [],
                                  kwargs= {})]
#start threats
for thread in if_threadlist:
    thread.start()
    
#wait for threads to join once programm is finished | thread internal check
for thread in if_threadlist:
    thread.join()



#client.close()




