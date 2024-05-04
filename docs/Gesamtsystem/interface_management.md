# Interface Management

### Setup

Der Aufbau des System besteht aus zwei Hauptcomputern. Der Computer von Wohninvest, welcher im folgenden als Server bezeichnet wird, und der Computer von AuVARes welcher als Client oder Drohnen Client bezeichnet wird. Es werden Optionen offen gehalten für einen dritten Computer und/oder einer externen Quelle zur Überwachung des Systems. Der Server ist der Ansprechpatner aller Clients und ist als notwendige Hardware des Kickers von Wohninvest zu betrachten.

### Schnittstelle

Innerhalb aller beteiligten Teilnehmer des lokalen Netzwerkes soll zur erfolgreichen Verbindung eine "..._interface()" Funktion vorhanden sein. Im Falle des Servers liegt die Funktion "server_interface" vor. Der Drohnen Client hat die Funktion "network_connection" dafür vorgesehen. Diese Funktion dient dazu die Verbindung zu einem Verbindungspartner aufzubauen, zu organisieren und zu empfangen.

Die Sende Funktionen werden dort abgerufen wo sie erzeugt werden.

##### Verbindungen

Im Falle des Servers werden die "Connection_type_objects" organisiert in dem Dictionary "connect_dic" hinterlegt. Diese "Connection_type_objects" enstehen aus der "socket_object.accept()" Funktion und beschreiben eine Verbindung von dem Server zu einem Client. Die Funktion "server_listen()" sucht kontinuierlich nach neuen Verbindungen und sotiert diese in "connect_dic". Bis zu vier Verbindungen können so erschaffen werden.

Der Dronen Client wird innerhalb des Netzwerkes nur Verbindung zu dem Server aufnehemen. Es ist somit nicht nötig meherere Verbindungen zu unterstützen. Die Funktionen der Schnittstelle werden also dadurch gesteuert das es überhaupt erst zu einer Verbindung kommt. Sobald dies geschehen muss die Funktion nur noch die Empfangenden Befehle managen. 
