<?php
session_start();

// Überprüfen, ob der Benutzer bereits im Spiel ist
if (isset($_SESSION["ingame"]) && $_SESSION["ingame"] === true) {

    if ($_SESSION["page"] === 1) {
        header("Location: drone_check.php");
    }

    if ($_SESSION["page"] === 2) {
        header("Location: drone_start.php");
    }

    if ($_SESSION["page"] === 3) {
        header("Location: back_home.php");
    }

    if ($_SESSION["page"] === 4) {
        header("Location: result.php");
    }
    exit();
}else{
    $_SESSION["page"] = 0;
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name1 = $_POST["name1"];
    $name2 = $_POST["name2"];

    if ($name1 == $name2) {
        $name2 = "Klon von " . $name1;
    }

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
    $data['button_stop'] = false;
    $data['button_power'] = false;
    $data['button_start'] = false;
    $data['game_id'] = "";

    // JSON-Datei schreiben
    $newJsonData = json_encode($data, JSON_PRETTY_PRINT);
    $result = file_put_contents($jsonFilePath, $newJsonData);

    header("Location: drone_check.php");
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
        <h1>Bitte Spielernamen eingeben</h1>
        <p></p>
        <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
            <label for="name1">Spieler weiß:</label>
            <input type="text" id="name1" name="name1">
            <label for="name2">Spieler grün:</label>
            <input type="text" id="name2" name="name2">
            <button>Speichern</button>
        </form>
        <p></p>
    </div>
</body>
</html>
