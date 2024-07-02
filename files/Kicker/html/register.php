<?php
/**
 * register.php
 * 
 * Registrierungsseite für Nutzer
 * 
 */

// Datenbankverbindung aufbauen (Passwortdeklaration nicht vergessen)
require_once "config.php";
 
// Variablen für die Eingabefelder initialisieren
$username = $password = "";
$username_error = $password_error = "";
$password_check = $password_check_error = "";

// Eingabefelderinhalt prüfen und ggf. verarbeiten
if($_SERVER["REQUEST_METHOD"] == "POST"){

	// Passworteingabe prüfen
	$password = trim($_POST["password"]);
    // Fehlermeldung setzen, wenn das Passwort leer ist oder weniger als 5 Zeichen hat
	if(empty($password) || strlen($password) < 5){
		$password_error = empty($password) ? "Bitte ein Passwort eingeben." : "Das Passwort sollte mindestens fünf Zeichen lang sein.";
	}

	// Passworteingabewiederholung prüfen
	$password_check = trim($_POST["confirm_password"]);
	if(empty($password_check)){
        // Fehlermeldung setzen, wenn das Passwort-Wiederholungsfeld leer ist
		$password_check_error = "Bitte das Passwort wiederholen.";     
	} elseif(empty($password_error) && ($password != $password_check)){
        // Fehlermeldung setzen, wenn die Passwörter nicht übereinstimmen
		$password_check_error = "Passwort stimmt nicht überein.";
	}

	// Nutzernameneingabe prüfen
	$username = trim($_POST["username"]);
	if(empty($username) || !preg_match('/^[a-zA-Z0-9_]+$/', $username)){
        // Fehlermeldung setzen, wenn der Nutzername leer ist oder ungültige Zeichen enthält
		$username_error = empty($username) ? "Bitte Nutzernamen angeben." : "Dieser Nutzername enthält unzulässige Zeichen.";
	} else {
		// Nutzernameneingabe für Datenbankabfrage vorbereiten
		$sql_cmd = "SELECT id FROM users WHERE username = ?";
		
		if($stmt = mysqli_prepare($link, $sql_cmd)){
            // Parameter binden und vorbereiten
			mysqli_stmt_bind_param($stmt, "s", $username_parameter);
			$username_parameter = $username;

            // SQL-Befehl ausführen
			if(mysqli_stmt_execute($stmt)){
				mysqli_stmt_store_result($stmt);
				
                // Wenn wir ein Ergebnis für diesen Nutzernamen bekommen,
				if(mysqli_stmt_num_rows($stmt) == 1){
                    // dann Fehlermeldung setzen, wenn der Nutzername bereits existiert
					$username_error = "Dieser Nutzer existiert bereits.";
				} else {
                    // sonst Nutzername beibehalten
					$username = $username;
				}
			} else {
				echo "Unbekannte Fehlermeldung.";
			}

			mysqli_stmt_close($stmt);
		}
	}
 
    // Datenbankeintragung durchführen, wenn Nutzereingaben zulässig sind
    if(empty($username_error) && empty($password_error) && empty($password_check_error)){
        
        // Nutzername und Passwort für Dateinbankeintrag vorbereiten
        $sql_cmd = "INSERT INTO users (username, password) VALUES (?, ?)";
         
        if($stmt = mysqli_prepare($link, $sql_cmd)){
            // Parameter binden und vorbereiten
            mysqli_stmt_bind_param($stmt, "ss", $username_parameter, $password_parameter);
            $username_parameter = $username;
            $password_parameter = password_hash($password, PASSWORD_DEFAULT);
            
            // Datenbankeintragung durchführen
            if(mysqli_stmt_execute($stmt)){
                // Umleitung nach erfolgreicher Registrierung
                header("location: login.php");
            } else {
                echo "Unbekannte Fehlermeldung";
            }

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
    <title>Registrierung</title>
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
                        <h2 class="card-title">Registrierung</h2>
                        <p class="card-text">Hier erstellen Sie ein Nutzerkonto.</p>
                        <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
                            <div class="form-group">
                                <label for="username">Nutzername</label>
                                <input type="text" id="username" name="username" class="form-control <?php echo (!empty($username_error)) ? 'is-invalid' : ''; ?>" value="<?php echo $username; ?>">
                                <span class="invalid-feedback"><?php echo $username_error; ?></span>
                            </div>
                            <div class="form-group">
                                <label for="password">Passwort</label>
                                <input type="password" id="password" name="password" class="form-control <?php echo (!empty($password_error)) ? 'is-invalid' : ''; ?>" value="<?php echo $password; ?>">
                                <span class="invalid-feedback"><?php echo $password_error; ?></span>
                            </div>
                            <div class="form-group">
                                <label for="confirm_password">Passwort wiederholen</label>
                                <input type="password" id="confirm_password" name="confirm_password" class="form-control <?php echo (!empty($password_check_error)) ? 'is-invalid' : ''; ?>" value="<?php echo $password_check; ?>">
                                <span class="invalid-feedback"><?php echo $password_check_error; ?></span>
                            </div>
                            <div class="form-group">
                                <input type="submit" class="btn btn-primary" value="Submit">
                            </div>
                            <p><a href="login.php">Zum Login</a>.</p>
							<p><a href="index.php">Zur Startseite</a>.</p>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
