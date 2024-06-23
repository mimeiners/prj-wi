# Abrufen von Daten aus InfluxDB mit PHP

Diese Anleitung erklärt, wie man mithilfe der InfluxDB PHP Library Daten aus einer InfluxDB-Datenbank abruft. Der Fokus liegt auf der Abfrage von Spielergebnissen aus einer Kicker-Datenbank.

## Voraussetzungen

- PHP installiert
- Composer installiert
- InfluxDB installiert und konfiguriert
- Zugangsdaten zur InfluxDB

## Installation der InfluxDB PHP Library

Verwenden Sie Composer, um die InfluxDB PHP Library zu installieren:

```bash
composer require influxdata/influxdb-client-php
```

## PHP Skript zum Abrufen von Daten

Das folgende PHP-Skript zeigt, wie man Daten aus InfluxDB abruft. Es verwendet die InfluxDB PHP Library, um eine Verbindung zur Datenbank herzustellen, eine Abfrage auszuführen und die Ergebnisse zu verarbeiten.

### Verbindungseinstellungen

Ersetzen Sie die Platzhalter in den Verbindungseinstellungen mit Ihren eigenen Zugangsdaten:

```php
<?php
require 'vendor/autoload.php';

use InfluxDB2\Client;

// Verbindungseinstellungen
$host = 'http://127.0.0.1:8086';
$token = 'YOUR_TOKEN_HERE';
$org = 'YOUR_ORG_HERE';
$bucket = 'kicker';
?>
```

### Abrufen von Spielernamen und Spiel-ID aus der URL

```php
<?php
// Spielername und Spiel-ID aus der URL abrufen
$playerName = isset($_GET['player']) ? $_GET['player'] : '';
$gameID = isset($_GET['game_id']) ? $_GET['game_id'] : '';
?>
```

### Initialisierung des InfluxDB-Clients

```php
<?php
// InfluxDB-Client initialisieren
$client = new Client([
    "url" => $host,
    "token" => $token,
    "org" => $org,
    "bucket" => $bucket,
]);

// Query API
$queryApi = $client->createQueryApi();
?>
```

### Definition und Ausführung der Flux-Abfrage

```php
<?php
// Flux-Abfrage definieren, um den Spielstand für den angegebenen Spieler und die game_id abzurufen
$query = 'from(bucket:"kicker")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "' . $gameID . '" and r._field == "Tore" and r.Spieler == "' . $playerName . '")
  |> last()';

// Abfrage ausführen
$result = $queryApi->query($query);
?>
```

### Verarbeitung und Ausgabe des Ergebnisses

```php
<?php
// Anzahl der Tore initialisieren
$goals = 0;

// Ergebnis verarbeiten und Anzahl der Tore speichern
foreach ($result as $table) {
    foreach ($table->records as $record) {
        $goals = $record->getValue();
    }
}

// Anzahl der Tore zurückgeben
echo htmlspecialchars($goals);
?>
```
