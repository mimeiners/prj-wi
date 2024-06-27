# Schnittstellen Verwaltung

### Funktion

Die Schnittstelle ermöglicht es dem Kicker, mit einem anderen Gerät zu kommunizieren. Dieses andere Gerät wird, durch das Patnerprojekt bestimmt, die Steuereinheit der AuVAReS-Drohne sein. Die Schnittstelle sucht nach einer Verbindung und überwacht den Verbindungsstatus, sobald dieser hergestellt ist. Über die Schnittstelle kann das Partnergerät Schlüsselwörter senden, die mit dem aktuellen Status des Hosts interagieren, und umgekehrt.

Das hauptsächlich genutzte Modul ist "socket", welches einer einer der Grund Module von Python 3.+ darstellt.

### Schnittstellen Konzept

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

Die Funktion "server_send()" kann von jeder Funktion im Code aufgerufen werden, die "LVL3_classes.py" importiert hat. Sie ermöglicht es jedem Teil des Codes, eine Nachricht an ein verbundenes Gerät zu senden. Die Funktion beinhaltet automatisch alle notwendigen Schritte für eine erfolgreiche Übertragung.

### Empfangen von Nachrichten, ACK und NACK

##### Konzept

Das System ist so konzipiert, dass es immer auf eingehende Nachrichten hört, eine ACK-Nachricht sendet und dann auf die empfangene Nachricht reagiert. Während einer Reaktion kann keine andere Nachricht empfangen werden! Das System kann jedoch während einer Reaktion Nachrichten senden.

Wenn ein Schlüsselwort empfangen wird, wird eine Bestätigung (ACK) gesendet. Ein ACK funktioniert wie ein weiteres Schlüsselwort, mit der Einschränkung, dass es nur gesendet wird, wenn sein Schlüsselwort empfangen wurde. Der Sender des Schlüsselworts kann somit überprüfen, ob ein gesendetes Schlüsselwort empfangen wurde. Die Schnittstelle kann auf ein empfangenes ACK genauso reagieren wie auf ein Schlüsselwort. Wenn kein ACK empfangen wurde, wird dies als NACK gezählt. Es gibt keine offizielle Implementierung eines NACK, und es muss bei Bedarf manuell hinzugefügt werden. Die Funktion "_ping()" in "LVL2_interface.py" dient als mögliches Beispiel.

##### Umsetzung

Das Empfangen von Nachrichten erfolgt im zweiten Thread von "interface()" mit dem Funktionsaufruf von "_recv()". Das eigentliche Empfangen einer Nachricht erfolgt mit der importierten Funktion "lvl3.connection_type_object.listen(1024)". Der Rest der Funktion ist eine aktive While-Schleife, welche die empfangenen Daten aus "utf-8" decodiert und den Funktionsaufruf von "_data_interpret()" enthält.

Die Funktion "_data_interpret()" wird verwendet, um eine angemessene Reaktion auf eine empfangene Nachricht zu bestimmen. Zuerst erfolgt eine Überprüfung, ob die empfangene Nachricht ein Schlüsselwort oder ein ACK ist. Sollte es sich um ein Schlüsselwort handeln, so wird automatisch ein entsprechendes ACK gesendet. Danach wird entsprechend "_keyword_react()" oder "_ack_react()" aufgerufen. Die Nachricht wird als Argument an diese weitergegeben. Durch eine if/else Kette wird dann eine entsprechde Reaktion ausgeführt. Diese Reaktionen können Funktionsaufrufe seinen, welche lokal in ihren entsprechenden Modulen definiert wurden, oder gleich die entsprechende Reaktion ausgeschrieben (z.B setzen von Variablen, das senden von Schlüsselwöretern etc.).

Alle ACK sind im voherein definiert in der Schlüsselwort Tabelle. Ein NACK ist nicht global definiert sondern muss gesondert eingesetzt werden. Eine mögliche Umsetzung nutzt das Schlüsselwort "ping". Die Funktion "_ping()" setzt in "LVL3_classes.py" die "ping_ack_flag" auf "False". Das zurücksetzen auf "True" erfolgt als Reaktionsfunktion auf das entsprechende ACK "hi". Nach einer Sekunde wird der Zustand der Flagge überprüft. Sollte dieser dann immer noch "False" sein, wird die Verbidnung geschlossen und eine neue wird gesucht. Ist die Flagge auf "True" gesetzt wird das nächste "ping" gesendet.

### Sende Funktion und Verbindungsstatus

##### Konzept

Alle Funktionen außerhalb von "LVL2_interface.py" interagieren nur durch das Senden von Nachrichten mit der Schnittstelle. Die Funktion "server_send()" wurde zu diesem Zweck erstellt. Sie dient als 'Schnittstelle' zwischen der eigentlichen Schnittstelle und dem System.

Das Verbindungsstatus-Flag "connection_status", das in "LVL3_classes.py" definiert ist, spiegelt den aktuellen Status einer Verbindung wider. Per Definition existiert entweder eine Verbindung (True) oder nicht (False). Alle Funktionen können das Status-Flag überprüfen, sofern sie "LVL3_classes.py" importiert haben.

##### Umsetzung

Soll eine Nachricht gesendet werden so geschieht dies über die Funktion "sendall()". Die Funktion "server_send()" übernimmt diese Funktion und auch alle anderen Aufgaben, die sich durch die Systemstruktur, ergeben. Auch Aufgaben welche immer durchgführt werden müssen, werden übernommen.

Die Funktion kodiert die zu übertragende Nachricht selbst in "utf-8".

Insgesamt versucht "server_send()" eine Nachricht 6 mal abzuschicken, falls ein vorheriger Versuch fehlschlägt. Zwischen jeden Versuch liegen 0.33 Sekunden wodurch ein Funktionsabruf ungefähr 2 Sekunden dauert. Dieses Intervall wurde gewählt um das ein sekündige Intervall des Pings mit einzuschließen. Sollte eine Verbindung beim Sendeversuch scheitern, kann die Ping Funktion die Verbindung wieder aufbauen und die Nachricht kann gesendet werden. Ein Fehlversuch entsteht wenn der Verbindungsstatus "connection_status" "False" ist.

Sollte der Status "True" sein, nutzt die Funktion das "port_lock". Die verschieden Locks kommen aus dem thread-modul und verwalten den Zugriff unterschiedlicher threads auf geteilelte Ressourcen.

Der Verbindungsstatus wird von zwei Funktionen verwaltet. "_find_connection()", definiert in "LVL3_classes.py", kann den Verbindungsstatus auf "True" setzen. "_ping()" kann den Verbindungsstatus auf "False" setzen.
Sie kann von allen Funktionen im System abgerufen werden, sollte aber nicht von diesen geändert werden.

Die bisher nicht erwähnte Funktion "set_connection_status()" wird verwendet, um "connection_status" auf einen beliebigen Zustand zu setzen. Diese Funktion wird genutzt, da Bedenken hinsichtlich des importierten Zustands von "connection_status" bestanden. Mit "set_connection_status()" kann die Funktion "connection_status" als lokale Variable in "LVL3_classes.py" geändert werden, anstatt eine importierte Variable zu verwenden.

### Verbindungsaufbau

##### Konzept

Nach dem Systemstart wird die Suche nach einer Verbindung gestartet. Solange keine Verbindung gefunden wird, findet keine Schnittstellenaktivität statt. Sobald eine Verbindung gefunden wird, wird das Verbindungsmanagement gestartet.

Wenn "_ping()" ein NACK feststellt so wird die aktuelle Verbindung geschlossen und eine neue wird gesucht. Solange keine Verbindung vorliegt werden auch alle Prozesse der Schnittstelle gestoppt bzw. virtuell aufgehalten.

##### Umsetzung

Das System sucht nach einer Verbindung, wenn die Funktion "_find_connection()" aufgerufen wird. Diese Funktion wird zuerst als Daemon-Thread innerhalb von "init()" in "LVL3_classes.py" aufgerufen. Solange keine Verbindung gefunden wird, wird der Schnittstellen-Thread nicht gestartet und bleibt stattdessen in einer While-Schleife gesperrt. Die Bedingung für die While-Schleife ist, dass "connection_type_object" gleich "None" ist. Dies stellt einen definierten Zustand in "LVL3_classes.init()" zu Beginn des Betriebs dar. Sobald eine Verbindung innerhalb von "_find_connection()" hergestellt ist, kehrt die Funktion zurück und beendet ihren Thread. Die While-Schleife wird unterbrochen und der Betrieb der Schnittstelle beginnt. Alle anderen Aufrufe von "_find_connection()" erfolgen innerhalb der Schnittstelle und nur über die Funktion "_ping()".

Wenn ein NACK erkannt wird dadurch das "ping_ack_flag" "False" ist, eine Sekunde nach dem Senden des Pings, schließt der Server die Verbindung, setzt "connection_status" auf "False" und ruft "_find_connection()" auf. Dieser Aufruf von "_find_connection()" erfolgt ohne Thread. Die Funktion "_ping()" muss daher auf ihre Rückkehr (return) warten und stoppt somit den Betrieb des Ping-Threads, bis eine Verbindung gefunden ist. Der Empfangsthread, der die Funktion "_recv()" aufruft, wird Exceptions auslösen, die einfach durch "except: pass" abgefangen werden. Die Betriebsfähigkeit der Schnittstelle wird dadurch praktisch gestoppt, bis eine neue Verbindung hergestellt werden kann.