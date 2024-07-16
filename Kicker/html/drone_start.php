<?php
session_start();
$buttonName = "hsfdofhis";
$_SESSION["ingame"] = True;
$_SESSION["page"] = 2;
if ($_SERVER["REQUEST_METHOD"] == "POST") {
        // Pfad zur JSON-Datei
        $jsonFilePath = 'game_data.json';

        // Überprüfe, ob die JSON-Datei existiert und lese die Daten
        if (file_exists($jsonFilePath)) {
            $jsonData = file_get_contents($jsonFilePath);
            $data = json_decode($jsonData, true);

            // Überprüfe, ob die JSON-Daten korrekt dekodiert wurden
            if ($data !== null) {
                // Setze die Werte für button_start auf true
                $data['button_start'] = true;

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

        // Weiterleitung mit Spieler-Namen und Drohnenstatus
        $buttonName = "geil";
        sleep(5);
        header("Location: back_home.php");
        exit(); // Beende das Skript, um eine doppelte Weiterleitung zu verhindern
}
?>

<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Drohne Start</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="bootstrap.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 800px;
            margin: auto;
            margin-top: 50px; /* Adjust this value to change the distance from the top */
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        table {
            width: 100%;
        }

        th {
            text-align: center;
            color: #136b9a;
            font-size: 24px;
            padding-bottom: 20px;
        }

        .game-status {
            font-size: 18px;
            padding: 10px 0;
        }

        .score {
            font-size: 150px;
            font-weight: bold;
            color: #136b9a;
        }

        .player-name {
            font-size: 50px;
            font-weight: bold;
            color: #136b9a;
        }

        .player-data {
            text-align: center;
            margin-top: auto;
            font-size: 18px;
        }

        .button-container {
        justify-content: center; /* Zentriert den Container horizontal */
        display: flex;
        gap: 10px; /* Abstand zwischen den Buttons */
        }

        button {
            display: block;
            margin: 20px auto;
            padding: 10px 20px;
            background-color: #136b9a;
            color: #fff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 18px;
            transition: background-color 0.3s;
        }

        .button2 {
            background-color: red;
        }

        .button3 {
            background-color: #136b9a;
        }

        button:hover {
            background-color: #0e547d;
        }
    </style>
</head>
<body>
    <div class="container">
        <table align="center">
            <tr><td><img src="Pictures/hsb-logo.png" width="250" ></td></tr>
            <br>
            <tr><th><font size="6"><span style="color:#c80000"> <a>Warung: Drohne starten </a></span></th></tr>
            <tr><td align="center">Die Drohne startet nach Drücken von "Start". Der Nutzer stellt sicher, dass die Drohne korrekt platziert wurde und sich keine Personen im Gefahrenbereich befinden. Die HSB übernimmt keinerlei Verantwortung für Fahrlässiges Verhalten und Verletzungen.<br></td></tr>
            <br>
        </table>
        <br>

        <div class="button-container">
            <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
                <button type="submit" id="myButton">Weiter</button>
            </form>
        </div>

        <script>
            document.getElementById("myButton").addEventListener("click", function() {
                this.textContent = "Spiel wird gestartet...";
            });
        </script>

        <div class="button-container">
        <form action="normal_stop.php" method="get">
            <button class="button3" type="submit">Spiel abbrechen</button>
        </form>
        </div>
    </div>
</body>
</html>
