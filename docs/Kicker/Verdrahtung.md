# Kickertisch Verdrahtungsplan

![Verdrahtungsplan](/docs/Gesamtsystem/Verdrahtungsplan.PNG)

## Beschreibung

Dieser Plan zeigt die Verdrahtung des Kickertisches. Er beinhaltet folgende Komponenten:


* **Spannungsversorgung:** 230V AC (Mehrfachstecker)

* **USB Powerhub:**  Versorgt die Peripheriegeräte mit Spannung

* **Beleuchtung & Lüfter:** Beleuchtung des Spielfelds und Kühlung des Raspberry Pi, bestizen eigene Netzteile.

* **Raspberry Pi 4:** Hauptrechner des Kickertisches

* **HDMI-Splitter:** Teilt das HDMI-Signal des Raspberry Pi auf zwei LCD-Bildschirme auf

* **LCD-Bildschirme:** Zeigen QR-Codes und den Spielstand

* **Arduino Nano:** Steuert die Kurbelerkennung der Spieler 1 und 2

* **Sensorik:** 

    * **Torerkennung:** 2 Einfache Infrarot-Sensoren, welche

    * **Kurbelerkennung:**  Überprüft die Bewegung der Spieler für mehr Informationen bitte unter [kurbel](kurbel.md) schauen.


**Legende:**


* **Spannung 230V AC:** Stromversorgung

* **Spannung 5V DC:** Stromversorgung der Peripheriegeräte

* **Daten Binär:** Eigentlich Digital aber um auszudrücken, dass die Sensoren entweder 0 V oder 5V ausgeben. Auslösekriterien der Sensoren entweder als Low oder High gecoded.

* **HDMI:**  Videodaten

  
## Weitere Informationen
Alle Versorgungs und Datenkabel die vom Raspberry Pi 4 ausgehen wurden selbst hergestellt. Für weitere Informationen bitte unter [Materialien](Materialien.md) die Bestelliste der Verkabelung Kurbelerkennung beachten. 


**Hinweis:** 

Dieser Plan ist vereinfacht und kann je nach verwendeter Hardware und Software angepasst werden.
