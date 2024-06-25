# Einrichtung des Raspberry PI
Damit der Raspberry Pi selbständig eine Webseite hosten kann, müssen einige Pakete installiert werden. Diese werden durch das Eingeben der untenstehenden Befehle über das interne Terminal installiert. 
## Einrichtung zum hosten der Weboberfläche 
### Pi vorbereiten:
Vor jeder Installation sollte der Pi auf den neusten Stand gebracht werden, solange es keinen Grund gibt dies nicht zu tun.
~~~
sudo apt-get update
~~~
~~~
sudo apt-get upgrate
~~~
### Apace2 und PHP installieren:
Apache2 ist ein Paket, welches dem Pi ermöglicht Webseiten zu hosten. 
~~~
sudo apt install apache2
~~~
Da Teile der Webseiten mit *php* geschrieben wurden, muss auch ein entsprechendes Paket zur Unterstützung installiert werden. Vorsichtshalber wird die Unterstützung für *MySQL* mit installiert.
~~~
sudo apt install php php-mysql php-mbstring
~~~
Damit die installieren Pakete in Kraft treten muss, Apache2 neugestartet werden.
~~~
sudo systemctl restart apache2
~~~

### Berechtigungen setzen und Testseite:
Standartmäßig führt Apache alle Dateien aus welche sich in **/var/www/html** befinden. Da dies jedoch Teil des root-Verzeichnis ist, müssen Berechtigungen gesetzt werden, damit drauf gearbeitet werden kann. <br>
~~~
sudo chown -R pi:www-data -R /var/www/html
~~~
~~~
chmod 750 -R /var/www/html
~~~
Hat der Benutzer ein andren Namen als *pi*, dann sollte *pi* durch den *Benutzernamen* ersetzt werden. <br>
Um zu testen ob die Pakete richtig installiert worden muss zuerst die IP-Adresse des Pi herausgefunden werden.
~~~
ifconfig -a
~~~
Je nachdem ob der Pi Teil eines bestehenden Netzwerkes ist oder selbst eines bildet, können zwei IP-Adressen angezeigt werden. <br>
Unter *wlan0* wird die Adresse der *W-LAN-Schnittstelle* angezeigt und unter *eth0* die der *Ethernet-Schnittstelle* <br>
<br>
**Wichtig:** sollte einer der Beiden Schnittstellen nicht genutzt werden, dann wird dessen IP-Adresse *nicht* angezeigt. <br>
<br>
Je nachdem welche Schnittstelle am Ende verwendet wird, ist es sinnvoll auch diese IP-Adresse zu nutzten. Alternativ lässt sich auch eine Statische IP setzten.<br>
<br>
Apache installiert eine Test-Seite namens *index.html*. Diese sollte sich im Browser mit: *http://10.42.0.1/index.html* aufrufen lassen. <br> 
Die IP-Adresse sollte hier durch die ersetzt werden, welche man vorher herausgefunden hat. <br>
Alternativ lässt sich die Test-Seite auch local auf dem Pi unter http://localhost/index.html öffnen. <br>
<br>
Sollte alles funktioniert haben, lassen sich nun alle Webseiten automatisch hosten, welche sich in dem Verzeichnis ( */var/www/html*) befinden.<br>
<br>
## Einrichtung einer Autostartroutine für den Main-Code
Zur automatischen Ausführung von Kode oder einem Programm beim Booten des Pi gibt es verschiedene Möglichkeiten. Hier haben wir uns für eine Methode über *rc.local* entschieden. <br>
Auf *rc.local* lässt sich über das Terminal zugreifen:
~~~
sudo nano /etc/rc.local
~~~
In dem Terminal-Fenster, ganz unten über *exit 0* lassen sich nun Zeilen einfügen, welche dann beim Boot ausgeführt werden. <br>
Für das automatische Ausführen eines Python-Scripts trägt man ein:
~~~
python3 /data_path/python_script.py &
~~~
Für das Ausführen eines beliebigen Python-Skript muss der *volle* Datei-Pfad angegen, Relative Pfade funktionieren nicht.<br>
<br>
**Wichtig:** Am Ende *jeder* Zeile **muss** ein "*&*" stehen, sonst bleib der Boot-Prozess an dieser Zeile hängen. Außerdem **muss** am *Ende* von *rc.local* immer "*exit 0*", sonst wird der Pi sich ebenfalls beim Boot-Prozess aufhängen.<br>
<br>
