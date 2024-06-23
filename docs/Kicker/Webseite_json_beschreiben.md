# Schreiben von Spielergebnissen in eine JSON-Datei mit PHP

Diese Anleitung erklärt, wie man mithilfe von PHP Spielergebnisse in einer JSON-Datei speichert und aktualisiert.

## Voraussetzungen

- PHP installiert
- Eine JSON-Datei (`game_data.json`) zum Speichern der Daten

## PHP Skript zum Schreiben von Daten in eine JSON-Datei

Das folgende PHP-Skript zeigt, wie man Spielergebnisse in einer JSON-Datei speichert und aktualisiert.

### Pfad zur JSON-Datei

Definieren Sie den Pfad zur JSON-Datei:

```php
<?php
// Pfad zur JSON-Datei
$jsonFilePath = 'game_data.json';
?>
```

### Funktion zum Lesen der aktuellen Daten

Erstellen Sie eine Funktion, um die aktuellen Daten aus der JSON-Datei zu lesen:

```php
<?php
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
?>
```

### Funktion zum Schreiben der Tore in die JSON-Datei

Erstellen Sie eine Funktion, um die Tore eines Spielers in die JSON-Datei zu schreiben:

```php
<?php
// Funktion zum Schreiben der Tore in die JSON-Datei
function writeGoalsToJson($playerName, $goals) {
    global $jsonFilePath;
    $currentData = readCurrentData();

    if ($currentData !== null) {
        // Debugging-Ausgabe
        echo "Aktuelle Daten aus JSON-Datei: <pre>";
        print_r($currentData);
        echo "</pre>";

        // Aktualisiere die Tore des Spielers in den finalen Werten
        if ($playerName == $currentData['player_1']['name']) {
            $currentData['final_player_1']['score'] = intval($goals);
        } elseif ($playerName == $currentData['player_2']['name']) {
            $currentData['final_player_2']['score'] = intval($goals);
        }

        // Debugging-Ausgabe
        echo "Zu aktualisierende Daten: <pre>";
        print_r($currentData);
        echo "</pre>";

        // Schreibe die aktualisierten finalen Werte in die JSON-Datei
        $jsonData = json_encode($currentData, JSON_PRETTY_PRINT);
        if (file_put_contents($jsonFilePath, $jsonData)) {
            echo "Tore erfolgreich in die JSON-Datei geschrieben.";
        } else {
            echo "Fehler beim Schreiben in die JSON-Datei.";
        }
    } else {
        echo "Fehler beim Lesen der JSON-Datei.";
    }
}
?>
```

### Überprüfung der POST-Daten und Aufruf der Schreibfunktion

Überprüfen Sie, ob die erforderlichen POST-Daten vorhanden sind, und rufen Sie die Schreibfunktion auf:

```php
<?php
// Überprüfe, ob die erforderlichen POST-Daten vorhanden sind
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['player']) && isset($_POST['goals'])) {
    $playerName = $_POST['player'];
    $goals = $_POST['goals'];

    // Debugging-Ausgabe
    echo "Spieler: $playerName, Tore: $goals";

    // Schreibe die Tore in die JSON-Datei
    writeGoalsToJson($playerName, $goals);
} else {
    echo "Ungültige Anfrage.";
}
?>
```

### Nutzung des Skripts

Speichern Sie das Skript als `update_score.php` und verwenden Sie eine POST-Anfrage, um Spielername und Tore zu senden. Beispiel für eine POST-Anfrage:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Update Score</title>
</head>
<body>
    <form method="POST" action="update_score.php">
        <label for="player">Spielername:</label>
        <input type="text" id="player" name="player">
        <label for="goals">Tore:</label>
        <input type="number" id="goals" name="goals">
        <input type="submit" value="Update Score">
    </form>
</body>
</html>
```

Dieses Formular sendet eine POST-Anfrage an das `update_score.php` Skript, das die Spielergebnisse in der JSON-Datei aktualisiert.

