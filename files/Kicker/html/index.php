<?php
//Wenn Post Request von Button getätigt wird, dann führe das Script aus
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    //Spielernamen aus dem Post in die Variabeln schreiben
    $name1 = $_POST["name1"];
    $name2 = $_POST["name2"];

    // Debugging: Zeige die erhaltenen Namen an
    echo "Empfangene Namen:<br>";
    echo "Spieler 1: $name1<br>";
    echo "Spieler 2: $name2<br>";

    // Speichern in die Textdatei
    $names = "$name1, $name2\n";
    $file = fopen("PlayerNames.txt", "w") or die("Kann Datei nicht öffnen");
    fwrite($file, $names);
    fclose($file);

    //Bestätigung des schreibens
    echo "Namen erfolgreich gespeichert in PlayerNames.txt:<br>$names";

    // Speichern in die JSON-Datei
    $jsonFilePath = 'game_data.json';

    // Überprüfe, ob das Verzeichnis beschreibbar ist
    $dir = dirname($jsonFilePath);
    if (!is_writable($dir)) {
        die("Das Verzeichnis ist nicht beschreibbar: $dir");
    } else {
        echo "Das Verzeichnis ist beschreibbar: $dir<br>";
    }

    // Debugging: Überprüfen, ob die Datei existiert
    if (file_exists($jsonFilePath)) {
        echo "JSON-Datei gefunden: $jsonFilePath<br>";
        //Öffnen und dekodieren der json Datie
        $jsonData = file_get_contents($jsonFilePath);
        $data = json_decode($jsonData, true);
        // Debugging: Überprüfen, ob die JSON-Daten korrekt dekodiert wurden
    } else {
        echo "JSON-Datei nicht gefunden, erstelle neue Datei.<br>";
        $data = [];
    }

    // Datenstruktur anpassen oder erstellen
    $data['player_1']['name'] = $name1;
    $data['player_2']['name'] = $name2;

    // JSON-Datei schreiben
    $newJsonData = json_encode($data, JSON_PRETTY_PRINT);
    $result = file_put_contents($jsonFilePath, $newJsonData);

    //Weiterleitung an drone Check
    header("Location: drone_check.php?player1=$name1&player2=$name2");
    exit();
}
?>

<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Namen speichern</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        h1 {
            text-align: center;
            color: #136b9a;
        }

        p {
            text-align: center;
            color: #c80000;
        }

        form {
            text-align: center;
            margin-top: 20px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            color: #136b9a;
        }

        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }

        button {
            background-color: #136b9a;
            color: #fff;
            border: none;
            border-radius: 4px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        button:hover {
            background-color: #0e547d;
        }
    </style>
</head>
<body>
    <div class="container">
        <img src="Pictures/hsb-logo.png" width="300" height="139">
        <h1>Bitte Spieler eingeben</h1>
        <p>Durch das Bestätigen der Taste wird dem Speichern der Spielernamen zugestimmt.</p>
        <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
            <label for="name1">Player 1:</label>
            <input type="text" id="name1" name="name1">
            <label for="name2">Player 2:</label>
            <input type="text" id="name2" name="name2">
            <button>Speichern</button>
        </form>
        <p>Hast du schonmal gespielt? Gib deinen letzten Namen ein, damit die Punkte weiter gezählt werden!</p>
    </div>
</body>
</html>
