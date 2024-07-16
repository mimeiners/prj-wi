<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name1 = $_POST["name1"];
    $name2 = $_POST["name2"];

    $names = "$name1, $name2\n";

    $file = fopen("PlayerNames.txt", "w") or die("Kann Datei nicht öffnen");
    fwrite($file, $names);
    fclose($file);

    echo "Namen erfolgreich gespeichert:<br>$names";
    header("Location: drone_check.php");
}
?>

<!DOCTYPE html>
<html lang="de">
<head>
	<meta charset="UTF-8">
	<title>Namen speichern</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        html, body {
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
            display: grid;
            place-items: center;
        }
        .container {
            max-width: 800px; /* Maximale Breite */
            height: 600px; /* Feste Höhe */
            margin: auto; /* Zentriert die Box */
            text-align: center;
        }
                button {
			width: 200px; 				/* Breite des Buttons */
            height: 50px; 				/* Höhe des Buttons */
            padding: 10px 20px; 		/* Innenabstand */
            font-size: 18px; 			/* Schriftgröße */
            background-color: #136b9a; 	/* Hintergrundfarbe */
            color: white; 				/* Textfarbe */
            border: none; 				/* Rahmen entfernen */
            border-radius: 5px; 		/* Abgerundete Ecken */
			}
			button:hover {
            background-color: #07c791; /* Hintergrundfarbe bei Hover */
        }
    </style>
</head>
<body>
	<div class="container">
    <table align="center">
		<tr><img src="Pictures/hsb-logo.png" width="300" height="139"></tr>
	</table>
	<table align="center">
		<tr><h1><span style="color:#136b9a"> <a>Bitte Spieler eingeben</a></span></h1></tr>
		<tr><td><span style="color:#c80000"> <a>Druch das bestätigen der Taste wird dem speichern der Spielernamen zugestimmt.<br></a></span></td></tr>
		<br>
		<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
			<label for="name1">Player 1:</label>
			<input type="text" id="name1" name="name1"><br><br>
			<label for="name2">Player 2:</label>
			<input type="text" id="name2" name="name2"><br><br>
			<button>Speichern</button>
		</form>
		<br>
		<tr><td>Hast du schonmal gespielt? Gebe deinen letzten Namen ein, damit die Punkte weiter gezählt werden!<br></td></tr>
	</table>
	</div>
</body>
</html>
