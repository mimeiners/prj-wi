# Anzeigetafel über Webseite

In diesem Segment wird der Aufbau und Funktion der auf der Anzeigetafel angezeigten QR-Kode und Punktestandseite beschrieben.

## QR-Seite:
Diese Seite wird immer auf den Anzeigetafeln angezeigt, wenn aktuell kein Spiel läuft. Zweck des QR-Kodes ist es auf die Anmeldeseite zu verweisen. <br>
Die Seite ist dabei folgendermaßen aufgebaut:
### Grundstruktur von QR.html:
Im ersten Abschnitt wird die Seite in *html* erstellt und formatiert:

```html
<!DOCTYPE html>
<html lang="de">
<head>
	<meta charset="UTF-8">
    <title>QR</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        html, body {
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
            display: grid;
            place-items: center;
            background-color: black;
        }
        .container {
            max-width: auto; 	/* Maximale Breite */
            height: auto; 		/* Feste Höhe */
            margin: auto; 		/* Zentriert die Box */
            text-align: center;
        }
         
    </style>
</head>
```
### Spielernamen Abfrage und Wechseln der Anzeigen:
Anschließend wird im *body* ein *javascript*-Segment erstellt. Dieser schaut in der .json-Datei nach, ob Spielernamen eingetragen wurden. Sollte dies der Fall sein, wird auf die Punktestandseite *Display_Site.php* weitergeleitet. Andernfalls wartet die Seite weiter, bis Spielernamen eingetragen wurden.

```html
<body>
    <script type="text/javascript">
        setInterval(function() {
            fetch('game_data.json')
            .then(response => response.json())
            .then(data => {
                const player_1 = data.player_1;
                if (player_1.name !== "") {
                    window.location.href = "Display_Site.php";
                }
            })
            .catch(error => console.error('Error:', error));
            
        }, 1000);
    </script>
```
### Restliche Formatierung:
Zu guter Letzt wird der QR-Kode an die richtige Stelle auf der Seite, zusammen mit dem HSB-Logo positioniert und das *html*-Dokument geschlossen:

```html
    <div id="result"></div>
	<div class="container">
    <table align="center">
        <tr><img src="Pictures/HSB_Logo_S_Weiss_sRGB.png" width="400"></tr>
    </table>
    <table align="center">
    <tr><img src="Pictures/qr.png" width="750" height="750"></tr>
    </table>
    
	</div>
</body>
</html>
```
## Punktestand:
Diese Seite zeigt den aktuellen Spielstand, zusammen mit den Spielernamen auf den Anzeigetafeln.
### Grundstruktur von Display_Site.php:
Zuerst wird eine *PHP-Session* gestartet und einige Session-Variablen gesetzt. Anschließend wird ein *html*-Segment erstellt in den weitere Formatierungen festgelegt werden:

```php
<?php
session_start();

$_SESSION["ingame"] = True;
$_SESSION["page"] = 3;
?>
```
```html
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
```
Im *body* wird die Struktur der Punkteanzeige festgelegt mit den Spielernamen, den Punkten sowie der *Game-ID*:
```html
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
```
### Aufrufen der Spieldaten und Anzeige:
Es werden Funktionen erstellt, welche ermöglichen die Spieldaten auszulesen wie Spielernamen, Anzahl der Tore, Game-Id und ob einer der beiden Spieler auf Foul durch Kurbeln ausgelöst hat:

```html
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
```
Eine weitere Funktion prüft den aktuellen Status des Spiel ab. Sollte kein Spiel laufen wird auf *QR.html* weitergeleitet. Sollten Spielernamen vorhanden sein, werden diese auch angezeigt.

```html
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
```
Zuletzt werden durch einen *AJAX Request* Die Spieldaten jedes Spielers einzeln ausgelesen und die Anzeige um diese aktualisiert:
```html
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
```
Auch an dieser Stelle werden die Punke in die .json-Datei geschrieben und das Dokument beendet:

 ```html
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
```
