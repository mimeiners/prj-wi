# Erklärung des PHP-Codes zur Aktualisierung von Spieler-Toren in einer JSON-Datei

_Datei:_ `html/write_goals_to_json.php`

Dieser PHP-Code ermöglicht es, die Tore von Spielern in einer JSON-Datei zu aktualisieren. Die Tore sind nachher für das result erforderlich, da die Daten von Python nach dem Spiel gecleart werden. Der Code ist in mehrere Funktionen unterteilt, die jeweils spezifische Aufgaben übernehmen. Im Folgenden wird der Code Schritt für Schritt erklärt.

## JSON-Dateipfad

Zuerst wird der Pfad zur JSON-Datei in einer Variablen gespeichert:

```php
$jsonFilePath = 'game_data.json';
```

Diese Variable wird später verwendet, um die Datei zu lesen und zu schreiben.

## Funktion zum Lesen der aktuellen Daten

Die Funktion `readCurrentData` liest die aktuellen Daten aus der JSON-Datei und gibt sie als assoziatives Array zurück:

```php
function readCurrentData() {
    global $jsonFilePath;
    if (file_exists($jsonFilePath)) {
        $jsonData = file_get_contents($jsonFilePath);
        return json_decode($jsonData, true);
    } else {
        return null;
    }
}
```

- `file_exists($jsonFilePath)`: Überprüft, ob die Datei existiert. Falls nicht, wird `null` zurückgegeben.
- `file_get_contents($jsonFilePath)`: Liest den gesamten Inhalt der Datei in einen String.
- `json_decode($jsonData, true)`: Wandelt den JSON-String in ein assoziatives Array um, sodass wir mit den Daten einfacher arbeiten können.

Diese Funktion wird verwendet, um die aktuellen Spielstandsdaten zu laden, bevor sie aktualisiert werden.

## Funktion zum Schreiben der Tore

Die Funktion `writeGoalsToJson` aktualisiert die Tore eines bestimmten Spielers in der JSON-Datei:

```php
function writeGoalsToJson($playerName, $goals) {
    global $jsonFilePath;
    $currentData = readCurrentData();

    if ($currentData !== null) {
        echo "Aktuelle Daten aus JSON-Datei: <pre>";
        print_r($currentData);
        echo "</pre>";

        if ($playerName == $currentData['player_1']['name']) {
            $currentData['final_player_1']['score'] = intval($goals);
        } elseif ($playerName == $currentData['player_2']['name']) {
            $currentData['final_player_2']['score'] = intval($goals);
        }

        echo "Zu aktualisierende Daten: <pre>";
        print_r($currentData);
        echo "</pre>";

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
```

- `readCurrentData()`: Ruft die Funktion auf, um die aktuellen Daten aus der JSON-Datei zu lesen.
- `print_r($currentData)`: Gibt die aktuellen Daten für Debugging-Zwecke aus.
- `if ($playerName == $currentData['player_1']['name']) { ... }`: Überprüft, ob der Spielername mit dem ersten Spieler übereinstimmt und aktualisiert die Tore entsprechend. Dasselbe gilt für den zweiten Spieler.
- `intval($goals)`: Wandelt die übergebenen Tore in einen Integer um, um sicherzustellen, dass sie korrekt gespeichert werden.
- `json_encode($currentData, JSON_PRETTY_PRINT)`: Wandelt das aktualisierte Array zurück in einen JSON-String, formatiert mit Einrückungen für bessere Lesbarkeit.
- `file_put_contents($jsonFilePath, $jsonData)`: Schreibt den JSON-String zurück in die Datei. Wenn der Schreibvorgang erfolgreich ist, wird eine Erfolgsmeldung ausgegeben, andernfalls eine Fehlermeldung.

## Verarbeiten der POST-Anfrage

Der folgende Code-Abschnitt überprüft, ob die erforderlichen POST-Daten vorhanden sind und ruft die Funktion `writeGoalsToJson` auf:

```php
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['player']) && isset($_POST['goals'])) {
    $playerName = $_POST['player'];
    $goals = $_POST['goals'];

    echo "Spieler: $playerName, Tore: $goals";

    writeGoalsToJson($playerName, $goals);
} else {
    echo "Ungültige Anfrage.";
}
```

- `$_SERVER["REQUEST_METHOD"] == "POST"`: Überprüft, ob die Anfrage eine POST-Anfrage ist. POST-Anfragen werden oft verwendet, um Daten sicher zu senden.
- `isset($_POST['player']) && isset($_POST['goals'])`: Überprüft, ob die erforderlichen POST-Daten vorhanden sind. Dies verhindert Fehler, die auftreten könnten, wenn Daten fehlen.
- `writeGoalsToJson($playerName, $goals)`: Ruft die Funktion auf, um die Tore des angegebenen Spielers in der JSON-Datei zu aktualisieren.

## Zusammenfassung

Der PHP-Code liest die aktuellen Spielstandsdaten aus einer JSON-Datei, aktualisiert die Tore eines bestimmten Spielers und speichert die aktualisierten Daten zurück in die JSON-Datei. Debugging-Ausgaben helfen, den Prozess zu überwachen und Fehler zu identifizieren. Der gesamte Prozess wird durch eine POST-Anfrage ausgelöst, die die erforderlichen Daten (Spielername und Tore) enthält.
