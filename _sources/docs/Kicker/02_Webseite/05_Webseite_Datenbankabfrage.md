# Voraussetzungen und Installation der InfluxDB PHP Library

_Datei:_ `html/get_game_status.php`

## Voraussetzungen

Bevor man den PHP-Code zur Abfrage von Spielstandsdaten aus einer InfluxDB-Datenbank verwenden können, muss man sicher stellen, dass die folgenden Voraussetzungen erfüllt sind:

- **PHP installiert**: PHP muss auf Ihrem Server oder lokalen Rechner installiert sein.
- **Composer installiert**: Composer ist ein Abhängigkeitsmanager für PHP, den Sie benötigen, um die InfluxDB PHP Library zu installieren.
- **InfluxDB installiert und konfiguriert**: InfluxDB muss auf Ihrem Server installiert und konfiguriert sein, um Daten speichern und abfragen zu können.
- **Zugangsdaten zur InfluxDB**: Sie benötigen die URL, das Token, die Organisation und den Bucket-Namen Ihrer InfluxDB-Instanz.

## Installation der InfluxDB PHP Library
Dazu benötigt man den Composer, um die InfluxDB PHP Library zu installieren:

```bash
composer require influxdata/influxdb-client-php
```

Dieser Befehl installiert die erforderliche InfluxDB-Client-Bibliothek und ihre Abhängigkeiten.

# Erklärung des PHP-Codes zur Abfrage von Spielstandsdaten aus InfluxDB

Dieser PHP-Code ermöglicht es, den Spielstand eines Spielers aus der InfluxDB-Datenbank abzurufen und zurückzugeben, als eingabe wird dafür der User und die Spiel-ID benötigt. Der Code nutzt die InfluxDB-Client-Bibliothek und ist in verschiedene Abschnitte unterteilt. Im Folgenden wird der Code Schritt für Schritt erklärt.

## Einbinden der notwendigen Bibliotheken

Zuerst wird der Autoloader der Composer-Abhängigkeiten eingebunden und die benötigte Klasse aus der InfluxDB-Client-Bibliothek verwendet:

```php
require 'vendor/autoload.php';

use InfluxDB2\Client;
```

Der `require`-Befehl lädt die von Composer verwalteten Abhängigkeiten, und `use` importiert die `Client`-Klasse, die für die Verbindung zu InfluxDB benötigt wird.

## Verbindungseinstellungen

Die Verbindungsparameter für die InfluxDB werden in Variablen gespeichert:

```php
$host = 'http://127.0.0.1:8086';
$token = '****';
$org = 'Hochschule Bremen';
$bucket = 'kicker';
```

Diese Variablen enthalten die URL des InfluxDB-Servers, das Authentifizierungstoken, die Organisation und den Bucket-Namen.

## Abrufen von Spielername und Spiel-ID

Der Spielername und die Spiel-ID werden aus den URL-Parametern abgerufen:

```php
$playerName = isset($_GET['player']) ? $_GET['player'] : '';
$gameID = isset($_GET['game_id']) ? $_GET['game_id'] : '';
```

`$_GET['player']` und `$_GET['game_id']` holen die entsprechenden Werte aus der URL. Falls diese nicht vorhanden sind, wird ein leerer String zurückgegeben.

## Initialisieren des InfluxDB-Clients

Der InfluxDB-Client wird mit den zuvor definierten Verbindungseinstellungen initialisiert:

```php
$client = new Client([
    "url" => $host,
    "token" => $token,
    "org" => $org,
    "bucket" => $bucket,
]);
```

Diese Konfiguration wird verwendet, um eine Verbindung zur InfluxDB herzustellen.

## Erstellen der Query API

Die Query API des Clients wird erstellt, um Abfragen an die InfluxDB zu senden:

```php
$queryApi = $client->createQueryApi();
```

## Definieren der Flux-Abfrage

Eine Flux-Abfrage wird definiert, um die Tore für den angegebenen Spieler und die Spiel-ID abzurufen:

```php
$query = 'from(bucket:"kicker")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "' . $gameID . '" and r._field == "Tore" and r.Spieler == "' . $playerName . '")
  |> last()';
```

- `from(bucket:"kicker")`: Wählt den Bucket `kicker` aus.
- `|> range(start: -1h)`: Beschränkt die Abfrage auf Daten der letzten Stunde.
- `|> filter(fn: (r) => r._measurement == "' . $gameID . '" and r._field == "Tore" and r.Spieler == "' . $playerName . '")`: Filtert die Daten nach der Spiel-ID, dem Feld "Tore" und dem Spielernamen.
- `|> last()`: Holt den letzten Eintrag.

## Ausführen der Abfrage

Die definierte Abfrage wird ausgeführt:

```php
$result = $queryApi->query($query);
```

## Verarbeiten des Ergebnisses

Die Anzahl der Tore wird initialisiert und das Ergebnis der Abfrage verarbeitet:

```php
$goals = 0;

foreach ($result as $table) {
    foreach ($table->records as $record) {
        $goals = $record->getValue();
    }
}
```

- `foreach ($result as $table)`: Iteriert über die Tabellen im Ergebnis.
- `foreach ($table->records as $record)`: Iteriert über die Datensätze in jeder Tabelle.
- `$record->getValue()`: Holt den Wert des Datensatzes (die Anzahl der Tore).

## Zurückgeben der Tore

Die Anzahl der Tore wird ausgegeben:

```php
echo htmlspecialchars($goals);
```

`htmlspecialchars($goals)` stellt sicher, dass die Ausgabe HTML-sicher ist, um potenzielle Sicherheitslücken zu vermeiden.

## Zusammenfassung

Der PHP-Code verbindet sich mit einer InfluxDB-Datenbank, führt eine Abfrage durch, um die Tore eines bestimmten Spielers aus der Datenbank abzurufen, und gibt die Anzahl der Tore zurück. Die Verbindungseinstellungen, die Abfrage und die Verarbeitung der Ergebnisse sind klar strukturiert, um die gewünschten Daten effizient zu erhalten.
