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
$username = $password = $confirm_password = "";
$username_err = $password_err = $confirm_password_err = "";
 
// Eingabefelderinhalt prüfen und ggf. verarbeiten
if($_SERVER["REQUEST_METHOD"] == "POST"){
 
    // Nutzernameneingabe prüfen
    if(empty(trim($_POST["username"]))){
        $username_err = "Bitte Nutzernamen angeben.";
    } elseif(!preg_match('/^[a-zA-Z0-9_]+$/', trim($_POST["username"]))){
        $username_err = "Dieser Nutzername enthält unzulässige Zeichen.";
    } else{
        // Nutzernameneingabe für Datenbankeintragung vorbereiten
        $sql = "SELECT id FROM users WHERE username = ?";
        
        if($stmt = mysqli_prepare($link, $sql)){
            mysqli_stmt_bind_param($stmt, "s", $param_username);
            $param_username = trim($_POST["username"]);

            if(mysqli_stmt_execute($stmt)){
                mysqli_stmt_store_result($stmt);
                
                if(mysqli_stmt_num_rows($stmt) == 1){
                    $username_err = "Dieser Nutzer existiert bereits.";
                } else{
                    $username = trim($_POST["username"]);
                }
            } else{
                echo "Unbekannte Fehlermeldung.";
            }

            mysqli_stmt_close($stmt);
        }
    }
    
    // Passworteingabe prüfen
    if(empty(trim($_POST["password"]))){
        $password_err = "Bitte ein Passwort eingeben.";     
    } elseif(strlen(trim($_POST["password"])) < 5){
        $password_err = "Das Passwort sollte mindestens fünf Zeichen lang sein.";
    } else{
        $password = trim($_POST["password"]);
    }
    
    // Passworteingabewiederholung prüfen
    if(empty(trim($_POST["confirm_password"]))){
        $confirm_password_err = "Bitte das Passwort wiederholen.";     
    } else{
        $confirm_password = trim($_POST["confirm_password"]);
        if(empty($password_err) && ($password != $confirm_password)){
            $confirm_password_err = "Passwort stimmt nicht überein.";
        }
    }
    
    // Datenbankeintragung durchführen, wenn Nutzereingaben zulässig sind
    if(empty($username_err) && empty($password_err) && empty($confirm_password_err)){
        
        // Nutzername und Passwort für Dateinbankeintrag vorbereiten
        $sql = "INSERT INTO users (username, password) VALUES (?, ?)";
         
        if($stmt = mysqli_prepare($link, $sql)){
            mysqli_stmt_bind_param($stmt, "ss", $param_username, $param_password);

            $param_username = $username;
            $param_password = password_hash($password, PASSWORD_DEFAULT);
            
            // Datenbankeintragung durchführen
            if(mysqli_stmt_execute($stmt)){
                // Umleitung nach erfolgreicher Registrierung
                header("location: login.php");
            } else{
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
                                <input type="text" id="username" name="username" class="form-control <?php echo (!empty($username_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $username; ?>">
                                <span class="invalid-feedback"><?php echo $username_err; ?></span>
                            </div>
                            <div class="form-group">
                                <label for="password">Passwort</label>
                                <input type="password" id="password" name="password" class="form-control <?php echo (!empty($password_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $password; ?>">
                                <span class="invalid-feedback"><?php echo $password_err; ?></span>
                            </div>
                            <div class="form-group">
                                <label for="confirm_password">Passwort wiederholen</label>
                                <input type="password" id="confirm_password" name="confirm_password" class="form-control <?php echo (!empty($confirm_password_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $confirm_password; ?>">
                                <span class="invalid-feedback"><?php echo $confirm_password_err; ?></span>
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
