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

