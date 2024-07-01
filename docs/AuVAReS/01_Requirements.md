# AuVAReS System Anforderungen 
**Stand: 11.04.2024**

**Status: vertraglich vorgegeben**

| ID  | Anforderungstext  | Verifikationsmethode| Priorität   | Typ | Status  |
|:----------|:----------|:----------|:----------|:----------|:----------|
| S1.1    | Das System muss die Funktion eines  Videoschiedsrichters realisieren.    | Demonstration   | Hoch    | Funktional   | offen    |
| S1.2     | Das System muss ein Spielfeld aus der Luft überwachen können.    | Demonstration   | Hoch   | Funktional   | offen    |
| S1.3     | Das System muss über einen hohen Grad von Autonomie verfügen.   | Demonstration    | Hoch   | Funktional    | offen   |
| S1.4    |  Das System muss Spieldaten auswerten und in Echtzeit verteilen.    | Analyse    | Hoch    | Funktional    | offen    |
| S1.5     | Das System muss in einem Netzwerk kommunizieren können.    | Demonstration   | Hoch    | Funktional    | offen    |
| S1.6     | Das System muss selbstlernend sein.    | Analyse    | Mittel   | Nicht-Funktional    | offen   |
| S1.7     | Das System muss einen sicheren Betrieb für Zuschauer und Spieler gewährleisten.    | Analyse    | Hoch   | Nicht-Funktional   | offen   |
| S1.8     | Das System soll im Maßstab 1:10 realisiert werden.     | Inspektion   | Hoch    | Nicht-Funktional    | offen    |


**Angepasste Anforderung**

**Stand: 01.07.2024**
**Status: mutually agreed**

| ID  | Anforderungstext  | Verifikationsmethode| Priorität   | Typ | Status  | Nachweis |
|:----------|:----------|:----------|:----------|:----------|:----------|:----------|
| S1.1a    | Das System muss ein Fußball-Spielfeld erkennen.    | Demonstration   | Hoch    | Funktional   | beendet   | FAT |
| S1.1b     | Das Sytem muss einen Ball der Größe 32 mm bis 36 mm Durchmesser erkennen.   | Demonstration   | Hoch   | Funktional   | beendet   | FAT |
| S1.1c     | Wenn ein zweiter Ball im Spielfeld erkannt wird, soll dies gemeldet werden.   | Demonstration    | Mittel   | Funktional    | offen   | FAT |
| S1.1d    |  Das System soll eine vorhandene Hand im Spielfeld melden.    | Demonstration    | Mittel    | Funktional    | offen    | FAT |
| S1.2a     | Das System muss das Spielgeschehen ergänzend zu dem System Kicker aufnehmen.    | Demonstration   | Hoch    | Funktional    | beendet    | FAT |
| S1.3a     |  Das System muss die Kamera zur Spielfeld-Überwachung selbständig in eine geeeignete Position manövrieren.    | Demonstration    | Hoch   | Funktional    | beendet  | FAT   |
| S1.3b     | Das System  muss bei einem niedrigen Akkustand selbständig zu einer Landeposition fliegen.    | Demonstration    | Niedrig   | Funktional   | beendet   | FAT   |
| S1.4a     | Das System muss eine Video-Wiederholung zur Verfügung stellen.     | Demonstration   | Hoch    | Funktional    | beendet    | FAT    |
| S1.5a     | Das System muss eine Kommunikationsschnittstelle  bereitstellen.    |  Inspektion   | Hoch    | Funktional    | beendet    | FAT |
| S1.6a     | Das System wird die Postion und Ausrichtung der Kamera zur Spielfeld-Überwachung, basierend auf bekannten Spielern, optimieren.     |  Analyse   | Niedrig    |  Funktional    | offen    | SAT |
| S1.7a     | Das System muss vor dem Starten von beiden Spielparteien freigegeben werden.     | Demonstration   | Hoch    | Funktional    | beendet    | FAT  |
| S1.7b     | Das System muss einen Sicherheitsabstand zu allen Spielen wahren.     | Analyse  | Hoch    | Funktional    | beendet   | FAT    |
| S1.7c     | Das System muss jederzeit eine manuell initierte Landung ermöglichen.     |   Analyse   | Hoch    | Funktional    | beendet   | FAT |
| S1.8a     | Das System muss für einen anderen Maßstab anpassbar sein.     | Analyse   | Hoch    | Nicht-Funktional    | beendet    | SAT |