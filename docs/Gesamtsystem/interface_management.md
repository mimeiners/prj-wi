# Interface Management

### Function

Die Schnittstelle ermöglicht es dem Kicker, mit einem anderen Gerät zu kommunizieren. Dieses andere Gerät wird, durch das Patnerprojekt bestimmt, die Steuereinheit der AuVAReS-Drohne sein. Die Schnittstelle sucht nach einer Verbindung und überwacht den Verbindungsstatus, sobald dieser hergestellt ist. Über die Schnittstelle kann das Partnergerät Schlüsselwörter senden, die mit dem aktuellen Status des Hosts interagieren, und umgekehrt.

Das hauptsächlich genutzte Modul ist "socket", welches einer einer der Grund Module von Python 3.+ darstellt.

### Network design

Der Netzwerkverkehr basiert auf globale Schlüsselwörtern. Hierbei ist ein Schlüsselwort eine Varible von Typ "str", die von jedem Gerät gesendet und von jedem Gerät empfangen werden kann. Sobald sie empfangen wird, wird eine Reaktion aufgerufen, die am Empfänger definiert ist. Die lokal definierte Reaktion ermöglicht es, dass jede Reaktion an jedes System angepasst werden kann, unabhängig vom Systemdesign. Natürlich müssen sich alle Parteien auf einen gemeinsamen Satz von Schlüsselwörtern und deren Funktionalität einigen (aber nicht auf die technische Umsetzung!). In dem unter Kapitel Schlüsselwörter ist eine Tabelle mit allen Schlüsselwörtern, deren Funktion und deren dazugehöriges ACK.

##### Schlüsselwörter

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

### Speicherorte

Die Schnittstelle ist in der Datei "LVL2_interface.py" definiert und enthält auch Funktionen und Definitionen in "LVL3_classes.py". "LVL2_interface.py" steuert den Verbindungsstatus, hört auf Schlüsselwörter und interpretiert alle eingehenden Nachrichten. Das Senden von Nachrichten sowie das Verbindungsstatus-Flag und das Finden einer Verbindung sind in "LVL3_classes.py" definiert. Auf diese Weise können sie leicht von anderen Funktionen aufgerufen werden und die Schnittstelle verwenden, ohne "LVL2_interface.py" importieren zu müssen.

Als eine Level-2-Funktion wird "LVL2_interface.py" bei Systemstart in "LVL1_threads.py" als Thread gestartet.

#### Struktur

##### LvL2_interface.py

Der Hauptteil der Schnittstelle ist in "LVL2_interface.py" definiert. Ihre Hauptstruktur ist in der Funktion "interface()" definiert, die in "LVL1_threads" als Thread gestartet wird. Innerhalb von "interface()" gibt es zwei Abschnitte.

Der erste Abschnitt initialisiert das verwendete Schlüsselwortverzeichnis für die Schnittstelle. Dieser Abschnitt enthält auch eine While-Schleife, welche verhindert das die Schnittstellenoperation startet bevor, nach einem Systemstart, eine erste Verbindung gefunden wurde.
 
Der zweite Abschnitt beinhaltet die Hauptfunktionen der Schnittstelle. Diese werden durch zwei Threads gestartet, von denen jeder eine Funktion ausführt. Die erste Funktion ist "_ping()", die ein Ping-Schlüsselwort an den verbundenen Client sendet und den aktuellen Verbindungsstatus überwacht. Der zweite Thread ruft die Funktion "_recv()" auf, welche es der Schnittstelle erlaubt jederzeit Nachrichten zu empfangen.

##### LVL3_classes.py

Ein weiterer Teil der Schnittstelle befindet sich in "LVL3_classes.py". Dieser Teil umfasst drei wesentliche Bestandteile der Schnittstelle: die Funktion "_find_connection()", die Variable "connection_status" und die Funktion "server_send()". Diese Bestandteile werden von anderen Funktionen, außerhalb "LVL2_interface.py" benötigt und werden deshalb in Level 3 definiert.

Die Funktion "_find_connection()" sucht nach einer neuen Verbindung. Es wird angenommen, dass zum Zeitpunkt des Funktionsaufrufs keine Verbindung zu einem anderen Gerät besteht. Da eine gefundene Verbindung durch eine Funktion in "LVL3_classes.py" definiert wurde, müssen alle Aktionen, welche die Schnittstelle betreffen, dem Objekt "connection_type_object" zugeordnet werden. Dieses Objekt umfasst das Verbindungsobjekt, wie es vom Modul "socket" definiert wird. Ein Aufruf dieses Objekts außerhalb von Level 3 könnte beispielsweise so aussehen: "LVL3_classes.connection_type_object.eine_funktion()".

Die Variable "connection_status" spiegelt den aktuellen Status einer Verbindung wieder. "True" bedeutet, dass eine Verbindung besteht, und "False" bedeutet, dass keine Verbindung besteht. Die bisher nicht erwähnte Funktion "set_connection_status()" wird verwendet, um den Wert von "connection_status" auf einen beliebigen Zustand zu setzen.

The function "server_send()" can be accessed by every function in the code, which imported "LVL3_classes.py". It allows each part of the code to send a message to a connected device. The function automatically includes all necessary steps for a successfull transmission, including to check if there is a connection at all and 6 retires if there isn't.

### Receiving Messages, ACK and NACK

##### Function

The system is designed to always listen for any incoming messages, send an ACK and then react to the received message. During a reaction no other message can be recieved! The system can send messages during a reaction.

If a keyword is received, an acknowldgement(ACK) is sended. An ACK acts like another keyword, with the limitation of only being sended if it's keyword was received. The sender of the keyword can therefore check if a sended keyword was received. The interface can react to a received ACK just like to a keyeword. If no ACK has been recieved, it is counted as a NACK. There is no official implementation of a NACK and it must be added manually, if needed. The funtion "_ping()" in "LVL2_interface.py" serves as a possible example.

##### Implementation

Receiving messages is done inside the second thread of the main interface function with the function call of "_recv()". The act of actually receiving a message is done with the imported function "lvl3.connection_type_object.listen(1024)". The rest of the function is an active while-loop, decoding from "utf-8" and the function call of "_data_interpret()".

The function "_data_interpret()" is used to decide on an appropiate response to a received message. First a check occurs which determines if a received message is a keyword or an ACK. Sollte es sich um ein Schlüsselwort handeln, so wird automatisch ein entsprechendes ACK gesendet. Danach wird entsprechend "_keyword_react()" oder "_ack_react()" aufgerufen. Die Nachricht wird als Argument an diese weitergegeben. Durch eine if/else Kette wird dann eine entsprechde Reaktion ausgeführt. Diese Reaktionen können Funktionsaufrufe seinen, welche lokal in ihren entsprechenden Modulen definiert wurden, oder gleich die entsprechende Reaktion ausgeschrieben (z.B setzen von Variablen, das senden von Schlüsselwöretern etc.).

Alle ACK sind im voherein definiert in der Schlüsselwort Tabelle. Ein NACK ist nicht global definiert sondern muss gesondert eingesetzt werden. Eine mögliche Umsetzung nutzt das Schlüsselwort "ping". Die Funktion "_ping()" setzt in "LVL3_classes.py" die "ping_ack_flag" auf "False". Das zurücksetzen auf "True" erfolgt als Reaktionsfunktion auf das entsprechende ACK "hi". Nach einer Sekunde wird der Zustand der Flagge überprüft. Sollte dieser dann immer noch "False" sein, wird die Verbidnung geschlossen und eine neue wird gesucht. Ist die Flagge auf "True" gesetzt wird das nächste "ping" gesendet.

### Sending Messages and Connection Status

##### Concept

All non-LVL2_interface.py functions only interact with the interface by sending messages. The function "server_send()" has been created for this purpose. It serves as a 'interface' between the interface and the system.

The connection status flag "connection_status" defined in "LVL3_classes.py" reflects the current status of a connection. By definition, a connection exists (True) or not (False). All functions can check the status flag if they imported "LVL3_classes.py".

##### Implementation

Soll eine Nachricht gesendet werden so geschieht dies über die Funktion "sendall()". Die Funktion "server_send()" übernimmt diese Funktion und auch alle anderen Aufgaben, die sich durch die Systemstruktur, ergeben. Auch Aufgaben welche immer durchgführt werden müssen, werden übernommen.

Die Funktion kodiert die zu übertragende Nachricht selbst in "utf-8".

Insgesamt versucht "server_send()" eine Nachricht 6 mal abzuschicken, falls ein vorheriger Versuch fehlschlägt. Zwischen jeden Versuch liegen 0.33 Sekunden wodurch ein Funktionsabruf ungefähr 2 Sekunden dauert. Dieses Intervall wurde gewählt um das ein sekündige Intervall des Pings mit einzuschließen. Sollte eine Verbindung beim Sendeversuch scheitern, kann die Ping Funktion die Verbindung wieder aufbauen und die Nachricht kann gesendet werden. Ein Fehlversuch entsteht wenn der Verbindungsstatus "connection_status" "False" ist.

Sollte der Status "True" sein, nutzt die Funktion das "port_lock". Die verschieden Locks kommen aus dem thread-modul und verwalten den Zugriff unterschiedlicher threads auf geteilelte Ressourcen.

The connection status is managed by two functions. "_find_connection()", defined in "LVL3_classes.py", can set the connection status to "True". "_ping()" can set the connection status to "False". Sie kann von allen Funktionen im System abgerufen werden, sollte aber nicht von diesen geändert werden.

The not yet mentioned function "set_connection_status()" is used to set "connection_status" to any state. This function is used as there were concerns about the imported state of "connection_status". With "set_connection_status()" the function can change "connection_status" as a local variable in "LVL3_classes.py" instead of an imported one.

### Finding a Connection and Reconnect

##### Concept

Once the system starts, a search for a connection is started. Aslong as no connection is found, no interface activity is done. Once it is found the connection mangement is started. 

Wenn "_ping()" ein NACK feststellt so wird die aktuelle Verbindung geschlossen und eine neue wird gesucht. Solange keine Verbindung vorliegt werden auch alle Porzesse der Schnittstelle gestoppt bzw. vrituell aufgehalten.

##### Implementation

The system searches for a connection if the function "_find_connection.py" is called. The function is first called as a daemon thread inside "init()" from "LVL3_classes.py". As long as no connection is found, the interface thread will not start operation, instead being locked inside a while loop. The condition for the while loop is defined by the "connection_type_object" being "None". This variabe being "None" is a defined state in "LVL3_classes.init()" at the start of operation. Once a connection is established inside "_find_connection()", "_find_connection()" will return, thus ending it's thread, the while loop is broken and operation of the interface starts. All other calls of "_find_connection()" are done inside the interface and only through the function "_ping()".

Once a NACK is detected by the "ping_ack_flag" being "False" a second after the ping was send, the connection is closed by the server, "connection_status" is set to "False" and "_find_connection()" is called. This call of "_find_connection()" is done without a thread. The function "_ping()" therefore has to wait for it to return, thus stopping operation of the ping thread until a connection is found. The receive thread which calls the function "_recv()" will raise Exceptions which are simply caught by an "except:pass". Interface operation is thereby virtually stopped until a new connection can be established.