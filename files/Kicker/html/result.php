<?php
session_start();
$_SESSION["page"] = 4;
// Pfad zur JSON-Datei
$jsonFilePath = 'game_data.json';

// Initialisiere Variablen
$finalPlayer1Name = '';
$finalPlayer2Name = '';
$finalScore1 = 0;
$finalScore2 = 0;
$winner = '';
$resultMessage = '';

// Überprüfe, ob die JSON-Datei existiert und lese die Daten
if (file_exists($jsonFilePath)) {
    $jsonData = file_get_contents($jsonFilePath);
    $data = json_decode($jsonData, true);

    // Überprüfe, ob die JSON-Daten korrekt dekodiert wurden
    if ($data !== null) {
        $finalPlayer1Name = $data['final_player_1']['name'] ?? '';
        $finalPlayer2Name = $data['final_player_2']['name'] ?? '';
        $finalScore1 = $data['final_player_1']['score'] ?? 0;
        $finalScore2 = $data['final_player_2']['score'] ?? 0;

        if ($finalScore1 > $finalScore2) {
            $winner = $finalPlayer1Name;
            $resultMessage = "Der Gewinner ist $winner mit einem Spielstand von $finalScore1 : $finalScore2!";
        } elseif ($finalScore2 > $finalScore1) {
            $winner = $finalPlayer2Name;
            $resultMessage = "Der Gewinner ist $winner mit einem Spielstand von $finalScore2 : $finalScore1!";
        } else {
            $resultMessage = "Das Spiel endet unentschieden mit einem Spielstand von $finalScore1 : $finalScore2!";
        }
    } else {
        $resultMessage = "Fehler beim Dekodieren der JSON-Daten.";
    }
} else {
    $resultMessage = "JSON-Datei nicht gefunden.";
}
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Spiel Ergebnis</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: auto;
            margin: auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        h1 {
            color: #136b9a;
        }

        .result-message {
            font-size: 20px;
            color: #333;
            margin: 20px 0;
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

        .game-status {
            font-size: 18px;
            padding: 10px 0;
        }

        .score {
            font-size: 100px;
            font-weight: bold;
            color: #136b9a;
        }

        .player-name {
            font-size: 30px;
            font-weight: bold;
            color: #136b9a;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Container-Inhalte hier -->
        <img src="Pictures/hsb-logo.png" width="250">
        <h1>Ergebnis:</h1>
        
        <div class="game-status">
                    <span class="player-name"><?php echo "$finalPlayer1Name"; ?></span>
                    <span class="player-name">&nbsp;:&nbsp;</span>
                    <span class="player-name"><?php echo "$finalPlayer2Name"; ?></span>
                    </div>
                    <div class="game-status">
                    
                    <span class="score">    </span>
                    <span class="score"><?php echo "$finalScore1"; ?></span>
                    <span class="score">&nbsp;:&nbsp;</span>
                    <span class="score"><?php echo "$finalScore2"; ?></span>
                    <span class="score">    </span>
                    
        </div>

        <div class="result-message"><?php echo htmlspecialchars($resultMessage); ?></div>
        <div class="result-message">
            <?php
            if ($finalPlayer1Name !== $winner) {
                #echo "<p>$finalPlayer1Name Tore: $finalScore1</p>";
            } elseif ($finalPlayer2Name !== $winner) {
                #echo "<p>$finalPlayer2Name Tore: $finalScore2</p>";
            }
            ?>
        </div>
        <form action="normal_stop.php" method="get">
            <button type="submit">Zurück zur Startseite</button>
        </form>
    </div>
</body>
</html>