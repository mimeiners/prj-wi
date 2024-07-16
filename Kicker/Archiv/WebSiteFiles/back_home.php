<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    $file = fopen("PlayerNames.txt", "w") or die("Kann Datei nicht öffnen");
    fwrite($file,"");
    fclose($file);
    
    $file = fopen("DroneCheck.txt", "w") or die("Kann Datei nicht öffnen");
    fwrite($file, "");
    fclose($file);
    
    header("Location: start_site.php");
}
$filename = 'PlayerNames.txt';

        // Überprüfen, ob die Datei existiert
        if (file_exists($filename)) {
            // Inhalt der Datei lesen
            $fileContent = file_get_contents($filename);

            // Dateiinhalt in einzelne Namen aufteilen
            $names = explode(',', $fileContent);

            // Whitespace um die Namen herum entfernen
            $names = array_map('trim', $names);

        } else {
            echo "Die Datei wurde nicht gefunden.";
        }
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Game Running</title>
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
            max-width: 800px; 	/* Maximale Breite */
            height: 600px; 	/* Feste Höhe */
            margin: auto; 	/* Zentriert die Box */
            text-align: center;
        }
	td {
            padding: 5px;
            text-align: center;
        }
	
        button {
	    width: 200px; 			/* Breite des Buttons */
            height: 50px; 			/* Höhe des Buttons */
            padding: 10px 20px; 		/* Innenabstand */
            font-size: 18px; 			/* Schriftgröße */
            background-color: #136b9a; 		/* Hintergrundfarbe */
            color: white; 			/* Textfarbe */
            border: none; 			/* Rahmen entfernen */
            border-radius: 5px; 		/* Abgerundete Ecken */
			}
	button:hover {
            background-color: #07c791; /* Hintergrundfarbe bei Hover */
        }
    </style>
</head>
<body>
    <div class="container">
    <table align="left">
	<tr><td><img src="Pictures/hsb-logo.png" width="300" height="139"><br></td></tr>
	<tr><th><font size="8"><span style="color:#136b9a"> <a>Spiel läuft</a></span></th></tr>
	<tr><td>Unten geht es zurück auf die Startseite<br></td></tr>
	<tr><td><br></td></tr>
	<?php 
	    echo "<tr>";
	    echo "<td>Player 1: " . htmlspecialchars($names[0]) . "</td>";
	    echo "</tr>";
	    echo "<tr>";
	    echo "<td>Player 2: " . htmlspecialchars($names[1]) . "</td>";
	    echo "</tr>";
	?>
	<tr><td><br></td></tr>
    </table>
    <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
        <button>Reset Game</button>
    </form>
    </div>
</body>
</html>
