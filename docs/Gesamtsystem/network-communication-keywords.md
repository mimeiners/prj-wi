### Schlüsselwörter bei Kommunikation im Netzwerk von Kicker-AuVAReS
Stand: 14.5.24

Das Schlüsselwort wird in das Netzwerk gesendet und sekündlich wiederholt, solange vom Empfänger kein ACK gesendet wird. Dies stellt sicher, dass Meldungen vom Empfänger wirklich verarbeitet wurden, bevor das Spielgeschehen fortgesetzt wird. Ein timeout für diese Wiederholungen ist empfohlen.


## Version:03
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

Liste für Reaktion für empfangene Nachrichten, Kickerseite

| Keyword | Keyword Reaktion | ACK Reaktion | NACK Reaktion | Kommentare |
|-|-|-|-|-|
| ping |  | setze Status der Verbindung auf True | Setze Status der Verbindung auf False | ACK reaktion und NACK sind Hardcoded |
| notify_drone_connect | | | | Sinn noch unbekannt. Der Verbindung status der entsprechenden Klassen Instanz sollte den gleichen Zweck aktive erfüllen |
| notify_start_permission | | sys_status auf ingame setzen | | Ein NACK steht nicht zur Erwartung, die Verbindung sollte zuvor überprüft werden. Ansonsten können wir auch einfach nen TOE setzen und sagen das der Verbindungsstatus auf False gesetzt werdem soll. Das macht aber schon der Ping. Ein return reicht also auch. |
| notify_gamestart | | | | Entsprechende Aufgaben sind bereits im ACK von notify_start_position, solle die getrennt sein? Sobald die Drohne in Position ist soll es ja losgehen |
| notify_newgoal | | | | hat eigene Reaktionen |
| notify_foul | | | | hat eigene Reaktionen |
| notify_gameover | | | | hat eigene Reaktionen |
| please_wait | sys_status auf wait ingame setzen | | | |
| please_resume | sys_status auf ingame setzen | | | |

Standardmäßig wird bei jedem empfangenen Keyword automatisch ein ACK gesendet.

## Version:01
| Sender  | Schlüsselwort  | Beschreibung |ACK|
|:----------|:----------|:----------|:----------|
| K | ping | Wird mindestens zum Programmstart benutzt, um AuVAReS zu detektieren; nach timeout werden keine AuVAReS-abhängigängen Funktionen verwendet.   |hi
| K | notify_gamestart    |Meldung, dass die Drohne gestartet werden kann; Spiel startet erst nach Meldung von ACK    |drone_in_position
| K | notify_newgoal |Ein Tor ist gefallen, ein replay sollte gestartet werden|received_newgoal 
| K | notify_foul |Ein Regelverstoß ist vorgefallen, ein replay sollte gestartet werden|received_foul
| K | notify_gameover |Zusätzlich zum replay des Siegertores wird die Abschlussroutine der Drohne ausgeführt.|received_gamover
| A | please_wait| AuVAReS kann das Spiel pausieren, bspw. wenn es Zwischenfälle gibt. Tore werden nicht gezählt. |waiting
| A |please_resume| AuVAReS ist wieder einsatzbereit und erlaubt dem Kicker, wieder Tore zu zählen.|gaming

