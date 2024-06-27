# Datenbank InxluxDB

## Zielsetzung:

Wir haben uns bei diesen Projekt für InfluxDB entschieden, da dies als Empfehlung vorgegeben wurde und InfluxDB einige Vorteile bietet was das zeitliche Erfassen von Ereignissen betrifft.

## Struktur der Datenbank

Um die Datenstruktur in der InfluxDB für das Kickerspiel zu verstehen, betrachten wir zunächst, wie die Daten bei jedem neuen Spiel organisiert werden. Hier sind die Hauptpunkte zur Struktur und den relevanten Details:

### Struktur der Daten in InfluxDB

1. **Measurement pro Spiel:**
   - Für jedes neue Spiel wird ein neues Measurement in der InfluxDB angelegt. Der Name dieses Measurements entspricht der Spiel-ID. Dies ermöglicht eine klare Trennung der Daten für jedes Spiel und erleichtert das Abrufen und Verarbeiten der Daten für ein bestimmtes Spiel.

2. **Datenpunkte (Points):**
   - Jeder Datenpunkt (Point) in einem Measurement repräsentiert ein Tor, das ein Spieler zu einem bestimmten Zeitpunkt erzielt hat.

3. **Tags und Felder:**
   - **Tags:**
     - `Spieler`: Der Name des Spielers, der das Tor erzielt hat.
   - **Felder:**
     - `Tore`: Die Anzahl der Tore, die der Spieler erzielt hat (in diesem Fall immer 1, da jeder Punkt ein einzelnes Tor darstellt).
   - **Timestamp:** Der Zeitstempel, wann das Tor erzielt wurde.

### Beispielhafter Datenaufbau

Angenommen, wir haben ein Spiel mit der Spiel-ID `game_123`. Während des Spiels erzielen die Spieler `PlayerA` und `PlayerB` mehrere Tore. Die Daten könnten dann wie folgt in InfluxDB gespeichert sein:

#### Measurement: `game_123`

| _time                  | Spieler | Tore |
|------------------------|---------|------|
| 2024-06-25T10:00:00Z   | PlayerA | 1    |
| 2024-06-25T10:02:00Z   | PlayerB | 2    |
| 2024-06-25T10:05:00Z   | PlayerA | 2    |
| 2024-06-25T10:07:00Z   | PlayerB | 3    |

- **_time**: Zeitstempel des Events
- **Spieler**: Name des Spielers
- **Tore**: Anzahl der Tore (immer 1 in diesem Fall)

### Abfrage

Die PHP-Abfrage im Code nutzt Flux, die Abfragesprache von InfluxDB, um die Daten zu verarbeiten. Die Query filtert die Daten nach Measurement (Spiel-ID), Spielername und Feld (`Tore`), und gibt den letzten Eintrag innerhalb der letzten Stunde zurück. Die `last()` Funktion sorgt dafür, dass nur der letzte Wert (das zuletzt erzielte Tor) zurückgegeben wird.

### Code-Beispiel zur Abfrage

Hier ist der relevante Teil der PHP-Abfrage aus deinem Code:

```php
$query = 'from(bucket:"kicker")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "' . $gameID . '" and r._field == "Tore" and r.Spieler == "' . $playerName . '")
  |> last()';
```

- **from(bucket:"kicker")**: Wählt den Bucket `kicker`.
- **range(start: -1h)**: Betrachtet die Daten der letzten Stunde.
- **filter(fn: (r) => r._measurement == "' . $gameID . '" and r._field == "Tore" and r.Spieler == "' . $playerName . '")**: Filtert nach dem Measurement (Spiel-ID), dem Feld (`Tore`) und dem Spielername.
- **last()**: Gibt den letzten Eintrag zurück.

### Zusammenfassung

Die Daten in InfluxDB sind so organisiert, dass jedes Spiel ein eigenes Measurement hat. Innerhalb jedes Measurements werden die Tore mit einem Zeitstempel und dem Namen des Spielers gespeichert. Dieser Aufbau erleichtert die Abfrage spezifischer Informationen für jedes Spiel und jeden Spieler, wie in deinem PHP-Code dargestellt.
