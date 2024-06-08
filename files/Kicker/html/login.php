<?php
// Initialize the session
session_start();

// Check if the user is already logged in
if (isset($_SESSION["loggedin"]) && $_SESSION["loggedin"] === true) {
    // Call the check_second_user.php script to get the value
    $secondUserValue = file_get_contents('check_second_user.php');

    // Redirect based on the value from check_second_user.php
    if ($secondUserValue == 2) {
        header("location: welcome.php");
        exit;
    } else {
        // Handle any other cases if needed
    }
} else {
}

// Include config file
require_once "config.php";

// Define variables and initialize with empty values
$username = $password = "";
$username_err = $password_err = $login_err = "";

// Processing form data when form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Check if username is empty
    if (empty(trim($_POST["username"]))) {
        $username_err = "Please enter username.";
    } else {
        $username = trim($_POST["username"]);
    }

    // Check if password is empty
    if (empty(trim($_POST["password"]))) {
        $password_err = "Please enter your password.";
    } else {
        $password = trim($_POST["password"]);
    }

    // Validate credentials
    if (empty($username_err) && empty($password_err)) {
        // Prepare a select statement
        $sql = "SELECT id, username, password FROM users WHERE username = ?";

        if ($stmt = mysqli_prepare($link, $sql)) {
            // Bind variables to the prepared statement as parameters
            mysqli_stmt_bind_param($stmt, "s", $param_username);

            // Set parameters
            $param_username = $username;

            // Attempt to execute the prepared statement
            if (mysqli_stmt_execute($stmt)) {
                // Store result
                mysqli_stmt_store_result($stmt);

                // Check if username exists, if yes then verify password
                if (mysqli_stmt_num_rows($stmt) == 1) {
                    // Bind result variables
                    mysqli_stmt_bind_result($stmt, $id, $username, $hashed_password);
                    if (mysqli_stmt_fetch($stmt)) {
                        if (password_verify($password, $hashed_password)) {
                            							
                            // Check if another user is already logged in
                            $check_sql = "SELECT COUNT(*) as count FROM active_users";
                            $check_result = mysqli_query($link, $check_sql);
                            $row = mysqli_fetch_assoc($check_result);
                            $count = $row['count'];

                            if ($count == 0) {
								// Password is correct
								$_SESSION["loggedin"] = true;
								//$_SESSION["id"] = $id;
								$_SESSION["username"] = $username;
                                // No other user is logged in, insert this user into the active_users table
                                $insert_sql = "INSERT INTO active_users (username) VALUES (?)";
                                $insert_stmt = mysqli_prepare($link, $insert_sql);
                                mysqli_stmt_bind_param($insert_stmt, "s", $username);
                                mysqli_stmt_execute($insert_stmt);
                                mysqli_stmt_close($insert_stmt);
								
								header("location: waiting.php");
								exit;
							

                            } elseif ($count == 1) {
								
								// Password is correct
								$_SESSION["loggedin"] = true;
								//$_SESSION["id"] = $id;
								$_SESSION["username"] = $username;
								// One user is already logged in, insert this user as the second user
								$insert_sql = "INSERT INTO active_users (username) VALUES (?)";
								$insert_stmt = mysqli_prepare($link, $insert_sql);
								mysqli_stmt_bind_param($insert_stmt, "s", $username);
								mysqli_stmt_execute($insert_stmt);
								mysqli_stmt_close($insert_stmt);
								
								header("location: welcome.php");
								exit;					

                            } else {
                                // More than two users are already logged in, display an error message
                                $login_err = "Es sind bereits zwei Spieler angemeldet.";
								
                            }

                        } else {
                            // Password is not valid, display a generic error message
                            $login_err = "Passwort oder Nutzername falsch.";
                        }
                    }
                } else {
                    // Username doesn't exist, display a generic error message
                    $login_err = "Passwort oder Nutzername falsch.";
                }
            } else {
                echo "Unbekannte Fehlermeldung.";
            }

            // Close statement
            mysqli_stmt_close($stmt);
        }
    }

    // Close connection
    mysqli_close($link);
}
?>

<!DOCTYPE html>
<html lang="en">
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
