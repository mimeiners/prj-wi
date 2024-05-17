"""
This is a dummy to test and simulate the program with the keywords and the corresponding ACKs.
"""
__author__ = "Julian Höpe"
__version__ = "1.0.0"
__status__ = " WIP"
__date__ = "2024-05-17"

'''
NOTE: THIS FILE IS ONLY FOR TESTING PURPOSES
'''

import socket
import time



def send_wait(s, index):
    global ack_dic
    keys = list(ack_dic.keys())
    acks = list(ack_dic.values())

    msg = keys[index]
    s.sendall(msg.encode('utf-8'))
    print("Sent: " + msg)


    while True:
        rec = s.recv(1024).decode().strip()
        if rec == acks[index]:
            print("Rec: " + rec)
            return
        else:
            time.sleep(0.5) # wait 0.5s
            s.sendall(msg.encode('utf-8'))
            print("Sent: " + msg)


     
ack_dic =   {'ping' : 'hi',                                         # k
            'notify_drone_powered' : 'connecting',                  # k
            'notify_drone_connected' : 'waiting_for_startbutton',   # a
            'notify_start_permission' : 'positioning_drone',        # k
            'notify_gamestart' : 'game_started',                    # a
            'notify_newgoal' : 'received_newgoal',                  # k
            'notify_foul' : 'received_foul',                        # k
            'notify_gameover' : 'received_gameover',                # k
            'please_wait' : 'waiting',                              # a
            'please_resume' : 'gaming'}                             # a


keys = list(ack_dic.keys())
acks = list(ack_dic.values())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Get local machine name
host = socket.gethostname()
# Reserve a port for your service
port = 12345
# Bind the socket to the host and port
s.bind((host, port))
# Listen for incoming connections
s.listen(5)

print(f"Server listening on {host}:{port}")

while True:
        try:
            # Wait for a connection
            conn, addr = s.accept()
            print(f'Got connection from {addr}')
            while True: 
                data = conn.recv(1024)
                print(f'Received {data}')

                ## if waiting_for_drone, nothing else will be received or send
                if data == 'please_wait':
                    print("Please wait")
                    s.sendall(b'waiting')
                    
                    while True:
                        waiting = s.recv(1024).decode().strip()
                        if waiting == "please_resume":
                            print("Continue Game")
                            s.sendall(b'gaming')
                        else:
                             pass
                        
                elif data == 'notify_drone_connected':
                    print("Drone connected")
                    s.sendall(b'waiting_for_startbutton')

                elif data == 'notify_gamestart':
                    print("Game start")
                    s.sendall(b'game_started')

                elif not data:
                    print('No data received')
                    var = int(input("Zu sendende Nachricht (INDEX) [0,1,3,5,6,7]: "))
                    send_wait(s, index=var)

            
        except KeyboardInterrupt:
            s.close()
            print("connection closed")