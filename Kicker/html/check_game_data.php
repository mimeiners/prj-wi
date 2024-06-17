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
