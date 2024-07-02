# Struktur des Frontends (Weboberfläche)
![WebseitenVerlaufsplan](/docs/Gesamtsystem/WebseitenVerlauf.jpg)
## Beschreibung
### Pregame:
Zu Beginn wird auf der Startseite *index.php* aufgerufen. welche direkt auf die Startseite weiterleitet. <br>
Anschließend wird auf die Spielernamen gewartet. Dies können entweder als Freundschaftsspiel über ein Gerät oder mit Login auf zwei Geräten eingegeben werden. <br>
Danach wird bestätigt, ob die Drohne bereit zum Starten und anschließend ob die starten darf. <br>
Nach bestätigen startet das Spiel <br>

### Ingame:
Hier wird man auf eine Seite weitergeleitet welche die Spielernamen sowie den aktuellen Punktestand und die *Game-ID* anzeigt. Sollte einer der beiden Spieler 6 Tore oder beide 5 Tore erzielt haben, endet das Spiel. <br>
Dabei wird die *.json*-Datei stätig mit dem Aktuellen Punktestand aktualisiert.<br>

### Endgame:
Hier werden die Spielergebnisse nochmal angezeigt und die Möglichkeit gegeben, zur Startseite zurückzukehren.


