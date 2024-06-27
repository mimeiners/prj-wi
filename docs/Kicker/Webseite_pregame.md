# Anmelde- und Registrierungsvorgänge der Webseite

Der Webserver des Raspberry Pi hostet eine Webseite auf welche die Spieler zugreifen um das Spiel zu starten, Punktestände und andere Informationen abzufragen, und um ggf. das Spielergebnis in die ewige Tabelle zu übergeben.

Dem Spiel vorgelagert gibt es die Möglichkeit zwischen einem Freundschaftsspiel und einem weiteren Spielmodus zu wählen, welcher Einfluss auf die ewige Tabellenplazierung hat. Um einer Tabellenmanipulation vorzubeugen ist für diesen Fall eine Nutzerkontoverwaltung notwendig. Im Folgenden werden die dazu verwendeten Dateien angeführt, welche sich im `html` Ordner auf dem Raspberry Pi befinden, und zum Verständnis ihrer Interrelation als Pseudocode skizziert. Die vollen Codes finden sich im Repository und sind durch weitere Kommentare ergänzt. Wir verwenden eine Datenbank mit zwei Tabellen, der Nutzertabelle `users` und der Tabelle aktiver Nutzer `active_users`, welche jene Nutzer enthält, die am aktuellen Spiel teilnehmen.

## index.php

Die Startseite des Projekts, die den Nutzer zur Anmeldeseite weiterleitet, wenn ein entsprechender Button gedrückt wird.
~~~
<?php
WENN Knopfdruck auf Login-Button
    LEITE um zu login.php
?>

<!DOCTYPE html> 
    RENDERE HTML-Seite mit Login-Button
</html>
~~~

## login.php

Diese Datei dient der Nutzeranmeldung. Sie startet eine Session und prüft, ob der Nutzer bereits eingeloggt ist. Falls ja, wird er zur Startseite weitergeleitet. Andernfalls wird die Anmeldung durchgeführt, indem die eingegebenen Nutzerdaten gegen die in der Datenbank gespeicherten Daten geprüft werden. Erfolgt die Anmeldung erfolgreich, wird der Nutzer zur entsprechenden Seite weitergeleitet. [^q1]

~~~ 
<?php
START Session

WENN Nutzer bereits angemeldet
    WENN zweiter Nutzer auch angemeldet
        LEITE um zu redirect.php

EINFÜGEN config.php

INITIALISIERE Variablen für Nutzername, Passwort, Fehlernachrichten

WENN HTML-Formular abgeschickt wurde
    PRÜFE Nutzernamen und Passwort auf formale Richtigkeit

    WENN Eingaben korrekt
        PRÜFE ob Nutzername existiert
        PRÜFE ob Passwort korrekt

        WENN Passwort korrekt
            PRÜFE Anzahl der angemeldeten Nutzer in active_users Tabelle
            WENN 0 Nutzer angemeldet
                LEITE um zu waiting.php
            WENN 1 Nutzer angemeldet
                LEITE um zu redirect.php
            WENN 2 Nutzer angemeldet
                FEHLERMELDUNG weil bereits zwei Nutzer spielen

SCHLIESSE Datenbankverbindung
?>

<!DOCTYPE html>    
    RENDERE HTML-Formular für die Anmeldung
    LEITE um zu register.php
</html>
~~~

## register.php

Diese Datei stellt die Registrierungsseite für neue Nutzer bereit. Sie bindet die config.php ein, um eine Datenbankverbindung zu nutzen. Die Datei prüft die vom Nutzer eingegebenen Daten auf Korrektheit, wie zum Beispiel die Formatierung des Nutzernamens und die Übereinstimmung der eingegebenen Passwörter. Erfolgreich verifizierte Daten werden in die Datenbank eingetragen. Bei erfolgreicher Registrierung wird der Nutzer zur Anmeldeseite weitergeleitet. [^q1]

~~~
<?php
EINFÜGEN config.php

INITIALISIERE Variablen für Nutzername, Passwort, Fehlernachrichten

WENN Formular abgeschickt wurde
    PRÜFE Nutzernamen auf unzulässige Zeichen
    PRÜFE ob Nutzername bereits existiert

    PRÜFE Passwort auf Mindestlänge
    PRÜFE ob Passwörter übereinstimmen

    WENN alle Eingaben korrekt
        SPEICHERE Nutzername und Passwort-Hash in users Tabelle
        LEITE um zu login.php

SCHLIESSE Datenbankverbindung
?>

<!DOCTYPE html> 
    RENDERE HTML-Formular für die Registrierung
</html>
~~~

## config.php

Diese Datei ist verantwortlich für den Aufbau der Datenbankverbindung. Sie enthält die notwendigen Parameter für den Datenbankzugriff wie den Servernamen, den Benutzernamen, das Passwort und den Datenbanknamen. Die Datei initialisiert die Verbindung zur Datenbank und prüft, ob die Verbindung erfolgreich hergestellt werden konnte. Bei einem Fehler wird eine Fehlermeldung ausgegeben.

~~~
<?php
DEFINIERE Datenbank-Parameter (Servername, Nutzername, Passwort, Datenbankname)
ERSTELLE Datenbankverbindung

WENN Verbindung fehlgeschlagen
    FEHLERMELDUNG
?>
~~~

## waiting.php

Diese Seite wird angezeigt, wenn der erste Spieler angemeldet ist und auf einen zweiten Spieler wartet. Sie prüft in regelmäßigen Abständen die Anzahl der aktiven Nutzer und leitet weiter, sobald ein zweiter Nutzer angemeldet ist.

~~~
<?php
START Session

WENN Nutzer angemeldet
    PRÜFE Anzahl der angemeldeten Nutzer
    WENN zweiter Nutzer angemeldet
        LEITE um zu redirect.php

WENN Nutzer nicht angemeldet
    LEITE um zu index.php

EINFÜGEN config.php
SCHLIESSE Datenbankverbindung
?>

<!DOCTYPE html> 
    RENDERE HTML-Seite
    SOLANGE zweiter Spieler nicht angemeldet
        ABFRAGEN von aktueller Nutzeranzahl in active_users Tabelle
</html>
~~~

## check_second_user.php

Diese Datei überprüft die Anzahl der angemeldeten Nutzer in der Datenbank und gibt diese Zahl zurück. Diese Datei wird von der Warteseite waiting.php verwendet, um die Anzahl der angemeldeten Nutzer in regelmäßigen Abständen zu überprüfen.

~~~
<?php
START Session

EINFÜGEN config.php

ABFRAGEN Anzahl der angemeldeten Nutzer aus der active_users Tabelle

SCHLIESSE Datenbankverbindung
?>
~~~

## redirect.php

Diese Datei leitet angemeldete Nutzer zum Spiel weiter. Sie prüft, ob der Nutzer eingeloggt ist und ermittelt die in der Datenbank gespeicherten aktiven Nutzer. Bei doppelter Anmeldung wird der Nutzer abgemeldet und auf die Startseite weitergeleitet. Die Datei erstellt zudem eine JSON-Datei mit den Nutzerdaten für den weiteren Spielverlauf.

~~~
<?php

START Session

WENN Nutzer nicht angemeldet
    LEITE um zu login.php

EINFÜGEN config.php

ABFRAGEN Anzahl der angemeldeten Nutzer aus der active_users Tabelle

WENN Doppelanmeldung entdeckt
    LÖSCHE alle aktiven Nutzer aus Active_users Tabelle
    BEENDE Session und LEITE um zu index.php

ERSTELLE JSON-Datei mit Spielernamen und Spielstatus

SCHLIESSE Datenbankverbindung
?>

<!DOCTYPE html> 
    RENDERE HTML-Seite für die Willkommensseite
</html>
~~~

## normal_stop.php

Wenn das Spiel vorbei ist, dann werden die Spieler aus der entsprechenden Datenbanktabelle für aktive Nutzer entfernt.

~~~
<?php

START Session

EINFÜGEN config.php

LÖSCHE alle aktiven Nutzer aus active_users Tabelle

SCHLIESSE Datenbankverbindung
?>

// Weiterer Quelltext

~~~
