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
    if(empty(trim($_POST["password"]))){
        $password_error = "Bitte ein Passwort eingeben.";     
    } elseif(strlen(trim($_POST["password"])) < 5) {
        $password_error = "Das Passwort sollte mindestens fünf Zeichen lang sein.";
    } else {
        $password = trim($_POST["password"]);
    }
    
    // Passworteingabewiederholung prüfen
    if(empty(trim($_POST["confirm_password"]))){
        $password_check_error = "Bitte das Passwort wiederholen.";     
    } else {
        $password_check = trim($_POST["confirm_password"]);
        if(empty($password_error) && ($password != $password_check)){
            $password_check_error = "Passwort stimmt nicht überein.";
        }
    }
 
    // Nutzernameneingabe prüfen
    if(empty(trim($_POST["username"]))){
        $username_error = "Bitte Nutzernamen angeben.";
    } elseif(!preg_match('/^[a-zA-Z0-9_]+$/', trim($_POST["username"]))){
        $username_error = "Dieser Nutzername enthält unzulässige Zeichen.";
    } else {
        // Nutzernameneingabe für Datenbankeintragung vorbereiten
        $sql_cmd = "SELECT id FROM users WHERE username = ?";
        
        if($stmt = mysqli_prepare($link, $sql_cmd)){
            mysqli_stmt_bind_param($stmt, "s", $username_parameter);
            $username_parameter = trim($_POST["username"]);

            if(mysqli_stmt_execute($stmt)){
                mysqli_stmt_store_result($stmt);
                
                if(mysqli_stmt_num_rows($stmt) == 1){
                    $username_error = "Dieser Nutzer existiert bereits.";
                } else{
                    $username = trim($_POST["username"]);
                }
            } else{
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
