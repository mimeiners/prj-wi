# Anmelde- und Registrierungsvorgänge der Webseite

Der Webserver des Raspberry Pi hostet eine Webseite auf welche die Spieler zugreifen um das Spiel zu starten, Punktestände und andere Informationen abzufragen, und um ggf. das Spielergebnis in die ewige Tabelle zu übergeben.

Dem Spiel vorgelagert gibt es die Möglichkeit zwischen einem Freundschaftsspiel und einem weiteren Spielmodus zu wählen, welcher Einfluss auf die ewige Tabellenplazierung hat. Um einer Tabellenmanipulation vorzubeugen ist für diesen Fall eine Nutzerkontoverwaltung notwendig. Im Folgenden werden die dazu verwendeten Dateien angeführt, welche sich im `html` Ordner auf dem Raspberry Pi zu befinden haben. Wir verwenden eine Datenbank mit zwei Tabellen, der Nutzertabelle `users` und der Tabelle aktiver Nutzer `active_users`, welche jene Nutzer enthält, die am aktuellen Spiel teilnehmen. Weiteres dazu findet sich im Abschnitt zur Nutzerkontoverwaltung.

## index.php

Die Startseite des Projekts, die den Nutzer zur Anmeldeseite weiterleitet, wenn ein entsprechender Button gedrückt wird.

```{literalinclude} ../../../files/Kicker/html/index.php
```

## login.php

Diese Datei dient der Nutzeranmeldung. Sie startet eine Session und prüft, ob der Nutzer bereits eingeloggt ist. Falls ja, wird er zur Startseite weitergeleitet. Andernfalls wird die Anmeldung durchgeführt, indem die eingegebenen Nutzerdaten gegen die in der Datenbank gespeicherten Daten geprüft werden. Erfolgt die Anmeldung erfolgreich, wird der Nutzer zur entsprechenden Seite weitergeleitet. [^q1]

```{literalinclude} ../../../files/Kicker/html/login.php
```

## register.php

Diese Datei stellt die Registrierungsseite für neue Nutzer bereit. Sie bindet die config.php ein, um eine Datenbankverbindung zu nutzen. Die Datei prüft die vom Nutzer eingegebenen Daten auf Korrektheit, wie zum Beispiel die Formatierung des Nutzernamens und die Übereinstimmung der eingegebenen Passwörter. Erfolgreich verifizierte Daten werden in die Datenbank eingetragen. Bei erfolgreicher Registrierung wird der Nutzer zur Anmeldeseite weitergeleitet. [^q1]

```{literalinclude} ../../../files/Kicker/html/register.php
```

## config.php

Diese Datei ist verantwortlich für den Aufbau der Datenbankverbindung. Sie enthält die notwendigen Parameter für den Datenbankzugriff wie den Servernamen, den Benutzernamen, das Passwort und den Datenbanknamen. Die Datei initialisiert die Verbindung zur Datenbank und prüft, ob die Verbindung erfolgreich hergestellt werden konnte. Bei einem Fehler wird eine Fehlermeldung ausgegeben. 

```{literalinclude} ../../../files/Kicker/html/config.php
```

## waiting.php

Diese Seite wird angezeigt, wenn der erste Spieler angemeldet ist und auf einen zweiten Spieler wartet. Sie prüft in regelmäßigen Abständen die Anzahl der aktiven Nutzer und leitet weiter, sobald ein zweiter Nutzer angemeldet ist.

```{literalinclude} ../../../files/Kicker/html/waiting.php
```

## check_second_user.php

Diese Datei überprüft die Anzahl der angemeldeten Nutzer in der Datenbank und gibt diese Zahl zurück. Diese Datei wird von der Warteseite waiting.php verwendet, um die Anzahl der angemeldeten Nutzer in regelmäßigen Abständen zu überprüfen.

```{literalinclude} ../../../files/Kicker/html/check_second_user.php
```

## redirect.php

Diese Datei leitet angemeldete Nutzer zum Spiel weiter. Sie prüft, ob der Nutzer eingeloggt ist und ermittelt die in der Datenbank gespeicherten aktiven Nutzer. Bei doppelter Anmeldung wird der Nutzer abgemeldet und auf die Startseite weitergeleitet. Die Datei erstellt zudem eine JSON-Datei mit den Nutzerdaten für den weiteren Spielverlauf.

```{literalinclude} ../../../files/Kicker/html/redirect.php
```

## normal_stop.php

Wenn das Spiel vorbei ist, dann werden die Spieler aus der entsprechenden Datenbanktabelle für aktive Nutzer entfernt.

```{literalinclude} ../../../files/Kicker/html/normal_stop.php
```

# Fußnoten

[^q1]: Vgl. [PHP MySQL Login System](https://www.tutorialrepublic.com/php-tutorial/php-mysql-login-system.php) und [PHP MySQL Improved Extension](https://www.php.net/manual/en/book.mysqli.php)