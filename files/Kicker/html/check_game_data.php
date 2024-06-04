<?php
// Pfad zur JSON-Datei
$jsonFilePath = 'game_data.json';

// Überprüfe, ob die JSON-Datei existiert und lese die Daten
if (file_exists($jsonFilePath)) {
    $jsonData = file_get_contents($jsonFilePath);
    $data = json_decode($jsonData, true);

    // Überprüfe, ob die JSON-Daten korrekt dekodiert wurden
    if ($data !== null) {
        $player1 = $data['player_1']['name'] ?? '';
        $player2 = $data['player_2']['name'] ?? '';
        $gameId = $data['game_id'] ?? '';

        echo json_encode(['player_1' => $player1, 'player_2' => $player2, 'game_id' => $gameId]);
    } else {
        echo json_encode(['player_1' => '', 'player_2' => '', 'game_id' => '']);
    }
} else {
    echo json_encode(['player_1' => '', 'player_2' => '', 'game_id' => '']);
}
?>
