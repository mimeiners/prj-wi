<?php
/**
 * redirect.php
 * 
 * Weiterleitung für angemeldete Nutzer zum Spiel
 * 
 */

// Neue Session starten bzw. vorhandene fortsetzen
session_start();

// Nur angemeldete Nutzer sollen auf diese Seite zugreifen
if (!isset($_SESSION["loggedin"]) || $_SESSION["loggedin"] !== true) {
    header("location: login.php");
    exit;
}

// Datenbankverbindung aufbauen (Passwortdeklaration nicht vergessen)
require_once "config.php";

// Datenbank active_users wird auf Nutzernamen abgefragt
$sql = "SELECT username FROM active_users";
$result = $link->query($sql);
$players = [];

if ($result->num_rows > 0) {
    // Nutzernamen an Variable übergeben
    while ($row = $result->fetch_assoc()) {
        $players[] = $row["username"];
    }

    // Bei Doppelanmeldung wird der Spieler abgemeldet
    $uniquePlayers = array_unique($players);
    if (count($players) !== count($uniquePlayers)) {
        // Aktive Nutzer aus Datenbank löschen
        $sql = "DELETE FROM active_users";

        if ($link->query($sql) === TRUE){
            // Nutzer gelöscht
        } else {
        }
        // Weiterleiten auf Startseite
        session_destroy();
        header("location: index.php");
        exit;
    }

    // Schnittstelle für json-Datei für weiteren Spielverlauf
    $data = [];

    // Nutzernamen für json-Datei vorbereiten
    if (count($uniquePlayers) >= 2) {
        $data['player_1']['name'] = $uniquePlayers[0];
		$player1 = $uniquePlayers[0];
        $data['player_2']['name'] = $uniquePlayers[1];
		$player2 = $uniquePlayers[1];
    } else {
        echo "Not enough players.";
        exit();
    }
    
    $data['button_stop'] = false;
    $data['button_power'] = false;
    $data['button_start'] = false;
    $data['game_id'] = "";
    
    $jsonData = json_encode($data, JSON_PRETTY_PRINT);

    // json-Datei für weiteren Spielverlauf schreiben und weiterleiten
    if (file_put_contents('game_data.json', $jsonData) === false) {
        echo "Failed to write to game_data.json.";
        exit;
    } else {
        echo "Player data successfully written to game_data.json.";
		header("Location: drone_check.php?player1=$player1&player2=$player2");
		exit();
    }
} else {
    echo "No active users found.";
    exit();
}

// Datenbankverbindung beenden
$link->close();
?>

<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Willkommen</title>
    <link rel="stylesheet" href="bootstrap.min.css">
    <style>
        body { font: 16px sans-serif; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <h1 class="mb-4">Willkommen Spieler</h1>
                <ul class="list-group">
                    <?php foreach ($players as $player): ?>
                        <li class="list-group-item"><?php echo htmlspecialchars($player); ?></li>
                    <?php endforeach; ?>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
