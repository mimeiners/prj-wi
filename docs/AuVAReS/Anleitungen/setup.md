# Einrichtung und Inbetriebnahme
*Stand: 14.06.2024*<br>
*Autoren: Julian Höpe, Finn Katenkamp,...*
## Hardware
AuVAReS ist auf einem Nvidia Jetson Orin Nano implementiert. Bei der Hardware handelt es sich um ein Entwicklungskit, damit die gesamte Peripherie rund um den Chip genutzt werden kann. <br>
Es ist nicht zwingend notwendig das Nvidia Jetson Board mit Ubuntu Linux 20.04 zu verwenden. Alle Codes sind auch auf anderen Systemen wie Windows oder MacOS lauffähig, es müssen hierzu lediglich die `subprocess` Eingaben, welche genutzt werden um CLI-Eingaben um beispielsweise die Drohne per Wifi zu verbinden, an das jeweilige Betriebssystem angepasst werden. Die Standard-CLI Eingaben sind für Ubuntu Linux ausgelegt.
### Nvidia Jetson Nano Orin

Für die entwicklung auf dem Jetson wurde ein VNC Server darauf eingerichtet, auf dem direkt nach start zugegriffen werden kann. Die IP ist dabei via DHCP eingestellt und muss initial nachgeguckt werden. Für die Verwendung des VNC Servers muss ggf. ein Bidschirm angeschlossen werden, da der desktop sonst nicht richtig upgedatet wird.

## Software
QUICKSTART-GUIDE zu
- Python venv mit allen packages
- Requirements für Yolo on jetson
## Besonderheiten

### Inbetriebnahme Jetson Nano
Zum Flashen des Jetsons kann eine SD Karte genutzt werden. Aufgrund von Schwierigkeiten mit `Cuda` und anderen Bibliotheken ist es zu empfehlen eine NVME Festplatte zu nutzen. Zum Flaschen benötigt man eine Linux Umgebung mit dem Nvidia SDK Manager installiert. Stand Mai 2024 ist die [`Version 5.1.2`](https://developer.nvidia.com/embedded/jetpack-sdk-512) die stabilste Version. Alle, für das Projekt relevanten Bibliotheken können bei dieser Version verhältnismäßig einfach eingerichtet werden. Zu empfehlen ist dabei das Video von [JetsonHacks](https://youtu.be/art0-99fFa8?si=-EsLxhJP-dhlvC51) um Cuda richtig zu installieren und zu aktivieren.

### Python-Modul djitellopy
Aus unbekannten Gründen sorgt die Python Library [`av`](https://pypi.org/project/av/) dafür, dass OpenCV kein Anzeigefenster für die Wiedergabe öffnen kann. Deshalb wurde eine angepasste Version der djitellopy Library erstellt. Da in dieser Library kein direkter Videostream zur Verfügung steht muss die UDP Adresse an ein OpenCV `VideoCapture`-Objekt übergeben werden. Von dem kann dann einfach ein `.read` genutzt werden zum auslesen des Videos.
```python
cap = VideoCapture(tello.get_udp_video_address()+"?overrun_nonfatal=1")
```
Die Angabe `overrun_nonfatal` ist um Errors zu verhindern, da sonst der zugewiesene Speicher überfüllt wird.
```python
cap.read()
```

In dem entgültigen Programm wird das Video in einem seperaten Thread verarbeitet. In der [export_drone.py](../../../files/Drohne/main/export_drone.py) wird eine vereinfachte Klasse namens VideoGrabber für den Abgegriff und Bereitgestellung des Videos genutzt.
