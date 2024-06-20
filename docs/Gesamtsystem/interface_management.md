# Interface Management

##### Function

The interface allows the Kicker to communicate with another device. By design, this other device is the PC which controlls the AuVAReS drone. The interface searches for a connection and controlls the connection's status once it is esstablished. Through the interface, the partner device can send keywords which interact with the current status of the host and the other way around.

##### Location

The interface is defined in the file LVL2_interface.py and also has functions and definitions in LVL3_classes.py . LVL2_interface controlls the connection status, listens for keywords and interprets all incoming messages. If a keyword is detected a function inside this file is called which includes the appropiate reaction to a keyword (e.g setting certain status flags). Sending messages aswell as the connection status flag and finding a connection are defined in LVL3_classes.py . That way they can easily be called by other functions and use the interface without importing LVL2_interface.py .

##### Network design

The Network traffic is designed around global keywords. Here, a keyword is a string message that can be sended by any device and can be received by any device. Once received, a reaction is called which is defined at the receiver. The reaction being defined locally allows the each reaction to be fitted to each system, regardless of system design. Of course, all parties must agree on a common set of keywords and their functionalty (but not the technical implementation!).

If a keyword is received, an acknowldgement(ACK) is sended. An ACK acts like another keyword, with the limitation of only being sended if it's keyword was received. The sender of the keyword can therefore check if a sended keyword was received. The interface can react to a received ACK just like to a keyeword. If no ACK has been recieved, it is counted as a NACK. There is no official implementation of a NACK and it must be added manually, if needed. The funtion _ping() in LVL2_interface.py serves as a possible example.

The system is designed to always listen for any incoming messages, send an ACK and then react to the received message. During a reaction no other message can be recieved! Messages can be sended during a reaction.

All non-LVL2_interface.py functions only interact with the interface by sending messages. The function "server_send()" has been created for this purpose. It serves as a 'interface' between the interface and the system. The connection status flag "connection_status" defined in LVL3_classes serves...