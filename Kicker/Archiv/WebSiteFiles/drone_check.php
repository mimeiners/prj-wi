<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $Check = $_POST["success"];

    $file = fopen("DroneCheck.txt", "w") or die("Kann Datei nicht öffnen");
    fwrite($file, "success");
    fclose($file);

    echo "Succsess: Drone can start!:<br>$names";
    header("Location: back_home.php");
}
?>

<!DOCTYPE html>
<html lang="de">
<head>
	<meta charset="UTF-8">
    <title>Drohnechekc</title>
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
            height: 600px; 		/* Feste Höhe */
            margin: auto; 		/* Zentriert die Box */
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
            background-color: #c80000; /* Hintergrundfarbe bei Hover */
        }
    </style>
</head>
<body>
	<div class="container">
    <table align="center">
		<tr><td><img src="Pictures/hsb-logo.png" width="300" height="139"></td></tr>
		<br>
		<tr><th><font size="8"><span style="color:#c80000"> <a>Warung: Drohne </a></span></th></tr>
		<tr><td>Durch das drücken der Taste wird bestätigt das der Akku sicher in die Drohne eingesetzt wurde und es sicher ist für diese zu starten.<br></td></tr>
		<br>
	</table>
	<br>
	<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
		<button>Start</button>
	</form>

	</div>
</body>
</html>
