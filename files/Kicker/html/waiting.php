<?php
session_start();

// Check if the user is already logged in
if (isset($_SESSION["loggedin"]) && $_SESSION["loggedin"] === true) {
    // Call the check_second_user.php script to get the value
    $secondUserValue = file_get_contents('check_second_user.php');

    // Redirect based on the value from check_second_user.php
    if ($secondUserValue == 2) {
        header("location: back_home.php");
        exit;
    } else {
        // Handle any other cases if needed
    }
} else {

        header("location: index.php"); // currently playing so redirect somewhere
		exit;

}

// Include config file
require_once "config.php";

$link->close();
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
                        <h2 class="card-title">Bitte auf einen zweiten Spieler warten.</h2>
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
                        window.location.href = 'welcome.php';
                    } else if (parseInt(data) === 0) {
                        window.location.href = 'index.php'; // someone used the same login twice; thus both are removed from active_users and you have to try again.
                    }
                })
                .catch(error => console.error('Error:', error));
        }

        setInterval(checkActiveUsers, 1000); // Check every second
    </script>
</body>
</html>