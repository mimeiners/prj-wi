# Bekannte Probleme mit dem Kicker
Aufgrund der begrenzten Zeit wurde der Kicker softwareseitig nicht lange genug getestet, weshalb es noch zu unerwarteten Fehlern kommen kann. Die meisten von denen lassen sich mit einem einfachen Neustart beheben. <br>
Um das Auftreten von Fehlern zu minimieren ist es daher notwendig **den Kicker erst dann abzuschalten wenn das aktuelle Spiel beendet wurde**, sei es durch einen Gewinner oder durch einen Spielabbruch.<br>
*Andernfalls können Fehler auftreten, die manuelles eingreifen auf den Raspberry PI erfordern.* <br><br>
Die bekannten Fehler sind dabei die Folgenden:
### Anzeigetafel aktualisiert nicht:
Auch wenn dieser Fehler mittlerweile weitestgehend behoben wurde, kann es dennoch vorkommen, dass die Anzeigetafel nicht aktualisiert und entweder nicht zur nächsten Seite wechselt oder die Punkte nicht anzeigt. 
Sollte das Auftreten muss das Spiel abgebrochen werden und der Kicker neugestartet werden.<br>
Wurde das Spiel nicht ordnungsgemäß beendet vor dem Neustart kann der Fehler bestehen bleiben, dann ist manuelles Eingreifen auf den PI notwendig und die QR.php bzw. Display_Site.php muss in einem neuen Browserfenster geöffnet werden.<br>

### Spiel startet nicht, keine Game-ID:
Es kann vorkommen das der Kicker nach längerer Zeit im Wartezustand kein Spiel startet. Der genaue Grund ist nicht bekannt, die Vermutung liegt aber nahe das es ein Überhitzungsproblem in Verbindung mit der Thread-Zuordnung (Thread Allocation) der CPU vom PI ist.<br>
Aufgefallen ist es bei der CPU-Auslastung, bei der im Wartezustand nur ein Kern statt alle vier belastet werden. Dieses Problem tritt üblicherweise erst nach ca. 30 Min bis 1 Stunde im Wartezustand auf.
Ein weg dies zu umgehen ist, während niemand spielt den Kicker entweder abzuschalten oder diesen in einem laufenden Spiel zu halten, denn während eines Spiels gibt es keine Probleme mit der Thread-Zuordnung und die Last wird auf alle vier Kerne verteilt.

### Kurbelerkennung funktioniert nicht:
Auch wenn dieses Problem keinen direkten Einfluss auf das Spielgeschehen hat, kann es dennoch stören. Der Grund für diesen Fehler ist uns nicht bekannt, da dieser uns recht spät aufgefallen ist. Hier hilft ein ordnungsgemäßer Neustart des Kickers.
