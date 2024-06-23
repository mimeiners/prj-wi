import socket
import time

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

                if not data:
                     print('No data received')

                
                data = ''   #clear data

                

                time.sleep(5)
                conn.sendall(b'SPECIAL_MESSAGE')
                print("SEND: SPECIAL_MESSAGE")



            '''
            if not data:
                conn.sendall(b'Thank you for connecting')
                print("SEND: Thank you for connecting'")
                conn.sendall(b"SPECIAL_MESSAGE")
                print("SEND: SPECIAL_MESSAGE")
            '''
            
        except KeyboardInterrupt:
            s.close()
            print("connection closed")
        '''    
        finally: 
            s.close()
            print("connection closed")    
        '''