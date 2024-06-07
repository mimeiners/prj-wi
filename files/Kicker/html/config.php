<?php
/*Database credentials for mysql usersdb database*/
define('DB_SERVER', 'localhost');
define('DB_USERNAME', 'admin');
define('DB_PASSWORD', 'polodingoswung8');
define('DB_NAME', 'usersdb');

/*Connect to database*/
$link = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);
	
if ($link === false){
	die("ERROR: Verbindung fehlgeschlagen. " . mysqli_connect_error());
}
?>
