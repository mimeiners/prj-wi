<?php
/**
 * waiting.php
 * 
 * Warteseite für ersten Spieler, der auf einen Gegner wartet
 * 
 */


// Neue Session starten bzw. vorhandene fortsetzen
session_start();

// Nur angemeldete Nutzer sollen hier zugreifen
if (isset($_SESSION["loggedin"]) && $_SESSION["loggedin"] === true) {
    // Datenbankabfrage zur Anzahl aktiver Nutzer 
    $secondUserValue = file_get_contents('check_second_user.php');

    // Wenn Nutzer einer der aktiven Spieler ist, dann weiterleiten
    if ($secondUserValue == 2) {
        header("location: back_home.php");
        exit;
    } else {
        // Andere Fälle
    }
} else {
        // Wenn nicht angemeldet, dann weiterleiten auf Startseite
        header("location: index.php");
		exit;

}

// Datenbankverbindung aufbauen (Passwortdeklaration nicht vergessen)
require_once "config.php";
// Datenbankverbindung beenden
$link->close();
?>

<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Warten</title>
    <link rel="stylesheet" href="bootstrap.min.css">
    <style>
        body { font: 13px sans-serif; }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card mt-5">
                    <div class="card-body">
                        <h2 class="card-title">Du bist auf der Seite "weiß". Eine zweite Person muss sich anmelden und wird Spieler der Seite "grün".</h2>
                        <div class="spinner-border text-primary" role="status"> </div>						
						<?php
                        if (!empty($login_err)) {
                            echo '<div class="alert alert-danger">' . $login_err . '</div>';
                        }
                        ?>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function checkActiveUsers() {
            fetch('check_second_user.php')
                .then(response => response.text())
                .then(data => {
                    if (parseInt(data) === 2) {
                        window.location.href = 'redirect.php'; // Sobald zwei Spieler in active_users stehen folgt Weiterleitung
                    } else if (parseInt(data) === 0) {
                        window.location.href = 'index.php'; // Wenn der zweite Spieler sich doppelt angemeldet hat, dann Warten abbrechen
                    }
                })
                .catch(error => console.error('Error:', error));
        }

        setInterval(checkActiveUsers, 1000); // Datenbank wiederholt abfragen
    </script>
</body>
</html>