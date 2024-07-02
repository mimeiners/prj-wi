# Pi-Einrichtung von InfluxDB und Grafana

## Einrichtung von InfluxDB

Wir haben uns bei diesen Projekt für InfluxDB entschieden, da dies als Empfehlung vorgegeben wurde und InfluxDB einige Vorteile bietet was das zeitliche Erfassen von Ereignissen betrifft.

### Installation von InfluxDB

**Installation von InfluxDB auf Linux**

Um InfluxDB auf Linux zu installieren, befolgen Sie diese Schritte:

1. **Paketverzeichnis aktualisieren:**
   ```bash
   sudo apt update
   ```

2. **InfluxDB installieren:**
   ```bash
   sudo apt install influxdb
   ```

3. **InfluxDB-Dienst starten:**
   ```bash
   sudo service influxdb start
   ```

4. **Status überprüfen:**
   ```bash
   sudo service influxdb status
   ```

5. **Webanwendung öffnen:**
   Besuchen Sie [http://localhost:8086](http://localhost:8086) in Ihrem Browser.

6. **Weitere Konfiguration:**
   Erstellen Sie eine Datenbank und beginnen Sie mit der Nutzung von InfluxDB für Ihre Projekte.

Das sind die Schritte für die Installation und Konfiguration von InfluxDB auf Linux.

### Struktur der Datenbank und Daten in InfluxDB

Um die Datenstruktur in der InfluxDB für das Kickerspiel zu verstehen, betrachten wir zunächst, wie die Daten bei jedem neuen Spiel organisiert werden. Hier sind die Hauptpunkte zur Struktur und den relevanten Details:

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

#### Beispielhafter Datenaufbau

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

#### Abfrage

Die PHP-Abfrage im Code nutzt Flux, die Abfragesprache von InfluxDB, um die Daten zu verarbeiten. Die Query filtert die Daten nach Measurement (Spiel-ID), Spielername und Feld (`Tore`), und gibt den letzten Eintrag innerhalb der letzten Stunde zurück. Die `last()` Funktion sorgt dafür, dass nur der letzte Wert (das zuletzt erzielte Tor) zurückgegeben wird.

#### Code-Beispiel zur Abfrage

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

## Einrichtung von Grafana auf dem Raspberry Pi

Im Folgenden installieren wir `grafana`. Nach der Installation erreichen wir die Oberfläche von `grafana` über `http://localhost:3000`. 
```bash
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
sudo apt update && sudo apt install -y grafana
sudo systemctl unmask grafana-server.service
sudo systemctl start grafana-server
sudo systemctl enable grafana-server.service
```
Um in grafana auf influxDB und zugreifen zu können legen wir in influxDB entsprechende Nutzer an.
Wir können influxDB mit dem Befehl `influx` aufrufen und die Datenbanken und Messungen im Terminal ausgeben.
```bash
influx

Connected to http://localhost:8086 version 1.6.7~rc0
InfluxDB shell version: 1.6.7~rc0
> create database db01
> use db01
Using database db01
> create user grafana with password '<password>' with all privileges
> grant all privileges on db01 to grafana
> exit 
```
Wir können so beispielsweise auch über `HTTP` Werte in die Datenbank schreiben (siehe docs für Syntax [^3]) 
```bash
curl -i -XPOST 'http://localhost:8086/write?db=db01' --data-binary '<measurement>[,<tag-key>=<tag-value>...] <field-key>=<field-value>[,<field2-key>=<field2-value>...] [unix-nano-timestamp]'
```

Wir können die Services mit dem `systemctl stop <grafana, influxdb>` beenden oder mit `systemctl restart <grafana, influxdb>` neu starten.
In der grafana Oberfläche können wir influxDB als Datenquelle hinzufügen indem wir unter Menüpunkt "Data sources" unsere Datenbank eintragen.
+ Database name: `influxdb-db01`
+ HTTP
    + URL: `http://localhost:8086`
+ InfluxDB Details
    + Database: `db01`
    + User: `grafana`
    + Password: `<password>`

Mit grafana können wir ein Dashboard erstellen, über welches das Gesamtsystem überwacht werden kann.  

# Fußnoten

[^3]: https://docs.influxdata.com/influxdb/v1/write_protocols/line_protocol_tutorial/
