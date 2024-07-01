# Bekannte Probleme
## Drohnensteuerung

- Der takeoff() Befehl führte diverse Male zu einem Absturz des Programms, da er auf eine "response" der Drohne wartet und diese Abfrage manchmal übersprungen wird, wodurch die Drohne keine weiteren Steuerbefehle akzeptiert. Dies führt zu dem Error "no-joystick" und beendet das Programm.
- Nachdem die Drohne abhebt kann es sein, dass diese absinkt. Dies liegt daran, dass die Drohne beim Start ca. 20 cm über dem Boden verweilen will. Driftet diese am Rand des Kickers z. B. ab und verlässt den Bereich, sinkt die Drohne auf die Höhe des Bodens. Daher muss die Fläche der Startplattform groß genug sein.
- Gelegentlich werden Befehle der Drohne als nicht akzeptiert beantwortet, hierbei tritt möglicherweise der Fehler auf, dass die Drohne den Befehl ausführt und die Flugsteuerung den Befehl erneut übermittelt. Dadurch wird ein Befehl ungewollt doppelt ausgeführt.
