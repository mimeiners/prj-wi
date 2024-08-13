# Dokumentation zu den 3D-Modellen

Folgend werden die im Projekt verwendeten 3D-Modelle beschrieben. Insgesammt gibt es 3 Verschiedene Komponenten. Diese sind die Displays, die Cases für die Kurbelerkennung und die Abdeckung für die Ballrückgabe.
Die Modelle mit FreeCAD sind für Anfänger einfacher zu erstellen. Um 3D-Modelle zu erstellen wurden diverse Youtube-Toutorials zu Hilfe gezogen und einfach ausprobiert was am besten Funktioniert.

# Verwendete Programme

Für die Erstellung des Display-Modells wurde das Programm Solid Edge 2024 verwendet. 
Für die Erstellung der Sensor-Cases und der Abdeckung für die Ballrückgabe wurde FreeCAD 0.21 verwendet.

# Design der Displays 

Die Displays waren das erste Modell das designed wurde und daher ist das selbe Programm wie bei dem Vorgänger-Projekt verwendet worden. 

Die Displays kann man in 9 einzelne Bauteile aufteilen. In Solid edge müssen größere Konstruckte zuerst in einzelnen part-Dateien designed werden, bevor man sie in ein Assembly Konstrukt zusammenfügt.
Hierfür wurde für die einzubauenden Displays maße genommen und dann die einzelnen Parts designed. Hierfür muss zuerst in der Part-Designoberfläche eine Skizze erstellt werden. Anschließend muss die 2D-Skizze über die Funktion Extrude aufgepuffert werden. Hier ist die Tiefe des Modells einzugeben. Danach wird das Modell mit den Loft oder Fillet funktionen entsprechend angepasst.
Die einzelnen Part Dateien werden dann in einer Baugruppe Zusammengebaut. 
Für den 3D-Druck muss eine STL-Datei exportiert werden. Hierfür einfach im Menü auf Exportieren gehen und dann den Datei-Typ auswählen.

# Design der Sensor-Cases 


Die Sensor-Cases wurden mit FreeCAD erstellt, da dieses Programm weniger komplex ist und man 2D-Skizzen einfacher erstellen kann.
Zuerst wurde eine 2D-Skizze in der Part-Design Workbench erstellt. Diese Skizze sollte dann relativ am anfang aufgepuffert werden, da Fehler beim Skizzieren ein Aufpuffern der Struktur verhinndern können und man dann erneut anfangen muss, sollte man den Fehler nicht finden. 
Die Einkerbungen der Kabel kann man mit einer neuen Skizze erstellen inden man eine Ebene auf das Vorherige Objekt legt und dann eine aushüllung macht.
Die Vor und Rück-Deckel wurden mit der Selben Methode seperat erstellt.

# Design der Torabdeckung

Auch hier ist mit FreeCAD gearbeitet worden. 
Zuerst ist eine 2D-Skitzze erstellt worden, die dann Aufgepuffert wurde. Anschließend wurde noch ein Bohrloch eingefügt.

