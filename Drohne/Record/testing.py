from auxilaryFunctions import *

import socket

import socket
import threading
import time

#%%
# Define the function to be run when a special message is received
def special_message_function():
    print("Special message received! Running special function...")
    # Add your custom logic here

# Define the function to handle the network connection
def network_connection():
    # Create a socket object
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
        # Wait for a connection
        conn, addr = s.accept()
        print(f'Got connection from {addr}')

        # Receive the data in small chunks and retransmit it
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("Received:", data.decode())

            # Check if the received message is a special message
            if data.decode().strip() == "SPECIAL_MESSAGE":
                special_message_function()
            
            # Send the received data back as confirmation
            conn.sendall(data)
        
        # Clean up the connection
        conn.close()

# Define the function for the other task
def other_task():
    while True:
        print("Doing other task...")
        time.sleep(5)

# Start the network connection and other task in separate threads
network_connection_thread = threading.Thread(target=network_connection)
other_task_thread = threading.Thread(target=other_task)

network_connection_thread.start()
other_task_thread.start()

# Wait for the threads to finish
network_connection_thread.join()
other_task_thread.join()


#%%
import socket
import threading
import time

# Define the function to be run when a special message is received
def special_message_function():
    print("Special message received! Running special function...")
    # Add your custom logic here

# Define the function for the main task
def main_task():
    while True:
        print("Doing main task...")
        time.sleep(5)

# Define the function to handle the network connection
def network_connection():
    # Create a socket object
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
        # Wait for a connection
        conn, addr = s.accept()
        print(f'Got connection from {addr}')

        # Receive the data in small chunks and retransmit it
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("Received:", data.decode())

            # Check if the received message is a special message
            if data.decode().strip() == "SPECIAL_MESSAGE":
                # Interrupt the main task and run the special function
                main_task_thread.do_run = False
                special_message_function()
                main_task_thread.do_run = True
            
            # Send the received data back as confirmation
            conn.sendall(data)
        
        # Clean up the connection
        conn.close()

# Define the main task thread
class MainTaskThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.do_run = True

    def run(self):
        main_task()

# Start the network connection and main task in separate threads
network_connection_thread = threading.Thread(target=network_connection)
main_task_thread = MainTaskThread()

network_connection_thread.start()
main_task_thread.start()

# Wait for the threads to finish
network_connection_thread.join()
main_task_thread.join()

#%% network on client edition
import socket
import threading
import time

# Define the function to be run when a special message is received
def special_message_function():
    print("Special message received! Running special function...")
    # Add your custom logic here

# Define the function for the main task
def main_task():
    while True:
        print("Doing main task...")
        time.sleep(5)

# Define the function to handle the network connection
def network_connection():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = socket.gethostname()

    # Reserve a port for your service
    port = 12345

    # Connect to the server
    s.connect((host, port))

    while True:
        # Send a message to the server
        s.sendall(b"Hello, server")

        # Receive the data in small chunks
        data = s.recv(1024)
        if not data:
            break
        print("Received:", data.decode())

        # Check if the received message is a special message
        if data.decode().strip() == "SPECIAL_MESSAGE":
            # Interrupt the main task and run the special function
            main_task_thread.do_run = False
            special_message_function()
            main_task_thread.do_run = True
    
    # Clean up the connection
    s.close()

# Define the main task thread
class MainTaskThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.do_run = True

    def run(self):
        main_task()

# Start the network connection and main task in separate threads
network_connection_thread = threading.Thread(target=network_connection)
main_task_thread = MainTaskThread()

network_connection_thread.start()
main_task_thread.start()

# Wait for the threads to finish
network_connection_thread.join()
main_task_thread.join()

def network_connection():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = socket.gethostname()

    # Reserve a port for your service
    port = 12345

    # Connect to the server
    s.connect((host, port))

    while True:
        try:
            # Send a message to the server
            s.sendall(b"Hello, server")

            # Receive the data in small chunks
            data = s.recv(1024)
            if not data:
                break
            print("Received:", data.decode())

            # Check if the received message is a special message
            if data.decode().strip() == "SPECIAL_MESSAGE":
                # Interrupt the main task and run the special function
                main_task_thread.do_run = False
                special_message_function()
                main_task_thread.do_run = True

        except ConnectionError:
            # If the connection is lost, try to reconnect
            print("Connection lost, trying to reconnect...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            continue
    
    # Clean up the connection
    s.close()

#%%
import socket
import threading
import time

# Define the function to be run when a special message is received
def special_message_function():
    print("Special message received! Running special function...")
    # Add your custom logic here

# Define the function for the main task
def main_task():
    while True:
        print("Doing main task...")
        time.sleep(5)

# Define the function to handle the network connection
def network_connection():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = socket.gethostname()

    # Reserve a port for your service
    port = 12345

    # Set the socket to non-blocking mode
    s.setblocking(False)

    # Connect to the server
    s.connect((host, port))

    while True:
        try:
            # Send a message to the server
            s.sendall(b"Hello, server")

            # Receive the data in small chunks with a timeout
            s.settimeout(5)
            data = b''
            while True:
                try:
                    chunk = s.recv(1024)
                    if not chunk:
                        break
                    data += chunk
                except socket.timeout:
                    break

            if data:
                print("Received:", data.decode())

                # Check if the received message is a special message
                if data.decode().strip() == "SPECIAL_MESSAGE":
                    # Interrupt the main task and run the special function
                    main_task_thread.do_run = False
                    special_message_function()
                    main_task_thread.do_run = True

        except (ConnectionError, socket.error):
            # If the connection is lost, try to reconnect
            print("Connection lost, trying to reconnect...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(False)
            s.connect((host, port))
            continue
    
    # Clean up the connection
    s.close()

# Define the main task thread
class MainTaskThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.do_run = True

    def run(self):
        main_task()

# Start the network connection and main task in separate threads
network_connection_thread = threading.Thread(target=network_connection)
main_task_thread = MainTaskThread()

network_connection_thread.start()
main_task_thread.start()

# Wait for the threads to finish
network_connection_thread.join()
main_task_thread.join()

#%% Best Version
import socket
import threading
import time

# Define the function to be run when a special message is received
def special_message_function():
    print("Special message received! Running special function...")
    # Add your custom logic here

# Define the function for the main task
def main_task():
    while True:
        print("Doing main task...")
        time.sleep(5)

# Define the function to handle the network connection
def network_connection():
    # Create a socket object
    global s    # global connection, to use the same connection in all threads
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = socket.gethostname()

    # Reserve a port for your service
    port = 12345

    # Set the socket to non-blocking mode
    s.setblocking(False)

    # Connect to the server
    s.connect((host, port))

    # Set the last keep-alive time
    last_keep_alive = time.time()

    while True:
        try:
            # Send a keep-alive message every 5 minutes
            if time.time() - last_keep_alive >= 300:
                s.sendall(b"KEEP_ALIVE")
                last_keep_alive = time.time()

            # Try to receive data
            try:
                data = s.recv(1024)
                if data:
                    print("Received:", data.decode())

                    # Check if the received message is a special message
                    if data.decode().strip() == "SPECIAL_MESSAGE":
                        # Interrupt the main task and run the special function
                        main_task_thread.do_run = False
                        special_message_function()
                        main_task_thread.do_run = True
            except BlockingIOError:
                # No data available, continue
                pass

        except (ConnectionError, socket.error):
            # If the connection is lost, try to reconnect
            print("Connection lost, trying to reconnect...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(False)
            s.connect((host, port))
            last_keep_alive = time.time()
            continue
    
    # Clean up the connection
    s.close()

# Define the main task thread
class MainTaskThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.do_run = True

    def run(self):
        main_task()

# Start the network connection and main task in separate threads
network_connection_thread = threading.Thread(target=network_connection)
main_task_thread = MainTaskThread()

network_connection_thread.start()
main_task_thread.start()

# Wait for the threads to finish
network_connection_thread.join()
main_task_thread.join()