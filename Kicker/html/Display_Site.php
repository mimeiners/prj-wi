<?php
session_start();

$_SESSION["ingame"] = True;
$_SESSION["page"] = 3;
?>


<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Score Display</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="bootstrap.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #000000;
            margin: 0;
            padding: 0;
        }

        .popup {
            position: fixed;
            text-align: center;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: white;
            padding: 40px;
            border: 2px solid #ccc;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
        }

        .container {
            
        }

        table {
            width: 100%;
        }

        th {
            text-align: center;
            color: #ffffff;
            font-size: 24px;
            
        }

        .game-status {
            font-size: 18px;
        }

        .score {
            font-size: 400px;
            font-weight: bold;
            color: #ffffff;
        }


        .game-data {
            font-size: 25px;
            font-weight: bold;
            color: #ffffff;
        }

        .player-name {
            font-size: 100px;
            font-weight: bold;
            color: #ffffff;
        }

        .player-data {
            text-align: center;
            margin-top: 20px;
            font-size: 18px;
        }

       
    </style>
</head>
<body>
    <div class="container">

    <div id="popup_player_1" class="popup">
    <strong class="font-weight-bold text-danger h1"><font size="500"><a>Foul Spiel</a></strong>
    <p>
    <span class="font-weight-bold" id="Player_1">--</span>
    <span class="font-weight-bold"> hat gekurbelt</span>
    </p>
    </div>

    <div id="popup_player_2" class="popup">
    <strong class="font-weight-bold text-danger h1"><font size="500"><a>Foul Spiel</a></strong>
    <p>
    <span class="font-weight-bold" id="Player_2">--</span>
    <span class="font-weight-bold"> hat gekurbelt</span>
    </p>
    </div>

        <table>
            <tr>
                <td colspan="2" align="left">
                    <img src="Pictures/HSB_Logo_S_Weiss_sRGB.png" width="500">
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
        <span class="game-data">Game ID:</span>
        <span class="game-data" id="playerData">--</span>
        </div>
    </div>

    <script>

        // Fetch game data on page load
        window.onload = function() {
            setInterval(updateGameStatus, 500);
            setInterval(fetchGameData, 500);
        };

        var gameId, player1, player2, lastCompletedGame, foulPlayer1, foulPlayer2;

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
                    foulPlayer1 = response.player_1_foul || false;
                    foulPlayer2 = response.player_2_foul|| false;

                    // Update HTML elements
                    document.getElementById('Player1').textContent = player1 || '--';
                    document.getElementById('Player2').textContent = player2 || '--';
                    document.getElementById('Player_1').textContent = player1 || '--';
                    document.getElementById('Player_2').textContent = player2 || '--';
                    document.getElementById('playerData').textContent = gameId || '--';

                }

            };
            xhttp.open("GET", "check_game_data.php", true);
            xhttp.send();
        }


        function updateGameStatus() {
            if (gameId && lastCompletedGame && gameId === lastCompletedGame && player1 === "" && player2 === "") {

                window.location.href = "QR.php";
            }else{

            if (foulPlayer1 === true) {
                document.getElementById('popup_player_1').style.visibility = 'visible';
            } else if (foulPlayer1 === false) {
                document.getElementById('popup_player_1').style.visibility = 'hidden';
            }

            if (foulPlayer2 === true) {
                document.getElementById('popup_player_2').style.visibility = 'visible';
            } else if (foulPlayer2 === false) {
                document.getElementById('popup_player_2').style.visibility = 'hidden';
            }

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
</body>
</html>