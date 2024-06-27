# Willkommen zur ewigen Liste!

Diese Schrift dokumentiert die softwareseitige Ausführung einer Erweiterung eines Tischkickers.

Das Ziel ist es, den Spielstand eines Spiels anzuzeigen und die Daten in einer Datenbank zu erfassen und
auszuwerten. Die Visualisierung des aktuellen Punktestandes erfolgt auf zwei Displays, welche auf dem
Tischkicker angebracht sind.

## Softwareseite

Im Folgenden wird die softwareseitige Erstellung aufgezeigt.

### Programmablauf

Das Programm auf dem Rasperry Pi startet, sobald dieser mit Netzspannung verbunden ist. Auf den beiden Displays steht zu
Beginn das HSB-Logo. Für ein schnelles Spiel, ohne die Ergebnisse in die Datenbank eintargen zu lassen, brauchen keine
weiteren Eingaben vorgenommen zu werden. Sobald eine Lichtschranke ein erstes Tor registriert, schaltet die Anzeige auf
den Displays um und zeigt nun den Spielstand an. Dabei stehen anonym Spieler eins und Spieler zwei als Spielernamen. Um
die Spielernamen einzugeben und auf den Displays auszugeben, kann über ein im Hochschulnetzwerk befindliches Gerät
verwendet werden. Zu diesem Zweck wird ein Tablett bereitgestellt. Von diesem aus kann auch die Einsicht in die
Spieltabellen geschehen. Der schematische Programmaufbau ist in der Abbildung 1 dargestellt.

```{figure} ../../images/Kicker/Ablauf.png
:align: center
:name: Abb. 1 

Ablaufplan des Programms
```

Die Lichtschranken sind an den Eingängen des Rasperry Pi angeschlossen. Erfolgt ein Tor, so wird das Signal, welches
durch die Lichtschranken ausgegeben wird, durch das Torerfassungsprogramm auf dem Pi ausgewertet. Die HTML Eingabe kann
mittels des dazugehörigen Tabletts erfolgen. Dabei können die Spielernamen und der Spieltag eingegeben werden. Dabei
erfolgt der Zugriff auf die Datenbank. Das Auswertungsprogramm wertet die Daten aus der Datenbank aus. Die Auswertung
kann über das Tablett abgerufen werden. In dem Auswertungsprogramm erfolgt die Berechnung der
Gewinnwahrscheinlichkeit. In einer Tabelle werden alle Spieler aufgelistet, die bisher mit dem Tischkicker gespielt
haben. In dem Displayausgabeprogramm wird die Ausgabe an die Displays vorbereitet. Über einen HDMI Splitter erfolgt die
Ausgabe an die Displays. 

### Vorgehen

Als erstet wurde untersucht, welche Komponenten für das Projekt benötigt werden. Bei der Recherche wurden die
Datenblätter und Produktbeschreibungen der Bauteile studiert, um den Anforderungen an das Projekt gerecht zu
werden. Nachdem die genauen Bauteile festgestanden haben, wurden diese bestellt.

o Display

Für die beiden Displays wurden anhand der Abmessungen dieser ein Gehäuse
und ein Stützmuster mit dem Programm Solid Edge von Siemens gezeichnet.
Nach der Fertigstellung der Zeichnung wurde diese genutzt, um die
Bauteile mit einem 3D-Drucker zu erstellen. Nach dem Druck mussten die
Gehäuse nachbearbeitet werden, da die Gehäuse nicht exakt nach den
vorgegebenen Maßen gedruckt wurde. Nach der Anpassung wurden die Stützen
auf dem Tischkicker mit sechs Schrauben befestigt. Im Vorfeld wurde
unter jeder Stütze jeweils eine 20er Bohrung vorgenommen, um die
benötigten Anschlüsse zwischen Display und Rasperry Pi zu gewährleisten.

o Lichtschranke

Die Lichtschranken wurden im Inneren der Tore platziert. Von außen sind
diese nicht sichtbar. Bei einem ersten Test stellte sich heraus , dass
wenn der Ball unter einem bestimmten Winkel in das Tor eintrifft, die
Lichtschranke den Ball nicht erkennt. Daraufhin wurde eine zweite
Lichtschranke parallel geschaltet, um das komplette Tor sicher
abzudecken, damit jedes Tor sicher gezählt wird. Als Befestigung diente
pro Lichtschranke jeweils eine Schrauben. Damit ist der Schutz durch
verdrehen infolge von Erschütterungen gewährleistet.

o Rasperry Pi

Auf dem Rasperry Pi wurde der Programmcode hinterlegt. Der Pi befindet
sich unterhalb des Tischkickers und wurde dort mit Schrauben befestigt.
Um mit dem Tablet auf das System zu zugreifen, wurde der Raspberry Pi
als Access-Point eingerichtet. Der Raspberry Pi 3 besitzt einen
integrierten WLAN-Chip, wird kein zusätzlicher Stick benötigt. Um dem PI
zum Access-Point zu konfigurieren wurden die Pakete „hostpad" und
„udhcpd" installiert und im Anschluss die zugehörigen Dateien angepasst.
Damit die installierten Dienste nach einem Neustart ausgeführt werden,
wurde die Autostartfunktion angepasst. Der W-Lan Schlüssel ist identisch
mit der SSID des Netzwerkes.

o Tablet

Um ein Direktes Zugreifen auf die HTML Seite an dem Tisch zu
gewährleisten wurde ein Tablet zur Verfügung gestellt. Dies ist an dem
Aufbau des Tisches befestigt und wird mit 5.5V Ladespannung versorg. Das
Tablet ist mit dem W-LAN Hotspot des Raspberry Pi verbunden und hat so
direkten Zugriff auf die HTML Seiten. Um die Webseite im Vollbild Modus
anzeigen lassen zu können, der „Boat Browser" auf dem Android System
installiert. Das Tablet ist mit keinem Passwort gesichert und ist nur
für die Bedienung des Datenbank Programms vorgesehen.

### Quellcode

Nachfolgend sind die für dieses Projekt verwendeten Quellcodes
aufgelistet. Diese sind Abschnittsweise im Code kommentiert.

* Abfragen der Lichtschranken

```{literalinclude} ../../files/Kicker/www/cgi-bin/Sensoren.py
```

* Anzeige des Spielstands auf den Anzeigetafeln

```{literalinclude} ../../files/Kicker/Anzeigetafel/main.py
```

* Index Datei der WEBGUI

```{literalinclude} ../../files/Kicker/www/index.html
```

* Funktion zum Hinzufügen und Löschen der Spiele

```{literalinclude} ../../files/Kicker/www/cgi-bin/function_add_game.py
```

* HTML Header der WEBGUI

```{literalinclude} ../../files/Kicker/www/cgi-bin/main_top.py
```

* HTML Main Seite

```{literalinclude} ../../files/Kicker/www/cgi-bin/main_home.py
```

* Einstellungen an der HTML-Seite vornehmen

```{literalinclude} ../../files/Kicker/www/cgi-bin/main_settings.py
```

* Funktionsblock

```{literalinclude} ../../files/Kicker/www/cgi-bin/function_settings.py
```

* Alle Spiele Anzeigen

```{literalinclude} ../../files/Kicker/www/cgi-bin/main_games.py
```

* Ewige Tabelle Anzeigen

```{literalinclude} ../../files/Kicker/www/cgi-bin/main_ever_table.py
```

* Spieler miteinander Vergleichen

```{literalinclude} ../../files/Kicker/www/cgi-bin/main_compare.py
```

* Funktionsblock

```{literalinclude} ../../files/Kicker/www/cgi-bin/function_compare.py
```

* Spieltag anzeigen und Spiel starten

```{literalinclude} ../../files/Kicker/www/cgi-bin/main_gameday.py
```
