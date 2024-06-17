<?php
session_start();

// Include config file
require_once "config.php";

// Check if another user is already logged in
$check_sql = "SELECT COUNT(*) as count FROM active_users";
$check_result = mysqli_query($link, $check_sql);
$row = mysqli_fetch_assoc($check_result);
$count = $row['count'];

echo $count; // Return the value of $count

$link->close();
?>
