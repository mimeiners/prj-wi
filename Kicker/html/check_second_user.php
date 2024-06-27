<?php
/**
 * check_second_user.php
 * 
 * Datenbankabrage zur Anzahl der angemeldeten Nutzer
 * 
 */

// Neue Session starten bzw. vorhandene fortsetzen
session_start();

// Datenbankverbindung aufbauen (Passwortdeklaration nicht vergessen)
require_once "config.php";

// Anzahl der angemeldeten Nutzer abfragen
$check_sql = "SELECT COUNT(*) as count FROM active_users";
$check_result = mysqli_query($link, $check_sql);
$row = mysqli_fetch_assoc($check_result);
$count = $row['count'];

echo $count; // Anzahl der aktiven Spieler ausgeben

// Datenbankverbindung beenden
$link->close();
?>
