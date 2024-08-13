# Programmablauf AuVAReS
## Hauptprogramm
### Kommunikationsschnittstelle zum Kicker
Das Hauptprogramm ist von AuVAReS ist so aufgebaut, dass die RJ45 Schnittstelle des Jetson-Boards genutzt wird um mit dem WI4.0-Kicker zu kommunizieren. Hierfür wird eine `socket-connection` mit Python aufgebaut, AuVAReS ist als Client konfiguriert.<br>
Die IP-Adresse und der entsprechende Port des Kickers zu dem sich AuVAReS verbinden soll sind in der `main.py` mit den Variablen `host` (IP-Adresse als String) und `port` (Port als Integer) einzustellen.<br><br>
Die Kommunikationsschnittstelle steuert den gesamten Ablauf von AuVAReS, hierzu wird die Funktion `network_connection` aus der Datei `auxiliaryFunctions.py` genutzt. Die Funktion wird in einem dedizierten Thread aufgerufen und hört die Socket-Verbindung zum Kicker auf Keywords (vgl. Gesamtsystem) ab:<br>
K : Kicker <br>
A : AuVAReS

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

Standardmäßig wird bei jedem empfangenen Keyword automatisch ein ACK gesendet.

### Verbinden mit der Drohne
AuVAReS verbindet sich automatisch mit der Drohne, sobald diese eingeschaltet ist. Für das Einschalten gibt der Kicker nach der Anmeldung entsprechende Anweisungen auf den Monitoren aus. Der Benutzer wird aufgefordert die Drohne anzuschalten und dies auch zu quittieren. Bei Quittierung sendet der Kicker das Keyword *notify_drone_powered*. Sobald AuVAReS dieses Keyword empfangen hat wird es mit passenden ACK bestätigt und die Funktion `connect_wifi` aus `auxiliaryFunctions.py` wird aufgerufen. In diesem Funktion sind die SSIDs der drei verwendeten Drohnen in einer Liste aufgeführt. Die Funktion aktiviert mit dem Modul `subprocess` mittels CLI die WLAN-Schnittstelle auf dem Jetson-Board und scannt die verfügbaren Netzwerke. Anschließend versucht die Funktion einen Verbindungsaufbau mit einem der in der Liste SSIDs enthaltenem Netzwerk. Anschließend wird geprüft, ob die Verbindung erfolgreich hergestellt wurde. Nach erfolgreicher Verbindung wird die Drohne dem VideoHandler-Objekt mittels der Methode `set_drone` hinzugefügt. Bei erfolgreicher Verbindung signalisiert die Drohne dies dem Kicker durch das Senden des Keywords *notify_drone_connected*.<br><br>
Nachdem die Drohne verbunden wurde, wird die Temperatur und der Ladezustand der Drohne ausgelesen. Bei einer Temperatur von über 70°C oder einer Akkuladung unter 50% wird eine Meldung über verkürzte Spieldauer auf den Kickerdisplays ausgegeben.

### Start der Drohne
Nachdem die Drohne erfolgreich verbunden ist und der Kicker die Statusmeldung quittiert hat, wird der Nutzer vom Kicker aufgefordert die Startfreigabe für die Drohne zu erteilen. Empfängt die Drohne das Keyword *notify_start_permission* quittiert sie den Empfang und die Drohne wird gestartet. Die Drohne hebt nun von ihrem Landingpad ab und richtet sich über dem Kickeraus. Nach Erreichen ihrer Position wird das Spiel durch Senden des Keywords *notify_gamestart* von der Drohne gestartet.

### Videoaufnahme und Wiedergabe
AuVAReS ist in der Lage, Videos aufzunehmen und wiederzugeben. Dazu wird die Klasse `VideoHandler` aus der Datei `VideoHandler.py` genutzt. Ein Objekt dieser Klasse wird in der `main.py` initialisiert. Im Laufe des Programmstarts wird diesem VideoHandler-Objekt ein Drohnenobjekt mit den Methode `set_drone` hinzugefügt. Dadurch kann der Videostream der Drohne mithilfe der Methode `get_img` Frame für Frame empfangen werden. Damit das Aufnehmen des Videos von der Drohne nicht das gesamte Programm stoppt, wird die Videoaufnahme in einem weiteren Thread ausgeführt. Der Aufnahme-Thread kann mit den Methoden `startRecord` und `stopRecord` gestartet bzw. gestoppt werden. Das Video wird durch die Methode `videoRecord` aufgenommen, solange das Attribut `record` den Wert `true` hat. <br>
Die Wiedergabe des Videos wird durch die Methode `videoPlayback` realisiert, welche in einzelnen Fällen (Tor, Foul etc.) aufgerufen wird. Der Aufruf dieser Methode erfolgt entweder aus dem Ergebnis der Objekterkennung (interner Trigger) oder durch den Empfang eines entsprechenden Keywords im `network_connection`-Thread (externer Trigger vom Kicker). 

### Ende des Spiels / Landung der Drohne
Um das Spiel zu beenden sendet der Kicker das Keyword *notify_gameover*, AuVAReS quittiert den Empfang mit dem ACK. Für die Beendigung wird eine Reihe von Schritten durchgeführt:
1. Landung der Drohne
2. Beenden der Videoaufnahme
3. Reinitialisierung des VideoHandler-Objektes, um alle Variablen inkl. Drohne zu resetten.<br><br>
AuVAReS ist nun wieder bereit für ein neues Spiel.
