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

<del>**Stand: 02.05.2024**</del>

**Stand: 03.05.2024**

| ID  | Anforderungstext  | Verifikationsmethode| Priorität   | Typ | Status  | 
<span style="color:red"> Nachweis |
|:----------|:----------|:----------|:----------|:----------|:----------|:----------|
| S1.1a    | <del>Das System muss das Spielfeld erkennen.</del> Das System muss ein Fußball-Spielfeld erkennen.    | Demonstration   | Hoch    | Funktional   | offen    | FAT |
| S1.1b     | <del>Das System muss den Ball erkennen.</del> Das Sytem muss einen Ball der Größe 32 mm bis 36 mm Durchmesser erkennen.   | Demonstration   | Hoch   | Funktional   | offen    | FAT |
| S1.1c     | Wenn ein zweiter Ball im Spielfeld erkannt wird, soll dies gemeldet werden.   | Demonstration    | Mittel   | Funktional    | offen   | FAT |
| S1.1d    |  <del> Wenn eine Hand im Spielfeld zu erkennen ist, soll das System dies melden.</del> Das System soll eine vorhandene Hand im Spielfeld melden.    | Demonstration    | Mittel    | Funktional    | offen    | FAT |
| S1.2a     | Das System muss das Spielgeschehen ergänzend zu dem **System "** Kicker **"** aufnehmen.    | Demonstration   | Hoch    | Funktional    | offen    | FAT |
| S1.3a     | <del>Das System muss sich selbstständig in eine geeignete Position manövrieren.</del> Das System muss die Kamera zur Spielfeld-Überwachung selbständig in eine geeeignete Position manövrieren.    | Demonstration    | Hoch   | Funktional    | offen   | FAT   |
| S1.3b     | Das System <del>kann</del> **muss** bei einem niedrigen Akkustand selbständig zu einer Landeposition fliegen.    | Demonstration    | <del>Mittel</del> **Niedrig**   | Funktional   | offen   | FAT   |
| S1.4a     | Das System muss eine Video-Wiederholung zur Verfügung stellen.     | Demonstration   | Hoch    | Funktional    | offen    | FAT    |
| S1.5a     | Das System muss eine Kommunikationsschnittstelle <del>besitzen</del> **bereitstellen**.    | <del>Analyse</del> **Inspektion**    | Hoch    | Funktional    | offen    | FAT |
| S1.6a     | <del>Das System wird sich basierend auf dem Spielstil bekannter Spieler selbst positionieren und seine Ausrichtung zu Spielgeschehen anpassen.</del> Das System wird die Postion und Ausrichtung der Kamera zur Spielfeld-Überwachung, basierend auf bekannten Spielern, optimieren.     | <del>Inspektion</del> **Analyse**   | Niedrig    | <del>Nicht-</del> Funktional    | offen    | SAT |
| S1.7a     | Das System muss vor dem Starten von <del>den</del> **einem** Spieler<del>n</del> freigegeben werden.     | Demonstration   | Hoch    | Funktional    | offen    | FAT  |
| S1.7b     | Das System muss <del>ausreichend Abstand</del> **einen Sicherheitsabstand** zu <del>den</del> **allen** Spielen wahren.     | <del>Demonstration</del>  **Analyse**  | Hoch    | <del>Nicht-</del>Funktional    | offen    | FAT    |
| S1.7c     | Das System muss jederzeit eine manuell initierte Landung ermöglichen.     | <del>Demonstration</del>  **Analyse**   | Hoch    | Funktional    | offen    | FAT |
| S1.8a     | Das System <del>wird</del> **muss** für einen <del>größeren</del> **anderen** Maßstab <del>angepasst</del> **anpassbar sein**.     | <del>Inspektion</del> **Analyse**   | Hoch    | Nicht-Funktional    | offen    | SAT |