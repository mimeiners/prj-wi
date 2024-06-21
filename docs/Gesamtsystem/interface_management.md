# Interface Management

##### Function

The interface allows the Kicker to communicate with another device. By design, this other device is the PC which controlls the AuVAReS drone. The interface searches for a connection and controlls the connection's status once it is esstablished. Through the interface, the partner device can send keywords which interact with the current status of the host and the other way around.

### Location

The interface is defined in the file "LVL2_interface.py" and also has functions and definitions in "LVL3_classes.py" . "LVL2_interface.py" controlls the connection status, listens for keywords and interprets all incoming messages. If a keyword is detected a function inside this file is called which includes the appropiate reaction to a keyword (e.g setting certain status flags). Sending messages aswell as the connection status flag and finding a connection are defined in "LVL3_classes.py" . That way they can easily be called by other functions and use the interface without importing "LVL2_interface.py" .

### Network design

The Network traffic is designed around global keywords. Here, a keyword is a string message that can be sended by any device and can be received by any device. Once received, a reaction is called which is defined at the receiver. The reaction being defined locally allows the each reaction to be fitted to each system, regardless of system design. Of course, all parties must agree on a common set of keywords and their functionalty (but not the technical implementation!).

##### Receiving Messages, ACK and NACK

The system is designed to always listen for any incoming messages, send an ACK and then react to the received message. During a reaction no other message can be recieved! The system can send messages during a reaction.

If a keyword is received, an acknowldgement(ACK) is sended. An ACK acts like another keyword, with the limitation of only being sended if it's keyword was received. The sender of the keyword can therefore check if a sended keyword was received. The interface can react to a received ACK just like to a keyeword. If no ACK has been recieved, it is counted as a NACK. There is no official implementation of a NACK and it must be added manually, if needed. The funtion "_ping()" in "LVL2_interface.py" serves as a possible example.

##### Sending Messages and Connection Status

All non-LVL2_interface.py functions only interact with the interface by sending messages. The function "server_send()" has been created for this purpose. It serves as a 'interface' between the interface and the system.

The connection status flag "connection_status" defined in "LVL3_classes.py" reflects the current status of a connection. By definition, a connection exists (True) or not (False). All functions can check the status flag if they imported LVL3_classes.py . The status is flaged is managed by two functions. "_find_connection()", defined in LVL3_classes.py , can set the connection status to "True". "_ping()", defined in LVL2_interface.py , can set the connection status to "False".

##### Finding a Conncetion and Reconnect

The system searches for a connection if the function "_find_connection.py" is called. The function is first called as a daemon thread inside "init()" from "LVL3_classes.py". As long as no connection is found, the interface Thread will not start operation, instead being locked inside a while loop. The condition for the while loop is defined by the "connection_type_object" being "None". This variabe being "None" is a defined state in "LVL3_classes.init()" at the start of operation. Once a connection is established inside "_find_connection()", "_find_connection()" will return, thus ending it's thread, the while loop is broken and operation of the interface starts. All other calls of "_find_connection()" are done inside the interface and only through the function "_ping()".

Once a NACK is detected by the "ping_ack_flag" being "False" a second after the ping was send, the connection is closed by the server, "connection_status" is set to "False" and "_find_connection()" is called. This call of "_find_connection()" is done without a thread. The function "_ping()" therefore has to wait for it to return, thus stopping operation of the ping thread until a connection is found. The receive thread which calls the function "_recv()" will raise Exceptions which are simply caught by an "except:pass". Interface operation is thereby virtually stopped until a new connection can be established.