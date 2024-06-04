<?php
// Dronen Bestätigung
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Überprüfe, ob die Parameter "player1" und "player2" im POST vorhanden sind und nicht leer sind
    if (!empty($_POST["player1"]) && !empty($_POST["player2"])) {
        // Spieler-Namen aus dem POST-Array extrahieren
        $player1 = $_POST["player1"];
        $player2 = $_POST["player2"];

        // Den Wert für die Drohne auf "true" setzen
        $drone_value = "true";

        // Den Wert in die Datei schreiben
        $file = fopen("DroneCheck.txt", "w") or die("Kann Datei nicht öffnen");
        fwrite($file, $drone_value);
        fclose($file);

        // Pfad zur JSON-Datei
        $jsonFilePath = 'game_data.json';

        // Überprüfe, ob die JSON-Datei existiert und lese die Daten
        if (file_exists($jsonFilePath)) {
            $jsonData = file_get_contents($jsonFilePath);
            $data = json_decode($jsonData, true);

            // Überprüfe, ob die JSON-Daten korrekt dekodiert wurden
            if ($data !== null) {
                // Setze die Werte für button_start und button_power auf true
                $data['button_start'] = true;
                $data['button_power'] = true;

                // Schreibe die aktualisierten Daten zurück in die JSON-Datei
                file_put_contents($jsonFilePath, json_encode($data, JSON_PRETTY_PRINT));
            } else {
                echo "Fehler beim Dekodieren der JSON-Daten.";
                exit();
            }
        } else {
            echo "JSON-Datei nicht gefunden.";
            exit();
        }

        // Erfolgsmeldung und Weiterleitung
        echo "Success: Drone can start! Spieler 1: $player1, Spieler 2: $player2";
        // Weiterleitung mit Spieler-Namen und Drohnenstatus
        header("Location: back_home.php?player1=$player1&player2=$player2&drone=true");
        exit(); // Beende das Skript, um eine doppelte Weiterleitung zu verhindern
    } else {
        // Fehlermeldung, falls die Parameter nicht vorhanden oder leer sind
        echo "Error: Spieler-Namen nicht gefunden oder leer!";
    }
}
?>

<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Drohnechekc</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        html, body {
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
            display: grid;
            place-items: center;
        }
        .container {
            max-width: 800px;   /* Maximale Breite */
            height: 600px;      /* Feste Höhe */
            margin: auto;       /* Zentriert die Box */
            text-align: center;
        }
        button {
            width: 200px;               /* Breite des Buttons */
            height: 50px;               /* Höhe des Buttons */
            padding: 10px 20px;         /* Innenabstand */
            font-size: 18px;            /* Schriftgröße */
            background-color: #136b9a;  /* Hintergrundfarbe */
            color: white;               /* Textfarbe */
            border: none;               /* Rahmen entfernen */
            border-radius: 5px;         /* Abgerundete Ecken */
        }
        button:hover {
            background-color: #c80000; /* Hintergrundfarbe bei Hover */
        }
    </style>
</head>
<body>
    <div class="container">
        <table align="center">
            <tr><td><img src="Pictures/hsb-logo.png" width="300" height="139"></td></tr>
            <br>
            <tr><th><font size="8"><span style="color:#c80000"> <a>Warung: Drohne </a></span></th></tr>
            <tr><td>Durch das drücken der Taste wird bestätigt das der Akku sicher in die Drohne eingesetzt wurde und es sicher ist für diese zu starten.<br></td></tr>
            <br>
        </table>
        <br>
        <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
            <input type="hidden" name="player1" value="Spieler_1">
            <input type="hidden" name="player2" value="Spieler_2">
            <button type="submit">Start</button>
        </form>
    </div>
</body>
</html>
