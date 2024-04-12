# Projektplan
[Der <font color='red'>**vorläufige**</font> Projektplan ist hier zu finden:](PRJ_AuVAReS_PRJ-PLAN_001.pdf)


# AuVAReS System Anforderungen 

<mark><font color='red'>**Hinweis**</font>: Vorläufige Aufschlüsselung der System-Anforderungen</mark>

**Stand: 11.04.2024**

**Status: vertraglich vorgegeben**


| ID  | Anforderungstext  | Verifikationsmethode| Priorität   | Typ | Status  |
|:----------|:----------|:----------|:----------|:----------|:----------|
| S1.1    | Das System muss die Funktion eines Videoschiedsrichters realisieren.    | Demonstration   | Hoch    | Funktional   | offen    |
| S1.2     | Das System muss ein Spielfeld aus der Luft überwachen können.    | Demonstration   | Hoch   | Funktional   | offen    |
| S1.3     | Das System muss über einen hohen Grad von Autonomie verfügen.   | Demonstration    | Hoch   | Funktional    | offen   |
| S1.4    |  Das System muss Spieldaten auswerten und in Echtzeit verteilen.    | Analyse    | Hoch    | Funktional    | offen    |
| S1.5     | Das System muss in einem Netzwerk kommunizieren können.    | Demonstration   | Hoch    | Funktional    | offen    |
| S1.6     | Das System muss selbstlernend sein.    | Analyse    | Mittel   | Nicht-Funktional    | offen   |
| S1.7     | Das System muss einen sicheren Betrieb für Zuschauer und Spieler gewährleisten.    | Analyse    | Hoch   | Nicht-Funktional   | offen   |
| S1.8     | Das System soll im Maßstab 1:10 realisiert werden.     | Inspektion   | Hoch    | Nicht-Funktional    | offen    |

## Aufschlüsselung System-Anforderungen

<mark><font color='red'>**Hinweis**</font>: Vorläufige Aufschlüsselung der System-Anforderungen</mark>

**S1.1: Funktionen Videoschiedsrichter**
- Kurbelerkennung
- Erkennung Spielfeld
- Erkennung Tor
- Erkennung Ball außerhalb des Spielfeldes
- Zwei Bälle innerhalb des Spielfeldes
- Unzulässiger Eingriff durch Spieler in das Spielgeschehen
\
\
**S1.2: Überwachung aus der Luft**
- VAR-Drohne fliegt über das Spielfeld
- Erfassung Spielgeschehen via Kamera
\
\
**S1.3: System muss über hohen Grad an Autonomie verfügen**
- Start- und Landevorgänge werden ohne Einfluss von außen durchgeführt
- Selbstständige Spielfelderfassung
- Flugoperationen werden selbstständig durchgeführt
- Bei Unterschreitung eines niedrigen Ladezustandes (tbd) kehrt die Drohne zu ihrer Landestation zurück
\
\
**S1.4: Auswertung und Bereitstellung von Spieldaten in Echtzeit**
- Im Falle eines Spielereignisses (vgl. S1.1) wird eine Wiederholung des Szene auf den Monitoren des Kickers ausgegeben
- Maximale Latenz (Echtzeit): tbd
- Dauer der Wiederholungen: tbd
- Replay-Funktion von Highlights (optional)
\
\
**S1.5: Netzwerkfunktionen**
- Kommunikation mit Kicker-Tisch
- Kommunikation mit KI-Server
- Kommunikation mit Steuer-Einheit der Drohne
\
\
**S1.6: Selbstlernfunktion**
- Spielfeld- und Spielballerkennung verbessert sich
- Anpassung Flugroute
\
\
**S1.7: Sicherer Betrieb**
- Abstand zu Menschen gewährleisten
- Eigenständige Landung bei geringem Ladezustand (vgl. S1.3)
- Vor einem Start der Drohne muss eine hindernisfreie Umgebung für den Start vom Benutzer quittiert werden
- tbd
\
\
**S1.8: Maßstab 1:10**
- Bezugsgröße muss definiert werden


