### Schlüsselwörter bei Kommunikation im Netzwerk von Kicker-AuVAReS
Stand: 04.06.24

Das Schlüsselwort wird in das Netzwerk gesendet und sekündlich wiederholt, solange vom Empfänger kein ACK gesendet wird. Dies stellt sicher, dass Meldungen vom Empfänger wirklich verarbeitet wurden, bevor das Spielgeschehen fortgesetzt wird. Ein timeout für diese Wiederholungen ist empfohlen.


## Version:04
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

