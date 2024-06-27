# Einrichtung der Softwareumgebung für Nutzerkontoverwaltung

Da ein zentrales Alleinstellungsmerkmal des Kickers die Verwaltung einer ELO-Rangliste aller Spieler sein soll, die sogenannte ewige Tabelle, haben wir uns für die funktionale Erweiterung der Software um eine Nutzerverwaltung entschieden. Durch den passwortgeschützten Anmeldeprozess für registrierte Benutzerkonten soll sichergestellt werden, dass die Leistung der Spielteilnehmer ordnungsgemäß verbucht werden und so die Möglichkeiten einer Tabellenmanipulation minimieren. Diese Anmeldefunktion lässt sich in den bestehenden Spielablauf einbinden, indem die Anmeldung der restlichen Spielinitialisierung vorgeschaltet wird, und die durch Nutzerkontoverifizierung via Datenbankabgleich bestätigten Nutzernamen an die Folgeprozesse übergeben werden. Der Raspberry Pi 4, auf dem der Webserver läuft, wird daher durch einige Softwarepakete erweitert.

Auf dem Raspberry Pi 4 ist bereits ein Apache-Webserver eingerichtet um den Spielablauf zu steuern. Speziell für die Nutzerkontoverwaltung, wird zusätzlich ein MariaDB Datenbankserver installiert, welcher mit dem PHP-MYSQL Modul die Interaktion zwischen PHP-Skripten und der Datenbank ermöglicht. Es sei an dieser Stelle darauf hingewiesen, dass die Verwendung von MySQL grundsätzlich durch das resourcensparendere SQLite3 ersetzt hätte werden können, in Anbetracht der Systemauslastung des Raspberry Pi 4 dies jedoch bei weitem keine Notwendigkeit darstellt.   

Mit `sudo apt update` und `sudo apt upgrade` aktualisieren wir die Paketlisten und aktualisieren die installierten Pakete auf dem Raspberry Pi auf die neuesten Versionen. Wir können mit `sudo apt install apache2 -y` die Installation des Apache-Webservers sicherstellen und diesen mit `sudo apt install libapache2-mod-php` um das PHP-Modul erweitern.
Der Nutzer des Raspberry pi 4 Systems sollte Besitzrechte für das `var/www/html` Verzeichnis haben, in welchem sich die Dateien befinden auf welche die Tischkickernutzer und die Softwarekomponenten später zur Anmeldung zugreifen müssen. Dazu wechseln wir in das Verzeichnis und erteilen die Befugnisse mit `cd /var/www` und `sudo chown kicker: /var/www/html`;   `kicker` ist im letzteren Befehl der Nutzername des Pi Nutzers.


Danach wird der MariaDB-Datenbankserver und das PHP MySQL-Modul mit `sudo apt install mariadb-server php-mysql -y` installiert, um die Interaktion zwischen PHP-Skripten und der Datenbank zu ermöglichen. In der MySQL-Befehlszeilenschnittstelle, aufgerufen über `sudo mysql`, wird ein neuer Benutzer namens `admin` mit einem Passwort erstellt und diesem Benutzer wurden alle Rechte für alle Datenbanken erteilt. Diese Datenbanknutzerdaten werden in die PHP-Skripte eingetragen um bei jedem Aufruf einen Datenbankzugriff durchzuführen.

~~~ sql
CREATE USER 'admin'@'localhost' IDENTIFIED BY '<password>';
GRANT ALL PRIVILEGES ON *.* to 'admin'@'localhost' WITH GRANT OPTION;
exit
~~~

Von hieran erfolgt die Anmeldung zur Datenbank via bash mit `sudo mysql -u admin -p`.

Anschließend wird phpMyAdmin mit `sudo apt install phpmyadmin` installiert, eine webbasierte Oberfläche zur Verwaltung von MySQL-Datenbanken da diese Zugriffsform auf die Datenbank zum Debuggen einfacher ist. Beim Installationsprozess gibt es eine Abfrage bezüglich der Verwendung von `dbcommon-config`; diese ist zu bejahen. Auch für phpmyadmin sollte im Zuge der Installation ein Passwort festgelegt werden. Wenn keine Fehlfunktionen im Zusammenhang mit dem Datenbankzugriff zu erwarten sind, kann auf die Installation auch in Gänze verzichtet werden. 


Das Root-Benutzerpasswort von MySQL wird geändert, damit der Datenbankzugriff über den Root-Nutzer nicht passwortlos möglich ist. Dazu dienen die Befehle `sudo mysql -u root` und `ALTER USER 'root'@'localhost' IDENTIFIED BY '<password>';`. Dann kann mit `sudo service mysql start` der MySQL Dienst gestartet werden. In der Apache-Konfigurationsdatei (`sudo nano /etc/apache2/apache2.conf`) wurde die Konfiguration für phpMyAdmin eingeschlossen (`Include /etc/phpmyadmin/apache.conf`), damit die Web-Oberfläche zugänglich ist. Abschließend wurde der Apache-Webserver mit `sudo /etc/init.d/apache2 restart` neu gestartet, um die Konfigurationsänderungen anzuwenden.

Es folgt zur Übersicht ein Wiederholung aller Befehle in einem Codeblock.

~~~ bash
sudo apt update
sudo apt upgrade
sudo apt install apache2 -y
sudo apt install libapache2-mod-php
cd /var/www
sudo chown pi: /var/www/html
sudo apt install mariadb-server php-mysql -y
sudo mysql
CREATE USER 'admin'@'localhost' IDENTIFIED BY '<password>';
GRANT ALL PRIVILEGES ON *.* to 'admin'@'localhost' WITH GRANT OPTION;
exit
sudo apt install phpmyadmin
sudo mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED BY '<password>';
exit
sudo service mysql start
sudo nano /etc/apache2/apache2.conf
Include /etc/phpmyadmin/apache.conf
sudo /etc/init.d/apache2 restart
sudo reboot
~~~

## Einrichtung der Nutzerdatenbank

In diesem Projekt wird für die Nutzerkontoverwaltung eine Datenbank mit zwei Tabellen verwendet. In der MySQL-Befehlszeilenschnittstelle erstellen wir mit `create database usersdb;` eine Datenbank mit dem Namen `usersdb` und wählen diese mit `use usersdb;` zur Bearbeitung aus. Die Tabelle `users` beinhaltet alle Nutzerkonten, bestehend aus einem Nutzernamen und einem Passwort. Die Tabelle `active_users` soll dazu dienen jene Nutzernamen zu beinhalten, die an einem laufenden Spiel beteiligt sind. Ist ein Spiel vorbei, oder wird es abgebrochen, werden alle Einträge in dieser Tabelle gelöscht, wodurch sichergestellt werden kann, dass zu jedem Zeitpunkt nur jene zwei Spieler Punkte für ihre Ranglistenplatzierung machen können, welche auch tatsächlich erfolgreich für das Spiel angemeldet sind. Mit `last_activity` ist es möglich zu sehen, zu welchem Zeitpunkt sich ein Nutzer angemeldet hat.   

~~~ sql
CREATE TABLE users (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(200) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE active_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(200) NOT NULL,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
~~~
