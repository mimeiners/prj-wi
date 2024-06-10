<?php
// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Redirect the user to the login page
    header("Location: login.php");
    exit();
}
?>

<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Namen speichern</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="bootstrap.min.css">
    <style>
        body { font: 16px sans-serif; }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center mt-5">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-body text-center">
                        <img src="Pictures/hsb-logo.png" class="img-fluid mb-4" alt="HSB Logo" width="300" height="139">
                        <h1 class="card-title">Willkommen beim Spiel</h1>
                        <p class="card-text">Klicken Sie auf den Button, um zum Login weitergeleitet zu werden.</p>
                        <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
                            <button type="submit" class="btn btn-primary">Zum Login</button>
                        </form>
                        <br>
                        <p><a href="indexfreund.php">Zum Freundschaftsspiel</a>, Punkte werden nicht gezählt.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
