### Schlüsselwörter bei Kommunikation im Netzwerk von Kicker-AuVAReS
Stand: 3.5.24

Das Schlüsselwort wird in das Netzwerk gesendet und sekündlich wiederholt, solange vom Empfänger kein ACK gesendet wird. Dies stellt sicher, dass Meldungen vom Empfänger wirklich verarbeitet wurden, bevor das Spielgeschehen fortgesetzt wird. Ein timeout für diese Wiederholungen ist empfohlen.

Unklar: Was soll passieren wenn kein ACK kommt?

## Version:02 ##
| Sender  | Schlüsselwort  | Beschreibung |ACK|
|:----------|:----------|:----------|:----------|
| K | ping | Wird mindestens zum Programmstart benutzt, um AuVAReS zu detektieren; nach timeout werden keine AuVAReS-abhängigängen Funktionen verwendet.   |hi
| K | notify_drone_connect | Meldung, dass die Drone eingeschaltet ist | connection_established
| K | notify_start_permission | Meldung, dass die Drone freigegeben ist zum Starten | drone_in_position
| A | notify_gamestart    | Meldung, dass das Spiel gestartet werden kann; Spiel startet erst nach Meldung von ACK    | game_started
| K | notify_newgoal |Ein Tor ist gefallen, ein replay sollte gestartet werden|received_newgoal 
| K | notify_foul |Ein Regelverstoß ist vorgefallen, ein replay sollte gestartet werden|received_foul
| K | notify_gameover |Zusätzlich zum replay des Siegertores wird die Abschlussroutine der Drohne ausgeführt.|received_gamover
| A | please_wait| AuVAReS kann das Spiel pausieren, bspw. wenn es Zwischenfälle gibt. Tore werden nicht gezählt. |waiting
| A |please_resume| AuVAReS ist wieder einsatzbereit und erlaubt dem Kicker, wieder Tore zu zählen.|gaming

## Version:01 ##
| Sender  | Schlüsselwort  | Beschreibung |ACK|
|:----------|:----------|:----------|:----------|
| K | ping | Wird mindestens zum Programmstart benutzt, um AuVAReS zu detektieren; nach timeout werden keine AuVAReS-abhängigängen Funktionen verwendet.   |hi
| K | notify_gamestart    |Meldung, dass die Drohne gestartet werden kann; Spiel startet erst nach Meldung von ACK    |drone_in_position
| K | notify_newgoal |Ein Tor ist gefallen, ein replay sollte gestartet werden|received_newgoal 
| K | notify_foul |Ein Regelverstoß ist vorgefallen, ein replay sollte gestartet werden|received_foul
| K | notify_gameover |Zusätzlich zum replay des Siegertores wird die Abschlussroutine der Drohne ausgeführt.|received_gamover
| A | please_wait| AuVAReS kann das Spiel pausieren, bspw. wenn es Zwischenfälle gibt. Tore werden nicht gezählt. |waiting
| A |please_resume| AuVAReS ist wieder einsatzbereit und erlaubt dem Kicker, wieder Tore zu zählen.|gaming

