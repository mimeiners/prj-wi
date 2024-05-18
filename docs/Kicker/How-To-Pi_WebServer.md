# Das ist eine Kurzanleitung wie man ein Webserver auf dem Pi erstellt:
Die originalen Infos stammen aus: https://u-labs.de/portal/dynmaische-webseiten-apache2-webserver-mit-php-und-mysql-mariadb-auf-dem-raspberry-pi-installieren-einfachster-weg-fuer-anfaenger-lamp/. <br>
Da gibt es auch ein Video, falls jemand dem besser folgen kann.

### Pi vorbereiten:
Vor jeder Installation sollte der Pi auf den neusten Stand gebracht werden, solange es keinen Grund gibt dies nicht zu tun.
Das geht ganz einfach mit den beiden Befehlen:

~~~
sudo apt-get update
~~~
~~~
sudo apt-get upgrate
~~~

### Apace2 und PHP installieren:
Dies wird benötigt damit der Server gehostet wird und php-Dateien ausgeführt werden können. Unterstützung für MySQL installieren wir hier gleich mit.
Zuerst installieren wir Apache2:
~~~
sudo apt install apache2
~~~
Und anschließend PHP mit den zusätzlichen Paketen:
~~~
sudo apt install php php-mysql php-mbstring
~~~
Damit die installieren Pakete in Kraft treten muss Apache2 neugestartet werden:
~~~
sudo systemctl restart apache2
~~~

### Berechtigungen setzen und Testseite
Standartmäßig führt Apache alle Datein aus welche sich in **/var/www/html** befinden. Da dies jedoch Teil des root-Verzeichnis ist, müssen Berechtigungen gesetzt werden, damit drauf gearbeitet werden kann. <br>
Dies ändern wir mit:
~~~
sudo chown -R pi:www-data -R /var/www/html
~~~
~~~
chmod 750 -R /var/www/html
~~~
Hat der Benutzer ein andren Namen als *pi*, dann sollte *pi* durch den *Benutzernamen* ersetzt werden. <br>
Um zu testen ob die Pakete richtig installiert worden muss zuerst die IP-Adresse des Pi herausgefunden werden. Diese erhält man mit dem Befehl:
~~~
ifconfig -a
~~~
Apache installiert eine Test-Seite namens *index.html*. Diese sollte sich im Browser mit: http://10.42.0.1/index.html aufrufen lassen. <br> 
Die IP-Adresse sollte hier durch die ersetzt werden, welche man vorher herausgefunden hat. <br>
**Wichtig** ist, dass die Seite von einem anderem Gerät als der Pi selbst aufgerufen wird *(wir wollen schließlich testen, ob der Webserver funktioniert)* und dass das Gerät sich im selben Netzt befindet wie der Pi.<br>
<br>
Eine einfache Möglichkeit ist es mit dem Pi ein W-LAN Hotspot einzurichten und sich damit zu verbinden. *Die IP ändert sich damit auch, deshalb bitte nochmal prüfen, welche der Pi hat!*<br>
<br>
**Dieser Teil wird später aktualisiert:** *Am Ende soll der PI eine Statische IP haben.* <br>
<br>

### Die Website
Die Datei: *start_site.php* ist eine einfache Webseite, in der man die Spielernamen eintragen kann. Die eingetragenen Namen werden dann in *PlayerNames.txt* geschrieben und sollen später vom Python-Skript ausgelesen werden.<br>
Beide Dateien (*start_site.php* & *PlaverNames.txt*) sollen unter **/var/www/html** abgelegt werden. Selbes gillt auch für die retlichen Datein (*drone_check.php*, *back_home.php*, *DroneCheck.txt*) sowie dem Ordner *Pictues* in welchem sich das HSB-Logo befindet.<br>
<br>
Dazugekommen ist jetzt der Verweis auf eine Weitere Seite (*drone_check.php*) in welcher man bestätigen muss, ob es sicher ist für die Drohne zu starten. Anschließend wird man auf eine Weitere Seite verwiesen (*back_home.php*) in der die eingetragenen Namen stehen. Auf dieser seite wir dit dem **Return** Button die beiden *txt* geleehrt und man wird wieder auf die *start_site.php* verwiesen. 
<br>
Da auf *PlayerNames.txt* und *DroneCheck.txt* geschrieben werden soll, fehlen noch die Berechtigungen dafür. Dies geben wir mit:
~~~
sudo chmod 666 /var/www/html/PlayerNames.txt
~~~
und 
~~~
sudo chmod 666 /var/www/html/DroneCheck.txt
~~~
Damit sollte alles eingerichtet sein und jedes Skript sollte nun in der Lagen sein, die abgelegten Namen zu lesen und zu schreiben.<br>
<br>
Dazu gibt es noch ein Python-Skript names *website.py* in welchem sich alle dazu benötigten Funktionen befinden mit einem einfachen loop zum testen.

