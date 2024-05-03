


# Dokumentation und Ideensammlung zum Training der KI-Objekterkennung

**Stand: 05.05.2024**

**LINK zum Projekt in Roboflow** [AuVAReS Training Red-Ball](https://app.roboflow.com/auvares-redball)


## Übersicht
Das Training wird derzeit in Roboflow erstellt und im Anschluss ein Datensatz erstellt. Dafür sind derzeit ca. 550 Bilder zu bearbeiten und Bounding-Boxes zu setzen.

- Teilnehmer zum Bearbeiten: 1 von 3. Beitritt via E-Mail nur auf Anfrage möglich.
- Anzahl Training für Red-Ball: unbekannt, derzeit 1
- Training für Landezone nicht gestartet!

#### Zusätzliche Erkennungen (Ideensammlung)
- Landezone (Hohe Priorität)
- Spielfelderkennung (Hohe Priorität) <br> Ein Logo dazu liegt im Gitlab
- Marker als Richtunganzeiger für Landezone auf Kicker (Mittlere Priorität). <br> Derzeit Klärung ob damit eine Richtungsweisung für die Drohne erstellt werden kann. Erleichtert das wiederfinden des Start- und Landeplatzes.
- Stangenerkennung (Geringe Priorität). Erkennung der Zonen im Spielfeld
- Hand im Spielgeschehen (Geringe Priorität)

Die quantitative Umsetzung dieser Punkte ist abhängig und beschränkt durch die zeitlich beschränkten Ressourcen bis zum FAT bzw. SAT. 

Weiter ist das genaue YOLO Modell zu klären, um eine nahezu Echtzeiterkennung zu gewährleisten mit hoher Zuverlässigkeit.



### Weitere Datensätze die von Dritten zur Verfügung stehen
- [Red-Ball-Finder (Roboflow)](https://universe.roboflow.com/work-nzct5/red-ball-finder) 