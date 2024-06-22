## Die Spielsteuerung des Kickers

Die Spielsteuerung ist die zentrale Logik des Kickers. Sie besteht aus sechs python-Skripts, die in drei Ebenen oder Level unterteilt sind: 
- Level 1: die oberste Ebene, in der alle Threads gestartet werden
- Level 2: Subsysteme, die parallel ausgeführt werden
- Level 3: hier sind globale Variablen vorhanden, auf die mehrere LVL2-Programme zugreifen; sowie Übersicht über die Routinen und Reaktionen auf Events in Level 2

Diese Hierarchie entsteht daraus, dass Variablen in ein Python-Skript importiert werden können, aber nicht wieder zurückgegeben werden können. Wenn ein Subsystem den Punktestand ändert, und ein anderes diesen auslesen will, muss dieser Wert in einer Import-Ebene unter beiden liegen - dafür ist Level 3 vorhanden. Diese Problematik gäbe es mit einer einzigen Datei nicht; der Übersicht halber wurden die Subsysteme aber aufgeteilt. Außerdem ermöglicht die Aufteilung ein besseres Arbeiten mit GIT, da einfacher an mehreren Dateien gleichzeitig gearbeitet werden kann, ohne viele merge conflicts zu erzeugen.

**ABBILDUNG ZU DEN THREADS** 🅾

### Hauptdatei (LVL1_threads.py)
Diese Datei ist die Datei, von der aus alles aufgerufen wird und Threads gestartet werden. Diese Datei sollte automatisch nach booten des Pis gestartet werden, um Spiele zu ermöglichen. **Dieses Skript muss als Admin ausgeführt werden, da GPIO in LVL2 sonst nicht verwendet werden kann.**
Eine Ausnahme der Skript-Anordnung stellt hier die Not-Aus-Routine dar, da sie nicht auf Level 2 sondern auch in Level 1 enthalten ist. Dadurch wird gewährleistet, dass die Funktion immer verfügbar ist und nicht eine andere Datei durch ihr Fehlen die Not-Aus-Funktion beeinträchtigt. (Das System wurde außerhalb des Labors nicht in Betrieb genommen und der Taster wurde nicht eingebaut. Es war auch ein normaler Taster und kein geeigneter Unterbrecher.)

### Torerkennung (LVL2_goal_detection.py)
Zwei Pins des GPIO des Raspberrys werden auf LOW geprüft, was beduetet, dass ein Reflektionslichttaster in der Ballrückgabe ausgelöst wurde. **Muss als Admin ausgeführt werden (bzw. LVL1, das LVL2 importiert).**
Der Code ist sehr übersichtlich und einfach zu verstehen. Die Funktion ```init()``` muss aufgerufen werden, bevor der restliche Code in ```goal()``` benutzt werden kann. ```GPIO.setmode(GPIO.BOARD)``` bedeutet, dass als Pinnummern nicht der Name des Pins (z. B. GPIO26), sondern die Position verwendet wird. Alle geraden Pinnummern sind in der rechten Spalte des GPIOs und alle ungeraden links. Pin 40 ist der letzte Pin.
```goal()``` ist die Funktion, die als Thread endlos laufen soll. Ist die [Spielphase](#spielphase) "ingame", werden konstant die beiden GPIO-Pins geprüft, an denen die Datenpins der beiden Sensoren zur Torerkennung angeschlossen sind. Löst ein Sensor aus (Pin fällt auf LOW), wird die Funktion ```lvl3.react_goal()``` mit der Nummer des Spielers aufgerufen. Läuft kein Spiel, ist die Funktion im idle-Zustand (beobachte CPU-Vollast in einzelnen Kernen könnte evtl. hierdurch entstehen, nicht überprüft).

### Kurbelerkennung (LVL2_foul_detection.py)
Die Kurbelerkennung besteht aus der Sicht des Kickers nur aus zwei Arduinos, die bei einem Foul HIGH melden. Zwei Pins des GPIO des Raspberrys werden konstant bei "ingame" auf HIGH geprüft, was beduetet, dass der Arduino einer Spielerseite ein Kurbeln des Spielers detektiert hat.
Restliche Funktionalität ist durch Doku der [Torerkennung](#torerkennung-lvl2_goal_detectionpy) zu verstehen.

### Interface (LVL2_interface.py)
War angedacht zur TCP Kommunikation mit einem zweiten Rechner (AuVAReS auf NVIDIA Jetson). So wird der zweite Rechner über Spielevents informiert und kann selber auch Schlüsselwörter senden, um den Spielablauf zu beeinflussen.

**>>> Doku by M.O. goes here <<<** 🅾

### Spielkonfiguration (LVL2_pregame.py)
Bevor das Spiel startet, müssen bspw. Spielernamen eingetragen werden. Dieses Skript durchläuft die Vorbereitung des Spiels schrittweise und startet jedes Spiel. Mit der Website wird über game_data.json kommuniziert. Es waren leider keine Web-Developer im Team und daher ist diese fragwürdige Methode nicht ersetzt wurden und wurde so hingenommen. Ob die Lebensdauer der SD-Karte durch die vielen Zugriffe auf diese Datei sinkt, wurde nicht geprüft oder beachtet.
Die einzige Funktion ``pregame()`` läuft endlos als Thread. Sie ist lang aber linear gegliedert; die Schritte 1 bis 5 passieren in der Phase "wait_pregame" (Achtung: im Code ist eine andere Nummerierung, es geht hier nur um die Reihenfolge).

0. Nach dem Poweron wird der [Systemstatus](#spielphase) auf "wait_pre" gesetzt. Die "init"-Phase ließe sich hier zeitlich verlängern, falls noch mehr Vorbereitungen getroffen werden müssen. Dieses Umschalten passiert einmalig, da die Phase "init" nur automatisch nach dem Poweron besteht.
1. Spielernamen: Die JSON-Datei wird beobachtet und sobald Spielernamen auftauchen, werden diese in python übernommen.
2. Website Button zum Drohnen-Akku: Hier wird gewartet, bis "button_power" in der JSON auf True gesetzt wird. Das passiert durch Drücken des ersten Bestätigungs-Buttons auf der Website, auch wenn keine Drohne vorhanden ist. Für diese Abfrage gibt es keinen Timeout und es wird endlos auf True gewartet. Anschließend wird AuVAReS das Keyword "notify_drone_powered" zugesendet.
3. AuVAReS abwarten: Besteht eine Verbindung zum Jetson-Board, wird die Antwort von AuVAReS abgewartet. Wir warten hier, dass die Drohne sich mit dem Board verbunden hat, bevor Schritt 4 kommt.
4. Der zweite Button muss gedrückt werden und setzt "button_start" auf True. Eine Art rechtliche Absicherung, dass der Nutzer die Drohne freigibt, da unser System nicht prüfen kann, ob jemand durch den Start der Drohne gefährdet wäre.
5. AuVAReS wird darüber benachrichtigt und wir warten auf Antwort, dass die Drohne sich erfolgreich in Position begeben hat.
6. Spielstart: Der unix time stamp wird als GameID gespeichert. Damit sind die Spielereignisse in der Datenbank einem Spiel zuordenbar. In der JSON werden die Button-Werte zurückgesetzt, damit das nächste Spiel nicht automatisch das pregame durchläuft. In python werden Torzählervariablen auf null gesetzt und in die Datenbank wird eine neues Spiel mit Spielernamen und Toren (noch 0:0) geschrieben. Der Spielstatus wird auf "ingame" gesetzt. Jetzt startet das richtige Kickerspiel.

Über die Website kann das Spiel jederzeit abgebrochen werden. Da `pregame()` während der aktiven Spielphase eigentlich idle ist, kann die Überprüfung des Buttons hier übernommen werden. Es passieren ähnliche Schritte wie bei der normalen Beendigung eines Spiels, wie etwa auch das Löschen der Spielernamen aus der JSON. Hier taucht besonders häufig ein Fehler auf, bei dem "button_stop" nicht erfolgreich aus der JSON gelesen werden konnte, vermutlich aufgrund zeitgleicher Zugriffe durch die Website oder eines Fehlers im Code der Website, der den Wert aus der JSON löscht.

### Variablen und Routinen (LVL3_classes.py)
Der Name der Datei stammt aus den Anfängen, als viele Funktionen als Klassen zusammengefasst waren. Hier sind globale Variablen vorhanden, auf die mehrere LVL2-Programme zugreifen; sowie Übersicht über die Routinen und Reaktionen auf Events in Level 2. So soll innerhalb einer Datei die Gesamtheit an Reaktionen auf Spielereignisse erkenntlich sein. In Level 2 werden Ereignisse detektiert oder ausgelöst und die Reaktion darauf findet sich in Level 3. 🅾

##### init()

#### connection
##### _find_connection()
##### server_send()
##### set_connection_status()

#### Spielphase
##### set_status()

#### event reactions
##### react_goal()
##### react_foul()
##### react_drone_connected() & react_drone_wants_gamestart
##### react_drone_pleasewait & react_drone_pleaseresume

#### Database & Website
##### database_write()
##### json_read()
##### json_write()