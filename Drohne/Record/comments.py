import socket
import threading
import time

# Define the function to be run when a special message is received
def special_message_function():
    global s
    print("Special message received! Running special function...")
    s.sendall(b"HELLO SERVER FROM special_message_function")
    # Add your custom logic here
    return

# Define the function for the main task
def main_task(connection_established):
    global s
    while connection_established.is_set():
        print("Doing main task...")
        s.sendall(b"HELLO SERVER from main_task")
        time.sleep(5)

# Define the function to handle the network connection
def network_connection():
    global s

    #while True:
    try:
        #s.connect((host, port))
        connection_established.set()
        s.sendall(b"HELLO SERVER FROM network_connection")
        print('Doing network connection')
        #break
    #except BlockingIOError:
        # Connection not established yet, wait and try again        
    #    time.sleep(0.1)
    except Exception as e:
        print(f"Error connecting: {e}")
        #break

    # Set the last keep-alive time
    last_keep_alive = time.time()
    while True:
        try:
            data = s.recv(1024)
            if data:
                print("Received:", data.decode())
                # Check if the received message is a special message
                if data.decode().strip() == "SPECIAL_MESSAGE":
                    # Interrupt the main task and run the special function
                    main_task_thread.do_run = False
                    print("interrupted main task")
                    special_message_function()
                    main_task_thread.do_run = True
                    print("continued main task")

        except KeyboardInterrupt:
            s.close()
        
'''   
#    
#    while connection_established.is_set():
#        try:
#            # Send a keep-alive message every 5 minutes
#            if time.time() - last_keep_alive >= 30:
#                s.sendall(b"KEEP_ALIVE")
#                last_keep_alive = time.time()
#
#            # Try to receive data
#            try:
#                data = s.recv(1024)
#                if data:
#                    print("Received:", data.decode())
#
#                    # Check if the received message is a special message
#                    if data.decode().strip() == "SPECIAL_MESSAGE":
#                        # Interrupt the main task and run the special function
#                        main_task_thread.do_run = False
#                        print("interrupted main task")
#                        special_message_function()
#                        main_task_thread.do_run = True
#                        print("continued main task")
#            except BlockingIOError:
#                # No data available, continue
#                pass
#        except KeyboardInterrupt:
#            s.close()
#            print('Connection closed by KeyboardInterrupt')
#
#        finally:
#            s.close()
#            print('Connection closed by line 72')
'''

'''
        except (ConnectionError, socket.error):
            # If the connection is lost, try to reconnect
            print("Connection lost, trying to reconnect...")
            s.close()  # Close the existing socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a new socket object
            s.setblocking(False)
            connection_established.clear()
            while True:
                try:
                    s.connect((host, port))
                    connection_established.set()
                    s.sendall(b"HELLO SERVER")
                    break
                except BlockingIOError:
                    # Connection not established yet, wait and try again
                    time.sleep(0.1)
                except Exception as e:
                    print(f"Error reconnecting: {e}")
                    break
        
            last_keep_alive = time.time()
            continue
        '''
        #finally:
        # Clean up the connection
        #    s.close()

# Define the main task thread


class MainTaskThread(threading.Thread):
    def __init__(self, connection_established):
        super().__init__()
        self.connection_established = connection_established
        self.do_run = True

    def run(self):
        while self.do_run:
            main_task(self.connection_established)

# Start the network connection and main task in separate threads
network_connection_thread = threading.Thread(target=network_connection)
connection_established = threading.Event()
main_task_thread = MainTaskThread(connection_established)

# pasted in for testing
# first establish the connection
# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = socket.gethostname()

# Reserve a port for your service
port = 12345

# connect to Server
s.connect((host, port))
connection_established.set()

network_connection_thread.start()
main_task_thread.start()

# Wait for the threads to finish
network_connection_thread.join()
main_task_thread.join()
# Clean up the connection
s.close()