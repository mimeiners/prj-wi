
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
