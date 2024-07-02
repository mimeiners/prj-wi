<?php
/**
 * login.php
 * 
 * Anmeldeseite für Nutzer
 * 
 */

// Neue Session starten bzw. vorhandene fortsetzen
session_start();

// Weiterleitung für bereits angemeldete Nutzer 
if (isset($_SESSION["loggedin"]) && $_SESSION["loggedin"] === true) {
    // Datenbankabfrage zur Anzahl der angemeldeten Nutzer
    $secondUserValue = file_get_contents('check_second_user.php');

    // Wenn der Nutzer der zweite Spieler ist, dann Warteseite überspringen
    if ($secondUserValue == 2) {
        header("location: redirect.php");
        exit;
    } else {
        // Fehlermeldung
    }
} else {
    // Fehlermeldung
}

// Für unangemeldete Nutzer neue Datenbankverbindung aufbauen (Passwortdeklaration nicht vergessen)
require_once "config.php";

// Variablen für die Eingabefelder initialisieren
$username = $password = "";
$username_error = $password_error = "";
$login_error = "";

// Eingabefelderinhalt prüfen und ggf. verarbeiten
if ($_SERVER["REQUEST_METHOD"] == "POST") {

	// Nutzernameneingabe übergeben
	$username = trim($_POST["username"]);
	$username_error = empty($username) ? "Bitte Nutzernamen eingeben." : "";

	// Passworteingabe übergeben
	$password = trim($_POST["password"]);
	$password_error = empty($password) ? "Bitte Passwort eingeben." : "";
   
    // Passwort und Nutzername prüfen
    if (empty($username_error) && empty($password_error)) {
        $sql_cmd = "SELECT id, username, password FROM users WHERE username = ?";

        // Nutzernameneingabe für Datenbankeintragung vorbereiten
        if ($stmt = mysqli_prepare($link, $sql_cmd)) {
            mysqli_stmt_bind_param($stmt, "s", $username_parameter);
            $username_parameter = $username;

            if (mysqli_stmt_execute($stmt)) {
                mysqli_stmt_store_result($stmt);

                // Wenn der Nutzername vorhanden ist, wird das Passwort verifiziert
                if (mysqli_stmt_num_rows($stmt) == 1) {
        
                    mysqli_stmt_bind_result($stmt, $id, $username, $password_hash);
                    if (mysqli_stmt_fetch($stmt)) {

                        // Wenn das Passwort stimmt, ermittle Anzahl an angemeldeten Nutzern
                        if (password_verify($password, $password_hash)) {
                            							
                            // Datenbanktabelle active_users wird abgefragt
                            $check_sql = "SELECT COUNT(*) as count FROM active_users";
                            $check_result = mysqli_query($link, $check_sql);
                            $row = mysqli_fetch_assoc($check_result);
                            $count = $row['count'];

                            // Wenn noch kein Nutzer angemeldet ist, eintragen und weiterleiten
                            if ($count == 0) {
								$_SESSION["loggedin"] = true;
								$_SESSION["username"] = $username;
                                // Nutzer als ersten Spieler eintragen
                                $insert_sql = "INSERT INTO active_users (username) VALUES (?)";
                                $insert_stmt = mysqli_prepare($link, $insert_sql);
                                mysqli_stmt_bind_param($insert_stmt, "s", $username);
                                mysqli_stmt_execute($insert_stmt);
                                mysqli_stmt_close($insert_stmt);
								
								header("location: waiting.php");
								exit;
							
                            // Wenn ein Nutzer angemeldet ist, eintragen und weiterleiten
                            } elseif ($count == 1) {	
								$_SESSION["loggedin"] = true;
								$_SESSION["username"] = $username;
								// Nutzer als zweiten Spieler eintragen
								$insert_sql = "INSERT INTO active_users (username) VALUES (?)";
								$insert_stmt = mysqli_prepare($link, $insert_sql);
								mysqli_stmt_bind_param($insert_stmt, "s", $username);
								mysqli_stmt_execute($insert_stmt);
								mysqli_stmt_close($insert_stmt);
								
								header("location: redirect.php");
								exit;					

                            // Wenn schon zwei Nutzer angemeldet sind, Fehler melden
                            } else {
                                $login_error = "Es sind bereits zwei Spieler angemeldet.";							
                            }

                        } else {
                            // Falsches Passwort
                            $login_error = "Passwort oder Nutzername falsch.";
                        }
                    }
                } else {
                    // Falscher Nutzername
                    $login_error = "Passwort oder Nutzername falsch.";
                }
            } else {
                echo "Unbekannte Fehlermeldung.";
            }

            // SQL statement beenden
            mysqli_stmt_close($stmt);
        }
    }

    // Datenbankverbindung beenden
    mysqli_close($link);
}
?>

<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Anmeldung</title>
    <link rel="stylesheet" href="bootstrap.min.css">
    <style>
        body { font: 16px sans-serif; }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card mt-5">
                    <div class="card-body">
                        <h2 class="card-title">Anmeldung</h2>
                        <p class="card-text">Hier bitte Nutzerdaten eingeben.</p>
                        <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
                            <div class="form-group">
                                <label for="username">Nutzername</label>
                                <input type="text" id="username" name="username" class="form-control <?php echo (!empty($username_error)) ? 'is-invalid' : ''; ?>" value="<?php echo $username; ?>">
                                <span class="invalid-feedback"><?php echo $username_error; ?></span>
                            </div>
                            <div class="form-group">
                                <label for="password">Passwort</label>
                                <input type="password" id="password" name="password" class="form-control <?php echo (!empty($password_error)) ? 'is-invalid' : ''; ?>">
                                <span class="invalid-feedback"><?php echo $password_error; ?></span>
                            </div>
                            <div class="form-group">
                                <input type="submit" class="btn btn-primary" value="Anmelden">
								<?php
								if (!empty($login_error)) {echo '<div class="alert alert-danger">' . $login_error . '</div>';}
								?>
                            </div>
                            <p><a href="register.php">Zur Registrierung</a>.</p>
							<p><a href="index.php">Zur Startseite</a>.</p>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>