# Datei: html/back_home.php

# Beschreibung des PHP-Codes für die "Ingame" Seite

Dieser PHP- und HTML-Code erstellt eine interaktive Webseite, die den aktuellen Spielstatus eines Spiels anzeigt, das in Echtzeit abläuft. Die Seite verwendet PHP-Sitzungsvariablen, um den Status des Spiels zu verfolgen und AJAX-Anfragen, um Spielerdaten und Spielstände dynamisch zu aktualisieren.

## PHP-Code zur Initialisierung der Sitzung

Zu Beginn des Skripts wird die PHP-Sitzung gestartet und einige Sitzungsvariablen gesetzt:

```php
<?php
session_start();

$_SESSION["ingame"] = True;
$_SESSION["page"] = 3;
?>
```

- `session_start()`: Startet eine neue oder bestehende Sitzung.
- `$_SESSION["ingame"] = True;`: Setzt die Sitzungsvariable `ingame` auf `True`, was bedeutet, dass ein Spiel läuft.
- `$_SESSION["page"] = 3;`: Setzt die Sitzungsvariable `page` auf 3, möglicherweise zur Verfolgung des aktuellen Seitenstatus.

## HTML-Struktur der Seite

Die HTML-Struktur definiert das Layout der Seite und enthält CSS für das Styling sowie JavaScript für die dynamische Aktualisierung.

### Kopfbereich (Head)

Der Kopfbereich enthält Meta-Tags, das Stylesheet und einige grundlegende CSS-Regeln:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Game Running</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="bootstrap.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
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
            padding: 20px;
            border: 2px solid #ccc;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
        }

        .container {
            margin-top: 50px;
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
```

### Seiteninhalt (Body)

Der Hauptinhalt der Seite enthält Popup-Fenster, eine Tabelle zur Anzeige des Spielstatus und Formulare zum Aktualisieren der Seite oder Abbrechen des Spiels.

```html
<body>
    <div class="container">
        <div id="popup_player_1" class="popup">
            <strong class="font-weight-bold text-danger h1">Foul Spiel</strong>
            <p>
                <span class="game-data" id="Player_1">--</span>
                <span class="game-data"> hat gekurbelt</span>
            </p>
        </div>

        <div id="popup_player_2" class="popup">
            <strong class="font-weight-bold text-danger h1">Foul Spiel</strong>
            <p>
                <span class="game-data" id="Player_2">--</span>
                <span class="game-data"> hat gekurbelt</span>
            </p>
        </div>

        <div class="justify-content-center mt-5">
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
                <span class="game-data">Game-ID:</span>
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
    </div>
```

### JavaScript zur dynamischen Aktualisierung

#### 1. `window.onload`

```javascript
window.onload = function() {
    setInterval(updateGameStatus, 500);
    setInterval(fetchGameData, 500);
};
```
- Diese Funktion wird aufgerufen, wenn die Seite vollständig geladen ist.
- Sie startet zwei wiederkehrende Aufgaben (`setInterval`), die alle 500 Millisekunden (`0.5 Sekunden`) ausgeführt werden:
  - `updateGameStatus`: Aktualisiert den Spielstatus.
  - `fetchGameData`: Ruft die Spielerdaten ab.

#### 2. `fetchGameData`

```javascript
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
            foulPlayer2 = response.player_2_foul || false;

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
- Erstellt eine AJAX-Anfrage (`XMLHttpRequest`), um Spielerdaten vom Server abzurufen.
- Sobald die Anfrage erfolgreich abgeschlossen ist (`readyState == 4` und `status == 200`), werden die empfangenen Daten (`responseText`) in JSON umgewandelt und in Variablen (`player1`, `player2`, `gameId`, `lastCompletedGame`, `foulPlayer1`, `foulPlayer2`) gespeichert.
- Aktualisiert die HTML-Elemente (`textContent`) mit den abgerufenen Daten.

#### 3. `updateGameStatus`

```javascript
function updateGameStatus() {
    if (gameId && lastCompletedGame && gameId === lastCompletedGame && player1 === "" && player2 === "") {
        window.location.href = "result.php";
    } else {
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
```
- Überprüft, ob das aktuelle Spiel beendet ist (`gameId === lastCompletedGame` und beide Spieler sind leer).
  - Wenn ja, wird die Seite auf `result.php` umgeleitet.
- Zeigt oder versteckt Popup-Fenster, basierend auf Fouls (`foulPlayer1`, `foulPlayer2`).
- Sendet AJAX-Anfragen, um die aktuellen Spielstände für `player1` und `player2` zu erhalten.
  - Bei erfolgreicher Antwort (`readyState == 4` und `status == 200`) wird die Funktion `writeGoalsToJSON` aufgerufen und die Spielstände (`goalsPlayer1`, `goalsPlayer2`) in die entsprechenden HTML-Elemente (`innerHTML`) geschrieben.

#### 4. `writeGoalsToJSON`

```javascript
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
```
- Erstellt eine AJAX-POST-Anfrage, um die Tore eines Spielers (`playerName`, `goals`) auf dem Server zu speichern.
- Sobald die Anfrage erfolgreich abgeschlossen ist (`readyState == 4` und `status == 200`), kann eine Antwort des Servers überprüft werden (falls erforderlich).

## Zusammenfassung

Dieser Code kombiniert PHP, HTML, CSS und JavaScript, um eine dynamische und interaktive Spielstatusseite zu erstellen. PHP wird verwendet, um Sitzungsvariablen zu verwalten, während JavaScript und AJAX verwendet werden, um Spielerdaten und Spielstände in Echtzeit zu aktualisieren. Das CSS sorgt für ein ansprechendes Layout und Styling der Seite.
