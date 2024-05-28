## Verwenden der Spielsteuerung zu Testzwecken
_Stand 28.05.2024 | V0.0_

Zum Starten der Spielsteuerung muss `LVL1_threads.py` als Administrator ausgeführt werden, zum beispiel in
```
sudo thonny
```
Jetzt können auf der Website des Kickers Spielernamen eingetragen werden. Erst danach ist es wirklich notwendig, dass die Verbindung zu AuVAReS steht. Nach ein paar erfolgslosen Verbindungsversuchen wird eine Fehlermeldung ausgegeben und das Spiel wird gestartet. Da es während des Spielverlaufs zu einem Verbindungsaufbau kommen kann, wird bei jeder zu sendenden Nachricht an AuVAReS zunächst der Verbindungsstatus geprüft, bevor die Nachricht gesendet oder übersprungen wird.
Lorem ispum dolor set amet