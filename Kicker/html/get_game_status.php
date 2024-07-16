<?php
require 'vendor/autoload.php';

use InfluxDB2\Client;

// Verbindungseinstellungen
$host = 'http://127.0.0.1:8086';
$token = '****';
$org = 'Hochschule Bremen';
$bucket = 'kicker';

// Spielername und Spiel-ID aus der URL abrufen
$playerName = isset($_GET['player']) ? $_GET['player'] : '';
$gameID = isset($_GET['game_id']) ? $_GET['game_id'] : '';

// InfluxDB-Client initialisieren
$client = new Client([
    "url" => $host,
    "token" => $token,
    "org" => $org,
    "bucket" => $bucket,
]);

// Query API
$queryApi = $client->createQueryApi();

// Flux-Abfrage definieren, um den Spielstand für den angegebenen Spieler und die game_id abzurufen
$query = 'from(bucket:"kicker")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "' . $gameID . '" and r._field == "Tore" and r.Spieler == "' . $playerName . '")
  |> last()';

// Abfrage ausführen
$result = $queryApi->query($query);

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
