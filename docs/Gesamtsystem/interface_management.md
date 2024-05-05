# Interface Management

Diese Beschreibungen dienen als Leitfaden für die Entwicklung und kontinuierliche Dokumentation des aktuellen Standes der Schnittstelle. Einwände und Ideen sind natürlich willkommen.

Da von der Serverside aus mehrere Verbindungen möglich sind muss der Zugriff innerhalb der Threads Kollisionsfrei verlaufen. Geplant ist dafür die Function "threading.lock" und dessen Komplimentärfunktionen. Die Umsetzung dieser muss aber noch im Detail ermitttelt werden. Bis jetzt ist geplant das diese Bedingungen über "with" abgerufen.

Innerhalb vieler Funktionskritischer Schleifen wird noch die Variable some_var abgerufen welche ersetzt werden soll durch eine global systemstatus Variable.

### Setup

Der Aufbau des System besteht aus zwei Hauptcomputern. Der Computer von Wohninvest, welcher im folgenden als Server bezeichnet wird, und der Computer von AuVARes welcher als Client oder Drohnen Client bezeichnet wird. Es werden Optionen offen gehalten für einen dritten Computer und/oder einer externen Quelle zur Überwachung des Systems. Der Server ist der Ansprechpatner aller Clients und ist als notwendige Hardware des Kickers von Wohninvest zu betrachten.

### Nutzer Handbuch

#### Verbindung bestimmen

Die Verbindung zu einem Clienten ist repräsentiert in einem Klassenobjekt der Klasse "connection". Alle Klassenobjekte befinden sich in dem globalen Dictionary "connect_dic".

    global connect_dic
    connect_dic = {'drone' : drone_connection,
                   'extern1' : extern_connection_1,
                   'extern2' : extern_connection_2,
                   'dynamic': dynamic_connection} 

Solange noch keine Vebindung gefunden wurde sind diese Objekte nur ein 'None' und haben keine Funktion. Sobald die Verbindung hinzugefügt wurde, was automatisch geschieht sobald eine Verbindung gefunden wurde, enstehen die entsprechenden Klassenobjekte.

Für das bisherige System ist nur die Verbindung "drone_connection" von Bedeutung. Die anderen Verbindungen dienen erstmal als Platzhalter, sind aber theoretisch schon funktional.

Um die Verbindung zu nutzen muss diese nur aus den Dictionary aufgeruden werden. Eine Variable ist dabei hilfreich

    verbindung_variable = connect_dic['drone']

#### Funktionen der Verbindung

    connection.send( message , timeout = 0 )

message : Argument des Typs str. Sollte ein definiertes Keyword sein. Leerzeichen   werden Nicht ignoriert.

timeout : Argument des Typs int. Bestimmt wie lange auf ein ACK gewartet wird.
|timeout = -1 | timeout = 0 | timeout = n |
|-|-|-|
| ACK wird ignoriert, keine Reaktion wird ausgelöst | Time out error Funktion wird sofort ausgelöst | n Sekunden Wartezeit (0.1 Sekunden Genauigkeit) um das ACK zu erwarten. Wird ACK empfangen so wird die ACK Reaktionsfunktion ausgelöst. Wird n überschritten wird die Time out error Funktion wird sofort ausgelöst |

Die Funktion "connection.send" sendet den Inhalt des string arguments "message" an den Verbindungspatner des Verbindungsobjektes und überwacht ob ein ACK empfangen wird.

    connection.send_thread( args )

args : Argument des Typs list. Liste aus Argumenten welche an "connection.send" weitergegeben werden.

Funktional passiert in dieser Funktion das gleiche wie bei "connection.send" aber sie findet in einem eigenen Thread start. Definition, start und ende werden von der Funktion selbst durchgeführt. So behindert das Warten auf ein ACK den den Ablauf des Programms. Die Reaktionsfunktionen auf ACK und NACK finden ebenfalls in dem Thread statt.

    connection_status()

Diese Funktion gibt den Status einer Verbindung wieder, nachdem diese mindestens einmal nicht dynamisch (als dynamic_connection) initialisiert wurde. Zurückgegeben wird True oder False. Der Zustand wird automatisch über sekündliche Pings
###### Empfangen

Empfangen und Interpretieren von Nachrichten geschieht automatisch. Reaktion auf Keywords, ACK und NACK wir über die Reaktionsfunktionen bestimmt. Diese werden definiert in dem Unterdictionary "connection.keyword_class_dic" . Diese Unterdictionary ist ein Dictionary bestehend aus allen offiziellen Keywords und dazugehörigen Keywordklassen. Über "connection.keyword_class_dic['keyword']" lässt sich somit auf die Eigenschaften eines Keywords zugreifen.

    connection.keyword_class_dic['keyword'].ack_status

Variable mit Eigenschaften. Gibt Status eine ACK von einerm Keyword an.

|None|False|True|
|-|-|-|
|Es wird kein ACK von diesem Keyword erwartet|Es wird ein ACK von diesem Keyword erwartet aber noch nicht empfangen|Ein ACK wurde von diesem Keyword ampfangen|

    connection.keyword_class_dic['keyword'].react

Diese Variable weißt dem Keyword eine Reaktionsfunktion zu. Im undefininierten Fall wird ein None wiedergegeben.

    connection.keyword_class_dic['keyword'].ack_react

Diese Variable weißt dem ACK dieses Keyword eine Reaktionsfunktion zu. Im undefininierten Fall wird ein None wiedergegeben.

    connection.keyword_class_dic['keyword'].ack_TOE

Diese Variable weißt dem NACK dieses Keyword eine Reaktionsfunktion zu. Im undefininierten Fall wird ein None wiedergegeben.
### Schnittstelle

## Ab hier noch nicht geupdated

Innerhalb aller beteiligten Teilnehmer des lokalen Netzwerkes soll zur erfolgreichen Verbindung eine "..._interface()" Funktion vorhanden sein. Im Falle des Servers liegt die Funktion "server_interface" vor. Der Drohnen Client hat die Funktion "network_connection" dafür vorgesehen. Diese Funktion dient dazu die Verbindung zu einem Verbindungspartner aufzubauen, zu organisieren und zu empfangen.

Die Sende Funktionen werden dort abgerufen wo sie erzeugt werden und werden vorgegeben. Progammierung steht aber noch aus.

![alt text](interface_structure-1.jpg)

##### Schnittstelle von Serverside

Im Falle des Servers werden die "Connection_type_objects" organisiert in dem Dictionary "connect_dic" hinterlegt. Diese "Connection_type_objects" enstehen aus der "socket_object.accept()" Funktion und beschreiben eine Verbindung von dem Server zu einem Client. Die Funktion "server_listen()" sucht kontinuierlich nach neuen Verbindungen und sotiert diese in "connect_dic". Bis zu vier Verbindungen können so erschaffen werden.

Zum empfangen von Informationen wird Funktion "server_recv_man()" bzw. dessen Unterfunktion "server_recv()" genutzt. Ersteres erstellt Threads für alle möglichen Verbindungen. Die zweite Funktion übernimmt dann eine Verbindung innerhalb jedes Threads. Hier wird nun überprüft ob überhaupt eine Verbindung vorliegt, ob etwas empfangen wird und was empgangen wird. Für den Inhalt der Nachrichten werden die dokumentierten Keywords aus "network-communication-keywords.md" verwendet welche in "ack_dic" zugeordnet werden.

![alt text](interface_connection_management.jpg)

Geplant ist auch neben den bestehenden Befehlen Stand 03.05.2024 auch noch weiter Befehle hinzufügen welche die Verbindungen schließen, Verbindungsart in "connect_dic" ändern etc. Dies steht aber nur als Idee und ist noch nicht festgelegt.

##### Schnittstelle von Clientside

Die schnittstelle wird von AuVAReS verwaltet

### Senden von Befehlen

Funktion WIP

Das senden von Befehlen wird vor Ort (wo die Bedingung erzeugt wird) geschehen. Dafür wird eine passende Funktion bereit gestellt welche sich über verschieden Parameter wie gewünscht einstellen lässt. Der zu sende Befehl wird als Argument in string in die Funktion eingesetzt und gesendet. Der gesendete Befehl wird von dem Empfänge interpretiert welcher dann wieder das entsprechende acknowledgement sendet. Wie lange auf das acknowledgement oder ob überhaupt gewartet wird ist variabel.

### Acknowledgement

Die Acknowledgements werden durch die dictionaries "ack_dic" und "ack_status_dic" gehandelt. Sobald ein Befehl/Keyword gesendet wird, wird das dazugehörige Value im "ack_status_dic" von None auf False gesetzt. Wenn das Acknowledgement empfangen wird und dessen status im "ack_status_dic" False ist so setzt die zuständige Empfangsfunktion das Value auf True. Sobald das Value auf True gesetzt wird, wird es in der ursprünglichen Sendefunktion wieder of None gesetzt und das Acknowledgment wird als angekommen gewertet.

## Offene Baustellen

- Grundlage für das desgin ist in Bearbeitung

- Aktive Überprüfung der Verbindung über ping abtausch

- Kollisionskontrolle ist in der Entwicklung

- Display Kontrolle ist noch unbekannt. Standard Ansteuerung über Website geplant.

- Es fehlen noch Reaktionsfunktionen auf Keywords und Acknowledgement timeouts. Zugriff auf diese wurde aber schon implementiert.