# In-Game Statusseite

Diese Anleitung beschreibt den Aufbau und die Funktionsweise der "In-Game" Statusseite, die den aktuellen Spielstatus anzeigt und regelmäßig aktualisiert.

## PHP Session Start und Initialisierung

Zu Beginn wird eine PHP-Session gestartet und einige Session-Variablen gesetzt, um den Status der Seite zu speichern:

```php
<?php
session_start();

$_SESSION["ingame"] = True;
$_SESSION["page"] = 3;
?>
```

## HTML Grundstruktur

Die Grundstruktur des HTML-Dokuments enthält das grundlegende Layout und Stil für die Seite:

```html
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
            max-width: auto;
            margin: auto;
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
            font-size: 100px;
            font-weight: bold;
            color: #136b9a;
        }
        .game-data {
            font-size: 25px;
            font-weight: bold;
            color: #136b9a;
        }
        .player-name {
            font-size: 30px;
            font-weight: bold;
            color: #136b9a;
        }
        .player-data {
            text-align: center;
            margin-top: 20px;
            font-size: 18px;
        }
        .button-container {
            justify-content: center;
            display: flex;
            gap: 10px;
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
        .button3 {
            background-color: red;
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
                    <img src="Pictures/hsb-logo.png" width="250">
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
                        <span class="player-name" id="Player1">--</span>
                        <span class="player-name">&nbsp;:&nbsp;</span>
                        <span class="player-name" id="Player2">--</span>
                    </div>
                    <div class="game-status">
                        <span class="score">    </span>
                        <span class="score" id="goalsPlayer1">--</span>
                        <span class="score">&nbsp;:&nbsp;</span>
                        <span class="score" id="goalsPlayer2">--</span>
                        <span class="score">    </span>
                    </div>
                </td>
            </tr>
        </table>
        <div class="player-data">
            <span class="game-data" id="playerData">--</span>
        </div>
        <div class="button-container">
            <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
                <button>Seite aktualisieren</button>
            </form>
            <form action="normal_stop.php" method="get">
                <button class="button3" type="submit">Spiel abbrechen</button>
            </form>
        </div>
    </div>
</body>
</html>
```

## JavaScript für dynamische Inhalte

Das JavaScript sorgt für die regelmäßige Aktualisierung des Spielstatus und der Spielergebnisse:

```html
<script>
    // Fetch game data on page load
    window.onload = function() {
        setInterval(updateGameStatus, 500);
        setInterval(fetchGameData, 500);
    };

    var gameId, player1, player2, lastCompletedGame;

    // Fetch game data
    function fetchGameData() {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var response = JSON.parse(this.responseText);
                player1 = response.player_1;
                player2 = response.player_2;
                gameId = response.game_id;
                lastCompletedGame = response.last_completed_game;

                // Update HTML elements
                document.getElementById('Player1').textContent = player1 || '--';
                document.getElementById('Player2').textContent = player2 || '--';
                document.getElementById('playerData').innerHTML = "<p>Game ID: " + (gameId || '--') + "</p>";
            }
        };
        xhttp.open("GET", "check_game_data.php", true);
        xhttp.send();
    }

    function updateGameStatus() {
        if (gameId && lastCompletedGame && gameId === lastCompletedGame && player1 === "" && player2 === "") {
            window.location.href = "result.php";
        } else {
            // AJAX request to get player 1's score
            var xhttpPlayer1 = new XMLHttpRequest();
            xhttpPlayer1.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var goalsPlayer1 = this.responseText;
                    
                    if (player1 !== "") {
                        writeGoalsToJSON(player1, goalsPlayer1);
                    }
                    // Update player 1's score display
                    document.getElementById("goalsPlayer1").innerHTML = goalsPlayer1;
                }
            };
            xhttpPlayer1.open("GET", "get_game_status.php?player=" + player1 + "&game_id=" + gameId, true);
            xhttpPlayer1.send();

            // AJAX request to get player 2's score
            var xhttpPlayer2 = new XMLHttpRequest();
            xhttpPlayer2.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var goalsPlayer2 = this.responseText;
                    
                    if (player2 !== "") {
                        writeGoalsToJSON(player2, goalsPlayer2);
                    }
                    // Update player 2's score display
                    document.getElementById("goalsPlayer2").innerHTML = goalsPlayer2;
                }
            };
            xhttpPlayer2.open("GET", "get_game_status.php?player=" + player2 + "&game_id=" + gameId, true);
            xhttpPlayer2.send();
        }
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
</script>
```

## Zusammenfassung

Die In-Game Statusseite zeigt den aktuellen Status eines laufenden Spiels an, einschließlich der Namen der Spieler und ihrer Tore. Die Seite wird regelmäßig mit AJAX-Anfragen aktualisiert, um den aktuellen Spielstand anzuzeigen. Die Benutzer können die Seite manuell aktualisieren oder das Spiel abbrechen.
