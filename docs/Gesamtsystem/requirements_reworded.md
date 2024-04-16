# Requirements für das Gesamtsystem
Es folgt eine Umformulierung der gegebenen Requirements, welche die Entwicklung des Gesamtsystems durch zwei Untergruppen (AuVAReS & Kicker) in eine gemeinsame Richtung lenken soll, ohne die Entwickler zu stark in der Problemlösung einzuschränken.
Für AuVAReS exisitiert unter docs/AuVAReS eine etwas detailiertere Aufschlüsselung mit Fokus auf dem Drohnensystem. Manchen Requirements kann das Gesamtsystem nur mit AuVAReS gerecht werden (vgl. S1.2), ohne dass der Kickertisch maßgeblich dazu beiträgt.

*Stand: 16.04.2024*


| ID  | Anforderungstext  | Redefinition für Entwicklung|
|:----------|:----------|:----------|
| S1.1    | Das System muss die Funktion eines Videoschiedsrichters realisieren.    | Die Drohne filmt das Spielgeschehen durchgehend und kann es auch zur Wiederholung auf ein Bildausgabegerät streamen.|
| S1.2     | Das System muss ein Spielfeld aus der Luft überwachen können.    |Die Drohne fliegt über dem Spielfeld und hat dabei entscheidende Elemente wie Ball und Tore im Blick, sodass das Spiel ausreichend verfolgt werden kann. |
| S1.3     | Das System muss über einen hohen Grad von Autonomie verfügen.   | Im Kicker ist die Spielsteuerung; sie greift auf mehrere Subroutinen zu und verwaltet so den Spielverlauf. Die Drohne muss nur platziert und geladen werden. Sie startet/fliegt/landet und kommuniziert selbstständig.|
| S1.4    |  Das System muss Spieldaten auswerten und in Echtzeit verteilen.|Es werden die Tore gezählt und in der Datenbank gesammelt. Das Spielgeschehen wird dadurch nicht verzögert/beeinträchtigt. Definition Echtzeit: TBD|
| S1.5     | Das System muss in einem Netzwerk kommunizieren können.|Für Zugriff auf die Datenbank wird ein WLAN bereitgestellt. Die Recheneinheiten des Systems sind für Informationsaustausch verbunden.|
| S1.6     | Das System muss selbstlernend sein.|TBD|
| S1.7     | Das System muss einen sicheren Betrieb für Zuschauer und Spieler gewährleisten.|Der Kicker stellt keine elektrische oder brandschutztechnische Gefährdung dar. Die Drohne fliegt nicht in Personen rein|
| S1.8     | Das System soll im Maßstab 1:10 realisiert werden.|TBD|
