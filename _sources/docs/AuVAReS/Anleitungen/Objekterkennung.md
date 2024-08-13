# Objekterkennung
## YOLOv8 Datensatzerstellung und Training
### Erstellen eines Datensatzes

Anhand von selbstaufgenommenen Bildern und Videos mit Drohne und Smartphone wird der Datensatz erstellt. Dies ist nötig um die Objekte zuverlässig zu erkennen und nicht auf vortrainierte Objekte aus Yolo selber zurückzugreifen, das es dabei zu unzuverlässigkeiten kommen kann und Objekte nicht zuverlässig erkannt werden. Für den genutzten Datensatz wurden ähnliche Bedingungen geschaffen, die im Flug der Drohne zu erwarten sind. Angepasst ist so beispielsweise die Auflösung. Die Ausrichtung des Bildes, welches durch einen Spiegel den Bereich unter der Drohne erfasst, wurde hier zudem stets nach unten gefilmt und fotographiert.
Das Bildmaterial wurde auf die kostenlos nutzbare Plattform Roboflow importiert, dort ist ein selbsterstelltes Projekt "AuVAReS RedBall" [https://universe.roboflow.com/auvares-redball/auvares-red-ball-detection] angelegt. Beim Importieren werden die Bilder der Auswertung hinzugefügt. Für Videos ist es möglich, aus den einzelnen Frames eine bestimmte Anzahl an Bildern zu generieren. Dadurch kamen ingesamt ca. 900 Bilder zusammen zusammen mit einem Datensatz eines anderen Users, welcher "Red Ball Finder" unabhängig erstellt und zur Nutzung freigegeben hat.
Die Bilder sind im nächsten Schritt verarbeitet worden. Es ist dazu nötig eine Bounding-Box um das zu erkennende Objekt zu ziehen und diese Box der entsprechenden Bezeichung zuzuweisen. Im Projekt genutzte Objekt-Bezeichnungen sind "red_ball", "kicker", "landingpad" und "pointer_kicker". Letzteres ist der Pfeil im Landepad.
Nachdem alle Bilder bearbeitet sind, ist der Datensatz für Yolov8 generiert worden, dabei wurden die Voreinstllungen genutzt. Für diese Arbeitsschritte gibt es Anleitungen von Roboflow als auch anderen zu finden, z. B. auf Youtube.

Es ist zu empfehlen nur die Boundingboxen zu nutzen. Auf die Nutzung von z. B. Polygonzügen zur Objekterkennung wurde letztendlich verzichtet, da hier die Handhabung anders ist als für Bounding-Boxen.

### Training durch den HSB-KI-Server (Umsetzung und Dauer) ; nur für uns die Überschrift?

Um die KI mit dem erstellten Datensatz trainieren zu können, wurde mithilfe von X2Go auf einem der sogenannten HSB-KI-Server zugegriffen. Der jeweilige Host besitzt die Bezeichnung **v-ki-001**. Durch das verändern der Zahl von 001 bis 005, kann der jeweiliger Server ausgewählt werden. In unserem Fall wurde der Server 005 genutzt. Dazu wurden folgende Einstellungen in den Sitzungsvoreinstellungen angepasst.

* Sitzung
  * Host: v-ki-005
  * Login: `<Benutzername>`
  * SSH-Port: 22
  * Proxy-Server für SSH-Verbindung verwenden: aktivieren
    * Typ: SSH
    * Host: apollon.fk4.hs-bremen.de
    * Port: 22
    * Gleiche Anmeldung wie für X2Go-Server: aktivieren
    * Gleiches Kennwort wie für X2Go-Server: aktivieren
  * Sitzungsart: XFCE
* Medien
  * Audiounterdtützung aktivieren: deaktivieren

Als nächstes wird ein virtuelles Python environment erstellt. Dazu wird das conda-terminal genutzt. Dies ist unter anderem unter Anwendungen/Entwicklung/Anaconda3 zu finden bzw. zu starten. Dabei werden folgende Befehle ausgeführt.

```
conda create -n prj-env 
conda activate prj-env  
python -m pip install ultralytics
python -m pip install roboflow
```

Somit ist die virtuele Umgebung fertig gestellt. In dem Python-Skript yolov8_train.py unter files/Drohne/YOLOv8_test wird der Vorgang und die Ausführung des Training beschrieben. In unserem Fall wurde ein zentrales Verzeichnis auf dem Hochschulserver der HSB für die Speicherung der Datensätze sowie der trainierten YOLO-Versionen angelegt (siehe yolov8_train.py). Dies muss je nach Bedarf angepasst werden.

## Handling der Drohne und Verwendung der Tello Befehle

Bei der uns vorliegender Drohne handelt es sich um eine RYZE Tello Drohne, welche mit einem python-skript gesteuert wird. Dafür wurde das Paket djitellopy installiert. Auf der Website [https://djitellopy.readthedocs.io/en/latest/tello/]() lassen sich die diversen Steuerbefehle herausfinden. Aufgrund des kleinen Flugsektors kam für den freien Flugbetrieb nur der send_rc_control() Befehl infrage. Dieser gibt bei einer voreingestellten Geschwindigkeit die prozentuale Nutzung der geschwindikeit in die verschiedenen Richtungen an. Konkretere Steuerbefehle wie move() konnten nicht genutzt werden, da diese eine minimale Flugstrecke von 20 cm besitzen und die Drohne oft nur wenige cm fliegen sollte. Da die Drohne von einer vorgegebenen Startposition abhebt, wird eine feste Startroutine genutzt. Bei dieser werden die takeoff(), move_up(), move_forward(), move_right() und rotate_clockwise() genutzt. So wird eine sichere Startposition gewährleistet.

## Bildauswertung

Das eingehende Video wird Bildweise ausgewertet. Dies geschieht zunächst, nachdem in python eine temporäre Kopie des Bildes einer Variable zugewiesen wird. Hat Yolo das Bild ausgewertet wird mit "results" innerhalb einer Schleife jedes erkannte Objekt ausgewertet. In der Auswertung werden Rahmen mit der "Confidence", also wie sicher Yolo sich ist, das richtige Objekt erkannt zu haben, sowie die Größe des Objektes im Bild in Pixeln. Diese Auswertung wird visuell nur im Debug-Videostream ausgegeben. Für die weitere Verarbeitung sind zudem der Mittelpunkt des "desired_objects" ausgewertet. Es handelt sich um das Objekt, anhand des die Drohne gesteuert wird, im regulären Flugbetrieb "kicker" bei Landung "landingpad" oder "pointer_kicker".

## Befehlskette anhand der Auswertung

> Hinweis: Kommentierten Code beachten!

#### Startvorgang

Der Start verläuft immer gleich. Es ist eine Routine vorprogrammiert. Mit welcher die Drohne  vom Landepad am Kicker sich ungefähr mittig über dem Kicker positioniert. Ausgeführt wird es so, da die Drohne vorher keine Orientierung hat, wo sie sich befindet, bzw. wo sich der Kicker befindet. Nachdem diese Startsequenz ausgeführt ist. Wird der reguläre Flugbetrieb ausgeführt.
Es ist zu beachten, dass die Drohne Abweichungen hat und daher nicht immer genau mittig über dem Kicker die Position einnimmt.

#### Flugbetrieb

Ist der Start abgeschlossen, wird das Objekt "kicker" gesucht. Bei erkanntem Objekt wird der Mittelpunkt von "kicker" ausgewertet. Im Anschluss wird geprüft, in welchem Abschnitt des Rasters sich der Mittelpunkt befindet. Hiermit als auch mit der Area, also größe der Bounding-Box des Kickers, werden die Flugbefehle generiert und anschließend gesendet.
Wie groß der Wert für die Area des Objektes ist in einer sicheren Höhe wurde durch Flugtests ermittelt.

#### Landung

Bei angeforderter Landung wird das "desired_object" von "kicker" auf "landingpad" geändert. Hierbei wird das Raster geändert. Für die Landing wird der Mittelpunkt für die Steuerung genutzt. So soll sich die Drohne so ausrichten, dass der Mittelpunkt des Landepads im mittleren Feld des Rasters ist. Ist dies der Fall senk sich die Drohne ab. Wird in der Zwischenzeit der Mittelpunkt in einem anderen Feld dedektiert als in dem mittleren Feld, wird die Position der Drohne korrigiert.
Ist die Drohne nah genug am Landeplatz, so wird "desired_object" zu "pointer_kicker" geändert. Der Ablauf ist gleich wie zuvor. Wenn die Drohne dieses mal nah genug ist, so wird die Drohne um 90° gedreht und der Tello-Befehl zum landen gesendet.
