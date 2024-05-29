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
import threading


def receive(conn):
    while True:
        data = conn.recv(1024).decode().strip()
        if data:
            print(f"Received: {data}")
        else:
            print(f"Received: None")


def send_wait(conn, index):
    global ack_dic
    keys = list(ack_dic.keys())
    acks = list(ack_dic.values())

    msg = keys[index]
    conn.sendall(msg.encode('utf-8'))
    print("Sent: " + msg)


    # while True:
    #     rec = conn.recv(1024).decode().strip()
    #     if rec == acks[index]:
    #         print("Rec: " + rec)
    #         return
    #     else:
    #         time.sleep(0.5) # wait 0.5s
    #         conn.sendall(msg.encode('utf-8'))
    #         print("Sent: " + msg)


     
# ack_dic =   {'ping' : 'hi',                                         # k
#             'notify_drone_powered' : 'connecting',                  # k
#             'notify_drone_connected' : 'waiting_for_startbutton',   # a
#             'notify_start_permission' : 'positioning_drone',        # k
#             'notify_gamestart' : 'game_started',                    # a
#             'notify_newgoal' : 'received_newgoal',                  # k
#             'notify_foul' : 'received_foul',                        # k
#             'notify_gameover' : 'received_gameover',                # k
#             'please_wait' : 'waiting',                              # a
#             'please_resume' : 'gaming'}                             # a

ack_dic =   {'ping' : 'hi',                                         # k
            'notify_drone_powered' : 'connecting_drone',            # k
            'waiting_for_startbutton' : 'notify_drone_connected',   # a
            'notify_start_permission' : 'positioning_drone',        # k
            'game_started' : 'notify_gamestart',                    # a
            'notify_newgoal' : 'received_newgoal',                  # k
            'notify_foul' : 'received_foul',                        # k
            'notify_gameover' : 'received_gameover',                # k
            'waiting' : 'please_wait',                              # a
            'gaming' : 'please_resume'}                             # a


keys = list(ack_dic.keys())
acks = list(ack_dic.values())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Get local machine name
host = "192.168.160.80"
# Reserve a port for your service
port = 28765
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
            receive_thr = threading.Thread(target=receive, args=(conn, ))
            receive_thr.start()
            while True: 
                # data = conn.recv(1024)
                # print(f'Received {data}')

                ## if waiting_for_drone, nothing else will be received or send
                # if data == 'please_wait':
                #     print("Please wait")
                #     conn.sendall(b'waiting')
                    
                #     while True:
                #         waiting = conn.recv(1024).decode().strip()
                #         if waiting == "please_resume":
                #             print("Continue Game")
                #             conn.sendall(b'gaming')
                #         else:
                #              pass
                        
                # elif data == 'notify_drone_connected':
                #     print("Drone connected")
                #     conn.sendall(b'waiting_for_startbutton')

                # elif data == 'notify_gamestart':
                #     print("Game start")
                #     conn.sendall(b'game_started')

                # elif not data:
                #     print('No data received')
                #     var = int(input("Zu sendende Nachricht (INDEX) [0,1,3,5,6,7]: "))
                #     send_wait(conn, index=var)
                var = int(input("Zu sendende Nachricht (INDEX) [0,1,3,5,6,7]: "))
                send_wait(conn, index=var)
                
        except KeyboardInterrupt:
            s.close()
            print("connection closed")
            receive_thr.join()
            
        except Exception as e:
            print(f"Error occurred {e}")
            
        print("loop")
        
        
        
        
        
        