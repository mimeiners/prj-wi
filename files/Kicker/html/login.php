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
$username_err = $password_err = $login_err = "";

// Eingabefelderinhalt prüfen und ggf. verarbeiten
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    // Nutzernameneingabe übergeben
    if (empty(trim($_POST["username"]))) {
        $username_err = "Bitte Nutzernamen eingeben.";
    } else {
        $username = trim($_POST["username"]);
    }

    // Passworteingabe übergeben
    if (empty(trim($_POST["password"]))) {
        $password_err = "Bitte Passwort eingeben.";
    } else {
        $password = trim($_POST["password"]);
    }

    // Passwort und Nutzername prüfen
    if (empty($username_err) && empty($password_err)) {
        $sql = "SELECT id, username, password FROM users WHERE username = ?";

        // Nutzernameneingabe für Datenbankeintragung vorbereiten
        if ($stmt = mysqli_prepare($link, $sql)) {
            mysqli_stmt_bind_param($stmt, "s", $param_username);

            $param_username = $username;

            if (mysqli_stmt_execute($stmt)) {
                mysqli_stmt_store_result($stmt);

                // Wenn der Nutzername vorhanden ist, wird das Passwort verifiziert
                if (mysqli_stmt_num_rows($stmt) == 1) {
        
                    mysqli_stmt_bind_result($stmt, $id, $username, $hashed_password);
                    if (mysqli_stmt_fetch($stmt)) {

                        // Wenn das Passwort stimmt, ermittle Anzahl an angemeldeten Nutzern
                        if (password_verify($password, $hashed_password)) {
                            							
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
                                $login_err = "Es sind bereits zwei Spieler angemeldet.";							
                            }

                        } else {
                            // Falsches Passwort
                            $login_err = "Passwort oder Nutzername falsch.";
                        }
                    }
                } else {
                    // Falscher Nutzername
                    $login_err = "Passwort oder Nutzername falsch.";
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
    <title>Login</title>
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
                        <h2 class="card-title">Login</h2>
                        <p class="card-text">Hier bitte Nutzerdaten eingeben.</p>

                        <?php
                        if (!empty($login_err)) {
                            echo '<div class="alert alert-danger">' . $login_err . '</div>';
                        }
                        ?>

                        <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
                            <div class="form-group">
                                <label for="username">Nutzername</label>
                                <input type="text" id="username" name="username" class="form-control <?php echo (!empty($username_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $username; ?>">
                                <span class="invalid-feedback"><?php echo $username_err; ?></span>
                            </div>
                            <div class="form-group">
                                <label for="password">Passwort</label>
                                <input type="password" id="password" name="password" class="form-control <?php echo (!empty($password_err)) ? 'is-invalid' : ''; ?>">
                                <span class="invalid-feedback"><?php echo $password_err; ?></span>
                            </div>
                            <div class="form-group">
                                <input type="submit" class="btn btn-primary" value="Login">
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
