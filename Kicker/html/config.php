<?php
/**
 * config.php
 * 
 * Zum Datenbankverbindungsaufbau
 * 
 */

// Datenbankverbindungsparameter aus Webserver-Konfiguration übernehmen
define('DB_LOGIN_SERVER', 'localhost');
define('DB_LOGIN_USERNAME', 'admin');
define('DB_LOGIN_PASSWORD', '<password>'); // Hier Passwort eintragen
define('DB_LOGIN_NAME', 'usersdb');

// Datenbankverbindung aufbauen
$link = mysqli_connect(DB_LOGIN_SERVER, DB_LOGIN_USERNAME, DB_LOGIN_PASSWORD, DB_LOGIN_NAME);
	
// ERROR: Datenbankverbindungsfehler
if ($link === false){
	die("ERROR: Verbindung fehlgeschlagen. " . mysqli_connect_error());
}
?>
