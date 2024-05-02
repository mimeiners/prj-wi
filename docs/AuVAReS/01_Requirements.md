# AuVAReS System Anforderungen 
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


**Angepasste Anforderung**

**Stand: 02.05.2024**

| ID  | Anforderungstext  | Verifikationsmethode| Priorität   | Typ | Status  | FAT/SAT |
|:----------|:----------|:----------|:----------|:----------|:----------|:----------|
| S1.1a    | Das System muss das Spielfeld erkennen.    | Demonstration   | Hoch    | Funktional   | offen    | FAT |
| S1.1b     | Das System muss den Ball erkennen.    | Demonstration   | Hoch   | Funktional   | offen    | FAT |
| S1.1c     | Wenn ein zweiter Ball im Spielfeld erkannt wird, soll dies gemeldet werden.   | Demonstration    | Mittel   | Funktional    | offen   | FAT |
| S1.1d    |  Wenn eine Hand im Spielfeld zu erkennen ist, soll das System dies melden.    | Demonstration    | Mittel    | Funktional    | offen    | FAT |
| S1.2a     | Das System muss das Spielgeschehen ergänzend zu dem Kicker aufnehmen.    | Demonstration   | Hoch    | Funktional    | offen    | FAT |
| S1.3a     | Das System muss sich selbstständig in eine geeignete Position manövrieren.    | Demonstration    | Hoch   | Funktional    | offen   | FAT   |
| S1.3b     | Das System kann bei einem niedrigen Akkustand selbständig zu einer Landeposition fliegen.    | Demonstration    | Mittel   | Funktional   | offen   | FAT   |
| S1.4a     | Das System muss eine Video-Wiederholung zur Verfügung stellen.     | Demonstration   | Hoch    | Funktional    | offen    | FAT    |
| S1.5a     | Das System muss eine Kommunikationsschnittstelle besitzen.   | Analyse    | Hoch    | Funktional    | offen    | FAT |
| S1.6a     | Das System wird sich basierend auf dem Spielstil bekannter Spieler selbst positionieren und seine Ausrichtung zu Spielgeschehen anpassen.     | Inspektion   | Niedrig    | Nicht-Funktional    | offen    | SAT |
| S1.7a     | Das System muss vor dem Starten von den Spielern freigegeben werden.     | Demonstration   | Hoch    | Funktional    | offen    | FAT  |
| S1.7b     | Das System muss ausreichend Abstand zu den Spielen wahren.     | Demonstration   | Hoch    | Nicht-Funktional    | offen    | FAT    |
| S1.7c     | Das System muss jederzeit eine manuell initierte Landung ermöglichen.     | Demonstration   | Hoch    | Funktional    | offen    | FAT |
| S1.8a     | Das System wird für einen größeren Maßstab angepasst.     | Inspektion   | Hoch    | Nicht-Funktional    | offen    | SAT |