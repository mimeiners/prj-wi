<?php
// Hauptdatei für den Spielablauf
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

// Funktion zum Schreiben der finalen Werte in die JSON-Datei
function writeFinalValues($player1Name, $player2Name, $player1Score, $player2Score) {
    global $jsonFilePath;
    $currentData = readCurrentData();

    if ($currentData !== null) {
        $data = $currentData;

        $data['final_player_1'] = [
            "name" => $player1Name,
        ];

        $data['final_player_2'] = [
            "name" => $player2Name,
        ];

        // Schreibe die finalen Werte in die JSON-Datei
        $jsonData = json_encode($data, JSON_PRETTY_PRINT);
        file_put_contents($jsonFilePath, $jsonData);
    }
}

// Überprüfe, ob das Formular gesendet wurde
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Lese Spielerdaten aus der JSON-Datei
    $currentData = readCurrentData();
    $player1Name = $currentData['player_1']['name'] ?? 'Spieler_1';
    $player2Name = $currentData['player_2']['name'] ?? 'Spieler_2';

    // Lese den Spielstand aus der get_game_status.php
    $player1Score = $_POST['player1_score'] ?? 0;
    $player2Score = $_POST['player2_score'] ?? 0;

    // Schreibe die finalen Werte in die JSON-Datei
    writeFinalValues($player1Name, $player2Name, $player1Score, $player2Score);
}
?>


<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Game Running</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 800px;
            margin: 50px auto;
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
            font-size: 32px;
            font-weight: bold;
            color: #136b9a;
        }

        .player-data {
            margin-top: 20px;
            font-size: 18px;
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

        button:hover {
            background-color: #0e547d;
        }
    </style>
</head>
<body>
    <div class="container">
        <table>
            <tr>
                <td colspan="2" align="center">
                    <img src="Pictures/hsb-logo.png" width="300" height="139">
                    <h1>Spiel läuft</h1>
                </td>
            </tr>
            <tr>
                <td colspan="2" align="center">
                    Unten geht es zurück auf die Startseite
                </td>
            </tr>
            <tr>
                <td colspan="2" align="center">
                    <div class="game-status">
                        <span class="score" id="gameStatusPlayer1">Wird geladen...</span>
                    </div>
                    <div class="game-status">
                        <span class="score" id="gameStatusPlayer2">Wird geladen...</span>
                    </div>
                </td>
            </tr>
        </table>
        <div class="player-data">
            <?php
            // Pfad zur JSON-Datei
            $jsonFilePath = 'game_data.json';

            // Überprüfe, ob die JSON-Datei existiert und lese die Daten
            if (file_exists($jsonFilePath)) {
                $jsonData = file_get_contents($jsonFilePath);
                $data = json_decode($jsonData, true);

                // Überprüfe, ob die JSON-Daten korrekt dekodiert wurden
                if ($data !== null) {
                    $player1 = $data['player_1']['name'] ?? 'Unbekannt';
                    $player2 = $data['player_2']['name'] ?? 'Unbekannt';
                    $gameId = $data['game_id'] ?? 'Unbekannt';
                    $player1Score = $data['final_player_1']['score'] ?? 0;
                    $player2Score = $data['final_player_2']['score'] ?? 0;

                    echo "<p>Player 1: " . htmlspecialchars($player1) . "</p>";
                    echo "<p>Player 1 Score: " . htmlspecialchars($player1Score) . "</p>";
                    
                    echo "<p>Player 2: " . htmlspecialchars($player2) . "</p>";
                    echo "<p>Player 2 Score: " . htmlspecialchars($player2Score) . "</p>";
                    
                    echo "<p>Game ID: " . htmlspecialchars($gameId) . "</p>";
                } else {
                    echo "<p>Fehler beim Dekodieren der JSON-Daten.</p>";
                }
            } else {
                echo "<p>JSON-Datei nicht gefunden.</p>";
            }

            ?>
        </div>
        <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
            <button>Reset Game</button>
        </form>
    </div>

    <script>
        var playerName1 = "<?php echo htmlspecialchars($player1 ?? ''); ?>";
        var playerName2 = "<?php echo htmlspecialchars($player2 ?? ''); ?>";
        var gameID = "<?php echo htmlspecialchars($gameId ?? ''); ?>";

        function updateGameStatus() {
            // AJAX-Anfrage zum Abrufen der Spielstandsinformationen für Spieler 1
            var xhttpPlayer1 = new XMLHttpRequest();
            xhttpPlayer1.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var goalsPlayer1 = this.responseText;
                    // Schreibe die Tore von Spieler 1 in die JSON-Datei
                    writeGoalsToJSON('<?php echo htmlspecialchars($player1); ?>', goalsPlayer1);
                    // Aktualisiere die Anzeige des Spielstands für Spieler 1
                    document.getElementById("gameStatusPlayer1").innerHTML = "Spieler 1: <?php echo htmlspecialchars($player1); ?> \t" + goalsPlayer1;

                }
            };
            xhttpPlayer1.open("GET", "get_game_status.php?player=<?php echo htmlspecialchars($player1); ?>&game_id=<?php echo htmlspecialchars($gameId); ?>", true);
            xhttpPlayer1.send();

            // AJAX-Anfrage zum Abrufen der Spielstandsinformationen für Spieler 2
            var xhttpPlayer2 = new XMLHttpRequest();
            xhttpPlayer2.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var goalsPlayer2 = this.responseText;
                    // Aktualisiere die Anzeige des Spielstands für Spieler 2
                    document.getElementById("gameStatusPlayer2").innerHTML = "Spieler 2: <?php echo htmlspecialchars($player2); ?> \t" + goalsPlayer2;
                }
            };
            xhttpPlayer2.open("GET", "get_game_status.php?player=<?php echo htmlspecialchars($player2); ?>&game_id=<?php echo htmlspecialchars($gameId); ?>", true);
            xhttpPlayer2.send();
        }

// Funktion zum Schreiben der Tore in die JSON-Datei
function writeGoalsToJSON(playerName, goals) {
    var xhttpWriteGoals = new XMLHttpRequest();
    xhttpWriteGoals.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // Überprüfe die Antwort der Serverseite, falls erforderlich
        }
    };
    xhttpWriteGoals.open("POST", "write_goals_to_json.php", true);
    xhttpWriteGoals.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttpWriteGoals.send("player=" + playerName + "&goals=" + goals);
}

        // Funktion zum Überprüfen der Spielernamen und der Spiel-ID
        function checkGameData() {
            var xhttpCheckData = new XMLHttpRequest();
            xhttpCheckData.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var response = JSON.parse(this.responseText);
                    if (!response.player_1 || !response.player_2 || !response.game_id) {
                        window.location.href = "result.php";
                    }
                }
            };
            xhttpCheckData.open("GET", "check_game_data.php", true);
            xhttpCheckData.send();
        }

        

        // Aktualisiere den Spielstand alle 5 Sekunden
        setInterval(updateGameStatus, 500);
        // Überprüfe die Spielernamen und die Spiel-ID alle 5 Sekunden
        setInterval(checkGameData, 5000);
    </script>
</body>
</html>
