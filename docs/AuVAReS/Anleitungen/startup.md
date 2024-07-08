# Startup des Jetson

Diese Anleitung bezieht sich au die Verwendung der Programms ohne die Steuerung vom Kicker.

Das Repository zum Projekt liegt im Verzeichniss `/home/jetson`. Es kann über den Ordner `jetson` auf dem desktop erreicht werden.

## Starten des Programms mit Kicker

Soll der Jetson mit der Kickersteuerung genutzt werden muss das main Terminal gestartet werden. Im der [`main.py`](files\Drohne\main\main.py) muss dann die IP-Adresse und der Port des Kickers eingestellt werden. Details siehe  [`Programm-Ablauf`](Programm-AuVAReS.md):

main Terminal:
```shell
jetson@ubuntu:~$ cd prj-wi/files/Drohne/main/
jetson@ubuntu:~/prj-wi/files/Drohne/main$ 
```
Nachdem der Server für die Socketconnection seitens des Kickers gestartet wurde kann das Hauptprogramm wie folgt über das main Terminal gestartet werden:

main Terminal:
```shell
jetson@ubuntu:~/prj-wi/files/Drohne/main$ python3 main.py 
Doing network connection
```

## Starten des Programms mit Dummy

Für den Start mit dem Dummy werden 2 Terminals benötigt. Beim Ausführen der Befehe ist die Reihnfolge zu beachten!

1. Zwei Terminals öffenen
2. In das Verzeichnis mit dem Dummy bzw. dem main-Programm wechseln
    
    Server Terminal:
    ```shell
    jetson@ubuntu:~$ cd prj-wi/files/Drohne/archiv/
    jetson@ubuntu:~/prj-wi/files/Drohne/archiv$ 
    ```
    main Terminal:
    ```shell
    jetson@ubuntu:~$ cd prj-wi/files/Drohne/main/
    jetson@ubuntu:~/prj-wi/files/Drohne/main$ 
    ```

3. Server Dummy starten:

    Server Terminal:
    ```shell
    jetson@ubuntu:~/prj-wi/files/Drohne/archiv$ python3 server_dummy.py
    Server listening on ubuntu:8765
    ```

4. main-Programm starten:

    main Terminal:
    ```shell
    jetson@ubuntu:~/prj-wi/files/Drohne/main$ python3 main.py 
    Doing network connection
    ```

    Server Terminal:
    ```shell
    jetson@ubuntu:~/prj-wi/files/Drohne/archiv$ python3 server_dummy.py
    Server listening on ubuntu:8765
    Got connection from ('127.0.0.1', 58446)
    Received: HELLO SERVER FROM network_connection
    Zu sendende Nachricht (INDEX) [0,1,3,5,6,7]: Received: HELLO SERVER FROM network_connection
    ```
    Die Terminals sollten dann den angegebenen Text anzeigen. Der Port auf der Serverseite kann variieren.

5. Verbindung Prüfen:

    Server Terminal:
    ```shell
    0
    Sent: ping
    Zu sendende Nachricht (INDEX) [0,1,3,5,6,7]: Received: hi
    ```
    main Terminal:
    ```shell
    RECV:ping 
    SEND: hi
    ```

6. Drohne einschalten:

    Drohne einschalten und `1` im Server Terminal eingeben\
    Wenn die Nachricht `notify_drone_connected` im Server Terminal empfangen wird, ist die Drohen mit dem Jetson verbunden.

    `2` im Server Terminal eingeben\
    Accnowledgement senden

7. Drohne starten:

    `3` im Server Terminal eingeben\
    Die Drohne wird gestartet und positioniert sich.
    
8. Spielstart:

    Sobald die Drohne fertig ist und das Spiel starten kann wird ein `notify_gamestart` im Server Terminal empfangen.
    Dann kann `4` im Server Terminal eingegeben werden und das Spiel startet.

9. Spiel beenden:

    Soll das Spiel beendet werden kann man eine `7` im Server Terminal eingeben und die drohne landet.

10. Während des Spiels:

    `5` senden im Server Terminal für `notify_new_goal`: Ereignissimulation Tor\
    `6` senden im Server Terminal für `notify_foul`: Ereignissimulation Faul

    Accnowledgements:\
    Wird ein `pleas_wait` empfangen, wird dies durch Senden von `8` bestätigt.\
    Wird ein `pleas_resume` empfangen, wird dies durch Senden von `9` bestätigt.

