# Ergebnis-Seite

_Datei:_ `html/result.php`

Diese Anleitung beschreibt den Aufbau und die Funktionsweise der Ergebnis-Seite, die das Endergebnis eines Spiels anzeigt.

## PHP Session Start und Initialisierung

Zu Beginn wird eine PHP-Session gestartet und eine Session-Variable gesetzt, um den Status der Seite zu speichern:

```php
<?php
session_start();
$_SESSION["page"] = 4;
```

## Lesen und Verarbeiten der JSON-Datei

Der nächste Abschnitt des Codes liest die Spielerdaten und Ergebnisse aus einer JSON-Datei und verarbeitet sie, um den Gewinner zu ermitteln:

Pfad zur JSON-Datei und Initialisierung der Variablen

Zunächst wird der Pfad zur JSON-Datei festgelegt und einige Variablen initialisiert, um die Daten zu speichern:

```php
// Pfad zur JSON-Datei
$jsonFilePath = 'game_data.json';

// Initialisiere Variablen
$finalPlayer1Name = '';
$finalPlayer2Name = '';
$finalScore1 = 0;
$finalScore2 = 0;
$winner = '';
$resultMessage = '';
```

    $jsonFilePath speichert den Pfad zur JSON-Datei.
    Die Variablen $finalPlayer1Name, $finalPlayer2Name, $finalScore1, $finalScore2, $winner und $resultMessage werden initialisiert, um später die Spielerdaten, die Punktzahlen und das Ergebnis zu speichern.

Überprüfen, ob die JSON-Datei existiert, und Lesen der Daten

Der nächste Schritt ist die Überprüfung, ob die JSON-Datei existiert, und das Lesen der Daten aus dieser Datei:


```php

// Überprüfe, ob die JSON-Datei existiert und lese die Daten
if (file_exists($jsonFilePath)) {
    $jsonData = file_get_contents($jsonFilePath);
    $data = json_decode($jsonData, true);

    file_exists($jsonFilePath): Überprüft, ob die JSON-Datei existiert.
    file_get_contents($jsonFilePath): Liest den Inhalt der JSON-Datei.
    json_decode($jsonData, true): Dekodiert den JSON-Inhalt in ein assoziatives Array.
```

Überprüfen der JSON-Daten und Zuweisen der Werte

Falls die JSON-Daten korrekt dekodiert wurden, werden die Daten den entsprechenden Variablen zugewiesen:


```php

    // Überprüfe, ob die JSON-Daten korrekt dekodiert wurden
    if ($data !== null) {
        $finalPlayer1Name = $data['final_player_1']['name'] ?? '';
        $finalPlayer2Name = $data['final_player_2']['name'] ?? '';
        $finalScore1 = $data['final_player_1']['score'] ?? 0;
        $finalScore2 = $data['final_player_2']['score'] ?? 0;

    ?? '': Wenn der Wert nicht existiert, wird ein leerer String zugewiesen.
    ?? 0: Wenn der Wert nicht existiert, wird 0 zugewiesen.
```

Bestimmen des Gewinners

Der Gewinner wird basierend auf den Punktzahlen der Spieler ermittelt:

```php
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
```

    Wenn $finalScore1 größer als $finalScore2 ist, wird $finalPlayer1Name als Gewinner gesetzt.
    Wenn $finalScore2 größer als $finalScore1 ist, wird $finalPlayer2Name als Gewinner gesetzt.
    Wenn die Punktzahlen gleich sind, wird ein Unentschieden festgestellt.
    Die entsprechende Nachricht wird in $resultMessage gespeichert.

## HTML Grundstruktur

Die Grundstruktur des HTML-Dokuments enthält das grundlegende Layout und Stil für die Seite:

```html
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
        <img src="Pictures/hsb-logo.png" width="250">
        <h1>Ergebnis:</h1>
        
        <div class="game-status">
            <span class="player-name"><?php echo "$finalPlayer1Name"; ?></span>
            <span class="player-name">&nbsp;:&nbsp;</span>
            <span class="player-name"><?php echo "$finalPlayer2Name"; ?></span>
        </div>
        <div class="game-status">
            <span class="score"><?php echo "$finalScore1"; ?></span>
            <span class="score">&nbsp;:&nbsp;</span>
            <span class="score"><?php echo "$finalScore2"; ?></span>
        </div>

        <div class="result-message"><?php echo htmlspecialchars($resultMessage); ?></div>

        <form action="normal_stop.php" method="get">
            <button type="submit">Zurück zur Startseite</button>
        </form>
    </div>
</body>
</html>
```

## Zusammenfassung

Die Ergebnis-Seite zeigt das Endergebnis eines Spiels an, einschließlich der Namen der Spieler und ihrer Tore. Abhängig von den Ergebnissen wird eine Nachricht angezeigt, die den Gewinner oder ein Unentschieden verkündet. Es gibt auch einen Button, um zur Startseite zurückzukehren.
