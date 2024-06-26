# Interface Management

### Function

The interface allows the Kicker to communicate with another device. By design, this other device will be the control unit of the the AuVAReS drone. The interface searches for a connection and controlls the connection's status once it is esstablished. Through the interface, the partner device can send keywords which interact with the current status of the host and the other way around.

### Network design

The Network traffic is designed around global keywords. Here, a keyword is a string message that can be sended by any device and can be received by any device. Once received, a reaction is called which is defined at the receiver. The reaction being defined locally allows the each reaction to be fitted to each system, regardless of system design. Of course, all parties must agree on a common set of keywords and their functionalty (but not the technical implementation!).

##### Keywords

| Sender  | Schlüsselwort  | Beschreibung |ACK|
|:----------|:----------|:----------|:----------|
| K | ping | Wird mindestens zum Programmstart benutzt, um AuVAReS zu detektieren; nach timeout werden keine AuVAReS-abhängigängen Funktionen verwendet.   |hi
| K | notify_drone_powered | Die Spielernamen sind eingetragen und sie haben die Drohne gestartet (Quittieren über Button) | connecting_drone
| A | notify_drone_connected | Meldung, dass die Drone verbunden ist | waiting_for_startbutton
| K | notify_start_permission | Meldung, dass die Drone freigegeben ist zum Starten | positioning_drone
| A | notify_gamestart | Meldung, dass das Spiel gestartet werden kann | game_started
| K | notify_newgoal |Ein Tor ist gefallen, ein replay sollte gestartet werden|received_newgoal 
| K | notify_foul |Ein Regelverstoß ist vorgefallen, ein replay sollte gestartet werden|received_foul
| K | notify_gameover |Zusätzlich zum replay des Siegertores wird die Abschlussroutine der Drohne ausgeführt.|received_gamover
| A | please_wait| AuVAReS kann das Spiel pausieren, bspw. wenn es Zwischenfälle gibt. Tore werden nicht gezählt. |waiting
| A |please_resume| AuVAReS ist wieder einsatzbereit und erlaubt dem Kicker, wieder Tore zu zählen.|gaming
| K |STOP| AuVAReS soll Notlandung einleiten | received_stop

### Location

The interface is defined in the file "LVL2_interface.py" and also has functions and definitions in "LVL3_classes.py" . "LVL2_interface.py" controlls the connection status, listens for keywords and interprets all incoming messages. If a keyword is detected a function inside this file is called which includes the appropiate reaction to a keyword (e.g setting certain status flags). Sending messages aswell as the connection status flag and finding a connection are defined in "LVL3_classes.py" . That way they can easily be called by other functions and use the interface without importing "LVL2_interface.py" .

As a Level 2 function "LVL2_interface.py" is started in "LVL1_threads.py" as a thread upon system start.

#### Structure

##### LvL2_interface.py

The main interface is defined in "LVL2_interface.py". It's main structure is defined in the function "interface()", which is started as a thread in "LVL1_threads". Inside "Interface()" there two sections.

 The first section initialises the used keyword dictionary for the interface. This section also includes a while loop which stops interface activity until the first connection, after a system start, has been found. The second section contains the main functionality of the interface, defined by two threads which both serve one function each. The first function is "_ping()", which sends a ping keyword to the connected client and governs the current connection status. The second the thread calls the function "_recv()" which constantly supervises the connection port. Once it receives a message from another device, it checks if this message is a keyword or a ACK. If a keyword or ACK has been detected, a reaction function is called. If the message is neither, no reation follows. The reaction funtion stops the "_recv" function detecting any more messages until the reaction resolved.

##### LVL3_classes.py

 Another part of the interface can be found in "LVL3_classes.py". This part includes three integral parts of the interface functionality. The function "_find_connection()", the variable "connection_status" and the function "server_send()".

 The function "_find_connection()" searches for a new connection. It is assumed that during the time of the function call, no connection with any other device exists. As a found connection has been defined by a function in "LVL3_classes.py", any action concerning the interface and must be attributed to the object "connection_type_object". This object includes the connection object, as defined by the module sockets. A call on this object outside of Level 3 might look like "LVL3_classes.connection_type_object".

 The variable "connection_status" reflects the current necessary status of a connection. "True" means there is connection and "False" means there is no connection. ##It can be called by any function inside the system, if needed. Most of the time the function "server_send()" accesses the variable to check if an message can be send. This variable is set by "_find_connection()" if a connection has been found and gets resetted by "_ping()" if an NACK has been received.## The not yet mentioned function "set_connection_status()" is used to set "connection_status" to any state. This function is used as there were concerns about the imported state of "connection_status". With "set_connection_status()" the function can change "connection_status" as a local variable in "LVL3_classes.py" instead of an imported one.

The function "server_send()" can be accessed by every function in the code, which imported "LVL3_classes.py". It allows each part of the code to send a message to a connected device. The function automatically includes all necessary steps for a successfull transmission, including to check if there is a connection at all.

### Receiving Messages, ACK and NACK

##### Function

The system is designed to always listen for any incoming messages, send an ACK and then react to the received message. During a reaction no other message can be recieved! The system can send messages during a reaction.

If a keyword is received, an acknowldgement(ACK) is sended. An ACK acts like another keyword, with the limitation of only being sended if it's keyword was received. The sender of the keyword can therefore check if a sended keyword was received. The interface can react to a received ACK just like to a keyeword. If no ACK has been recieved, it is counted as a NACK. There is no official implementation of a NACK and it must be added manually, if needed. The funtion "_ping()" in "LVL2_interface.py" serves as a possible example.

##### Implementation

Receiving messages is done inside the second thread of the main interface function with the function call of "_recv()". The act of actually receiving a message is done with the imported function "lvl3.connection_type_object.listen(1024)". The rest of the function is an active while-loop, decoding from "utf-8" and the function call of "_data_interpret()".

The function "_data_interpret()" is used to decide on an appropiate response to a received message. First a check occurs which determines if a received message is a keyword or an ACK. Sollte es sich um ein Schlüsselwort handeln, so wird automatisch ein entsprechendes ACK gesendet. Danach wird entsprechend "_keyword_react()" oder "_ack_react()" aufgerufen. Die Nachricht wird als Argument an diese weitergegeben. Durch eine if/else Kette wird dann eine entsprechde Reaktion ausgeführt. Diese Reaktionen können Funktionsaufrufe seinen, welche lokal in ihren entsprechenden Modluen definiert wurden, oder gleich die entsprechende Reaktion ausgeschrieben (z.B setzen von Variablen, das senden von Schlüsselwöretern etc.).

Alle ACK sind im voherein definiert in der Schlüsselwort Tabelle. Ein NACK ist nicht global definiert sondern muss gesondet eingesetzt werden. Eine mögliche Umsetzung nutzt das Schlüsselwort "ping". Die Funktion "_ping()" setzt in "LVL3_classes.py" die "ping_ack_flag" auf "False". Das zurücksetzen auf "True" erfolgt als Reaktionsfunktion auf das entsprechende ACK "hi". Nach einer Sekunde wird der Zustand der Flagge überprüft. Sollte dieser dann immer noch "False" sein, wird die Verbidnung geschlossen und eine neue wird gesucht. Ist die Flagge auf "True" gesetzt wird das nächste "ping" gesendet,

### Sending Messages and Connection Status

All non-LVL2_interface.py functions only interact with the interface by sending messages. The function "server_send()" has been created for this purpose. It serves as a 'interface' between the interface and the system.

The connection status flag "connection_status" defined in "LVL3_classes.py" reflects the current status of a connection. By definition, a connection exists (True) or not (False). All functions can check the status flag if they imported LVL3_classes.py . The status is flaged is managed by two functions. "_find_connection()", defined in LVL3_classes.py , can set the connection status to "True". "_ping()", defined in LVL2_interface.py , can set the connection status to "False".

### Finding a Connection and Reconnect

##### Concept

Once the system starts a search for a connection is started. Aslong as no connection is found, no interface activity is done. Once it is found the connection mangement is started. Part of the management is a ping function which checks the current state of the connection by sending a ping keyword each second. If an ACK has been detected one second after the ping was send, the next ping is sendend. If a NACK is detected, the connection is closed and all interface activity is stopped. The system then automatically starts another search for a connection. Once found, interface activity is continued.

##### Implementation

The system searches for a connection if the function "_find_connection.py" is called. The function is first called as a daemon thread inside "init()" from "LVL3_classes.py". As long as no connection is found, the interface thread will not start operation, instead being locked inside a while loop. The condition for the while loop is defined by the "connection_type_object" being "None". This variabe being "None" is a defined state in "LVL3_classes.init()" at the start of operation. Once a connection is established inside "_find_connection()", "_find_connection()" will return, thus ending it's thread, the while loop is broken and operation of the interface starts. All other calls of "_find_connection()" are done inside the interface and only through the function "_ping()".

Once a NACK is detected by the "ping_ack_flag" being "False" a second after the ping was send, the connection is closed by the server, "connection_status" is set to "False" and "_find_connection()" is called. This call of "_find_connection()" is done without a thread. The function "_ping()" therefore has to wait for it to return, thus stopping operation of the ping thread until a connection is found. The receive thread which calls the function "_recv()" will raise Exceptions which are simply caught by an "except:pass". Interface operation is thereby virtually stopped until a new connection can be established.