<?php
// Neue Session starten bzw. vorhandene fortsetzen
session_start();

// Datenbankverbindung aufbauen (Passwortdeklaration nicht vergessen)
require_once "config.php";

// Nutzer aus der Datenbank entfernen
$sql = "DELETE FROM active_users";

// SQL Statement ausführen 
if ($link->query($sql) === TRUE){
} else {
}

// Datenbankverbindung beenden
$link->close();

// Pfad zur JSON-Datei
$jsonFilePath = 'game_data.json';

// Überprüfe, ob die JSON-Datei existiert und lese die Daten
if (file_exists($jsonFilePath)) {
    $jsonData = file_get_contents($jsonFilePath);
    $data = json_decode($jsonData, true);

    // Überprüfe, ob die JSON-Daten korrekt dekodiert wurden
    if ($data !== null) {
        // Setze die Werte für button_start und button_power auf false
        $data['button_stop'] = true;

        $data['player_1']['name'] = "";
        $data['player_2']['name'] = "";

        $_SESSION["ingame"] = True;

        // Schreibe die aktualisierten Daten zurück in die JSON-Datei
        file_put_contents($jsonFilePath, json_encode($data, JSON_PRETTY_PRINT));
        // Session beenden
        session_destroy();
        header("Location: index.php");  
        exit(); // Beende das Skript, um eine doppelte Weiterleitung zu verhindern
    } else {
        echo "Fehler beim Dekodieren der JSON-Daten.";
        // Session beenden
        session_destroy();
        header("Location: index.php");  
        exit();
    }
} else {
    echo "JSON-Datei nicht gefunden.";
    // Session beenden
    session_destroy();
    header("Location: index.php");  
    exit();
}
// Session beenden
session_destroy();
// Weiterleitung mit Spieler-Namen und Drohnenstatus
header("Location: index.php");
exit(); // Sicherstellen, dass das Skript nach der Weiterleitung beendet wird
?>

