# Einrichtung und Inbetriebnahme
## Hardware
AuVAReS ist auf einem Nvidia Jetson Orin Nano implementiert. Bei der Hardware handelt es sich um ein Entwicklungskit, damit die gesamte Peripherie rund um den Chip genutzt werden kann. <br>
Es ist nicht zwingend notwendig das Nvidia Jetson Board mit Ubuntu Linux 20.04 zu verwenden. Alle Codes sind auch auf anderen Systemen wie Windows oder MacOS lauffähig, es müssen hierzu lediglich die `subprocess` Eingaben, welche genutzt werden um CLI-Eingaben um beispielsweise die Drohne per Wifi zu verbinden, an das jeweilige Betriebssystem angepasst werden. Die Standard-CLI Eingaben sind für Ubuntu Linux ausgelegt.
### Nvidia Jetson Nano Orin

Für die Entwicklung auf dem Jetson wurde ein VNC-Server darauf eingerichtet, auf dem direkt nach start zugegriffen werden kann. Die IP ist dabei via DHCP eingestellt und muss initial nachgeguckt werden. Für die Verwendung des VNC-Servers muss ggf. ein Bidschirm angeschlossen werden, da der desktop sonst nicht richtig upgedatet wird.

## Software
Die verwendete Python-Version ist `3.8.10`, eine Liste der installierten Module ist [hier](#python-module) zu finden. Python inkl. aller benötigten Module ist bereits auf dem bestehenden Image installiert. Zudem sind neben Python alle weiteren Installationen wie beispielsweise: <br>
- Cuda
- Torch
- VideoCodecs
- OpenCV

bereits auf dem bestehenden Image installiert.


## Besonderheiten

### Inbetriebnahme Jetson Nano
Zum Flashen des Jetsons kann eine SD Karte genutzt werden. Aufgrund von Schwierigkeiten mit `Cuda` und anderen Bibliotheken ist es zu empfehlen eine NVME Festplatte zu nutzen. Zum Flaschen benötigt man eine Linux Umgebung mit dem Nvidia SDK Manager installiert. Stand Mai 2024 ist die [`Version 5.1.2`](https://developer.nvidia.com/embedded/jetpack-sdk-512) die stabilste Version. Alle für das Projekt relevanten Bibliotheken können bei dieser Version verhältnismäßig einfach eingerichtet werden. Zu empfehlen ist dabei das Video von [JetsonHacks](https://youtu.be/art0-99fFa8?si=-EsLxhJP-dhlvC51) um Cuda richtig zu installieren und zu aktivieren.

### Python-Modul djitellopy
Aus unbekannten Gründen sorgt die Python Library [`av`](https://pypi.org/project/av/) dafür, dass OpenCV kein Anzeigefenster für die Wiedergabe öffnen kann. Deshalb wurde eine angepasste Version der djitellopy Library erstellt. Da in dieser Library kein direkter Videostream zur Verfügung steht muss die UDP Adresse an ein OpenCV `VideoCapture`-Objekt übergeben werden. Von dem kann dann einfach ein `.read` genutzt werden zum auslesen des Videos.
```python
cap = VideoCapture(tello.get_udp_video_address()+"?overrun_nonfatal=1")
```
Die Angabe `overrun_nonfatal` ist um Errors zu verhindern, da sonst der zugewiesene Speicher überfüllt wird.
```python
cap.read()
```

In dem endgültigen Programm wird das Video in einem seperaten Thread verarbeitet. In der [export_drone.py](../../../files/Drohne/main/export_drone.py) wird eine vereinfachte Klasse namens VideoGrabber für den Abgriff und Bereitstellung des Videos genutzt.

## Python-Module
| Modul                       | Version                    |
| --------------------------- | -------------------------- |
| absl-py                     | 2.1.0                      |
| apturl                      | 0.5.2                      |
| astunparse                  | 1.6.3                      |
| attrs                       | 23.2.0                     |
| av                          | 12.0.0                     |
| bcrypt                      | 3.1.7                      |
| blinker                     | 1.4                        |
| Brlapi                      | 0.7.0                      |
| cachetools                  | 5.3.3                      |
| cattrs                      | 23.2.3                     |
| certifi                     | 2019.11.28                 |
| chardet                     | 3.0.4                      |
| charset-normalizer          | 3.3.2                      |
| Click                       | 7.0                        |
| colorama                    | 0.4.3                      |
| contourpy                   | 1.1.1                      |
| coremltools                 | 7.2                        |
| cryptography                | 2.8                        |
| cupshelpers                 | 1.0                        |
| cycler                      | 0.10.0                     |
| dbus-python                 | 1.2.16                     |
| decorator                   | 4.4.2                      |
| defer                       | 1.0.6                      |
| distro                      | 1.4.0                      |
| distro-info                 | 0.23+ubuntu1.1             |
| djitellopy                  | 2.5.0                      |
| duplicity                   | 0.8.12.0                   |
| entrypoints                 | 0.3                        |
| evdev                       | 1.7.1                      |
| exceptiongroup              | 1.2.1                      |
| fasteners                   | 0.14.1                     |
| ffmpeg-python               | 0.2.0                      |
| filelock                    | 3.14.0                     |
| flatbuffers                 | 24.3.25                    |
| fonttools                   | 4.52.1                     |
| fsspec                      | 2024.5.0                   |
| future                      | 0.18.2                     |
| gast                        | 0.4.0                      |
| google-auth                 | 2.29.0                     |
| google-auth-oauthlib        | 1.0.0                      |
| google-pasta                | 0.2.0                      |
| graphsurgeon                | 0.4.6                      |
| grpcio                      | 1.64.0                     |
| h5py                        | 3.10.0                     |
| httplib2                    | 0.14.0                     |
| idna                        | 2.8                        |
| imageio                     | 2.34.1                     |
| importlib_metadata          | 7.1.0                      |
| importlib_resources         | 6.4.0                      |
| Jetson.GPIO                 | 2.1.1                      |
| jetson-stats                | 4.2.8                      |
| Jinja2                      | 3.1.4                      |
| keras                       | 2.13.1                     |
| keyring                     | 18.0.1                     |
| kiwisolver                  | 1.0.1                      |
| language-selector           | 0.1                        |
| lapx                        | 0.5.9                      |
| launchpadlib                | 1.10.13                    |
| lazr.restfulclient          | 0.14.2                     |
| lazr.uri                    | 1.0.3                      |
| libclang                    | 18.1.1                     |
| lockfile                    | 0.12.2                     |
| louis                       | 3.12.0                     |
| macaroonbakery              | 1.3.1                      |
| Mako                        | 1.1.0                      |
| Markdown                    | 3.6                        |
| MarkupSafe                  | 2.1.5                      |
| matplotlib                  | 3.7.5                      |
| monotonic                   | 1.5                        |
| mpmath                      | 1.3.0                      |
| networkx                    | 3.1                        |
| numpy                       | 1.24.4                     |
| oauthlib                    | 3.1.0                      |
| olefile                     | 0.46                       |
| onboard                     | 1.4.1                      |
| onnx                        | 1.16.1                     |
| onnx-graphsurgeon           | 0.3.12                     |
| opencv-contrib-python       | 4.9.0.80                   |
| opencv-python               | 4.9.0.80                   |
| openvino                    | 2024.1.0                   |
| openvino-telemetry          | 2024.1.0                   |
| opt-einsum                  | 3.3.0                      |
| packaging                   | 20.9                       |
| pandas                      | 2.0.3                      |
| paramiko                    | 2.6.0                      |
| pexpect                     | 4.6.0                      |
| pillow                      | 10.3.0                     |
| pip                         | 24.0                       |
| protobuf                    | 3.20.3                     |
| psutil                      | 5.9.8                      |
| py-cpuinfo                  | 9.0.0                      |
| pyaml                       | 24.4.0                     |
| pyasn1                      | 0.6.0                      |
| pyasn1_modules              | 0.4.0                      |
| pycairo                     | 1.16.2                     |
| pycrypto                    | 2.6.1                      |
| pycups                      | 1.9.73                     |
| pygame                      | 2.5.2                      |
| PyGObject                   | 3.36.0                     |
| PyJWT                       | 1.7.1                      |
| pymacaroons                 | 0.13.0                     |
| PyNaCl                      | 1.3.0                      |
| pynput                      | 1.7.7                      |
| pyparsing                   | 2.4.6                      |
| pyRFC3339                   | 1.1                        |
| python-apt                  | 2.0.1+ubuntu0.20.4.1       |
| python-dateutil             | 2.9.0.post0                |
| python-dbusmock             | 0.19                       |
| python-debian               | 0.1.36+ubuntu1.1           |
| python-xlib                 | 0.33                       |
| pytz                        | 2024.1                     |
| pyxdg                       | 0.26                       |
| PyYAML                      | 5.3.1                      |
| requests                    | 2.32.2                     |
| requests-oauthlib           | 2.0.0                      |
| requests-unixsocket         | 0.2.0                      |
| rsa                         | 4.9                        |
| scipy                       | 1.10.1                     |
| seaborn                     | 0.13.2                     |
| SecretStorage               | 2.3.1                      |
| setuptools                  | 45.2.0                     |
| simplejson                  | 3.16.0                     |
| six                         | 1.14.0                     |
| smbus2                      | 0.4.3                      |
| sympy                       | 1.12                       |
| systemd-python              | 234                        |
| tensorboard                 | 2.13.0                     |
| tensorboard-data-server     | 0.7.2                      |
| tensorflow                  | 2.13.1                     |
| tensorflow-cpu-aws          | 2.13.1                     |
| tensorflow-estimator        | 2.13.0                     |
| tensorflow-hub              | 0.12.0                     |
| tensorflow-io-gcs-filesystem| 0.35.0                     |
| tensorflowjs                | 3.18.0                     |
| tensorrt                    | 8.5.2.2                    |
| termcolor                   | 2.4.0                      |
| thop                        | 0.1.1.post2209072238       |
| torch                       | 2.1.0a0+41361538.nv23.6    |
| torchvision                 | 0.16.2+c6f3977             |
| tqdm                        | 4.66.4                     |
| typing_extensions           | 4.5.0                      |
| tzdata                      | 2024.1                     |
| ubuntu-drivers-common       | 0.0.0                      |
| ubuntu-pro-client           | 8001                       |
| uff                         | 0.6.9                      |
| ultralytics                 | 8.2.22                     |
| urllib3                     | 1.25.8                     |
| urwid                       | 2.0.1                      |
| wadllib                     | 1.3.3                      |
| Werkzeug                    | 3.0.3                      |
| wheel                       | 0.34.2                     |
| wrapt                       | 1.16.0                     |
| xkit                        | 0.0.0                      |
| zipp                        | 3.18.2                     |
