# Datei: html/get_game_data.php

# Erklärung des PHP-Codes zum Lesen und Zurückgeben von JSON-Daten

Dieser PHP-Code liest die Spielerdaten und Informationen aus einer JSON-Datei und gibt sie im JSON-Format zurück. Der Code stellt sicher, dass die Daten korrekt dekodiert werden und behandelt Fälle, in denen die Datei nicht existiert oder die Dekodierung fehlschlägt. Der Prozess ist in mehrere Abschnitte unterteilt, die im Folgenden beschrieben werden.

## Pfad zur JSON-Datei

Zuerst wird der Pfad zur JSON-Datei definiert:

```php
// Pfad zur JSON-Datei
$jsonFilePath = 'game_data.json';
```

Diese Variable `$jsonFilePath` enthält den Pfad zur JSON-Datei, aus der die Daten gelesen werden sollen.

## Überprüfen, ob die JSON-Datei existiert, und Lesen der Daten

Der nächste Schritt ist die Überprüfung, ob die JSON-Datei existiert, und das Lesen der Daten aus dieser Datei:

```php
// Überprüfe, ob die JSON-Datei existiert und lese die Daten
if (file_exists($jsonFilePath)) {
    $jsonData = file_get_contents($jsonFilePath);
    $data = json_decode($jsonData, true);
```

- `file_exists($jsonFilePath)`: Überprüft, ob die JSON-Datei existiert.
- `file_get_contents($jsonFilePath)`: Liest den Inhalt der JSON-Datei.
- `json_decode($jsonData, true)`: Dekodiert den JSON-Inhalt in ein assoziatives Array.

## Überprüfen der JSON-Daten und Zuweisen der Werte

Falls die JSON-Daten korrekt dekodiert wurden, werden die Daten den entsprechenden Variablen zugewiesen:

```php
    // Überprüfe, ob die JSON-Daten korrekt dekodiert wurden
    if ($data !== null) {
        $player1 = $data['player_1']['name'] ?? '';
        $player2 = $data['player_2']['name'] ?? '';
        $gameId = $data['game_id'] ?? '';
        $lastCompletedGame = $data['last_completed_game'] ?? '';
        $player1_foul = $data['player_1']['foul'] ?? '';
        $player2_foul = $data['player_2']['foul'] ?? '';
```

- `?? ''`: Wenn der Wert in der JSON-Datei nicht existiert, wird ein leerer String zugewiesen.
- Die Daten werden aus dem JSON-Array ausgelesen und den entsprechenden Variablen zugewiesen (`$player1`, `$player2`, `$gameId`, `$lastCompletedGame`, `$player1_foul`, `$player2_foul`).

## Rückgabe der JSON-Daten

Die Daten werden als JSON-Format zurückgegeben:

```php
        echo json_encode([
            'player_1' => $player1,
            'player_2' => $player2,
            'game_id' => $gameId,
            'last_completed_game' => $lastCompletedGame,
            'player_1_foul' => $player1_foul,
            'player_2_foul' => $player2_foul
        ]);
```

- `json_encode`: Kodiert die Daten in ein JSON-Format und gibt sie aus.

Falls die JSON-Daten nicht korrekt dekodiert wurden, wird eine leere Struktur zurückgegeben:

```php
    } else {
        echo json_encode([
            'player_1' => '',
            'player_2' => '',
            'game_id' => '',
            'last_completed_game' => '',
            'player_1_foul' => '',
            'player_2_foul' => ''
        ]);
    }
```

## Behandlung des Fehlers, wenn die Datei nicht existiert

Falls die JSON-Datei nicht existiert, wird ebenfalls eine leere Struktur zurückgegeben:

```php
} else {
    echo json_encode([
        'player_1' => '',
        'player_2' => '',
        'game_id' => '',
        'last_completed_game' => '',
        'player_1_foul' => '',
        'player_2_foul' => ''
    ]);
}
```

## Zusammenfassung

Dieser PHP-Code liest die Spielerdaten aus einer JSON-Datei, verarbeitet sie und gibt die Informationen im JSON-Format zurück. Er überprüft, ob die Datei existiert und ob die JSON-Daten korrekt dekodiert wurden. Falls die Datei nicht existiert oder die Dekodierung fehlschlägt, wird eine leere Struktur zurückgegeben. Der Code ist klar strukturiert und behandelt verschiedene Fehlerszenarien, um sicherzustellen, dass immer eine gültige JSON-Antwort zurückgegeben wird.
