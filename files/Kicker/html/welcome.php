<?php
// Initialize the session
session_start();

// Check if the user is logged in, if not then redirect to the login page
if (!isset($_SESSION["loggedin"]) || $_SESSION["loggedin"] !== true) {
    header("location: login.php");
    exit;
}

// Include config file
require_once "config.php";

// Query to fetch the names of players from the active_users table
$sql = "SELECT username FROM active_users";
$result = $link->query($sql);

$players = [];

if ($result->num_rows > 0) {
    // Fetch all player names and store them in the $players array
    while ($row = $result->fetch_assoc()) {
        $players[] = $row["username"];
    }

    // Check for duplicate usernames
    $uniquePlayers = array_unique($players);
    if (count($players) !== count($uniquePlayers)) {
        // Remove the user from the active_users table
        $sql = "DELETE FROM active_users";

        if ($link->query($sql) === TRUE){
        } else {
        }
        // Logout all users and redirect to login page
        session_destroy();
        header("location: index.php");
        exit;
    }
 // Initialize data array
    $data = [];

    // Ensure there are at least two players
    if (count($uniquePlayers) >= 2) {
        $data['player_1']['name'] = $uniquePlayers[0];
		$player1 = $uniquePlayers[0];
        $data['player_2']['name'] = $uniquePlayers[1];
		$player2 = $uniquePlayers[1];
    } else {
        echo "Not enough players.";
        exit();
    }
    
    $data['button_stop'] = false;
    $data['button_power'] = false;
    $data['button_start'] = false;
    $data['game_id'] = "";
    
    // Convert the data array to JSON
    $jsonData = json_encode($data, JSON_PRETTY_PRINT);

    // Write the JSON data to a file
    if (file_put_contents('game_data.json', $jsonData) === false) {
        echo "Failed to write to game_data.json.";
        exit;
    } else {
        echo "Player data successfully written to game_data.json.";
		header("Location: drone_check.php?player1=$player1&player2=$player2");
		exit();
    }
} else {
    echo "No active users found.";
    exit();
}



// Close the database connection
$link->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Welcome</title>
    <link rel="stylesheet" href="bootstrap.min.css">
    <style>
        body { font: 16px sans-serif; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <h1 class="mb-4">Willkommen Spieler</h1>
                <ul class="list-group">
                    <?php foreach ($players as $player): ?>
                        <li class="list-group-item"><?php echo htmlspecialchars($player); ?></li>
                    <?php endforeach; ?>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
