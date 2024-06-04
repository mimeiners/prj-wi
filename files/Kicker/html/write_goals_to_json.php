<?php
// Funktion zum schreiben der Tore in die JSON Datei für die result Auswertung
// Pfad zur JSON-Datei
$jsonFilePath = 'game_data.json';

// Funktion zum Lesen der aktuellen Daten aus der JSON-Datei
function readCurrentData() {
    global $jsonFilePath;
    if (file_exists($jsonFilePath)) {
        $jsonData = file_get_contents($jsonFilePath);
        return json_decode($jsonData, true);
    } else {
        return null;
    }
}

// Funktion zum Schreiben der Tore in die JSON-Datei
function writeGoalsToJson($playerName, $goals) {
    global $jsonFilePath;
    $currentData = readCurrentData();

    if ($currentData !== null) {
        // Debugging-Ausgabe
        echo "Aktuelle Daten aus JSON-Datei: <pre>";
        print_r($currentData);
        echo "</pre>";

        // Aktualisiere die Tore des Spielers in den finalen Werten
        if ($playerName == $currentData['player_1']['name']) {
            $currentData['final_player_1']['score'] = intval($goals);
        } elseif ($playerName == $currentData['player_2']['name']) {
            $currentData['final_player_2']['score'] = intval($goals);
        }

        // Debugging-Ausgabe
        echo "Zu aktualisierende Daten: <pre>";
        print_r($currentData);
        echo "</pre>";

        // Schreibe die aktualisierten finalen Werte in die JSON-Datei
        $jsonData = json_encode($currentData, JSON_PRETTY_PRINT);
        if (file_put_contents($jsonFilePath, $jsonData)) {
            echo "Tore erfolgreich in die JSON-Datei geschrieben.";
        } else {
            echo "Fehler beim Schreiben in die JSON-Datei.";
        }
    } else {
        echo "Fehler beim Lesen der JSON-Datei.";
    }
}

// Überprüfe, ob die erforderlichen POST-Daten vorhanden sind
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['player']) && isset($_POST['goals'])) {
    $playerName = $_POST['player'];
    $goals = $_POST['goals'];

    // Debugging-Ausgabe
    echo "Spieler: $playerName, Tore: $goals";

    // Schreibe die Tore in die JSON-Datei
    writeGoalsToJson($playerName, $goals);
} else {
    echo "Ungültige Anfrage.";
}
?>
