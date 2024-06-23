# Lesen und Ausgeben von JSON-Daten mit PHP

Diese Anleitung zeigt, wie man JSON-Daten aus einer Datei liest und die Daten in einem bestimmten Format ausgibt.

## Voraussetzungen

- PHP installiert
- Eine JSON-Datei (`game_data.json`) mit den relevanten Spieldaten

## PHP Skript zum Lesen und Ausgeben von JSON-Daten

Das folgende PHP-Skript liest die JSON-Daten aus einer Datei und gibt sie als JSON-Antwort zurück.

### Pfad zur JSON-Datei

Definieren Sie den Pfad zur JSON-Datei:

```php
<?php
// Pfad zur JSON-Datei
$jsonFilePath = 'game_data.json';
?>
```

### Lesen und Überprüfen der JSON-Daten

Lesen Sie die Daten aus der JSON-Datei und überprüfen Sie, ob sie korrekt dekodiert wurden:

```php
<?php
// Überprüfe, ob die JSON-Datei existiert und lese die Daten
if (file_exists($jsonFilePath)) {
    $jsonData = file_get_contents($jsonFilePath);
    $data = json_decode($jsonData, true);
?>
```

### Extrahieren und Ausgeben der Daten

Extrahieren Sie die relevanten Daten und geben Sie sie im JSON-Format aus:

```php
<?php
    // Überprüfe, ob die JSON-Daten korrekt dekodiert wurden
    if ($data !== null) {
        $player1 = $data['player_1']['name'] ?? '';
        $player2 = $data['player_2']['name'] ?? '';
        $gameId = $data['game_id'] ?? '';
        $lastCompletedGame = $data['last_completed_game'] ?? '';

        echo json_encode([
            'player_1' => $player1,
            'player_2' => $player2,
            'game_id' => $gameId,
            'last_completed_game' => $lastCompletedGame
        ]);
    } else {
        echo json_encode([
            'player_1' => '',
            'player_2' => '',
            'game_id' => '',
            'last_completed_game' => ''
        ]);
    }
} else {
    echo json_encode([
        'player_1' => '',
        'player_2' => '',
        'game_id' => '',
        'last_completed_game' => ''
    ]);
}
?>
```

### Nutzung des Skripts

Speichern Sie das Skript als `get_game_data.php` und rufen Sie es im Browser oder über eine API-Anfrage auf. Das Skript gibt die JSON-Daten zurück, entweder mit den tatsächlichen Werten aus der Datei oder mit leeren Werten, wenn die Datei nicht existiert oder die Daten nicht korrekt dekodiert wurden.

Beispielaufruf:

```
http://localhost/get_game_data.php
```

### Beispiel für die JSON-Datei

Die `game_data.json` Datei könnte wie folgt aussehen:

```json
{
    "player_1": {
        "name": "John Doe",
        "score": 5
    },
    "player_2": {
        "name": "Jane Smith",
        "score": 3
    },
    "game_id": "12345",
    "last_completed_game": "2024-06-22"
}
```

Dieses Skript überprüft, ob die Datei existiert und die Daten korrekt dekodiert wurden. Wenn ja, extrahiert es die relevanten Informationen und gibt sie als JSON-Antwort zurück. Wenn nicht, gibt es leere Werte zurück.
